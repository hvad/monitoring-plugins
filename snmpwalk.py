#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#   Autors: David Hannequin <david.hannequin@gmail.com>,
#   Date: 2017-07-23
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
    parser.add_argument('-H', '--host', default='127.0.0.1', type=str, help='hostname or ip address')
    parser.add_argument('-p', '--port', default='161', type=int, help='port')
    args = parser.parse_args()
    host = args.host
    port = args.port
    
    return host,port

def get_data():

    host,port = parse_args()

    for (errorIndication,
      errorStatus,
      errorIndex,
      varBinds) in nextCmd(SnmpEngine(),
      UsmUserData('usr-md5-none', 'authkey1'),
      UdpTransportTarget((host, port)),
      ContextData(),
      ObjectType(ObjectIdentity('IF-MIB'))):
      
      if errorIndication:
        print(errorIndication)
        break
      elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        break
      else:
        for varBind in varBinds:
          print(' = '.join([x.prettyPrint() for x in varBind]))

def main():

    get_data()
         
if __name__ == "__main__":
    main()
