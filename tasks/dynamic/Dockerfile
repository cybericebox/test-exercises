FROM alpine:3.24@sha256:f59abe656b692d901e184be3445e084786602108599d2a51d229c0f5a48c71bf AS test-tools
RUN apk add --no-cache wireguard-tools iptables iproute2 curl openssh-client sshpass nginx

FROM alpine:3.24@sha256:f59abe656b692d901e184be3445e084786602108599d2a51d229c0f5a48c71bf AS runtime
RUN apk add --no-cache nginx openssh-server python3 curl iproute2 ca-certificates \
 && adduser -D -u 1000 -s /bin/ash demo \
 && echo 'demo:cybericebox' | chpasswd \
 && chmod 750 /home/demo \
 && mkdir -p /run/sshd /opt/demo \
 && rm -f /etc/ssh/ssh_host_*_key*
COPY tasks/dynamic/nginx.conf /etc/nginx/nginx.conf
COPY tasks/dynamic/sshd_config /etc/ssh/sshd_config
COPY tasks/dynamic/runtime.py /opt/demo/runtime.py
COPY tasks/dynamic/site /opt/demo/site
EXPOSE 8080 2222
HEALTHCHECK --interval=5s --timeout=2s --start-period=5s --retries=5 CMD curl -fsS http://127.0.0.1:8080/healthz || exit 1
ENTRYPOINT ["python3", "/opt/demo/runtime.py"]
