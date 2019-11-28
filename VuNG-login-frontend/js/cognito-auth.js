var ManTen = window.ManTen || {};

(function scopeWrapper($) {
    var signinUrl = 'signin.html';
    var indexUrl = 'index.html';

    var poolData = {
        UserPoolId: _config.cognito.userPoolId,
        ClientId: _config.cognito.userPoolClientId
    };

    var userPool;

    /*if (!(_config.cognito.userPoolId &&
          _config.cognito.userPoolClientId &&
          _config.cognito.region)) {
        $('#noCognitoMessage').show();
        return;
    }*/

    userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

    if (typeof AWSCognito !== 'undefined') {
        AWSCognito.config.region = _config.cognito.region;
    }

    ManTen.signOut = function signOut() {
        userPool.getCurrentUser().signOut();
    };

    ManTen.authToken = new Promise(function fetchCurrentAuthToken(resolve, reject) {
        var cognitoUser = userPool.getCurrentUser();
        var currentUserData = {};

        if (cognitoUser) {
            cognitoUser.getSession(function sessionCallback(err, session) {
            	
                /*if (err) {
                    reject(err);
                    //console.log(err);
                    //$(location).attr("href", signinUrl);
                } else if (!session.isValid()) {
                    resolve(null);
                    //console.log(err);
                    //$(location).attr("href", signinUrl);
                } else {
                    // get user property
                	cognitoUser.getUserAttributes(function(err, result) {
                        console.log(result)
                    	if (err) {
                            //console.log(err);
                        	$(location).attr("href", signinUrl);
                    	}
                    	
                    	// save user property in array
                    	for (i = 0; i < result.length; i++) {
                        	currentUserData[result[i].getName()] = result[i].getValue();
                    	}
                    	var username = currentUserData["email"]
                    	var username1 = username.split('@')
                    	$("div#menu h1").text("Welcome " + username1[0]);
                	});
                }*/
                $.ajax({
        			contentType : "application/json",
        			headers: {
                        'Content-Type':'application/json',
            			'Authorization': session.getIdToken().jwtToken
        			},
        			dataType : "json",
        			type : "GET",
        			url : "https://urz6axoj4b.execute-api.ap-northeast-1.amazonaws.com/dev/cognito-autho-sample",
        			success : function(data) {
            			$("div#menu h1").text(data);
        			},
        			error : function(data) {
            			console.log("error", data);
        			}
    			})
            });
        } else {
            resolve(null);
        }
    });


    /*
     * Cognito User Pool functions
     */

    function register(username, email, password, onSuccess, onFailure) {
        var dataEmail = {
            Name: 'email',
            Value: email
        };
        var attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute(dataEmail);

        userPool.signUp(username, password, [attributeEmail], null,
            function signUpCallback(err, result) {
                if (!err) {
                    onSuccess(result);
                } else {
                    onFailure(err);
                }
            }
        );
    }

    function signin(username, password, onSuccess, onFailure) {
        var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails({
            Username: username,
            Password: password
        });

        var cognitoUser = createCognitoUser(username);
        cognitoUser.authenticateUser(authenticationDetails, {
            onSuccess: onSuccess,
            onFailure: onFailure
        });
    }

    function verify(email, code, onSuccess, onFailure) {
        createCognitoUser(email).confirmRegistration(code, true, function confirmCallback(err, result) {
            if (!err) {
                onSuccess(result);
            } else {
                onFailure(err);
            }
        });
    }

    function createCognitoUser(email) {
        return new AmazonCognitoIdentity.CognitoUser({
            Username: email,
            Pool: userPool
        });
    }

    /*
     *  Event Handlers
     */

    $(function onDocReady() {
        $('#signinForm').submit(handleSignin);
        $('#registrationForm').submit(handleRegister);
        $('#verifyForm').submit(handleVerify);
    });

    function handleSignin(event) {
        var username = $('#usernameInputSignin').val();
        var password = $('#passwordInputSignin').val();
        event.preventDefault();
        signin(username, password,
            function signinSuccess() {           
                console.log('Successfully Logged In');
                window.location.href = indexUrl;
            },
            function signinError(err) {
                alert(err);
            }
        );
    }

    function handleRegister(event) {
        var username = $('#usernameInputRegister').val();
        var email = $('#emailInputRegister').val();
        var password = $('#passwordInputRegister').val();
        var password2 = $('#password2InputRegister').val();

        var onSuccess = function registerSuccess(result) {
            var cognitoUser = result.user;
            console.log('user name is ' + cognitoUser.getUsername());
            var confirmation = ('Registration successful.');
            alert(confirmation);
            if (confirmation) {
                window.location.href = indexUrl;
            }
        };
        var onFailure = function registerFailure(err) {
            alert(err);
        };
        event.preventDefault();

        if (password === password2) {
            register(username, email, password, onSuccess, onFailure);
        } else {
            alert('Passwords do not match');
        }
    }

    function handleVerify(event) {
        var email = $('#emailInputVerify').val();
        var code = $('#codeInputVerify').val();
        event.preventDefault();
        verify(email, code,
            function verifySuccess(result) {
                console.log('call result: ' + result);
                console.log('Successfully verified');
                alert('Verification successful. You will now be redirected to the login page.');
                window.location.href = signinUrl;
            },
            function verifyError(err) {
                alert(err);
            }
        );
    }
}(jQuery));
