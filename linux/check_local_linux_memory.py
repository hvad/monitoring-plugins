#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#   Autors: David Hannequin <david.hannequin@gmail.com>,
#   Date: 2017-02-17
#   URL: https://github.com/hvad/monitoring-plugins
#   
#   Plugins to check linux memory usage.
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
#
# Requires: Python >= 2.7 
# Requires: Psutil

import argparse
import psutil

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--warning', default='80', type=int, help='Warning thresold')
    parser.add_argument('-c', '--critical', default='90', type=int, help='Critical thresold')
    args = parser.parse_args()
    warning = args.warning
    critical = args.critical
    
    return warning,critical

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

def get_data():
    memory_info = psutil.virtual_memory()
    total = int(memory_info.total)
    available = int(memory_info.available)
    percent = int(memory_info.percent)
    used = int(memory_info.used)
    active = int(memory_info.active)
    inactive = int(memory_info.inactive)
    total = bytes2human(total)
    available = bytes2human(available)
    used = bytes2human(used)
    active = bytes2human(active)
    inactive = bytes2human(inactive)
    return total,available,percent,used,active,inactive

def main():

    warning,critical = parse_args()

    total,available,percent,used,active,inactive = get_data()

    if percent >= critical:
        print ('CRITICAL - Memory percentage usage : %2.1f%% Total Memory : %s Free Memory : %s Used Memory : %s |mem_percent =%s;%s;%s;0;100' % (percent, total, inactive, active, percent, warning, critical))
        raise SystemExit(2)
    elif percent >= warning:
        print ('WARNING - Memory percentage usage : %2.1f%% Total Memory : %s Free Memory : %s Used Memory : %s |mem_percent =%s;%s;%s;0;100' % (percent, total, inactive, active, percent, warning, critical))
        raise SystemExit(1)
    else:
        print ('OK - Memory percentage usage : %2.1f%% Total Memory : %s Free Memory : %s Used Memory : %s |mem_percent =%s;%s;%s;0;100' % (percent, total, inactive, active, percent, warning, critical))
        raise SystemExit(0)

if __name__ == "__main__":
    main()
