"""this is a system utils pakge"""
# -*- coding:utf-8 -*-


import socket
import sys
import time


class SysUtils(object):
    """system utils"""
    @staticmethod
    def get_argv():
        """get argvs"""
        return sys.argv[1:]

    def check_port(self):
        """chk port"""
        argvs = self.get_argv()
        _ip, ports = argvs[0], argvs[1:]

        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(1)

        print '*****check port start*****'
        for p in ports:
            try:
                sk.connect((_ip, int(p)))
                print '[+]{0} ok'.format(p)
                time.sleep(1)
            except Exception, e:
                print p + ' fail ' + e.message
        print '*****check port end*****'
        sk.close()


if __name__ == '__main__':
    sysutils = SysUtils()
    sysutils.check_port()
