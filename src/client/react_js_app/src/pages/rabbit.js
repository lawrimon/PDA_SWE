import React, { useEffect, useState } from 'react';
import amqp from 'amqplib';

const RabbitMqConsumer = () => {
  const [messages, setMessages] = useState([]);
  const [connection, setConnection] = useState(null);

  useEffect(() => {
    async function consumeMessages() {
      const connection = await amqp.connect('amqp://guest:guest@localhost:5672');
      const channel = await connection.createChannel();

      await channel.assertQueue('notifications', { exclusive: true });

      await channel.consume('notifications', (msg) => {
        setMessages((prevMessages) => [...prevMessages, msg.content.toString()]);
        channel.ack(msg);
      });

      setConnection(connection);
    }

    consumeMessages();

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