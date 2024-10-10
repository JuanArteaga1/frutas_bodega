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
document.querySelector(".formulario-sacar").reset();
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

function capturar_eliminar_producto() {
  const datos_eliminar_producto = {
    tipo: "eliminarproducto",
    id_producto: document.getElementById("id_producto_eliminar1").value,
    nombre_producto: document.getElementById("nombre_eliminar1").value
  }
  
  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_eliminar_producto);

  // Resetea el formulario después de enviar los datos
  document.querySelector(".formulario-eliminar").reset();
}



function capturar_actualizar_producto() {
  const datos_actualizar_producto = {
    tipo: "actualizar_producto",
    id_producto: document.getElementById("id_producto_actualizar1").value,
    nombre_producto: document.getElementById("nombre_actualizar1").value,
    origen_producto: document.getElementById("origen_actualizar1").value,
    precio_producto: document.getElementById("precio_actualizar1").value,
    cantidad_producto: document.getElementById("cantidad_actualizar1").value
  }
  
  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_actualizar_producto);

  // Resetea el formulario después de enviar los datos
  document.querySelector(".formulario-actualizar").reset();
}


function capturar_eliminar_proveedor() {
  const datos_eliminar_proveedor = {
      tipo: "eliminar_proveedor",
      id_proveedor: document.getElementById("id_proveedor_eliminar").value,
      nombre_proveedor: document.getElementById("nombre_proveedor_eliminar").value
  };

  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_eliminar_proveedor);

  // Resetea el formulario después de enviar los datos
  document.querySelector(".formulario-eliminar").reset();
}




function capturar_actualizar_proveedor() {
  const datos_actualizar_proveedor = {
    tipo: "actualizar_proveedores",
    id_proveedor: document.getElementById("id_proveedor_actualizar").value,
    nombre_proveedor: document.getElementById("nombre_proveedor_actualizar").value,
    telefono_proveedor: document.getElementById("telefono_proveedor_actualizar").value,
    direccion_proveedor: document.getElementById("direccion_proveedor_actualizar").value,
    email_proveedor: document.getElementById("email_proveedor_actualizar").value
  }

  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_actualizar_proveedor);

  // Resetea el formulario después de enviar los datos
  document.querySelector(".formulario-actualizar").reset();
}

function capturar_eliminar_empleado() {
  const datos_eliminar_empleado = {
    tipo: "eliminar_empleado",
    id_empleado: document.getElementById("id_producto_eliminar").value,
    nombre_empleado: document.getElementById("nombre_eliminar").value
  }
  
  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_eliminar_empleado);

  // Resetea el formulario después de enviar los datos
  document.querySelector(".formulario-eliminar").reset();
}


function capturar_actualizar_empleado() {
  const datos_actualizar_empleado = {
    tipo: "actualizar_empleado",
    id_empleado: document.getElementById("id_empleado_actualizar").value,
    nombre: document.getElementById("nombre_actualizar").value,
    apellido: document.getElementById("apellido_actualizar").value,
    direccion: document.getElementById("direccion_actualizar").value,
    email: document.getElementById("email_actualizar").value,
    telefono: document.getElementById("telefono_actualizar").value
  }
  
  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_actualizar_empleado);

  // Resetea el formulario después de enviar los datos
  document.querySelector(".formulario-actualizar").reset();
}

