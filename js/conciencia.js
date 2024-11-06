//este en mi archivos conciencia.js que esta una carperta que se llama js. js/conciencia.js//

function enviarDatosAlServidor(url, datos, metodo = 'POST') {
  fetch(url, {
      method: metodo,  // Método HTTP POST para enviar datos
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
  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_salida, 'PATCH');
  document.querySelector(".formulario-sacar").reset();
}



// Función para capturar datos del formulario proveedor
function capturarProveedor() {
  const datos_proveedor = {
      tipo: 'proveedor',
      id_proveedor: document.getElementById("id_proveedor").value,
      nombre: document.getElementById("nombre").value,
      telefono: document.getElementById("telefono").value,
      direccion: document.getElementById("direccion").value,
      email: document.getElementById("email").value
  };

  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_proveedor);
  alert('Proveedor agregado con éxito.'); // Alerta de éxito
  document.querySelector(".formulario-proveedor").reset(); // Limpiar formulario
}

// Capturar datos del formulario empleado
function capturarEmpleado() {
  const datos_empleado = {
    tipo: 'empleado',
    tipo1: document.getElementById("tipo_usuario_empleado").value, // Obtener el tipo de usuario
    id_empleado: document.getElementById("id_empleado").value,
    nombre: document.getElementById("nombre").value,
    apellido: document.getElementById("apellido").value,
    direccion: document.getElementById("direccion").value,
    telefono: document.getElementById("telefono").value,
    email: document.getElementById("email").value,
    contraseña: document.getElementById("contraseña").value,
  }
  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_empleado);
  alert('empleado agregado con éxito.'); // Alerta de éxito

  document.querySelector(".formulario-empleado").reset();
}


// Función para eliminar producto
function capturaEliminar() {
  const datos_eliminar = {
      tipo: 'eliminar_producto',
      id_producto: document.getElementById("id_producto_eliminar1").value,
      nombre: document.getElementById("nombre_eliminar1").value
  };
  
  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_eliminar, 'DELETE');
  alert('Producto eliminado con éxito.'); // Alerta de éxito
  document.querySelector(".formulario-eliminar").reset(); // Limpiar formulario
}

// Función para actualizar producto
function capturaActualizar() {
  const datos_actualizar = {
      tipo: 'actualizar_producto', // Corrige 'actulizar' a 'actualizar'
      nombre: document.getElementById("eliminar_producto").value,
      origen: document.getElementById("origen_actualizar1").value,
      precio: document.getElementById("precio_actualizar1").value,

  };
  
  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_actualizar, 'PUT');
  alert('Información del producto actualizada con éxito.'); // Alerta de éxito
  document.querySelector(".formulario-actualizar").reset(); // Limpiar formulario
}

//funcion para eliminar proveedor
function capturarEliminarProveedor() {
  const datos_eliminar = {
      tipo: 'eliminar_proveedor',
      id_proveedor: document.getElementById("id_proveedor_eliminar1").value, 
      nombre: document.getElementById("nombre_proveedor_eliminar1").value 
  };

  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_eliminar, 'DELETE');
  alert('Proveedor eliminado con éxito.');
  document.querySelector(".formulario-eliminar").reset(); // Limpiar formulario
}


//funcion para actulizar proveedor 

function capturarActualizarProveedor() {
  const datos_actualizar = {
      tipo: 'actualizar_proveedores',
      id_proveedor: document.getElementById("id_proveedor_actualizar1").value, 
      nombre: document.getElementById("nombre_proveedor_actualizar1").value, 
      telefono: document.getElementById("telefono_proveedor_actualizar1").value, 
      direccion: document.getElementById("direccion_proveedor_actualizar1").value, 
      email: document.getElementById("email_proveedor_actualizar1").value 
  };

  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_actualizar, 'PUT');
  alert('Información del proveedor actualizada con éxito.');
  document.querySelector(".formulario-actualizar").reset(); // Limpiar formulario
}


// Función para eliminar empleado

function capturarEliminarEmpleado() {
  const datos_eliminar = {
      tipo: 'eliminar_empleado',
      id_empleado: document.getElementById("id_empleado_eliminar1").value, 
      nombre: document.getElementById("nombre_empleado_eliminar1").value 
  };

  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_eliminar, 'DELETE');
  alert('Empleado eliminado con éxito.');
  document.querySelector(".formulario-eliminar").reset(); // Limpiar formulario
}

// Función para actualizar empleado

function capturarActualizarEmpleado() {
  const datos_actualizar = {
      tipo: 'actualizar_empleado',
      id_empleado: document.getElementById("id_empleado_actualizar1").value, 
      nombre: document.getElementById("nombre_empleado_actualizar1").value, 
      apellido: document.getElementById("apellido_empleado_actualizar1").value, 
      direccion: document.getElementById("direccion_empleado_actualizar1").value, 
      email: document.getElementById("email_empleado_actualizar1").value, 
      telefono: document.getElementById("telefono_empleado_actualizar1").value 
  };

  enviarDatosAlServidor('http://127.0.0.1:5000/administrar_datos', datos_actualizar, 'PUT');
  alert('Información del empleado actualizada con éxito.');
  document.querySelector(".formulario-actualizar").reset(); // Limpiar formulario
}