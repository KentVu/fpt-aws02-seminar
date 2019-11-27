// var AmazonCognitoIdentity = import("./vendor/amazon-cognito-identity.min.js");
// var AWSCognito = import("./vendor/aws-cognito-sdk.min.js");

var API_URL = "https://kjo9vkj58l.execute-api.ap-northeast-1.amazonaws.com/dev";

function verify() {
    var token = localStorage.token;
    if (!token) {
        alert("Log in please!");
        window.location.replace("login-register.html");
    }
    var verifyData = {
        "token": token
    };
    $.ajax({
        type: "POST",
        url: API_URL + "/verify",
        data: JSON.stringify(verifyData),
        //Bach's code: fix CORS bug
        headers:{
        	'Content-Type':'application/json'
      	},
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

// var UserPoolId = "ap-northeast-1_qq5PZSCpC";
// var AppClientId = "112nlnmfihjfahnbl4h8evlb7";
// var AwsRegion = "ap-northeast-1";

// if (typeof AWSCognito !== 'undefined') {
//     AWSCognito.config.region = AwsRegion;
// }

// var poolData = {
//     UserPoolId: UserPoolId,
//     ClientId: AppClientId
// };
// var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

// function signOut() {
//     userPool.getCurrentUser().signOut();
// };

// function register(username, email, password, onSuccess, onFailure) {
//     var dataEmail = {
//         Name: 'email',
//         Value: email
//     };
//     var attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute(dataEmail);

//     userPool.signUp(username, password, [attributeEmail], null,
//         function signUpCallback(err, result) {
//             if (!err) {
//                 onSuccess(result);
//             } else {
//                 onFailure(err);
//             }
//         }
//     );
// }

// function signin(username, password, onSuccess, onFailure) {
//     var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails({
//         Username: username,
//         Password: password
//     });

//     var cognitoUser = createCognitoUser(username);
//     cognitoUser.authenticateUser(authenticationDetails, {
//         onSuccess: onSuccess,
//         onFailure: onFailure
//     });
// }

// function verify(email, code, onSuccess, onFailure) {
//     createCognitoUser(email).confirmRegistration(code, true, function confirmCallback(err, result) {
//         if (!err) {
//             onSuccess(result);
//         } else {
//             onFailure(err);
//         }
//     });
// }