import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector import pooling

from database.Config import dbConf


class Databaza(object):

    def __init__(self):
        self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="pynative_pool", pool_size=5, pool_reset_session=True,
            host=dbConf["host"], port=dbConf["port"], database=dbConf["database"],
            user=dbConf["user"], password=dbConf["password"])

    #
    # def __getDb__(self):
    #     if self.db.is_connected():
    #         print("connected")
    #         return
    #     else:
    #         self.db = self.__connect__()
    #         return self.db
    #
    # def __connect__(self):
    #     return mysql.connector.connect(host=dbConf["host"], port=dbConf["port"], database=dbConf["database"],
    #
    #                                   user=dbConf["user"], password=dbConf["password"])

    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="pynative_pool", pool_size=5, pool_reset_session=True,
        host=dbConf["host"], port=dbConf["port"], database=dbConf["database"],
        user=dbConf["user"], password=dbConf["password"])

    def AccountIsBlocked(self, idClient):
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_info)
            cur2 = connection_object.cursor()
            queryBlockIB = "select * from loginhistory where idl = %s order by UNIX_TIMESTAMP(logDate) desc limit 3;"
            cur2.execute(queryBlockIB, (idClient,))
            records = cur2.fetchall()
            if (connection_object.is_connected()):
                cur2.close()
                connection_object.close()
                print("MySQL connection is closed")
                return records

    def Login(self, login, ):
        # todo: add password
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_info)
            cur1 = connection_object.cursor()
            queryLogin = "select idc from loginclient where login = %s;"
            cur1.execute(queryLogin, (login,))
            userLogin = cur1.fetchone()
            if (connection_object.is_connected()):
                cur1.close()
                connection_object.close()
                print("MySQL connection is closed")
                return userLogin

    def InsertToDb(self, idClient):
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_info)
            # cur1 = self.__getDb__().cursor()
            cur4 = connection_object.cursor()
            queryWrongLP = "insert into loginhistory (idl,success) values (%s,%s)"
            insert = cur4.execute(queryWrongLP, (idClient, 1))
            if (connection_object.is_connected()):
                cur4.close()
                connection_object.close()
                print("MySQL connection is closed")

    def verification(self, login, password):
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ",db_info)
            cur = connection_object.cursor()
            # cur1 = self.__getDb__().cursor()
            queryClient = "SELECT * FROM client " \
                          "inner join loginclient " \
                          "on client.id=loginclient.idc where login = %s and password = %s;"
            cur.execute(queryClient, (login, password))
            user = cur.fetchone()
            if (connection_object.is_connected()):
                cur.close()
                connection_object.close()
                print("MySQL connection is closed")
                return user

    def wrongInsert(self, idClient):
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_info)
            cur = connection_object.cursor()
            queryWrongLP = "insert into loginhistory (idl,success) values (%s,%s)"
            insert = cur.execute(queryWrongLP, (idClient, 0))
            if (connection_object.is_connected()):
                cur.close()
                connection_object.close()
                print("MySQL connection is closed")

    def getUserInfo(self, login):
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_info)
            cur1 = connection_object.cursor()
            # cur1 = self.__getDb__().cursor()
            queryUser = 'select * from loginclient ' \
                        'inner join client on loginclient.idc = client.id where loginclient.login like %s'
            cur1.execute(queryUser, (login,))
            infoUser = cur1.fetchone()
            if (connection_object.is_connected()):
                cur1.close()
                connection_object.close()
                print("MySQL connection is closed")
                return infoUser

    def getAccounts(self, id):
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_info)
            cur1 = connection_object.cursor()
            # cur1 = self.__getDb__().cursor()
            queryAccounts = 'select * from account where idc = %s'
            cur1.execute(queryAccounts, (id,))
            infoAccounts = cur1.fetchall()
            print("z db", infoAccounts)
            if (connection_object.is_connected()):
                cur1.close()
                connection_object.close()
                print("MySQL connection is closed")
                return infoAccounts

    def getOneAccount(self, accnum):
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_info)
            cur1 = connection_object.cursor()
            queryAccountsDetails = 'select * from account where accNum = %s'
            cur1.execute(queryAccountsDetails, (accnum,))
            detailsAccount = cur1.fetchone()
            print("z db", detailsAccount)
            if (connection_object.is_connected()):
                cur1.close()
                connection_object.close()
                print("MySQL connection is closed")
                return detailsAccount

    def getCards(self, accId):
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_info)
            cur1 = connection_object.cursor()
            queryCards = 'select * from card where ida = %s'
            cur1.execute(queryCards, (accId,))
            infoCards = cur1.fetchall()
            print("z db", infoCards)
            if (connection_object.is_connected()):
                cur1.close()
                connection_object.close()
                print("MySQL connection is closed")
                return infoCards

    def getOneCard(self, idcard):
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_info)
            cur1 = connection_object.cursor()
            queryCards = 'select * from card where id = %s'
            cur1.execute(queryCards, (idcard,))
            infoCard = cur1.fetchone()
            print("z db", infoCard)
            if (connection_object.is_connected()):
                cur1.close()
                connection_object.close()
                print("MySQL connection is closed")
                return infoCard

    def getTrans(self, accid):
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_info)
            cur1 = connection_object.cursor()
            queryTrans = 'select * from transaction where idAcc = %s'
            cur1.execute(queryTrans, (accid,))
            infoTrans = cur1.fetchall()
            print("z db", infoTrans)
            if (connection_object.is_connected()):
                cur1.close()
                connection_object.close()
                print("MySQL connection is closed")
                return infoTrans

    def changePass(self, newPass, login, oldPass):
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_info)
            cur4 = connection_object.cursor()
            queryChangePass = "update loginclient set password= %s where login = %s and password = %s"
            update = cur4.execute(queryChangePass, (newPass, login, oldPass))
            print("vypisujem update")
            print("affected rows = {}".format(cur4.rowcount))
            if (connection_object.is_connected()):
                cur4.close()
                connection_object.close()
                print("MySQL connection is closed")
                print("changing done")

    def getTrans2(self, recAcc):
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_info)
            cur1 = connection_object.cursor()
            queryTrans = 'select * from transaction inner join account on transaction.idacc = account.id and ' \
                         'recAccount = %s'
            cur1.execute(queryTrans, (recAcc,))
            infoTrans2 = cur1.fetchall()
            print("z db trans2", infoTrans2)
            if (connection_object.is_connected()):
                cur1.close()
                connection_object.close()
                print("MySQL connection is closed")
                return infoTrans2

    def blockCard(self, idAcc):
        connection_object = self.connection_pool.get_connection()
        if connection_object.is_connected():
            db_info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_info)
            cur1 = connection_object.cursor()
            queryBlock = 'update card set active= 0 where ida = %s'
            cur1.execute(queryBlock, (idAcc,))
            print("vypisujem update blokovania")
            print("affected rows = {}".format(cur1.rowcount))
            if (connection_object.is_connected()):
                cur1.close()
                connection_object.close()
                print("MySQL connection is closed")
