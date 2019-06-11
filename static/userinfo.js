let userData = {};
let accData = {};
let accounts = {};
let transaction = {};


$(document).ready(function(){
  userinfo();
  loadAccountes();
  $("#btnLogout").click(function() {
    logout();
  });
  document.getElementById('userko').style.display= "none"

});


function userinfo(){
  let data = {token : window.tokenSecret, id : window.userID};
    data = JSON.stringify(data);
    console.log(data);
    $.ajax({
      type: 'POST',
      url: "/userinfo",
      data: data,
      contentType:"application/json; charset=utf-8",
        dataType:"json",
      success: function(resultData) { userData = resultData; console.log(resultData); fillUserData(); }
  });
}

function loadAccountes(){
    let data = {token : window.tokenSecret, id : window.userID};
    data = JSON.stringify(data);
    console.log(data);
    $.ajax({
      type: 'POST',
      url: "/accounts",
      data: data,
      contentType:"application/json; charset=utf-8",
        dataType:"json",
      success: function(resultData) {
        accounts = resultData;
        console.log(resultData);
        if(resultData.length > 0){
            let accnum = resultData[0].accNum;
            accinfo(accnum);
            loadTransactions();
        }
        else{
            $("#accNumber").text("You don't have any accounts.");
        }
      }
  });
}

function accountsMenu(){
   let data = {token : window.tokenSecret, id : window.userID};
   data = JSON.stringify(data);
   console.log(data);
   $.ajax({
     type: 'POST',
     url: "/accounts",
     data: data,
     contentType:"application/json; charset=utf-8",
       dataType:"json",
     success: function(resultData) {
       accounts = resultData;
       console.log("acounty usera, acounts menu");
       console.log(resultData);
       for (var item in resultData) {
         makeAccountDiv(item);
       }
     }
 });
}


function accinfo(accnum){
    let data = {token : window.tokenSecret, id : window.userID,};
    data = JSON.stringify(data);
    console.log(data);
    $.ajax({
      type: 'POST',
      url: "/accountsinfo",
      data: data,
      contentType:"application/json; charset=utf-8",
        dataType:"json",
      success: function(resultData) { accData = resultData; console.log(resultData); fillAccData();}
  });
}

function loadTransactions(){
    let data = {token : window.tokenSecret, id : window.userID};
    data = JSON.stringify(data);
    console.log(data);
    $.ajax({
      type: 'POST',
      url: "/transactions",
      data: data,
      contentType:"application/json; charset=utf-8",
        dataType:"json",
      success: function(resultData) {
        transactions = resultData;
        console.log(resultData);
        console.log("ma urobit cyklus")
        console.log(resultData.length)
        if(resultData.length > 0){
            var table = document.getElementById("tbltrans");
            for(var i=1; i<resultData.length; i++){
                var row = table.insertRow(i);
                var cell1 = row.insertCell(0);
                cell1.innerHTML = resultData[i][1];
                var cell2 = row.insertCell(0+1);
                cell2.innerHTML = resultData[i][2];
                var cell3 = row.insertCell(0+2);
                cell3.innerHTML = resultData[i][4];
                var cell4 = row.insertCell(0+3);
                cell4.innerHTML = resultData[i][5];
            }
        }
        else{
            $("#allTrans").text("You don't have any transactions on this account.");
        }
        }
     });
}

function logout(){
    let data = {token : window.tokenSecret, id : window.userID,};
    data = JSON.stringify(data);
    console.log(data);
    $.ajax({
      type: 'POST',
      url: "/logout",
      data: data,
      contentType:"application/json; charset=utf-8",
        dataType:"json",
      success: function(resultData) { window.tokenSecret = ""; window.userID=""; window.location.href="http://localhost:5000";}
  });
}






function fillUserData(){
    $("#ownerFname").text(userData.fname);
    $("#ownerLname").text(userData.lname);
    $("#tblName").text(userData.fname);
    $("#tblSurname").text(userData.lname);
    $("#tblLogin").text(userData.login);
    $("#tblEmail").text(userData.mail);
}

function fillAccData(){
    $("#accNumber").text(accData.accNum);
    $("#currBal").text(accData.accAmount);
}


function hiding(){
    document.getElementById('mainDiv').style.display = "none";
    document.getElementById('userko').style.display ="block";
}

function showing(){
    document.getElementById('mainDiv').style.display = "block";
    document.getElementById('userko').style.display ="none";
}

function showingAcc(){
    document.getElementById('mainDiv').style.display = "none";
    document.getElementById('containerAccounts').style.display ="block";
    accountsMenu();
}

function makeAccountDiv(data){
  let container = $("#containerAccounts");
  let smallDivAcc = $('<div>');
  smallDivAcc.className = "smallDivAcc";

  let credentialsAcc = document.createElement("DIV");
  credentialsAcc.className = "credentialsAcc";

  let numberAcc = document.createElement("LABEL");
  numberAcc.className = "accOwner";
  let numberA = document.createElement("SPAN");
  numberA.className = "numberA";
  numberA.value = data[2];

  numberAcc.appendChild(numberA);
  credentialsAcc.appendChild(numberAcc);

  let line = document.createElement("HR");
  credentialsAcc.appendChild(line);

  let balanceCur = document.createElement("LABEL");
  balanceCur.className = "balanceCur";
  let money= document.createElement("SPAN");
  money.className= "money";
  money.value = data[3];
  let pay = document.createElement("DIV");
  pay.className= "pay";

  balanceCur.appendChild(money);
  credentialsAcc.appendChild(balanceCur);
  credentialsAcc.appendChild(pay);

  smallDivAcc.append(credentialsAcc);
  container.append(smallDivAcc);
}



