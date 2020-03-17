# ASA Static IP Tunnels

*Static IP Tunnel Configuration Generator for ASAs and AnyConnect VPN*

This repo contains helper functions designed to generate static IP tunnel configurations for the ASA CLI.

From a high level:
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
  ip pool a  ->  10.0.0.1    ip local b -> 10.0.0.2
         |                          |
         v                          v
     Connected!                 Connected!
```

Please take note of the DAP LUA configuration that goes along with this:
```
EVAL(cisco.aaa.username, "EQ", cisco.aaa.tunnelgroup)
```
This is a security necessity to ensure static IPs are taken by the users intended.

The original intent for this program was to satisfy India's VoIP exception for users with static IPs in light of recent events due to COVID-19.

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
