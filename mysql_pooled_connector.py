from mysql.connector import Error, pooling

__author__ = 'Yujie Zhu'


class MyPooledConnector:
    def __init__(self):
        try:
            self.cnx_pool = pooling.MySQLConnectionPool(pool_name="my_mysql_pool",
                                                        pool_size=5,
                                                        pool_reset_session=True,
                                                        host='3.239.70.186',
                                                        database='COEN241Database',
                                                        user='remoteuser',
                                                        password='12345678',
                                                        port=3306,
                                                        autocommit=True)
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def execute(self, sql):
        connection_object = self.cnx_pool.get_connection()
        cursor = connection_object.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        connection_object.close()
        return res
