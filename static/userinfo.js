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

//function accountsMenu(){
//    let data = {token : window.tokenSecret, id : window.userID};
//    data = JSON.stringify(data);
//    console.log(data);
//    $.ajax({
//      type: 'POST',
//      url: "/accounts",
//      data: data,
//      contentType:"application/json; charset=utf-8",
//        dataType:"json",
//      success: function(resultData) {accounts = resultData;console.log(resultData);
//      }
//  });
//}


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
         var count = 0
            for(var i=0; i<resultData.length; i++){
                var table = document.getElementById("tbltrans");
                var row = table.insertRow(i);

                var cell1 = row.insertCell(i);
                cell1.innerHTML = resultData[1];
                var cell2 = row.insertCell(i+1);
                cell2.innerHTML = resultData[2];
                var cell3 = row.insertCell(i+2);
                cell3.innerHTML = resultData[4];
                var cell4 = row.insertCell(i+3);
                cell4.innerHTML = resultData[3];
               }
                count++;
        }
        else{
            $("#accNumber").text("You don't have any accounts.");
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
    $("tblName").text(userData.fname);
    $("tblSurname").text(userData.lname);
    $("tblLogin").text(userData.login);
    $("tblEmail").text(userData.mail);
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



