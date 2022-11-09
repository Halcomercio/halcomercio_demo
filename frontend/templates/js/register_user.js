function insertUser(){

    let email = document.getElementById('login-name');
    let password = document.getElementById('login-pass');
    let name = document.getElementById('name');
    let matricula = document.getElementById('matricula');

    console.log('Email Recibido : ' + email.value);
    console.log('Password Recibido : ' + password.value);
    console.log('Nombre Recibido : ' + name.value);
    console.log('Matricula Recibido : ' + matricula.value);

    let payload = {
        "name": name.value,
        "matricula": matricula.value,
        "email": email.value,
        "password": password.value
      }

    var request = new XMLHttpRequest();
    request.open("POST","http://206.189.255.11/register",true);
    request.setRequestHeader('Accept', 'application/json');
    request.setRequestHeader('Content-Type', 'application/json');

    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        console.log("Response : " + response);
        console.log("Status   : " + status);
        console.log("Payload  :"  + payload);

        if (status == 202){
            alert("Usuario creado con exito");
            window.location.replace("/index.html");
        }
        else{
            alert(json.detail);
        }

    };
    request.send(JSON.stringify(payload));
};