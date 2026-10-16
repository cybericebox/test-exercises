#!/usr/bin/env python3
"""Isolated Docker test: HTTP proxy, real WireGuard, SSH, flags and internet egress."""

import json, os, subprocess, time, uuid

IMAGE = os.environ.get("CIB_DEMO_IMAGE", "cib-test-exercises:local")
TOOLS = os.environ.get("CIB_TOOLS_IMAGE", "cib-test-exercises:tools")
prefix = "cib-demo-" + uuid.uuid4().hex[:8]
containers = []
networks = []


def run(*args, input=None, check=True):
    r = subprocess.run(list(args), input=input, text=True, capture_output=True)
    if check and r.returncode:
        raise RuntimeError("Command failed: " + " ".join(args) + "\n" + r.stderr)
    return r


def docker(*args, **kwargs):
    return run("docker", *args, **kwargs)


def create_net(suffix, subnet, gateway, internal=False):
    name = prefix + "-" + suffix
    docker(
        "network",
        "create",
        *(["--subnet", subnet, "--gateway", gateway] if subnet else []),
        *(["--internal"] if internal else []),
        name,
    )
    networks.append(name)
    return name


def start(
    name, image, network, ip, extra=(), command=("infinity",), entrypoint="sleep"
):
    name = prefix + "-" + name
    docker(
        "run",
        "-d",
        "--name",
        name,
        "--network",
        network,
        *(["--ip", ip] if ip else []),
        *extra,
        *(["--entrypoint", entrypoint] if entrypoint else []),
        image,
        *command,
    )
    containers.append(name)
    return name


def execute(container, *args, **kwargs):
    return docker("exec", container, *args, **kwargs).stdout


