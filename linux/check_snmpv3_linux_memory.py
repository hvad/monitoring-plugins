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
    parser.add_argument('-w', '--warning', default='80', type=int, help='Warning thresold')
    parser.add_argument('-c', '--critical', default='90', type=int, help='Critical thresold')
    args = parser.parse_args()

    return args

def data():

    args = parse_args()

    oid_ram='1.3.6.1.4.1.2021.4.5.0'
    oid_ram_used='1.3.6.1.4.1.2021.4.6.0'
    oid_swap='1.3.6.1.4.1.2021.4.3.0'
    oid_swap_used='1.3.6.1.4.1.2021.4.4.0'
    
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               UsmUserData(args.username, args.auth_pass, args.priv_pass,
                           authProtocol=usmHMACSHAAuthProtocol,
                           privProtocol=usmAesCfb128Protocol),
               UdpTransportTarget((args.host, args.port)),
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
      memory=[]
      for oid, val in varBinds:
        memory.append(val.prettyPrint())
  
    return memory

def main():

    args = parse_args()

    if args.critical < args.warning: 
      print ('Warning thresold is greater than thresold critical.')
      raise SystemExit(3)
   
    memory = data()

    ram_used_percent = int((int(memory[1])*100)/int(memory[0]))

    swap_used_percent = int((int(memory[3])*100)/int(memory[2]))

    if ram_used_percent >= args.critical:
      print ('CRITICAL - Memory usage %s%%' % (ram_used_percent))
      raise SystemExit(2)
    elif ram_used_percent >= args.warning:  
      print ('WARNING - Memory usage %s%%' % (ram_used_percent))
      raise SystemExit(1)
    else:
      print ('OK - Memory usage %s%%' % (ram_used_percent))  
      raise SystemExit(0)

if __name__ == "__main__":
    main()
