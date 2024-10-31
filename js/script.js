function obtenerDatos() {
    fetch('http://localhost:5000/administrar_datos_sacar') // URL correcta
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Convertir la respuesta a JSON
        })
        .then(data => {
            // Mostrar los productos en una lista desplegable
            cargarProductos(data.productos);
            // Mostrar los empleados en una lista desplegable
            cargarEmpleados(data.empleados);
            // Mostrar los proveedores en una lista desplegable
            cargarProveedores(data.proveedores);
            
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud Fetch:', error);
        });
}

// Función para cargar productos en un <select> desplegable
function cargarProductos(productos) {
    const selectProductos = document.getElementById('productos');

    // Limpiar la lista antes de cargar nuevos datos
    selectProductos.innerHTML = '<option value="">--Seleccione un producto--</option>';

    productos.forEach(producto => {
        const option = document.createElement('option');
        option.textContent = producto.nombre; // Mostrar nombre del producto
        selectProductos.appendChild(option);
    });
}

// Función para cargar empleados en un <select> desplegable
function cargarEmpleados(empleados) {
    const selectEmpleados = document.getElementById('empleados');
    
    // Limpiar la lista antes de cargar nuevos datos
    selectEmpleados.innerHTML = '<option value="">--Seleccione un empleado--</option>';
    
    empleados.forEach(empleado => {
        const option = document.createElement('option');
        option.textContent = empleado.nombre; // Nombre del empleado
        selectEmpleados.appendChild(option);
    });
}

// Función para cargar proveedores en un <select> desplegable
function cargarProveedores(proveedores) {
    const selectProveedores = document.getElementById('proveedores');  // Cambié el ID a 'proveedores'
    
    // Limpiar la lista antes de cargar nuevos datos
    selectProveedores.innerHTML = '<option value="">--Seleccione un proveedor--</option>';
    
    proveedores.forEach(proveedor => {
        const option = document.createElement('option');
        option.textContent = proveedor.nombre; // Nombre del proveedor
        selectProveedores.appendChild(option);
    });
}

// Llama a la función para obtener datos cuando se carga la página
window.onload = obtenerDatos;
