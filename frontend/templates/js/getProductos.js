function getProductos(){
    var request = new XMLHttpRequest();
    request.open('GET', 'http://206.189.255.11/getProducts');
    request.setRequestHeader('Accept', 'application/json');
    request.setRequestHeader('Content-Type', 'application/json');

    const tabla = document.getElementById('tabla-productos');

    var tableHead = document.createElement("thead");
    var tableBody = document.createElement("tbody");

    tableHead.innerHTML = `
        <tr>
            <th>Nombre</th>
            <th>Precio</th>
            <th>Cantidad</th>
            <th>Categoria</th>
            <th>Descripcion</th>
        </tr>
    `;

    request.onload = () => {
        const response = request.responseText;
        const json  = JSON.parse(response);
        console.log('Response: '+response);
        console.log('JSON: '+json);
        for (let i = 0; i < json.length; i++){

            var tr = document.createElement("tr");
            var tr_nombre = document.createElement("td");
            var tr_precio = document.createElement("td");
            var tr_cantidad = document.createElement("td");
            var tr_categoria = document.createElement("td");
            var tr_descripcion = document.createElement("td");

            tr_nombre.innerHTML = json[i].nombre;
            tr_precio.innerHTML = json[i].precio;
            tr_cantidad.innerHTML = json[i].stock;
            tr_categoria.innerHTML = json[i].categoria;
            tr_descripcion.innerHTML = json[i].descripcion;

            // DAR A CADAR TR(COLUMNAS) DEL HTML LOS VALORES DE CADA FILA
            tr.appendChild(tr_nombre);
            tr.appendChild(tr_precio);
            tr.appendChild(tr_cantidad);
            tr.appendChild(tr_categoria);
            tr.appendChild(tr_descripcion);
            // PASAR AL BODY DE LA TABLA LOS DATOS 
            tableBody.appendChild(tr);
        }

        tabla.appendChild(tableHead);
        tabla.appendChild(tableBody);

    };
    request.send();
};