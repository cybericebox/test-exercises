FROM alpine:3.24@sha256:294b683cb724975bec92580e1e685676bd4b50bda910ddb8c51d4cabeaec77e6 AS test-tools
RUN apk add --no-cache wireguard-tools iptables iproute2 curl openssh-client sshpass nginx

FROM alpine:3.24@sha256:294b683cb724975bec92580e1e685676bd4b50bda910ddb8c51d4cabeaec77e6 AS runtime
RUN apk add --no-cache nginx openssh-server python3 curl iproute2 ca-certificates \
 && adduser -D -u 1000 -s /bin/ash demo \
 && echo 'demo:cybericebox' | chpasswd \
 && chmod 750 /home/demo \
 && mkdir -p /run/sshd /opt/demo \
 && rm -f /etc/ssh/ssh_host_*_key*
COPY dynamic/nginx.conf /etc/nginx/nginx.conf
COPY dynamic/sshd_config /etc/ssh/sshd_config
COPY dynamic/runtime.py /opt/demo/runtime.py
COPY dynamic/site /opt/demo/site
EXPOSE 8080 2222
HEALTHCHECK --interval=5s --timeout=2s --start-period=5s --retries=5 CMD curl -fsS http://127.0.0.1:8080/healthz || exit 1
ENTRYPOINT ["python3", "/opt/demo/runtime.py"]
