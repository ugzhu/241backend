import mysql.connector
from mysql.connector import Error

__author__ = 'Yujie Zhu'


class Database:

    def __init__(self, sql):
        self.sql = sql

    def execute(self):
        res = ""
        try:
            connection_config = {
                'user': 'remoteuser',
                'password': '12345678',
                'host': '3.239.70.186',
                'port': 3306,
                'database': 'COEN241Database',
                'autocommit': True,
            }
            connection = mysql.connector.connect(**connection_config)

            if connection.is_connected():
                # db_Info = connection.get_server_info()
                # print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute(self.sql)
                res = cursor.fetchall()

        except Error as e:
            raise Exception(e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                # print("MySQL connection is closed")
        return res
