#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#   Autors: David Hannequin <david.hannequin@gmail.com>,
#   Date: 2019-08-08
#   URL: https://github.com/hvad/monitoring-plugins
#   
#   Plugins to check linux memory and swap by SNMP.
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

from pysnmp.hlapi import *
import argparse

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', required=True, type=str, help='hostname or ip address')
    parser.add_argument('-p', '--port', default='161', type=int, help='port')
    parser.add_argument('-u', '--username', required=True, type=str, help='login for snmpv3')
    parser.add_argument('-x', '--auth_pass', required=True, type=str, help='auth password for snmpv3')
    parser.add_argument('-a', '--priv_pass', required=True, type=str, help='private password for snmpv3')
#    parser.add_argument('-p', '--partition', required=True, type=str, help='disk name')
    parser.add_argument('-w', '--warning', default='80', type=int, help='Warning thresold')
    parser.add_argument('-c', '--critical', default='90', type=int, help='Critical thresold')
    parser.add_argument('-t', '--timeout', default='15', type=int, help='timeout')
    args = parser.parse_args()

    return args

def data(oid):

    args = parse_args()

    result=[]
    for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(SnmpEngine(),
                UsmUserData(args.username, args.auth_pass, args.priv_pass,
                authProtocol=usmHMACSHAAuthProtocol,
                privProtocol=usmAesCfb128Protocol),
                UdpTransportTarget((args.host, args.port), timeout=args.timeout, retries=0),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                lexicographicMode=False):
        if errorIndication:
            print(errorIndication)
            raise SystemExit(3)
        elif errorStatus:
            print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'
                )
            )
            break
            raise SystemExit(3)
        else:
            for oid, val in varBinds:
                result.append(val.prettyPrint())
    return result

# Disk name .1.3.6.1.4.1.2021.9.1.2
#Path where the disk is mounted: .1.3.6.1.4.1.2021.9.1.2.1
#Path of the device for the partition: .1.3.6.1.4.1.2021.9.1.3.1
#Total size of the disk/partion (kBytes): .1.3.6.1.4.1.2021.9.1.6.1
#Available space on the disk: .1.3.6.1.4.1.2021.9.1.7.1
#Used space on the disk: .1.3.6.1.4.1.2021.9.1.8.1
#Percentage of space used on disk: .1.3.6.1.4.1.2021.9.1.9.1
#Percentage of inodes used on disk: .1.3.6.1.4.1.2021.9.1.10.1
   
#    oid_ram='1.3.6.1.4.1.2021.4.5.0'
#    oid_ram_used='1.3.6.1.4.1.2021.4.6.0'
#    oid_swap='1.3.6.1.4.1.2021.4.3.0'
#    oid_swap_used='1.3.6.1.4.1.2021.4.4.0'

def main():

    args = parse_args()

    if args.critical < args.warning: 
      print ('Warning thresold is greater than thresold critical.')
      raise SystemExit(3)
   
    oid='1.3.6.1.4.1.2021.9.1.2.1'
    result = data(oid)

    print (result)


if __name__ == "__main__":
    main()
