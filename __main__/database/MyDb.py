import mysql.connector

from database.Config import dbConf


class databaza(object):
    def __init__(self, db):
        self.db = mysql.connector.connect(host=dbConf["host"], port=dbConf["port"], database=dbConf["database"],
                                     user=dbConf["user"], password=dbConf["password"])

    def AccountIsBlocked(self, idClient):
        cur2 = self.db.cursor()
        queryBlockIB = "select * from loginhistory where idl = %s order by UNIX_TIMESTAMP(logDate) desc limit 3;"
        cur2.execute(queryBlockIB, (idClient,))
        records = cur2.fetchall()

    def Login(self, login):
        # todo: add password
        cur1 = self.db.cursor()
        queryLogin = "select idc from loginclient where login = %s;"
        cur1.execute(queryLogin, (login,))
        userLogin = cur1.fetchone()
        return userLogin

    def InsertToDb(self, idClient):
        cur4 = self.db.cursor()
        queryWrongLP = "insert into loginhistory (idl,success) values (%s,%s)"
        insert = cur4.execute(queryWrongLP, (idClient, 1))
        self.db.commit()

