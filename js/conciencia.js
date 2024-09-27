//capturar datos del formulario agregar frutas
function capturaAgregar(){
    var id,nomfruta,origen,precio,cantidad;

    id = document.getElementById("id_producto").value;
    nomfruta = document.getElementById("nombre").value;
    origen = document.getElementById("origen").value;
    precio= document.getElementById("precio").value;
    cantidad = document.getElementById("cantidad").value;


    console.log("ID: " + id + ", nombre: "+ nomfruta + ", origen: " + origen + ", precio: " + precio + ", cantidad: "+ cantidad);

    alert("exitoso")

    document.querySelector(".formulario-producto").reset();
}
//capturar datos del formulario sacar frutas
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