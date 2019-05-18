from flask import Flask, render_template, request
import mysql.connector
import secrets

app = Flask(__name__)  # spravi z tohto suboru web aplikaciu


db = mysql.connector.connect(host='itsovy.sk', port='3306', database='glbank', user='glbank', password='password')


@app.route("/")  # pripajanie na web
def index():  # whoami bude default
    return render_template("index.html", )  # uz mam konkretnu stranku svoju, ak prijma parameter tak /?name=Mim


class UserToken(object):
    def __init__(self, clientID, clientToken):
        self.clientId = clientID
        self.clientToken = clientToken


@app.route("/login", methods=["POST"])
def register():
    login = request.form.get("name")
    password = request.form.get("pass")
    tokens = []

    if not login or not password:
        return "fail"

    # overenie ci taky client podla loginu existuje
    cur1 = db.cursor()
    queryLogin = "select idc from loginclient where login = %s;"
    cur1.execute(queryLogin, (login,))
    userLogin = cur1.fetchone()
    print(userLogin)
    idClient = userLogin[0]
    print(idClient)
    if userLogin is None:
        # user neexistuje
        return "Wrong login"
    else:
        #overuje blokovania uctu
        cur2 = db.cursor()
        queryBlockIB = "select * from loginhistory where idl = %s order by UNIX_TIMESTAMP(logDate) desc limit 3;"
        cur2.execute(queryBlockIB, (idClient,))
        records = cur2.fetchall()
        print(records)
        if not records:
            # insert do db - right
            cur4 = db.cursor()
            queryWrongLP = "insert into loginhistory (idl,success) values (%s,%s)"
            insert = cur4.execute(queryWrongLP, (idClient, 1))
            print(insert)
            db.commit()
            return render_template("userinfo.html")
        else:
            success = []
            for row in records:
                print(row)
                print(row[2])
                success.append(row[2])

            # if last record is not null
            if success[0] is not None:
                # success ci sa == 1 alebo sa da zretazit ??
                if success[0] == 1 and success[1] == 1 and success[2] == 1:
                    return "Your IB is blocked"
                else:
                    # "Your IB is unblocked"
                    # overuje sa ucet
                    cur = db.cursor()
                    queryClient = "SELECT * FROM client inner join loginclient on client.id=loginclient.idc where login = %s and password = %s;"
                    cur.execute(queryClient, (login, password))
                    user = cur.fetchone()
                    print(user)
                    if user is None:
                        # insert do db - wrong
                        cur4 = db.cursor()
                        queryWrongLP = "insert into loginhistory (idl,success) values (%s,%s)"
                        insert = cur4.execute(queryWrongLP, (idClient, 0))
                        print(insert)
                        db.commit()
                        return "You typed wrong password"
                    else:
                        # insert do db - right
                        cur4 = db.cursor()
                        queryWrongLP = "insert into loginhistory (idl,success) values (%s,%s)"
                        insert = cur4.execute(queryWrongLP, (idClient, 1))
                        print(insert)
                        db.commit()

                        # generate token
                        token = secrets.token_urlsafe()
                        print("Token: "+token)

                        # client = UserToken()
                        # client.clientId = idClient
                        # client.clientToken = token
                        #
                        # tokens.append(client)
                        #
                        # print("User id: %s" + client.clientId)
                        # print("User token: %s" + client.clientToken)
                        # # print(UserToken.clientId)
                        # # print(UserToken.clientToken)
                        #
                        # print("clienta by malo vypisat: "+tokens[0].clientId + " " +tokens[0].clientToken)

                        return render_template("userinfo.html")

            else:
                return "Your IB ib blocked by Bank Employee"

    db.close()


if __name__ == "__main__":
    app.run(debug=True)
