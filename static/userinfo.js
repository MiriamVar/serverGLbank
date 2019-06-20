let userData = {};
let accData = {};
let accounts = {};
let transaction = {};
let cards = {};
let accForPayment = "";
let transactions1 ={};
let transactions2 = {};


$(document).ready(function(){
  userinfo();
  loadAccountes();
  $("#btnLogout").click(function() {
    logout();
  });
  document.getElementById('userProfile').style.display= "none";
  document.getElementById('containerAccounts').style.display ="none";
  document.getElementById('containerCards').style.display ="none";
  document.getElementById('createPay').style.display ="none";
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
    console.log("loaduju sa accounty");
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
            loadCards();
            loadTransactions2();
        }
        else{
            $("#accNumber").text("You don't have any accounts.");
            $("#containerAccounts").text("You don't have any accounts.");
        }
      }
  });
}

function loadCards(){
    console.log("loaduju sa karty");
    let data = {token : window.tokenSecret, id : window.userID};
    data = JSON.stringify(data);
    console.log(data);
    $.ajax({
      type: 'POST',
      url: "/cards",
      data: data,
      contentType:"application/json; charset=utf-8",
        dataType:"json",
      success: function(resultData) {
        cards = resultData;
        console.log(resultData);
        if(resultData.length > 0){
            cardsMenu();
        }
        else{
            $("#containerCards").text("You don't have any cards.");
        }
      }
  });
}

function accountsMenu(){
    $("#containerAccounts").empty();
    console.log("acounty usera, acounts menu");
    console.log(accounts);
    for(var i=0; i<accounts.length; i++){
         makeAccountDiv(accounts[i])
    }
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
    console.log("loaduju sa prve trans");
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
        transactions1 = resultData;
        console.log(resultData);
        console.log("ma urobit cyklus")
        console.log(resultData.length)
        if(resultData.length > 0){
            var table = document.getElementById("allTransUP");
            for(var j=0; j<1;j++){
                var row = table.insertRow(j);
                var cell = row.insertCell(0);
                cell.innerHTML = "Id Account"

                var cellO = row.insertCell(0+1);
                cellO.innerHTML = "Rec Account"

                var cellP = row.insertCell(0+2);
                cellP.innerHTML = "TransDate"

                var cellL = row.insertCell(0+3);
                cellL.innerHTML = "TransAccount"
            }

            var table = document.getElementById("tbltrans");
            for(var i=0; i<resultData.length; i++){
                var row = table.insertRow(i);

                var cell1 = row.insertCell(0);
                cell1.innerHTML = resultData[i][1];

                var cell2 = row.insertCell(0+1);
                cell2.innerHTML = resultData[i][2];

                var cell3 = row.insertCell(0+2);
                var stringDate = (resultData[i][4]);
                console.log("string date .. jaky vytiahnem");
                console.log(stringDate);
                var d = new Date(stringDate);
                cell3.innerHTML = d.getFullYear()+"-"+("0"+(d.getMonth()+1)).slice(-2)+"-"+("0" + d.getDate()).slice(-2)+" "+("0" + d.getHours()).slice(-2)+":"+("0" + d.getMinutes()).slice(-2)+":"+("0" + d.getSeconds()).slice(-2);

                var cell4 = row.insertCell(0+3);
                cell4.innerHTML ="+"+resultData[i][5];
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
      success: function(resultData) { window.tokenSecret = ""; window.userID=""; userData =""; accData =""; accounts =""; transaction = ""; window.location.href="http://localhost:5000";}
  });
}

