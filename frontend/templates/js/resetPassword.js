function resetPassword(){
    let email = document.getElementById('login-name');

    console.log('Email Recibido : ' + email.value);

    payload = {"email" : email.value}
    var request = new XMLHttpRequest();
    request.open("POST","http://206.189.255.11/passwordR",true);
    request.setRequestHeader('Accept', 'application/json');
    request.setRequestHeader('Content-Type', 'application/json');

    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        if (status == 202){
            alert("Correo enviado");
            window.location.replace("/templates/login.html");
        }
        else{
            alert(json.detail);
        }
    };
    request.send(JSON.stringify(payload))
};