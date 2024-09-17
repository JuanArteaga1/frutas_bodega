const { ipcRenderer } = require('electron');

document.getElementById('changePageButton').addEventListener('click', ventanasecundaria);

function ventanasecundaria() {
    ipcRenderer.send('change-page', 'second-page.html'); // Enviar un mensaje para cambiar la página
}