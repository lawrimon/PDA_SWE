import React, { useState, useEffect, useCallback, useRef } from 'react';
import io from 'socket.io-client';

const ENDPOINT = 'http://websocket:5010/';


function RabbitMqConsumer() {
  const [queueName, setQueueName] = useState('user1');
  const [messages, setMessages] = useState([]);
  const socketRef = useRef(null);

  const handleConnect = useCallback(() => {
    const socket = io(ENDPOINT, {});
    socketRef.current = socket;
  
    socket.emit('start', { user_id: queueName });
    console.log(`Connected to ${queueName} room`);

    socket.on('message', (message) => {
      handleMessages(message)
    });

    socket.on('disconnect', () => {
      console.log(`Disconnected from ${queueName} room`);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  useEffect(() => {
    handleConnect();

    return () => {
      if (socketRef.current) {
        console.log(`Disconnected from ${queueName} room`);
        socketRef.current.disconnect();
      }
    };
  }, []);

  const handleAcknowledge = (deliveryTag) => {

    // Acknowledge Message
    socketRef.current.emit('ack', { delivery_tag: deliveryTag });
  };

  const handleQueueNameChange = useCallback((event) => {
    const newQueueName = event.target.value;
    setQueueName(newQueueName);
    if (socketRef.current) {
      console.log(`Disconnected from ${newQueueName} room`);
      socketRef.current.disconnect();
    }
    
    const socket = io(ENDPOINT, {});
    socketRef.current = socket;
    socket.emit('start', { user_id: newQueueName });
    console.log(`Connected to ${newQueueName} room from QueueNameChange`);
  
    socket.on('message', (message) => {
      handleMessages(message)
    });
  
    socket.on('disconnect', () => {
      console.log(`Disconnected from ${newQueueName} room`);
    });
  }, []);

  const handleConnectClick = () => {
    handleConnect();
  };

  const handleMessages = (message) => {
    console.log("Message received")
    setMessages((prevMessages) => [...prevMessages, message]);
  };


  return (
    <div>
      <input
        type="text"
        value={queueName}
        onChange={handleQueueNameChange}
      />
      <button onClick={handleConnectClick}>Connect</button>
      {messages.map((message, index) => (
        <div key={index}>
          <p>User ID: {message.user_id}</p>
          <p>Message: {message.message}</p>
          <button onClick={() => handleAcknowledge(message.delivery_tag)}>
            Acknowledge
          </button>
        </div>
      ))}
    </div>
  );
}

export default RabbitMqConsumer;