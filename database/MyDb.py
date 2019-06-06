import mysql.connector

from database.Config import dbConf

db = mysql.connector.connect(host=dbConf["host"], port=dbConf["port"], database=dbConf["database"],
                                  user=dbConf["user"], password=dbConf["password"])


class Databaza(object):

    def AccountIsBlocked(self, idClient):
        cur2 = db.cursor()
        queryBlockIB = "select * from loginhistory where idl = %s order by UNIX_TIMESTAMP(logDate) desc limit 3;"
        cur2.execute(queryBlockIB, (idClient,))
        records = cur2.fetchall()
        return records


    def Login(self, login):
        # todo: add password
        cur1 = db.cursor()
        queryLogin = "select idc from loginclient where login = %s;"
        cur1.execute(queryLogin, (login,))
        userLogin = cur1.fetchone()
        return userLogin


    def InsertToDb(self, idClient):
        cur4 = db.cursor()
        queryWrongLP = "insert into loginhistory (idl,success) values (%s,%s)"
        insert = cur4.execute(queryWrongLP, (idClient, 1))
        db.commit()


    def verification(self, login, password):
        cur = db.cursor()
        queryClient = "SELECT * FROM client " \
                      "inner join loginclient " \
                      "on client.id=loginclient.idc where login = %s and password = %s;"
        cur.execute(queryClient, (login, password))
        user = cur.fetchone()
        return user


    def wrongInsert(self, idClient):
        cur4 = db.cursor()
        queryWrongLP = "insert into loginhistory (idl,success) values (%s,%s)"
        insert = cur4.execute(queryWrongLP, (idClient, 0))
        db.commit()


    def getUserInfo(self, login):
        cur1 = db.cursor()
        queryUser = 'select * from loginclient ' \
                    'inner join client on loginclient.idc = client.id where loginclient.login like %s'
        cur1.execute(queryUser, (login,))
        infoUser = cur1.fetchone()
        return infoUser


    def getAccounts(self, id):
        cur1 = db.cursor()
        queryAccounts = 'select * from account where idc = %s'
        cur1.execute(queryAccounts, (id,))
        infoAccounts = cur1.fetchall()
        print("z db", infoAccounts)
        return infoAccounts


    def getOneAccount(self, accnum):
        cur1 = db.cursor()
        queryAccountsDetails = 'select * from account where accNum = %s'
        cur1.execute(queryAccountsDetails, (accnum,))
        detailsAccount = cur1.fetchone(0)
        return detailsAccount


    def getCards(self, accId):
        cur1 = db.cursor()
        queryCards = 'select * from card where ida = %s'
        cur1.execute(queryCards, (accId,))
        infoCards = cur1.fetchall()
        return infoCards


    def getOneCard(self, idcard):
        cur1 = db.cursor()
        queryCards = 'select * from card where id = %s'
        cur1.execute(queryCards, (idcard,))
        infoCard = cur1.fetchone()
        return infoCard

