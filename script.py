from json import dumps

from flask import Flask, render_template, request, jsonify, json, make_response
import secrets
import hashlib
from database.MyDb import Databaza


app = Flask(__name__)  # spravi z tohto suboru web aplikaciu
db = Databaza()


@app.route("/")  # pripajanie na web
def index():  # whoami bude default
    return render_template("index.html", )  # uz mam konkretnu stranku svoju, ak prijma parameter tak /?name=Mim


class UserToken(object):
    def __init__(self, clientId, clientToken, clientLogin):
        self.clientId = clientId
        self.clientToken = clientToken
        self.clientLogin = clientLogin


class Account(object):
    def __init__(self, accId, clientId, accNum, accAmount):
        self.accId = accId
        self.clientId = clientId
        self.accNum = accNum
        self.accAmount = accAmount


class Card(object):
    def __init__(self, cardId, accId, pin, expirem, expirey, active):
        self.cardId =cardId
        self.accId = accId
        self.pin = pin
        self.expirem = expirem
        self.expirey = expirey
        self.active = active


class UserInfo(object):
    def __init__(self, login, fname, lname, mail):
        self.login = login
        self.fname = fname
        self.lname = lname
        self.mail = mail


tokens = []

json_user = []
accountiky = dict()
allCards = dict()


# ide
@app.route("/login", methods=["POST"])
def register():
    login = request.form.get("name")
    passswap = request.form.get("pass")
    if login == "" or login is None or passswap == "" or passswap is None:
        return jsonify({"mess": "blud"})
    encoder = hashlib.md5()
    encoder.update(passswap.encode('utf-8'))
    password = encoder.hexdigest()
    print(password)
    # password = hashlib.md5(passswap.encode()).hexdigest()
    # encoder = hashlib.md5()
    # encoder.update(passswap)
    # password = encoder.hexdigest()
    print(password)
    if not login or not password:
        return render_template("loginError.html", usernameErr="", passwordErr="", blockedErr="Wrong username or password.")

    # overenie ci taky client podla loginu existuje
    userLogin = db.Login(login=login)

    print(userLogin)
    if userLogin is None:
        # user neexistuje
        return render_template("loginError.html", usernameErr="Wrong username.", passwordErr="", blockedErr="")
    else:
        idClient = userLogin[0]
        print(idClient)

        # overuje blokovania uctu
        records = db.AccountIsBlocked(idClient=idClient)
        print(records)
        if not records:
            # insert do db - right
            db.InsertToDb(idClient=idClient)

            # generate token
            token = secrets.token_urlsafe()

            client = UserToken(clientId=idClient, clientToken=token, clientLogin=login)
            tokens.append(client)

            return render_template("userinfo.html", token=token, userID=idClient)
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
                    return render_template("loginError.html", usernameErr="", passwordErr="", blockedErr="Your IB is blocked.")
                else:
                    # "Your IB is unblocked"

                    # overuje sa ucet
                    user = db.verification(login=login, password=password)
                    print("User")
                    print(user)

                    if user is None:
                        # insert do db - wrong
                        db.wrongInsert(idClient=idClient)
                        return render_template("loginError.html", usernameErr="", passwordErr="Wrong Password.", blockedErr="")
                    else:
                        json_user.append({'id': user[0], 'name': user[1], 'surname': user[2], 'email': user[3]})
                        print("Userko")
                        print(json.dumps({'user': json_user}))

                        # insert do db - right
                        db.InsertToDb(idClient=idClient)

                        # generate token
                        token = secrets.token_urlsafe()

                        client = UserToken(clientId=idClient, clientToken=token, clientLogin=login)
                        tokens.append(client)

                        print(client.clientId)
                        print(client.clientToken)
                        print("clienta by malo vypisat")
                        print(tokens[0].clientId)
                        print(tokens[0].clientToken)

                        return render_template("userinfo.html", token=token, userID=idClient)

            else:
                return render_template("loginError.html", usernameErr="", passwordErr="",
                                       blockedErr="Your IB is blocked by Bank Employee.")


# ide
@app.route("/userinfo", methods=["POST"])
def userDetails():
    token = ""
    id = ""
    if request.is_json:
        content = request.get_json()
        token = content["token"]
        id = content["id"]
    else:
        return jsonify({"status": "wrong request"})
    login = getLogin(token, id)
    if login is not None:
        print("dostanem sa tu")
        infoUser = db.getUserInfo(login=login)
        print("info o userovi .. druha route")
        print(infoUser)
        return jsonify({"login": infoUser[2], "fname": infoUser[5], "lname": infoUser[6], "mail": infoUser[7]})
    else:
        return "wrong credentials"


# ide
@app.route("/logout", methods=["POST"])
def logout():
    i = 0
    x = json.loads(request.data)
    print(x["token"])
    for element in tokens:
        if element.clientToken == x["token"] and element.clientId == x["id"]:
            del tokens[i]
            print("zmazalo token")
            break
        else:
            i += 1
    return jsonify({"mess": "OK"})


# ide
@app.route("/accounts", methods=["POST"])
def accounts():
    token = ""
    id = ""
    if request.is_json:
        content = request.get_json()
        token = content["token"]
        id = content["id"]
    else:
        return jsonify({"status": "wrong request"})
    if isValidTokenAndId(token, id) is True:
        print("dostanem sa tuuuu UCTY")
        infoAccounts = db.getAccounts(id=id)
        print(infoAccounts)

        swap_accounts = []
        for row in infoAccounts:
            swap_accounts.append(row)
            print(row)

        accountiky[token] = swap_accounts
        accounts2 = json.dumps(swap_accounts, separators=(',', ':'))
        print("JSON acoounty")
        print(accounts2)

        print("info o accountoch... stvrta  route")
        return accounts2
    else:
        return jsonify({"status": "wrong credentials"})


