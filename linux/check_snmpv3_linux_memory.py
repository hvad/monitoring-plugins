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

from pysnmp.hlapi import *
import argparse

oid_ram='1.3.6.1.4.1.2021.4.5.0'
oid_ram_used='1.3.6.1.4.1.2021.4.6.0'
oid_swap='1.3.6.1.4.1.2021.4.3.0'
oid_swap_used='1.3.6.1.4.1.2021.4.4.0'

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1', type=str, help='hostname or ip address')
    parser.add_argument('-p', '--port', default='161', type=int, help='port')
    parser.add_argument('-u', '--username', default='nagios', type=str, help='login for snmpv3')
    parser.add_argument('-x', '--auth_pass', default='password', type=str, help='auth password for snmpv3')
    parser.add_argument('-a', '--priv_pass', default='private', type=str, help='private password for snmpv3')
    parser.add_argument('-w', '--warning', default='80', type=int, help='Warning thresold')
    parser.add_argument('-c', '--critical', default='90', type=int, help='Critical thresold')
    args = parser.parse_args()
    host = args.host
    port = args.port
    username = args.username
    auth_pass = args.auth_pass
    priv_pass = args.priv_pass
    warning = args.warning
    critical = args.critical

#    critical = map(int, args.critical.split(','))
#    warning = map(int, args.warning.split(','))

    return host,port,username,auth_pass,priv_pass,warning,critical

def get_data():

    host,port,username,auth_pass,priv_pass,warning,critical = parse_args()
    
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               UsmUserData(username, auth_pass, priv_pass,
                           authProtocol=usmHMACSHAAuthProtocol,
                           privProtocol=usmAesCfb128Protocol),
               UdpTransportTarget((host, port)),
               ContextData(),
               ObjectType(ObjectIdentity(oid_ram)),
               ObjectType(ObjectIdentity(oid_ram_used)),
               ObjectType(ObjectIdentity(oid_swap)),
               ObjectType(ObjectIdentity(oid_swap_used)))
     )
    
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
      tab=[]
      for oid, val in varBinds:
        tab.append(val.prettyPrint())

    ram=float(tab[0])
    ram_used=float(tab[1])
    swap=float(tab[2])
    swap_used=float(tab[2])
  
    return ram,ram_used,swap,swap_used

def main():

    host,port,username,auth_pass,priv_pass,warning,critical = parse_args()
   
    ram,ram_used,swap,swap_used = get_data()

    ram_used_percent=int((ram_used*100)/ram)

    ram=int(ram/1024)
    ram_used=int(ram_used/1024)
    swap=swap/1024
    swap_used=swap_used/1024
   
    if ram_used_percent >= critical:
      print ('CRITICAL - Memory usage %s%%' % (ram_used_percent))
      raise SystemExit(2)
    elif ram_used_percent >= warning:  
      print ('WARNING - Memory usage %s%%' % (ram_used_percent))
      raise SystemExit(1)
    else:
      print ('OK - Memory usage %s%%' % (ram_used_percent))  
      raise SystemExit(0)

if __name__ == "__main__":
    main()
