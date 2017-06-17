# -*- coding:utf-8 -*-
from __future__ import division
import os
import time


def byte_format(byte):
    unit = 'KB'
    byte = int(byte)
    if byte < 1024:
        unit = 'KB'
    elif byte < 1048576:
        byte = round(byte / 1024, 2)
        unit = 'MB'
    else:
        byte = round(byte / 1048576, 2)
        unit = 'GB'

    return str(byte) + unit


class CheckServer(object):
    @staticmethod
    def cpu_percent():
        info = os.popen('top -bi -n 2 -d 0.02').read().split('\n\n\n')[1].split('\n')[2]
        return info

    @staticmethod
    def cpu_info():
        with open('/proc/cpuinfo') as f:
            cpu_dict = {}
            for line in f:
                if line.strip():
                    name, value = line.split(':')
                    name = name.strip()
                    value = value.strip()
                    if name == 'model name':
                        num = cpu_dict.setdefault(value, 0)
                        cpu_dict[value] = num + 1

            cpu_str = ''
            if cpu_dict:
                c = 0
                for index in cpu_dict:
                    if c != 0:
                        cpu_str += "\n"
                    cpu_str += index + ': ' + str(cpu_dict[index])
                    c += 1
            return 'CpuType: ' + cpu_str

    @staticmethod
    def load_avg():
        with open('/proc/loadavg') as f:
            for line in f:
                l = line.split()
            return 'LoadAvg: ' + l[0] + ' 1min , ' + l[1] + ' 5min , ' + l[2] + ' 15min'

    @staticmethod
    def mem_info():
        with open('/proc/meminfo') as f:
            mem_dict = {
                'MemTotal': 0,
                'MemFree': 0
            }
            c = 0
            for line in f:
                if line.strip():
                    name, value = line.split(':')
                    name = name.strip()
                    value = value.strip()
                    if name in mem_dict:
                        mem_dict[name] = int(value.split(' ')[0])
                        c += 1
                if c == len(mem_dict):
                    break
                    
            mem_str = ''
            if mem_dict['MemTotal']:
                for key, value in mem_dict.items():
                    if mem_str:
                        mem_str += '\n'
                    mem_str += key + ': ' + byte_format(value)
                mem_str += '\n' + 'MemUsed: ' \
                    + str(round(((mem_dict['MemTotal'] - mem_dict['MemFree']) / mem_dict['MemTotal'] * 100), 2)) + '%'

            return mem_str

    @staticmethod
    def net_info():
        interface = 'eth0'
        stats = []
        print 'Interface:', interface

        def rx():
            ifstat = open('/proc/net/dev').readlines()
            for i in ifstat:
                if interface in i:
                    stat = float(i.split()[1])
                    stats[0:] = [stat]

        def tx():
            ifstat = open('/proc/net/dev').readlines()
            for i in ifstat:
                if interface in i:
                    stat = float(i.split()[9])
                    stats[1:] = [stat]

        print 'In		Out'
        rx()
        tx()
        rxstat_o = list(stats)

        print rxstat_o
        rx()
        tx()
        rx = float(stats[0])
        rx_o = rxstat_o[0]
        tx = float(stats[1])
        tx_o = rxstat_o[1]
        rx_rate = round((rx - rx_o)/1024/1024, 3)
        tx_rate = round((tx - tx_o)/1024/1024, 3)
        print rx_rate, 'MB		', tx_rate, 'MB'

    def run(self):
        print self.cpu_info()
        print self.cpu_percent()
        print self.load_avg()
        print self.mem_info()
        self.net_info()

if __name__ == '__main__':
    init = CheckServer()
    init.run()
