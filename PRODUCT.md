# Cyber ICE Box — Training Exercises

Two Ukrainian introductory exercises help participants inspect an attachment, recover and submit a flag, and connect to a running laboratory. Organizers can import either example or both using the `cib-exercise/v1` archives.

## Examples

- **Перший прапор** (`static/`): a downloadable Go source file contains a byte packet, the XOR mask (`0x2a`) and a `restore` function. Recovering the packet yields the fixed flag `ICE{welcome_to_cyber_ice_box}`. The supplied program reports the byte count; merely running it does not print the flag. Compilation is optional.
- **Перевірка підключення** (`dynamic/`): one topology contains independent web and SSH tasks. The platform generates separate values from templates and injects `WEB_FLAG` and `SSH_FLAG`; each template has 96 bits of randomness. Startup requires both resolved flags.

## Participant flow

The web exercise is a two-page Ukrainian communications archive. The journal (`/`) contains a shift note, an incoming message and a short objective. The participant opens `/message.html`, reads the transmission and downloads `/files/packet.txt`. Startup generates that text attachment with the Base64-encoded web flag. Recovering the original text gives the answer for the web task. A native expandable hint explains Base64; the note is a separate text file. The interface does not print the decoded web flag.

The journal also gives SSH access instructions for the independent second task. The participant connects through VPN and reads `~/flag.txt`; an optional native hint introduces `ls` and `cat`. The SSH flag is not written into the web site or its attachment.

## Access and delivery

The platform's external link serves HTTP on container port 8080. VPN supports HTTP on 8080 and SSH on 2222. The public training account is `demo`, password `cybericebox`; it has no root privileges, and SSH forwarding is disabled. Laboratory provides the VPN and internet gateways; the event must have the required dynamic resources and networks.

Release artifacts are `static.zip`, `dynamic.zip`, `test-exercises.zip` and `SHA256SUMS`. The dynamic image targets Linux amd64 and arm64. The default VPN return route assumes the Laboratory client pool `10.128.0.0/10`; installations with a different pool must update the exercise route before import.

These are intentionally approachable recovery and connectivity exercises. `README.md` owns local commands, import details and release procedure. Local checks do not establish deployment in production Laboratory.