# ide
@app.route("/accountsinfo", methods=["POST"])
def accountsInfo():
    token = ""
    id = ""
    if request.is_json:
        content = request.get_json()
        token = content["token"]
        id = content["id"]
    else:
        return jsonify({"status": "wrong request"})

    accnum = getAccnum(token, id)

    if accnum is not None:
        print("dostanem sa tu intoooooooo")
        detailsAccount = db.getOneAccount(accnum=accnum)
        print("info o accountoch... piata  route")
        print(detailsAccount)
        return jsonify({"accId": detailsAccount[0], "clientId": detailsAccount[1], "accNum": detailsAccount[2],
                        "accAmount": detailsAccount[3]})
    else:
        return jsonify({"status": "wrong credentials"})


@app.route("/cards", methods=["POST"])
def cards():
    token = ""
    id = ""
    if request.is_json:
        content = request.get_json()
        token = content["token"]
        id = content["id"]
    else:
        return jsonify({"status": "wrong request"})

    accId = getAccid(token, id)
    print('idecko accountu')
    print(accId)
    if accId is not None:
        print("dostanem sa tuuuuu kartyyyy")
        infoCards = db.getCards(accId=accId)
        print(infoCards)

        swap_cards = []
        for row in infoCards:
            swap_cards.append(row)
            print(row)

        allCards[token] = swap_cards
        cards2 = json.dumps(swap_cards, separators=(',', ':'))
        print("JSON karty")
        print(cards2)

        print("info o kartach... siesta  route")
        return cards2
    else:
        return jsonify({"status": "wrong credentials"})
#
#
# @app.route("/cardsinfo", methods=["POST"])
# def cardsinfo():
#     token = ""
#     id = ""
#     if request.is_json:
#         content = request.get_json()
#         token = content["token"]
#         id = content["id"]
#     else:
#         return jsonify({"status": "wrong request"})
#
#     idcard = getCardID(token, id)
#     if idcard is not None:
#         print("dostanem sa tu")
#         infoCard = db.getOneCard(idcard=idcard)
#         print(infoCard)
#         print("info o karte... siedma  route")
#         return jsonify({"cardId": infoCard[0], "accId": infoCard[1], "pin": infoCard[2],
#                         "expirem": infoCard[3], "expirey": infoCard[4], "active": infoCard[5]})
#     else:
#         return jsonify({"status": "wrong credentials"})
#
#


#ide
@app.route("/transactions", methods=["POST"])
def transactions():
    token = ""
    id = ""
    print(id)
    if request.is_json:
        content = request.get_json()
        token = content["token"]
        id = content["id"]
    else:
        return jsonify({"status": "wrong request"})

    accId = getAccid(token, id)
    print("transaction accid ma vypisat")
    print(accId)
    if accId is not None:
        print("dostanem sa tu")
        infotrans = db.getTrans(accid=accId)
        print(infotrans)
        trans = []

        for row in infotrans:
            trans.append(row)
            print(row)

        trans2 = json.dumps(trans, separators=(',', ':'))
        print("JSON transactions")
        print(trans2)

        print("info o transactions... deviata  route")
        return trans2
    else:
        return jsonify({"status": "wrong credentials"})


@app.route("/changepassword", methods=["POST"])
def changePass():
    token = ""
    id = ""
    swap_oldPass = ""
    newPass = ""
    newPass2 = ""
    oldPass = ""

    if request.is_json:
        content = request.get_json()
        token = content["token"]
        id = content["id"]
        swap_oldPass = content["old"]
        newPass = content["newP"]
        newPass2 = content["confP"]
    else:
        return jsonify({"status": "wrong request prvy"})

    login = getLogin(token, id)
    print(login)
    if login == "" or login is None:
        return
    if login is not None and newPass == newPass2:
        print("dostanem sa tu ... na change password")
        oldPass = hashlib.md5(swap_oldPass.encode()).hexdigest()
        swap_newPass = hashlib.md5(newPass.encode()).hexdigest()
        db.changePass(newPass=swap_newPass, login=login, oldPass=oldPass)
        print("info o karte... siedma  route")
        return jsonify({"status": "OK"})
    else:
        return jsonify({"status": "wrong request druhy"})


# @app.route("/blockcard", methods=["POST"])
# def blockingcard():


def isValidTokenAndId(token, id):
    print(token)
    for element in tokens:
        if element.clientToken == token and element.clientId == id:
            return True
    return False


def getLogin(token, id):
    print(token)
    for element in tokens:
        if element.clientToken == token and element.clientId == id:
            login = element.clientLogin
            print(login)
            return login
    return None


def getAccid(token, id):
    for element in tokens:
        if element.clientToken == token and element.clientId == id:
            for swap in accountiky[token]:
                accId = swap[0]
                print(accId)
                return accId


def getAccnum (token, id):
    for element in tokens:
        if element.clientToken == token and element.clientId == id:
            for swap in accountiky[token]:
                accnum = swap[2]
                print(accnum)
                return accnum


def getCardID(token, id):
    for element in tokens:
        if element.clientToken == token and element.clientId == id:
            for swap in allCards[token]:
                idcard = swap[0]
                print(idcard)
                return idcard


if __name__ == "__main__":
    app.run(debug=True)
