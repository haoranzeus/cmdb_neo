#!/usr/bin/env python3
# coding=utf-8
# author zhanghaoran
import re

import pymysql.cursors


class DbHandler:
    cmdb_url_base = 'http://localhost:10001'
    reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')

    def __init__(self, host, port, table, user, password):
        self.db_conf = {
            'host': host,
            'port': port,
            'db': table,
            'user': user,
            'password': password,
            'charset': 'utf8'
        }

    @property
    def connection(self):
        return pymysql.connect(**self.db_conf)

    def do_func(self, func_name, **paras):
        func = getattr(self, func_name)
        func(**paras)

    def helloworld(self, name):
        print('hello {}'.format(name))

    def do_sql(self, sql_str):
        connection = self.connection
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_str)
            connection.commit()
        finally:
            connection.close()
        return cursor.fetchall()
