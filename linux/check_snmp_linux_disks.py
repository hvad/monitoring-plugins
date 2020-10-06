#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#   Autors: David Hannequin <david.hannequin@gmail.com>,
#   Date: 2019-02-05
#   URL: https://github.com/hvad/monitoring-plugins
#
#   Plugins to check linux load by SNMP.
#
# Shinken plugin is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinken plugin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Shinken.  If not, see <http://www.gnu.org/licenses/>.

from pysnmp.hlapi import *
import argparse


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1',
                        type=str, help='hostname or ip address')
    parser.add_argument('-p', '--port', default='161',
                        type=int, help='port')
    parser.add_argument('-C', '--community', default='public',
                        type=str, help='snmp community')
    parser.add_argument('-P', '--protocol', choices=['2c', '3'],
                        default='2c', type=str, help='snmp version')
    parser.add_argument('-w', '--warning', default='85', type=int, help='')
    parser.add_argument('-c', '--critical', default='90', type=int, help='')
    args = parser.parse_args()
    host = args.host
    port = args.port
    community = args.community

    critical = args.critical
    warning = args.warning

    return host, port, community, warning, critical


def main():

    host, port, community, warning, critical = parse_args()

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((host, port)),
               ContextData(),
               ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.4.5.0')),
               ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.4.11.0')),
               ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.4.6.0')))
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and
                            varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        tab = []
        for oid, val in varBinds:
            tab.append(val.prettyPrint())

    ram_t = int(tab[0])
    ram_f = int(tab[1])
    ram_u = int(tab[2])
    ram_t = ram_t/1024
    ram_f = ram_f/1024
    ram_u = ram_u/1024
    print('total ram in the machine : %s\n' % ram_t)
    print('total ram free : %s\n' % ram_f)
    print('total ram used : %s\n' % ram_u)


if __name__ == "__main__":
    main()
