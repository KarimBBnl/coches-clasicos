# Car Classic San Valero

Proyecto final Serverless para presentar una exposición de coches clásicos y recibir consultas de visitantes.

## Estado

- Sitio estático inicial en `index.html`, con JavaScript en `js/app.js` e imágenes locales en `assets/`.
- El formulario requiere `name`, `email` y `message`; permite `phone` opcional y adjunta el vehículo seleccionado.
- El endpoint está pendiente. Se configurará en `js/app.js` cuando exista la API propia de este proyecto.
- No utilizar los recursos AWS del proyecto Ebook.

## Arquitectura prevista

GitHub Pages y Amazon S3 publicarán la web estática. Para las consultas se crearán recursos propios:

`Navegador → API Gateway → Lambda → DynamoDB + SNS`

## Bloque 03 · primera Lambda

La función propia se llama `carclassic-contact`. El código de inicio está en `lambda/index.mjs`; configúrala con el handler `index.handler` y crea un evento de prueba a partir de `lambda/test-event.json`.

Esta primera versión solo valida la invocación y devuelve un saludo. DynamoDB, SNS y API Gateway se integrarán en sus bloques correspondientes.

## Desarrollo local

Abre `index.html` en un navegador. Hasta configurar y desplegar la API propia, el formulario validará los datos y avisará claramente que no los ha enviado.
