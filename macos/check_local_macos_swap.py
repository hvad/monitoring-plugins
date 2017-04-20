#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#   Autors: David Hannequin <david.hannequin@gmail.com>,
#   Date: 2017-02-17
#   URL: https://github.com/hvad/monitoring-plugins
#   
#   Plugins to check macos memory usage.
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
    swap_info = psutil.swap_memory()
    #sswap(total=2147479552L, used=0L, free=2147479552L, percent=0.0, sin=0, sout=0)
    total = int(swap_info.total)
    used = int(swap_info.used)
    free = int(swap_info.free)
    percent = int(swap_info.percent)

    total = bytes2human(total)
    used = bytes2human(used)
    free = bytes2human(free)

    return total,used,free,percent

def main():

    warning,critical = parse_args()

    total,used,free,percent = get_data()

    if percent >= critical:
        print ('CRITICAL - Swap percentage usage : %2.1f%% Total Swap : %s Free Swap : %s Used Swap : %s |swap_percent =%s;%s;%s;0;100' % (percent, total, free, used, percent, warning, critical))
        raise SystemExit(2)
    elif percent >= warning:
        print ('WARNING - Swap percentage usage : %2.1f%% Total Swap : %s Free Swap : %s Used Swap : %s |swap_percent =%s;%s;%s;0;100' % (percent, total, free, used, percent, warning, critical))
        raise SystemExit(1)
    else:
        print ('OK - Swap percentage usage : %2.1f%% Total Swap : %s Free Swap : %s Used Swap : %s |swap_percent =%s;%s;%s;0;100' % (percent, total, free, used, percent, warning, critical))
        raise SystemExit(0)

if __name__ == "__main__":
    main()
