import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';


// have a look at localhost:3000/rabbit
// Just connect to the socket via ENDPOINT and subscribe to the queue with user_id via the "start" event
// Managing connections is crucial, so you should definitely try to close each connection (see below)


const ENDPOINT = 'http://localhost:5010/';

function RabbitMqConsumer() {
  // State variables
  const [queueName, setQueueName] = useState('user1');
  const [messages, setMessages] = useState([]);

  // Ref to hold the socket instance
  const socketRef = useRef(null);

  // Function to connect to the socket server
  const handleConnect = () => {
    // Disconnect from previous socket room
    if (socketRef.current) {
      console.log(`Disconnected from ${queueName} room Print1`);
      socketRef.current.disconnect();
      socketRef.current = null;
    }

    // Connect to the socket server and emit 'start' event with user_id
    const socket = io(ENDPOINT, {});
    socketRef.current = socket;

    socket.emit('start', { user_id: queueName });
    console.log(`Connected to ${queueName} room Print2`);

    // Listen for 'message' event and update messages state
    socket.on('message', (message) => {
      handleMessages(message);
    });

    // Listen for 'disconnect' event and log
    socket.on('disconnect', () => {
      console.log(`Disconnected from server Print3`);
    });

    // Return cleanup function to disconnect from socket
    return () => {
      socket.disconnect();
    };
  };

  // Call handleConnect on component mount and disconnect on unmount
  useEffect(() => {
    handleConnect();

    return () => {
      if (socketRef.current) {
        console.log(`Disconnected from ${queueName} room Print4`);
        socketRef.current.disconnect();
        socketRef.current = null;
      }
    };
  },[]);

  // Function to acknowledge a message
  const handleAcknowledge = (deliveryTag) => {

    try {
    // Check if the delivery tag is a valid integer
    if (deliveryTag) {
      // Acknowledge Message by emitting 'ack' event with delivery_tag
      socketRef.current.emit('ack', { delivery_tag: deliveryTag });

      // Remove acknowledged message from messages array
      setMessages((prevMessages) => {
        return prevMessages.filter((message) => message.delivery_tag !== deliveryTag);
      });
    } else {
      console.error('Invalid delivery tag:', deliveryTag);
    }
    } catch (error) {
      console.error(error);
    }
  };

  // Function to handle incoming messages
  const handleMessages = (message) => {
    console.log('Message received');
    // Add message to messages state
    setMessages((prevMessages) => [...prevMessages, message]);
  };

  // Function to handle queue name submission
  const handleQueueNameSubmit = (event) => {
    // Acknowledge the first message in the current queue before switching queues (cosmetics)
    if(messages.length > 0){
    handleAcknowledge(messages[0].delivery_tag);
    }
    event.preventDefault();

    // Disconnect from current socket room
    if (socketRef.current) {
      console.log(`Disconnected from old room Print5`);
      socketRef.current.disconnect();
      socketRef.current = null;
    }

    // Connect to the new socket room with the updated queue name
    handleConnect();
  };

  return (
    <div>
      <form onSubmit={handleQueueNameSubmit}>
        <input type="text" value={queueName} onChange={(event) => setQueueName(event.target.value)} />
        <button type="submit">Connect</button>
      </form>

      {messages.map((message, index) => (
        <div key={index}>
          <p>User ID: {message.user_id}</p>
          <p>Message: {message.message}</p>
          <button onClick={() => handleAcknowledge(message.delivery_tag)}>Acknowledge</button>
        </div>
      ))}
    </div>
  );
}

export default RabbitMqConsumer;