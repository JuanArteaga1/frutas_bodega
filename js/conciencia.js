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
