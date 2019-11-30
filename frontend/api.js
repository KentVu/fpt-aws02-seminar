// var AmazonCognitoIdentity = import("./vendor/amazon-cognito-identity.min.js");
// var AWSCognito = import("./vendor/aws-cognito-sdk.min.js");

var API_URL = "https://kjo9vkj58l.execute-api.ap-northeast-1.amazonaws.com/dev";
var TOKEN = "";
var TOKEN_O = {};

function verify() {
    TOKEN = localStorage.token;
    if (!TOKEN) {
        alert("Log in please!");
        window.location.replace("login-register.html");
    }

    TOKEN_O = jQuery.parseJSON(TOKEN);
    var verifyData = {
        "token": TOKEN
    };
    $.ajax({
        type: "POST",
        url: API_URL + "/verify",
        data: JSON.stringify(verifyData),
        success: function (data) {
            console.log('success:');
            console.log(data);
            if (!data || !data['result'] || data['result'] == 'error') {
                alert("Log in please!");
                window.location.replace("login-register.html");
            }

        }, error: function (data) {
            console.log('An error occurred:');
            console.log(data);
            alert("Log in please!");
            window.location.replace("login-register.html");
        }
    });
};
