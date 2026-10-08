import { DynamoDBClient, PutItemCommand } from '@aws-sdk/client-dynamodb';
import { SNSClient, PublishCommand } from '@aws-sdk/client-sns';
import crypto from 'node:crypto';

const dynamodb = new DynamoDBClient({});
const sns = new SNSClient({});

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Allow-Methods': 'POST,OPTIONS',
  'Content-Type': 'application/json'
};

function response(statusCode, payload) {
  return {
    statusCode,
    headers: corsHeaders,
    body: JSON.stringify(payload)
  };
}

function readRequestBody(event) {
  if (!event.body) return {};

  const body = event.isBase64Encoded
    ? Buffer.from(event.body, 'base64').toString('utf8')
    : event.body;

  return JSON.parse(body);
}

export const handler = async (event) => {
  console.log('Solicitud recibida:', JSON.stringify(event));

  const method = event.httpMethod ?? event.requestContext?.http?.method;
  if (method === 'OPTIONS') {
    return { statusCode: 204, headers: corsHeaders, body: '' };
  }
  if (method && method !== 'POST') {
    return response(405, { success: false, error: 'Método no permitido' });
  }

  let body;
  try {
    body = readRequestBody(event);
  } catch (error) {
    console.warn('El body de la solicitud no contiene JSON válido:', error);
    return response(400, { success: false, error: 'El cuerpo debe ser JSON válido' });
  }

  const name = typeof body.name === 'string' ? body.name.trim() : '';
  const email = typeof body.email === 'string' ? body.email.trim() : '';
  const phone = typeof body.phone === 'string' ? body.phone.trim() : '';
  const message = typeof body.message === 'string' ? body.message.trim() : '';

  if (!name || !email || !message) {
    return response(400, {
      success: false,
      error: 'Nombre, correo y consulta son obligatorios'
    });
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return response(400, { success: false, error: 'Introduce un correo válido' });
  }

  const tableName = process.env.TABLE_NAME;
  const topicArn = process.env.TOPIC_ARN;
  if (!tableName || !topicArn) {
    console.error('Falta configurar TABLE_NAME o TOPIC_ARN en las variables de entorno.');
    return response(500, { success: false, error: 'El servicio no está configurado' });
  }

  const id = crypto.randomUUID();
  const timestamp = new Date().toISOString();
  const item = {
    id: { S: id },
    name: { S: name },
    email: { S: email },
    phone: { S: phone || 'N/A' },
    message: { S: message },
    timestamp: { S: timestamp }
  };

  try {
    await dynamodb.send(new PutItemCommand({
      TableName: tableName,
      Item: item
    }));

    await sns.send(new PublishCommand({
      TopicArn: topicArn,
      Subject: 'Nueva consulta Car Classic San Valero',
      Message: JSON.stringify({
        id,
        name,
        email,
        phone: phone || 'N/A',
        message,
        timestamp
      })
    }));

    console.log('Consulta guardada y notificada:', id);
    return response(200, {
      success: true,
      message: 'Consulta guardada y notificada correctamente',
      id
    });
  } catch (error) {
    console.error('No se pudo completar el guardado y la notificación:', { id, error });
    return response(500, {
      success: false,
      error: 'No se pudo procesar la consulta'
    });
  }
};
