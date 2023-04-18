import { useState } from 'react';

function useListenForSpeech() {
  const [transcript, setTranscript] = useState('');

  const recognition = new window.webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = 'en-US';

  recognition.onresult = event => {
    let interimTranscript = '';
    let finalTranscript = '';

    for (let i = event.resultIndex; i < event.results.length; i++) {
      let transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalTranscript += transcript + ' ';
      } else {
        interimTranscript += transcript;
      }
    }

    setTranscript(finalTranscript.trim());
  };

  recognition.onerror = event => {
    console.error('Speech recognition error:', event);
  };

  return new Promise((resolve, reject) => {
    recognition.start();

    let timeoutId = setTimeout(() => {
      recognition.stop();
      resolve(transcript.trim());
    }, 5000);

    recognition.onend = () => {
      clearTimeout(timeoutId);
      resolve(transcript.trim());
    };

    recognition.onerror = () => {
      clearTimeout(timeoutId);
      reject('Speech recognition error');
    };
  });
}

export default useListenForSpeech;