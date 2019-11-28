var jose = require('node-jose');
 
exports.handler = async (event) => {
    try{
        var token     = event.headers["Authorization"];
        var sections  = token.split('.');
        var payload   = jose.util.base64url.decode(sections[1]);
        payload       = JSON.parse(payload);
         
        // 以下の要領で、ユーザープールの各項目を取得できる
        console.log("Cognito User (username) : " + payload["cognito:username"]);
        console.log("Cognito User (email) : " + payload["email"]);
 
        const response = {
            statusCode: 200,
            headers: {
                "Access-Control-Allow-Origin" : "*", 
                "Access-Control-Allow-Credentials" : true,  
                "Access-Control-Allow-Headers" : "Origin, X-Requested-With, Content-Type, Accept"
            },
            body: JSON.stringify("ようこそ！" + payload["cognito:username"] + "さん"),
        };
        return response;
    } catch (err) {
        // エラー発生時はエラー文をreturnする
        console.error(`[Error]: ${JSON.stringify(err)}`);
        return err;
    }
};
