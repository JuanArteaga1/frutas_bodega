function enviarDatosAlServidor(url, datos) {
    fetch(url, {
        method: 'POST',  // Método HTTP POST para enviar datos
        headers: {
        'Content-Type': 'application/json',  // Indicamos que estamos enviando datos en formato JSON
    },
      body: JSON.stringify(datos),  // Convertimos los datos en formato JSON
    })
    .then(response => response.json())  // Convertimos la respuesta en JSON
    .then(data => {
      console.log('Respuesta del servidor:', data);  // Mostramos la respuesta del servidor en la consola
    })
    .catch((error) => {
      console.error('Error al enviar los datos:', error);  // Manejamos cualquier error
    });
  }


function enviarDatos() {
    const datosProducto = {
        tipo: "producto",
        id_producto: document.getElementById("id_producto").value,
        nombre: document.getElementById("nombre").value,
        origen: document.getElementById("origen").value,
        precio: document.getElementById("precio").value,
        cantidad: document.getElementById("cantidad").value
    };

    // Llamar a la función para enviar los datos al servidor
    enviarDatosAlServidor('http://127.0.0.1:5000/agregar_fruta', datosProducto);
    
}
document.getElementById('btn_agregar').addEventListener('click', enviarDatos);


function capturaSacar(){
    var id,nomfruta,cantidad;

    id = document.getElementById("id_producto").value;
    nomfruta = document.getElementById("nombre").value;
    cantidad = document.getElementById("cantidad").value;


    console.log("ID: " + id + ", nombre: "+ nomfruta + ", cantidad: "+ cantidad);

    alert("exitoso")

    document.querySelector(".formulario-producto").reset();

}
//capturar datos del formulario proveedor
function capturarProveedor(){
    var id, nomproveedor, telefono, direccion, email;

    id = document.getElementById("id_proveedor").value;
    nomproveedor = document.getElementById("nombre").value;
    telefono = document.getElementById("telefono").value;
    direccion = document.getElementById("direccion").value;
    email = document.getElementById("email").value;

    console.log("ID: " + id + ", nombre: " + nomproveedor + ", telefono: " + telefono + ", direccion: " + direccion + ", email: " + email);

    alert("exitoso");

    document.querySelector(".formulario-proveedor").reset();
}

//capturar datos del formulario empleado
function capturarEmpleado(){
    var id,nomempleado,direccion,email,contraseña;

    id = document.getElementById("id_empleado").value;
    nomempleado = document.getElementById("nombre").value;
    direccion = document.getElementById("direccion").value;
    email = document.getElementById("email").value;
    contraseña = document.getElementById("contraseña").value;


    console.log("ID: " + id + ", nombre: "+ nomempleado + ", direccion: " + direccion +  ", email : "+ email + ", contraseña : " + contraseña);

    alert("exitoso")

    document.querySelector(".formulario-empleado").reset();

}