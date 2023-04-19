const recognitionRef = useRef(null);
const transcriptRef = useRef("");

export const startListening = () => {
  const recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!recognition) {
    console.log('Speech recognition API not supported');
    return;
  }

  console.log('Speech recognition API supported');
  const recognitionInstance = new recognition();
  recognitionInstance.continuous = true;
  recognitionInstance.lang = 'en-US';
  recognitionInstance.interimResults = true;
  recognitionInstance.onresult = handleResult;

  recognitionRef.current = recognitionInstance;
  recognitionInstance.start();
};

const handleResult = (event) => {
  let interimTranscript = '';
  let finalTranscript = '';
  for (let i = event.resultIndex; i < event.results.length; i++) {
    const transcript = event.results[i][0].transcript;
    if (event.results[i].isFinal) {
      finalTranscript += transcript;
    } else {
      interimTranscript += transcript;
    }
  }
  transcriptRef.current = interimTranscript + finalTranscript;
};

export const stopListening = () => {
  if (recognitionRef.current) {
    recognitionRef.current.stop();
    const transcript = transcriptRef.current;
    transcriptRef.current = '';
    return transcript;
  }
};

export function listenForSpeech(timeout = 5000) {
  return new Promise((resolve, reject) => {
    startListening();
    let finalTranscript = "";
    const timeoutId = setTimeout(() => {
      finalTranscript = stopListening();
      console.log("Final transcript", finalTranscript);
      resolve(finalTranscript);
    }, timeout);
  })
}

export async function listenForSpeech2() {
  const isSpeechRecognitionSupported = 'SpeechRecognition' in window || 'webkitSpeechRecognition' in window;
  
  if (isSpeechRecognitionSupported) {
    console.log("speech recognition API supported");
  } else {
    console.log("speech recognition API not supported")
    return;
  }

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

    globalTranscript = finalTranscript.trim();
  };

  recognition.onerror = event => {
    console.error('Speech recognition error:', event);
  };

  return new Promise((resolve, reject) => {
    recognition.start();

    let timeoutId = setTimeout(() => {
      recognition.stop();
      resolve(globalTranscript.trim());
    }, 5000);

    recognition.onend = () => {
      clearTimeout(timeoutId);
      resolve(globalTranscript.trim());
    };

    recognition.onerror = () => {
      clearTimeout(timeoutId);
      reject('Speech recognition error');
    };
  });
}

export async function speak(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 1;
  utterance.pitch = 1;
  utterance.lang = 'en-US';

  return new Promise((resolve, reject) => {
    utterance.addEventListener('start', () => {
      console.log('Started speaking:', text);
    });
    utterance.addEventListener('error', (event) => {
      console.error('Error while speaking:', event);
      reject(event);
    });
    utterance.addEventListener('end', () => {
      console.log('Finished speaking:', text);
      resolve();
    });
    speechSynthesis.cancel();
    speechSynthesis.speak(utterance);
  });
}