def main():
    bad = docker("run", "--rm", IMAGE, check=False)
    assert bad.returncode != 0, "Missing flags must fail closed"
    # Docker's --internal bridge rejects routed sources from the separate VPN client pool.
    # Keep this unexposed bridge routable; the client has no route to it before WireGuard.
    vpn = create_net("vpn", "10.128.7.0/24", "10.128.7.254")
    internet = create_net("internet", "10.192.7.0/24", "10.192.7.1")
    transport = create_net("transport", None, None, True)
    app = start(
        "app",
        IMAGE,
        internet,
        "10.192.7.10",
        extra=(
            "--cap-add",
            "NET_ADMIN",
            "-e",
            "WEB_FLAG=ICE{web_runtime_smoke}",
            "-e",
            "SSH_FLAG=ICE{ssh_runtime_smoke}",
            "-e",
            "VPN_ADDRESS=10.128.7.10",
        ),
        command=(),
        entrypoint=None,
    )
    docker("network", "connect", "--ip", "10.128.7.10", vpn, app)
    gateway = start(
        "gateway",
        TOOLS,
        vpn,
        "10.128.7.1",
        extra=("--cap-add", "NET_ADMIN", "--sysctl", "net.ipv4.ip_forward=1"),
    )
    docker("network", "connect", transport, gateway)
    gateway_ip = json.loads(docker("inspect", gateway).stdout)[0]["NetworkSettings"][
        "Networks"
    ][transport]["IPAddress"]
    client = start("client", TOOLS, transport, None, extra=("--cap-add", "NET_ADMIN"))
    proxy = start("proxy", TOOLS, transport, None)
    proxy_ip = json.loads(docker("inspect", proxy).stdout)[0]["NetworkSettings"][
        "Networks"
    ][transport]["IPAddress"]
    docker("network", "connect", "--ip", "10.128.7.20", vpn, proxy)
    execute(
        app, "ip", "route", "add", "10.128.0.0/10", "via", "10.128.7.1", "dev", "eth1"
    )
    for _ in range(40):
        if (
            docker(
                "exec",
                app,
                "curl",
                "-fsS",
                "http://127.0.0.1:8080/healthz",
                check=False,
            ).returncode
            == 0
        ):
            break
        time.sleep(0.25)
    else:
        raise RuntimeError("Lab did not become healthy")
    assert (
        docker(
            "exec",
            client,
            "curl",
            "--connect-timeout",
            "1",
            "--max-time",
            "2",
            "-fsS",
            "http://10.128.7.10:8080/",
            check=False,
        ).returncode
        != 0
    ), "Client should need VPN for the lab IP"
    nginx = "events {} http { access_log off; server { listen 8081; location / { proxy_pass http://10.128.7.10:8080; } } }"
    docker("exec", "-i", proxy, "sh", "-c", "cat > /tmp/proxy.conf", input=nginx)
    execute(proxy, "nginx", "-c", "/tmp/proxy.conf")
    page = execute(client, "curl", "-fsS", f"http://{proxy_ip}:8081/")
    assert "ICE{web_runtime_smoke}" in page and "ICE{ssh_runtime_smoke}" not in page
    print("PASS HTTP proxy without VPN", flush=True)
    private = {c: execute(c, "wg", "genkey").strip() for c in [gateway, client]}
    public = {
        c: docker("exec", "-i", c, "wg", "pubkey", input=key + "\n").stdout.strip()
        for c, key in private.items()
    }
    for c, address in [(gateway, "10.128.8.1/24"), (client, "10.128.8.2/24")]:
        execute(c, "ip", "link", "add", "wg0", "type", "wireguard")
        execute(c, "ip", "addr", "add", address, "dev", "wg0")
    server = f"[Interface]\nPrivateKey = {private[gateway]}\nListenPort = 51820\n[Peer]\nPublicKey = {public[client]}\nAllowedIPs = 10.128.8.2/32\n"
    peer = f"[Interface]\nPrivateKey = {private[client]}\n[Peer]\nPublicKey = {public[gateway]}\nAllowedIPs = 10.128.7.0/24, 10.128.8.0/24\nEndpoint = {gateway_ip}:51820\nPersistentKeepalive = 1\n"
    for c, config in [(gateway, server), (client, peer)]:
        docker("exec", "-i", c, "wg", "setconf", "wg0", "/dev/stdin", input=config)
        execute(c, "ip", "link", "set", "wg0", "up")
    execute(client, "ip", "route", "add", "10.128.7.0/24", "dev", "wg0")
    page = execute(
        client, "curl", "--max-time", "8", "-fsS", "http://10.128.7.10:8080/"
    )
    assert "ICE{web_runtime_smoke}" in page
    handshake = execute(gateway, "wg", "show", "wg0", "latest-handshakes").split()[-1]
    assert int(handshake) > 0
    print("PASS HTTP through an actual WireGuard tunnel", flush=True)
    ssh = [
        "sshpass",
        "-p",
        "cybericebox",
        "ssh",
        "-o",
        "StrictHostKeyChecking=no",
        "-o",
        "UserKnownHostsFile=/dev/null",
        "-o",
        "ConnectTimeout=5",
        "-p",
        "2222",
        "demo@10.128.7.10",
    ]
    assert execute(client, *ssh, "cat flag.txt").strip() == "ICE{ssh_runtime_smoke}"
    assert execute(client, *ssh, "id -u").strip() == "1000"
    assert "200" in execute(
        client, *ssh, "curl -fsSI --max-time 20 https://example.com"
    )
    assert (
        docker(
            "exec",
            client,
            "curl",
            "-fsS",
            "http://10.128.7.10:8080/flag.txt",
            check=False,
        ).returncode
        != 0
    )
    print(
        "PASS SSH flag, non-root account, internet egress and flag separation",
        flush=True,
    )
    docker("stop", "--time", "8", app)
    assert json.loads(docker("inspect", app).stdout)[0]["State"]["ExitCode"] == 0
    print("PASS graceful shutdown", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        for name in containers:
            for args in [("ip", "route"), ("wg", "show"), ("iptables", "-S")]:
                result = docker("exec", name, *args, check=False)
                if result.returncode == 0:
                    print(name, args, result.stdout, flush=True)
        raise
    finally:
        for name in reversed(containers):
            docker("rm", "-f", name, check=False)
        for name in reversed(networks):
            docker("network", "rm", name, check=False)
