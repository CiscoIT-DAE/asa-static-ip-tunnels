# ASA Static IP Tunnels

*Static IP Tunnel Configuration Generator for ASAs and AnyConnect VPN*

This repo contains helper functions designed to generate static IP tunnel configurations for the ASA CLI.

High level design of static IP tunnels on the ASA in tandem with AnyConnect VPN:
```
  VPN Client "a"             VPN Client "b"
         |                          |
         v                          v
https://<vpn-device>/a     https://<vpn-device>/b
         |                          |
         v                          v
   tunnel-group a ----------- tunnel-group b ---> shared group-policy
         |                          |          -> shared DAP                                
         v                          v
     ip pool a  ->  10.0.0.1    ip pool b -> 10.0.0.2
         |                          |
         v                          v
     Connected!                 Connected!
```

Please take note of the DAP LUA configuration that goes along with this:
```
EVAL(cisco.aaa.username, "EQ", cisco.aaa.tunnelgroup)
```
This is a security necessity to ensure static IPs are taken by the users intended.

The original intent for this program was to satisfy India's VoIP exception for users with static IPs due to COVID-19.

## Installation

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## To Run
```
python asa_static_ip_tunnels.py
```

The following constants are declared in `"__main__"`:
```
START_IP = '10.0.0.1'   # first IP address in IP pool, increments by 1 for each user
DEVICE = 'vpn-device'   # hostname of the VPN headend
AAA_SERVER = 'AAA_Server'   # name of the AAA server declared on the ASA
GROUP_POLICY = 'Default_Group_Policy'   # group policy shared by all static tunnels
```

The program starts by pulling users from `users.txt`:
```
cecId1
cecId2
cecId3
cecId4
cecId5
```
User IDs can be separated by ` ` or `\n` characters.

Based off the constants and users, CLI configuration is generated in the `output/` folder.
```
filename: output/config.txt

ip local pool cecId1 10.0.0.1 mask 255.255.255.255   ! address pool with single IP
tunnel-group cecId1 type remote-access   ! unique tunnel group with same name as user ID
tunnel-group cecId1 general-attributes
  address-pool cecId1
  authentication-server-group AAA_Server
  default-group-policy Default_Group_Policy
tunnel-group cecId1 webvpn-attributes
  group-url https://vpn-device/cecId1 enable  ! connection URL for user

...
```

A file labeled `clear_config.txt` is also created, which contains ASA CLI configuration to undo the static IP tunnels created.

## Technologies & Frameworks Used

**Cisco Products & Services:**

- ASA OS Software
- AnyConnect VPN Client

**Tools & Frameworks:**

- Python 3.7
- `ipaddress` module

## File Structure
```
.
├── asa_static_ip_tunnels.py (where __main__ lies and a code explanation on how to use functions)
├── users.txt (input file for user IDs)
├── static_tunnels.py (configuration generation functions)
├── output (configuration output)
|   ├── config.txt (creation)
|   └── clear_config.txt (deletion)
```

## Authors & Maintainers
- Drew Taylor <dretaylo@cisco.com>

## Credits

- Damien Stenning <dstennin@cisco.com>
- Nishant Singh <nishansi@cisco.com>
- Pete Davis <psd@cisco.com>
- Fernando De Jesus Sancho Vargas <fsanchov@cisco.com>
- Tejas Amin <teamin@cisco.com>

## License

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/CiscoDevNet/asa-static-ip-tunnels)
