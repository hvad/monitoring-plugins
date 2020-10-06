#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#   Autors: David Hannequin <david.hannequin@gmail.com>,
#   Date: 2019-08-08
#   URL: https://github.com/hvad/monitoring-plugins
#
#   Plugins to check linux load by SNMP.
#
# Monitoring plugin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Monitoring plugin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import argparse
from pysnmp.hlapi import *


oid_load1 = '1.3.6.1.4.1.2021.10.1.3.1'
oid_load5 = '1.3.6.1.4.1.2021.10.1.3.2'
oid_load15 = '1.3.6.1.4.1.2021.10.1.3.3'


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1',
                        type=str, help='hostname or ip address')
    parser.add_argument('-p', '--port', default='161', type=int, help='port')
    parser.add_argument('-u', '--username', default='nagios',
                        type=str, help='login for snmpv3')
    parser.add_argument('-x', '--auth_pass', default='password',
                        type=str, help='auth password for snmpv3')
    parser.add_argument('-a', '--priv_pass', default='private',
                        type=str, help='private password for snmpv3')
    parser.add_argument('-w', '--warning', default='3,2,1')
    parser.add_argument('-c', '--critical', default='4,3,2')
    parser.add_argument('-t', '--timeout', default='15')

    args = parser.parse_args()
    host = args.host
    port = args.port
    username = args.username
    auth_pass = args.auth_pass
    priv_pass = args.priv_pass
    timeout = int(args.timeout)

    critical = map(int, args.critical.split(','))
    warning = map(int, args.warning.split(','))

    (cload1, cload5, cload15) = critical
    (wload1, wload5, wload15) = warning

    return host, port, username, auth_pass, priv_pass, timeout, \
        cload1, cload5, cload15, wload1, wload5, wload15


def get_data():

    host, port, username, auth_pass, priv_pass, timeout, \
        cload1, cload5, cload15, wload1, wload5, wload15 = parse_args()

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               UsmUserData(username, auth_pass, priv_pass,
                           authProtocol=usmHMACSHAAuthProtocol,
                           privProtocol=usmAesCfb128Protocol),
               UdpTransportTarget((host, port), timeout=timeout),
               ContextData(),
               ObjectType(ObjectIdentity(oid_load1)),
               ObjectType(ObjectIdentity(oid_load5)),
               ObjectType(ObjectIdentity(oid_load15)))
     )

    if errorIndication:
        print(errorIndication)
        raise SystemExit(3)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and
                            varBinds[int(errorIndex) - 1][0] or '?'))
        raise SystemExit(3)
    elif len(varBinds) == 0:
        print('Error: Could not fetch data at this time.')
        raise SystemExit(3)
    else:
        tab = []
        for oid, val in varBinds:
            tab.append(val.prettyPrint())

    load1 = float(tab[0])
    load5 = float(tab[1])
    load15 = float(tab[2])

    load1 = int(load1)
    load5 = int(load5)
    load15 = int(load15)

    return load1, load5, load15


def main():

    host, port, username, auth_pass, priv_pass, timeout, \
        cload1, cload5, cload15, wload1, wload5, wload15 = parse_args()

    load1, load5, load15 = get_data()

    if load1 >= cload1 or load5 >= cload5 or load15 >= cload15:
        print('CRITICAL - Load average : %s,%s,%s|load1=%s;load5=%s;load15=%s'
              % (load1, load5, load15, load1, load5, load15))
        raise SystemExit(2)
    elif load1 >= wload1 or load5 >= wload5 or load15 >= wload15:
        print('WARNING - Load average : %s,%s,%s|load1=%s;load5=%s;load15=%s'
              % (load1, load5, load15, load1, load5, load15))
        raise SystemExit(1)
    else:
        print('OK - Load average : %s,%s,%s|load1=%s;load5=%s;load15=%s'
              % (load1, load5, load15, load1, load5, load15))
        raise SystemExit(0)


if __name__ == "__main__":
    main()
