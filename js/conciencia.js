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


function enviarDatos()  {
  const datos_entrada = {
      tipo: 'entrada',
      id_producto: document.getElementById("id_producto").value,
      nombre: document.getElementById("nombre").value,
      origen: document.getElementById("origen").value,
      precio: document.getElementById("precio").value,
      cantidad: document.getElementById("cantidad").value
  };
  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_entrada);
  document.querySelector(".formulario-producto").reset();
  
}
document.getElementById('btn_agregar').addEventListener('click', enviarDatos);


function capturaSacar(){
  const datos_salida = {
    tipo: 'salida',
    id_producto: document.getElementById("id_producto").value,
    nomfruta: document.getElementById("nombre").value,
    cantidad: document.getElementById("cantidad").value
  }
  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_salida);
}
//capturar datos del formulario proveedor
function capturarProveedor(){
const datos_proveedor = {
    tipo: 'proveedor',
    id_proveedor: document.getElementById("id_proveedor").value,
    nombre: document.getElementById("nombre").value,  // Cambié "nomproveedor" a "nombre"
    telefono: document.getElementById("telefono").value,
    direccion: document.getElementById("direccion").value,
    email: document.getElementById("email").value
}
enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_proveedor);

}

//capturar datos del formulario empleado
function capturarEmpleado(){
  const datos_empleado = {
    tipo: "empleado",
    id_empleado: document.getElementById("id_empleado").value,
    nombre: document.getElementById("nombre").value,
    apellido: document.getElementById("apellido").value,
    direccion: document.getElementById("direccion").value,
    telefono: document.getElementById("telefono").value,
    email: document.getElementById("email").value,
    contraseña: document.getElementById("contraseña").value,
  }
  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_empleado);


  document.querySelector(".formulario-empleado").reset();

}