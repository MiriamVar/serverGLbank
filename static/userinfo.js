let userData = {};
let accData = {};
let accounts = {};


$(document).ready(function(){
  userinfo();
  loadAccountes();
  $("#btnLogout").click(function() {logout();});

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
    $("#ownerFname").text(userData.fname, );
    $("#ownerLname").text(userData.lname);
}

function fillAccData(){
    $("#accNumber").text(accData.accNum);
    $("#currBal").text(accData.accAmount);
}

//function fillAccNumbers(){
//
//}



