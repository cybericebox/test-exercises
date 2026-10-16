#!/usr/bin/env python3
"""Materialize platform-provided flags, then supervise nginx and OpenSSH."""

import fcntl, html, os, pathlib, re, shutil, signal, socket, struct, subprocess, sys, time


def materialize(env, root, source):
    flags = {name: env.get(name, "") for name in ["WEB_FLAG", "SSH_FLAG"]}
    if any(
        not re.fullmatch(r"ICE\{[^{}\s\x00-\x1f]+\}", value) for value in flags.values()
    ):
        raise ValueError("WEB_FLAG and SSH_FLAG must contain resolved ICE flags")
    site = root / "site"
    shutil.copytree(source, site, dirs_exist_ok=True)
    page = (site / "index.html").read_text()
    page = page.replace(
        "@WEB_FLAG@", html.escape(flags["WEB_FLAG"], quote=True)
    ).replace(
        "@VPN_ADDRESS@", html.escape(env.get("VPN_ADDRESS", "10.128.0.10"), quote=True)
    )
    (site / "index.html").write_text(page)
    (root / "flag.txt").write_text(flags["SSH_FLAG"] + "\n")
    (root / "flag.txt").chmod(0o400)


def vpn_address():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        return socket.inet_ntoa(
            fcntl.ioctl(sock.fileno(), 0x8915, struct.pack("256s", b"eth0"))[20:24]
        )


def main():
    root = pathlib.Path("/run/demo")
    root.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["VPN_ADDRESS"] = env.get("VPN_ADDRESS") or vpn_address()
    materialize(env, root, pathlib.Path("/opt/demo/site"))
    shutil.copyfile(root / "flag.txt", "/home/demo/flag.txt")
    os.chown("/home/demo/flag.txt", 1000, 1000)
    os.chmod("/home/demo/flag.txt", 0o400)
    (root / "flag.txt").unlink()
    subprocess.run(["ssh-keygen", "-A"], check=True, stdout=subprocess.DEVNULL)
    for key in ["WEB_FLAG", "SSH_FLAG"]:
        os.environ.pop(key, None)
    children = [
        subprocess.Popen(["/usr/sbin/nginx", "-g", "daemon off;"]),
        subprocess.Popen(["/usr/sbin/sshd", "-D", "-e", "-f", "/etc/ssh/sshd_config"]),
    ]
    stopping = False

    def stop(signum, frame):
        nonlocal stopping
        stopping = True
        for process in children:
            if process.poll() is None:
                process.terminate()

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        while not stopping and all(p.poll() is None for p in children):
            time.sleep(0.2)
    finally:
        for process in children:
            if process.poll() is None:
                process.terminate()
        for process in children:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
    return 0 if stopping else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
