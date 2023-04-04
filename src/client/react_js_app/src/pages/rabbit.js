import React, { useEffect, useState } from 'react';
import Connection from 'rabbitmq-client';

const RabbitMqConsumer = () => {
  const [messages, setMessages] = useState([]);
  const [connection, setConnection] = useState(null);

  useEffect(() => {
    const rabbit = new Connection({
      url: 'amqp://guest:guest@localhost:5672',
      retryLow: 1000,
      retryHigh: 30000,
    });

    rabbit.on('error', (err) => {
      console.error(err);
    });

    rabbit.on('connection', () => {
      console.log('The connection is successfully (re)established');
    });

    async function consumeMessages() {
      const ch = await rabbit.acquire();

      await ch.queueDeclare({ queue: 'notifications', exclusive: true });

      await ch.basicConsume({ queue: 'notifications' }, (msg) => {
        setMessages((prevMessages) => [...prevMessages, msg.content.toString()]);
        ch.basicAck({ deliveryTag: msg.deliveryTag });
      });
    }

    rabbit
      .connect()
      .then(() => {
        console.log('Connected to RabbitMQ');
        setConnection(rabbit);
        consumeMessages();
      })
      .catch((err) => {
        console.error(err);
      });

    return () => {
      if (connection) {
        connection.close();
      }
    };
  }, []);

  useEffect(() => {
    console.log(messages);
  }, [messages]);

  return (
    <div>
      <h1>Incoming Messages:</h1>
      <table>
        <thead>
          <tr>
            <th>Message</th>
          </tr>
        </thead>
        <tbody>
          {messages.map((message, index) => (
            <tr key={index}>
              <td>{message}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RabbitMqConsumer;