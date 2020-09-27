#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#   Autors: David Hannequin <david.hannequin@gmail.com>,
#   Date: 2017-02-17
#   URL: https://github.com/hvad/monitoring-plugins
#   Plugins to check linux disk usage.
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
    parser.add_argument('-p', '--partition', default='/',
                        type=str, help='Disk')
    parser.add_argument('-w', '--warning', default='80',
                        type=int, help='Warning thresold')
    parser.add_argument('-c', '--critical', default='90',
                        type=int, help='Critical thresold')
    args = parser.parse_args()
    partition = args.partition
    warning = args.warning
    critical = args.critical

    return warning, critical, partition


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
    warning, critical, partition = parse_args()
    disk_usage = psutil.disk_usage(partition)
    disk_usage_total = bytes2human(disk_usage.total)
    disk_usage_used = bytes2human(disk_usage.used)
    disk_usage_free = bytes2human(disk_usage.free)
    disk_usage_percent = disk_usage.percent
    return \
        disk_usage_total, \
        disk_usage_used, \
        disk_usage_free, \
        disk_usage_percent


def main():

    warning, critical, partition = parse_args()

    disk_usage_total, disk_usage_used, disk_usage_free, \
        disk_usage_percent = get_data()

    if disk_usage_percent >= critical:
        print('CRITICAL - Disk percentage usage : %2.1f%% Total Disk :\
              %s Free Disk : %s Used Disk : %s |disk_percent =%s;%s;%s;0;100'
              % (disk_usage_percent, disk_usage_total, disk_usage_free,
                     disk_usage_used, disk_usage_percent, warning, critical))
        raise SystemExit(2)
    elif disk_usage_percent >= warning:
        print('WARNING - Disk percentage usage : %2.1f%% Total Disk : \
              %s Free Disk : %s Used Disk : %s |disk_percent =%s;%s;%s;0;100'
              % (disk_usage_percent, disk_usage_total, disk_usage_free,
               disk_usage_used, disk_usage_percent, warning, critical))
        raise SystemExit(1)
    else:
        print('OK - Disk percentage usage : %2.1f%% Total Disk : \
              %s Free Disk : %s Used Disk : %s |disk_percent =%s;%s;%s;0;100'
              % (disk_usage_percent, disk_usage_total, disk_usage_free,
              disk_usage_used, disk_usage_percent, warning, critical))
        raise SystemExit(0)


if __name__ == "__main__":
    main()
