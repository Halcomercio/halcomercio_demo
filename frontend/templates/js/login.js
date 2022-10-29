function loginUser(){
    let email = document.getElementById('login-name');
    let password = document.getElementById('login-pass');

    let payload = {
        "email": email.value,
        "password": password.value
      }

    var request = new XMLHttpRequest();
    request.open("POST","http://127.0.0.1:8000/signin/",true);
    request.setRequestHeader('Accept', 'application/json');
    request.setRequestHeader('Content-Type', 'application/json');

    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        console.log("Response : " + response);
        console.log("Status   : " + status);

        if (status == 202){
            window.location.replace("index.html");
            sessionStorage.setItem("token", json.user_dat);
            console.log("Response : " + response);
            alert
        }       
        else{
            alert(json.detail);
        }

    };
    request.send(JSON.stringify(payload));
};