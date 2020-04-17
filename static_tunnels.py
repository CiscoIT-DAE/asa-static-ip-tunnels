"""ASA Static IP Tunnels Console Script.

Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Drew Taylor"
__email__ = "dretaylo@cisco.com"
__version__ = "0.1.1"
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


import ipaddress
import re

def generateStaticTunnelsConfig(users, device, ip_start, aaa_server, group_policy):
    """
        Generates ASA configuration for static IP allocation to users.
        This creates a unique address pool and tunnel group for each user.

        :param users: username ids that need static IPs
        :type users: list
        :param device: hostname of device
        :type device: str
        :param ip_start: first IP address in address pool
        :type ip_start: str
        :param aaa_server: name of authentication server for tunnel group
        :type aaa_server: str
        :param group_policy: name of group policy to attach tunnel groups to
        :type group_policy: str

        :return: configuration for the ASA
        :rtype: str
    """

    config = ""
    ip = ipaddress.ip_address(ip_start)

    for user in users:
        # issue reported with assigned IP address ending in 0 or 255 receiving no internal access
        while True:
            ip_check = re.search(r"\d+$", str(ip))
            if ip_check and (ip_check[0] == "0" or ip_check[0] == "255"):
                ip += 1
            else:
                break
    
        config += staticTunnelTemplate(user, device, ip, aaa_server, group_policy)
        config += "\n"
        ip += 1

    return config

def staticTunnelTemplate(user, device, ip, aaa_server, group_policy):
    """
        Template for static IP tunnel configuration for a user.
        This creates a unique address pool and tunnel group for a user.

        :param user: username id associated with static IP
        :type user: str
        :param device: hostname of device
        :type device: str
        :param ip_start: first IP address in address pool
        :type ip_start: str
        :param aaa_server: name of authentication server for tunnel group
        :type aaa_server: str
        :param group_policy: name of group policy to attach tunnel groups to
        :type group_policy: str

        :return: configuration for the ASA
        :rtype: str
    """

    config = ""

    # ip local pool <USER> X.X.X.X mask 255.255.255.255
    config += f"ip local pool {user} {str(ip)} mask 255.255.255.255\n"

    # tunnel-group <USER> type remote-access
    config += f"tunnel-group {user} type remote-access\n"

    # tunnel-group <USER> general-attributes
    config += f"tunnel-group {user} general-attributes\n"

    # address-pool <USER>
    config += f"address-pool {user}\n"

    # authentication-server-group <AAA_SERVER>
    config += f"authentication-server-group {aaa_server}\n"

    # default-group-policy <GROUP-POLICY>
    config += f"default-group-policy {group_policy}\n"

    # tunnel-group <USER> webvpn-attributes
    config += f"tunnel-group {user} webvpn-attributes\n"

    # group-url https://<DEVICE>/<USER> enable
    config += f"group-url https://{device}/{user} enable\n"

    return config

def clearStaticTunnelsConfig(users):
    """
        Template to clear static IP tunnel configuration for a user.

        :param users: username ids that have unique address pools and tunnel groups
        :type users: list

        :return: configuration for the ASA
        :rtype: str
    """

    config = ""

    for user in users:
        config += clearStaticTunnelTemplate(user)
        config += "\n"

    return config

def clearStaticTunnelTemplate(user):
    """
        Generates ASA configuration to clear static IP allocation for users.

        :param user: username ids that has a unique address pool and tunnel group
        :type user: str

        :return: configuration for the ASA
        :rtype: str
    """

    config = ""

    # clear configure tunnel-group <USER>
    config += f"clear configure tunnel-group {user}\n"

    # no ip local pool <USER>
    config += f"no ip local pool {user}\n"

    return config
