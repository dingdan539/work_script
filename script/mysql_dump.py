#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import time
import subprocess


class MysqlDump(object):
    dump_path = '/data/mysql_dump/'
    
    mysql_host = '127.0.0.1'
    mysql_port = '3306'
    mysql_user = 'dump2'
    mysql_pwd = 'dump'
    mysql_db = ['ddtest', 'ddtest2']

    @staticmethod    
    def _command(cmdstr):
        proc = subprocess.Popen(cmdstr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        code = proc.returncode
        return code, stdout, stderr

    @staticmethod
    def get_date(time_stamp=0):
        return time.strftime('%Y%m%d', time.localtime(time.time() - time_stamp))
    
    def get_del_file(self, mysql_db):
        d = self.get_date(86400 * 5)
        return mysql_db + '_' + d + '.sql'
    
    def get_dump_file(self, mysql_db):
        d = self.get_date()
        return mysql_db + '_' + d + '.sql'
    
    def del_file(self):
        for db_name in self.mysql_db:
            file_name = self.get_del_file(db_name)
            file_path_name = self.dump_path + db_name + '/' + file_name
            if os.path.exists(file_path_name):
                os.remove(file_path_name)
    
    def mysql_dump(self):
        for db_name in self.mysql_db:
            dump_file_name = self.get_dump_file(db_name)
            export_path = self.dump_path + db_name
            if not os.path.exists(export_path):
                os.makedirs(export_path)
            cmd = "mysqldump -h{0} -P{1} -u{2} -p{3} {4} > {5}".format(
            self.mysql_host, self.mysql_port, 
            self.mysql_user, self.mysql_pwd, db_name, export_path + '/' + dump_file_name)
            try:
                code, stdout, stderr = MysqlDump._command(cmd)
                if code == 0:
                    print db_name + "dump success"
                else:
                    print db_name + "error:" + stderr
            except Exception, e:  
                print Exception, ":", e
    
    def run(self):
        self.del_file()
        self.mysql_dump()
        

if __name__ == '__main__':
    a = MysqlDump()
    a.run()
