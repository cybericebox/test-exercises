Test tasks «Загублений пакет» (static) and «Журнал зв’язку» (dynamic).

- Static Go file: a fixed flag restored with XOR; the mask and the restore function are in the attachment.
- Two web pages: a message log and the card of transmission Р-17. Download the packet and restore the message from Base64.
- Independent template flags for the web part and for SSH; the platform passes the values at start.
- Web through the proxy or the VPN, SSH through the VPN, internet through the Laboratory gateway.
- Import archives `static.zip`, `dynamic.zip`, the combined `test-exercises.zip` and `SHA256SUMS`.
- Image `cybericebox/test-exercises:v1.0.0` for `linux/amd64` and `linux/arm64`; the tag `latest` too.

With the owner's agreement this release replaces the first build under the same tags. Checked with the validator of daemon v2.5.0 and with the network test over a real WireGuard tunnel, the HTTP proxy and SSH. No production event is deployed by this release.