function changePassword(){
    let data = {token : window.tokenSecret, id : window.userID, old : $("#oldPassword").val(), newP : $("#newPassword").val(), confP : $("#confirmPassword").val()};
    data = JSON.stringify(data);
    console.log(data);
    alert(data);
    $.ajax({
      type: 'POST',
      url: "/changepassword",
      data: data,
      contentType:"application/json; charset=utf-8",
        dataType:"json",
      success: function(resultData) {
      console.log(resultData);
      console.log("change urobeny");
      var obj = JSON.stringify(resultData);
      console.log(obj);
      if (obj.status = "OK"){
        clearInputs();
        $("#error").text("Your passsword has been changed.");
        $('#error').css("color", "green");
      }
      else{
        clearInputs();
        $("#error").text("Your passsword has not been changed.");
        $('#error').css("color", "red");
      }
      }
  });
}

function cardsMenu(){
    $("#containerCards").empty();
    console.log("karty usera, cards menu");
    console.log(cards);
    for(var i=0; i<cards.length; i++){
         makeCardDiv(cards[i])
    }
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
    document.getElementById('userProfile').style.display ="block";
    document.getElementById('containerAccounts').style.display ="none";
    document.getElementById('containerCards').style.display ="none";
    document.getElementById('createPay').style.display ="none";
}

function showing(){
    document.getElementById('mainDiv').style.display = "block";
    document.getElementById('userProfile').style.display ="none";
    document.getElementById('containerAccounts').style.display ="none";
    document.getElementById('containerCards').style.display ="none";
    document.getElementById('createPay').style.display ="none";
}

function showingAcc(){
    document.getElementById('mainDiv').style.display = "none";
    document.getElementById('userProfile').style.display ="none";
    document.getElementById('containerAccounts').style.display ="block";
    document.getElementById('containerCards').style.display ="none";
    document.getElementById('createPay').style.display ="none";
    accountsMenu();
}

function showingCards(){
    document.getElementById('mainDiv').style.display = "none";
    document.getElementById('userProfile').style.display ="none";
    document.getElementById('containerAccounts').style.display ="none";
    document.getElementById('containerCards').style.display ="block";
    document.getElementById('createPay').style.display ="none";
    cardsMenu();
}

function showingPay(idAcc){
    document.getElementById('mainDiv').style.display = "none";
    document.getElementById('userProfile').style.display ="none";
    document.getElementById('containerAccounts').style.display ="none";
    document.getElementById('containerCards').style.display ="none";
    document.getElementById('createPay').style.display ="block";
    accForPayment = idAcc;
}

function makeAccountDiv(data){
  console.log("data v make accoutns... vytvaraju na tabulky s datami");
  let container = $("#containerAccounts");
  let smallDivAcc = $('<div class="smallDivAcc"><div class="credentialsAcc"><label class="accOwner">Account Number:  <span class="numberA">'+data[2]+'</span></label></div><hr style="margin-top: 0px;"><label class="balanceCur"> Current Balance: <span class="money">'+data[3]+'</span><span id="euro">€</span></label><div id="acc'+data[0]+'" class="pay">Payment</div></div>');
    $("div").click(function(){
    $("#acc"+data[0]).attr("onclick", "showingPay("+data[0]+")");
  });
  container.append(smallDivAcc);
}

function makeCardDiv(data){
  console.log("data v make cards... vytvaraju sa tabulky s datami");
  console.log(data);
  let container = $("#containerCards");
  let active ="";
  if(data[5] == 0){
    active = "False";
  }
  else{
    active = "True";
  }
  let smallDivCard = $('<div class="smallDivCard"><div class="credentialsAcc"><label class="accOwner">Account ID:  <span class="numberA">'+data[1]+'</span></label></div><hr style="margin-top: 0px;"><label class="accOwner"> PIN: <span class="numberA">'+data[2]+'</span></label><div class="accOwner">Expire Date: <span class="numberA">'+data[3]+'</span> <span id="slash">/</span><span class="numberA">'+data[4]+'</span></div><label class="accOwner"> Active: <span id="activeCH" class="numberA">'+active+'</span></label><div class="block">Block</div></div></div>');
  $("div").click(function(){
    $(".block").attr("onclick", "blockingCard("+data[1]+")");
  });
  container.append(smallDivCard);
}

