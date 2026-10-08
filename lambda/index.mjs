export const handler = async (event) => {
  console.log('Evento recibido:', JSON.stringify(event));

  const nombre = typeof event?.nombre === 'string' && event.nombre.trim()
    ? event.nombre.trim()
    : 'visitante';

  return {
    statusCode: 200,
    body: JSON.stringify({
      message: `Hola ${nombre}. Car Classic San Valero está en marcha.`
    })
  };
};
