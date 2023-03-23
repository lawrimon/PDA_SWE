import React, { useEffect, useState } from 'react';
import { useAmqp, useAmqpQueue } from 'amqplib';

const RabbitMqConsumer = () => {
  const [messages, setMessages] = useState([]);
  const { connection, error: connectionError } = useAmqp({
    url: 'amqp://localhost',
  });

  const { error: consumerError } = useAmqpQueue({
    connection,
    queue: 'task_queue',
    onMessage: (msg) => {
      setMessages((prevMessages) => [...prevMessages, msg.content.toString()]);
    },
  });

  useEffect(() => {
    console.log(messages);
  }, [messages]);

  if (connectionError || consumerError) {
    return <div>Error connecting to RabbitMQ</div>;
  }

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