function clearInputs(){
    $('#oldPassword').val('');
    $('#newPassword').val('');
    $('#confirmPassword').val('');
}

function clearInputsPay(){
    $('#moneyToSent').val('');
    $('#recipient').val('');
}

function blockingCard(num){
    let data = {token : window.tokenSecret, id : window.userID, accId: num, };
    data = JSON.stringify(data);
    console.log(data);
    $.ajax({
      type: 'POST',
      url: "/blockcard",
      data: data,
      contentType:"application/json; charset=utf-8",
        dataType:"json",
      success: function(resultData) {
      console.log(resultData);
      console.log("block urobeny");
      var obj = JSON.stringify(resultData);
      console.log(obj);
      if (obj.status = "OK"){
        $("#activeCH").text("False");
      }
      }
  });
}

function loadTransactions2(){
    console.log("loaduju sa druhe trans");
    let data = {token : window.tokenSecret, id : window.userID,};
    data = JSON.stringify(data);
    console.log(data);
    $.ajax({
      type: 'POST',
      url: "/trans",
      data: data,
      contentType:"application/json; charset=utf-8",
        dataType:"json",
      success: function(resultData) {
        transactions2 = resultData;
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
                var stringDate = (resultData[i][4]);
                console.log("string date .. jaky vytiahnem");
                console.log(stringDate);
                var d = new Date(stringDate);
                cell3.innerHTML = d.getFullYear()+"-"+("0"+(d.getMonth()+1)).slice(-2)+"-"+("0" + d.getDate()).slice(-2)+" "+("0" + d.getHours()).slice(-2)+":"+("0" + d.getMinutes()).slice(-2)+":"+("0" + d.getSeconds()).slice(-2);

                var cell4 = row.insertCell(0+3);
                cell4.innerHTML ="-"+resultData[i][5];

            }
            createChart();
        }
        else{
            $("#allTrans").text("You don't have any transactions on this account.");
        }
        }
     });
}

function sendingMoney(){
    let data = {token : window.tokenSecret, id : window.userID, idAcc: accForPayment, amount: Number($("#moneyToSent").val()), recNum: $("#recipient").val()};
    data = JSON.stringify(data);
    console.log(data);
    $.ajax({
      type: 'POST',
      url: "/sendMoney",
      data: data,
      contentType:"application/json; charset=utf-8",
        dataType:"json",
      success: function(resultData) {
        console.log(resultData);
        console.log("peniaze poslane");
        var obj = JSON.stringify(resultData);
        console.log(obj);
         if (obj.status = "OK"){
            clearInputsPay();
            $("#errPay").text("Your payment was successful.");
            $('#errPay').css("color", "green");
         }
        else{
            clearInputsPay();
            $("#errPay").text("Your payment was not successful.");
            $('#errPay').css("color", "red");
        }
      }
  });
}

function createChart(){
     console.log("vytvara sa chart");
     console.log(transactions1);
     console.log(transactions2);
     var chart = document.getElementById("expenses").getContext('2d');
     var expense = [];
     var income = [];

      for(var i=0; i<transactions2.length;i++){
        swap_expense = transactions2[i][5];
        expense.push(swap_expense);
    }
    for(var j=0; j<transactions1.length;j++){
        swap_income = transactions1[j][5];
        income.push(swap_income);
    }
    console.log("incomes");
    console.log(income);
    console.log("expenses");
    console.log(expense);


    let barChart = new Chart(chart, {
        type: 'bar',
        data:{
            labels: ["January", "February", "March","April","May","June","July","August","September","October","November","December"],
            datasets: [{
                label: 'Income',
                data: income,
                backgroundColor: '#8ed18e',
                borderWidth: 0,
            },{
                label: 'Expenses',
                data: expense,
                backgroundColor: '#f48484',
                borderWidth: 0,
            }]
        },
    });

}
