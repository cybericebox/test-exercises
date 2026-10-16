# Cyber ICE Box — Training Exercises

Two Ukrainian training examples help participants verify that they can receive an attachment, submit a flag, and connect to a running laboratory. Organizers can import either example or both together using the `cib-exercise/v1` archives.

## Examples

- **Перший прапор** (`static/`): a downloadable Go source file contains the deliberately visible, fixed flag `ICE{welcome_to_cyber_ice_box}`. Compilation is not required to solve it.
- **Перевірка підключення** (`dynamic/`): one topology contains two independent tasks. The platform generates separate web and SSH flags from templates and injects them through `WEB_FLAG` and `SSH_FLAG`; each template has 96 bits of randomness. The container requires both values at startup.

## Participant flow

The dynamic page confirms that web access works, explains browser proxy and VPN access, reveals the web flag on request, and supports copying it into the first task's answer. A secondary SSH example shows how to connect through VPN and read `~/flag.txt` for the second task. The web page never exposes the SSH flag.

The platform's external link serves HTTP on container port 8080. VPN supports HTTP on 8080 and SSH on 2222. The public training account is `demo` with password `cybericebox`; it has no root privileges, and SSH forwarding is disabled. Laboratory provides the VPN and internet gateways, and the event must have the required dynamic resources and networks.

## Delivery and boundaries

Release artifacts are `static.zip`, `dynamic.zip`, `test-exercises.zip` and `SHA256SUMS`. The dynamic image targets Linux amd64 and arm64. The default VPN return route assumes the Laboratory client pool `10.128.0.0/10`; installations with a different pool must update the exercise route before import.

This is an intentionally approachable connectivity exercise, with a Ukrainian page and explicit instructions. The canonical behavior, local commands, import details and release procedure live in `README.md`. Local isolated networking checks do not establish deployment in production Laboratory.
