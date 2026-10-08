# Car Classic San Valero

Proyecto final Serverless para presentar una exposición de coches clásicos y recibir consultas de visitantes.

## Estado

- Sitio estático inicial en `index.html`, con JavaScript en `js/app.js` e imágenes locales en `assets/`.
- El formulario requiere `name`, `email` y `message`; permite `phone` opcional y adjunta el vehículo seleccionado.
- El formulario envía consultas a la API Gateway propia desplegada en `us-east-1`.
- No utilizar los recursos AWS del proyecto Ebook.

## Arquitectura

GitHub Pages y Amazon S3 publican la web estática. Las consultas usan recursos propios:

`Navegador → API Gateway → Lambda → DynamoDB + SNS`

## Backend · Lambda final

La función propia se llama `carclassic-contact`. El handler definitivo está en `lambda/index.mjs` y usa `index.handler`. Procesa peticiones proxy de API Gateway, valida la consulta, la guarda en DynamoDB y publica una notificación en SNS.

Configura estas variables de entorno en Lambda:

- `TABLE_NAME`: nombre de la tabla propia de consultas, con partition key `id` de tipo String.
- `TOPIC_ARN`: ARN del topic SNS propio de Car Classic San Valero.

El Execution Role de Lambda necesita `dynamodb:PutItem` en esa tabla y `sns:Publish` en ese topic. La política de mínimo privilegio para el role está en `lambda/execution-role-policy.json`. La prueba proxy está en `lambda/test-event.json`. API Gateway expone `POST /contact` en el stage `dev`; su URL está configurada en `js/app.js`. La Lambda responde a `OPTIONS` para CORS.

## Desarrollo local

Abre `index.html` en un navegador. El formulario validará los datos y enviará las consultas a la API propia.
