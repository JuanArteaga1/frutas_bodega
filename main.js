const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let ventanaPrincipal;

function crearVentanaPrincipal() {
    ventanaPrincipal = new BrowserWindow({
        width: 1920,
        height: 1080,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    ventanaPrincipal.loadFile('home.html');
}


// Manejar el evento IPC para cambiar de página
ipcMain.on('change-page', (event, page) => {
    if (ventanaPrincipal) {
        ventanaPrincipal.loadFile(page);
    }
});

app.whenReady().then(crearVentanaPrincipal);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        crearVentanaPrincipal();
    }
});