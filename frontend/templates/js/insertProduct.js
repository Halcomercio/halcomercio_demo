function insertProduct() {
    let nombreP = document.getElementById("nombreP").value;
    let precioP = document.getElementById("precioP").value;
    let descripcionP = document.getElementById("descripcionP").value;
    let categoriaP = document.getElementById("categoria").value;
    let stockP = document.getElementById("cantidadP").value;

    let payload = 
        {
            "nombre": nombreP,
            "descripcion": descripcionP,
            "precio": precioP,
            "categoria": categoriaP,
            "stock": stockP,
            "uid_vendedor": "string"
    }

    var request = new XMLHttpRequest();
    request.open("POST","http://206.189.255.11/addProduct",true);
    request.setRequestHeader('Accept', 'application/json');
    request.setRequestHeader('Content-Type', 'application/json');

    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        console.log("Response : " + response);
        console.log("Status   : " + status);
        console.log("Payload  :"  + payload);

        if (status == 200){
            alert("Producto creado con exito");
            window.location.replace("catalogo.html");
        }
        else{
            alert(json.detail);
        }

    };
    request.send(JSON.stringify(payload));
};