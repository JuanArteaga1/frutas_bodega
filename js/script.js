var productos = [

]
document.addEventListener('DOMContentLoaded', obtenerDatos);
function obtenerDatos() {
    fetch('http://localhost:5000/administrar_datos') // URL correcta
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Convertir la respuesta a JSON
        })
        .then(data => {
            productos = data
            console.log(productos)
            cargarpersonas(data);
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud Fetch:', error);
        });
}

function cargarpersonas(productos) {
    const selectproductos = document.getElementById('eliminar_producto');

    // Limpiar la lista antes de cargar nuevos datos
    selectproductos.innerHTML = '<option value="">--Seleccione un producto--</option>';

    productos.forEach(producto => {
        const option = document.createElement('option');
        option.textContent = producto.nombre;
        option.value = producto.nombre;
        selectproductos.appendChild(option);
    });
}
function seleccionarpersona() {
    const productoid = document.getElementById("eliminar_producto").value
    const producto = productos.find(producto => producto.nombre == productoid)
    console.log(producto)
    document.getElementById("precio_actualizar1").value = producto.precio
    document.getElementById("origen_actualizar1").value = producto.origen
}