var Jimp = require('jimp');
 


const express = require("express"),
    path = require("path"),
    app = express(),
    port = 3000;

app.get('/', (peticion, respuesta) => {
    var fs = require('fs');
    var files = fs.readdirSync(path.join(__dirname,'pre-images/'));
    files.forEach(function(name, i) {
        Jimp.read(path.join(__dirname,`pre-images/${name}` ), (err, img) => {
            if (err) throw err;
            img
              .cover(512, 512/*, Jimp.HORIZONTAL_ALIGN_LEFT | Jimp.VERTICAL_ALIGN_TOP*/) // resize
              .quality(80) // set JPEG quality
              .write(path.join(__dirname,`images/young-man-${i}.jpg`)); // save
          });
    });
    
    respuesta.send("Done!");
});

app.get('/photo', (peticion, respuesta) => {
    Jimp.read(path.join(__dirname,'pre-images/pexels-italo-melo-2379004.png'))
    .then(img => {
        return img
            .resize(512, 512) // resize
            .quality(72) // set JPEG quality
            .greyscale() // set greyscale
            .write(path.join(__dirname,'images/pexels-italo-melo-2379004.png')); // save
        })
        .catch(err => {
        console.error(err);
        });
      
    respuesta.send("Done!");
});
app.get('/pagina', (peticion, respuesta) => {
    // Servir archivo HTML, o cualquier otro archivo
    let rutaDeArchivo = path.join(__dirname, "plantilla.html");
    respuesta.sendFile(rutaDeArchivo);
});

app.get('/hola', (peticion, respuesta) => {
    let mascota = {
        nombre: "Maggie",
        edad: 2,
    };
    respuesta.json(mascota);
});

// Una vez definidas nuestras rutas podemos iniciar el servidor
app.listen(port, err => {
    if (err) {
        // Aquí manejar el error
        console.error("Error escuchando: ", err);
        return;
    }
    // Si no se detuvo arriba con el return, entonces todo va bien ;)
    console.log(`Escuchando en el port :${port}`);
});