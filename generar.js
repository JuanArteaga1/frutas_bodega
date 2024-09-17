function generarQR(tipo) {
    const qrcodeContainer = document.getElementById('qrcode');
    qrcodeContainer.innerHTML = ''; // Limpia el contenedor

    let textoQR;
    switch(tipo) {
        case 'entradas':
            textoQR = 'Código de Entradas';
            break;
        case 'salidas':
            textoQR = 'Código de Salidas';
            break;
        case 'perdidas':
            textoQR = 'Código de Pérdidas';
            break;
        default:
            textoQR = 'Código QR';
    }

    // Crear un elemento canvas para el QR
    const canvas = document.createElement('canvas');
    qrcodeContainer.appendChild(canvas);

    // Genera el código QR
    QRCode.toCanvas(canvas, textoQR, { width: 400 }, function (error) {
        if (error) {
            console.error('Error al generar el QR:', error);
            alert('Error al generar el QR. Revisa la consola para más detalles.');
        } else {
            console.log('QR generado correctamente!');
        }
    });
}

