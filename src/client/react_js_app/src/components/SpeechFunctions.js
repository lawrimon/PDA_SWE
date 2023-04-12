import { useState, useEffect } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

export function useSpeech() {
  const [textToSpeak, setTextToSpeak] = useState('');
  const { SpeechSynthesisUtterance, speechSynthesis } = window;

  async function speak(text) {
    if (speechSynthesis.speaking) {
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    var voices = window.speechSynthesis.getVoices();
    utterance.voice = voices[15];
    utterance.lang = 'en-US';

    await new Promise((resolve, reject) => {
      utterance.onend = resolve;
      utterance.onerror = reject;
      speechSynthesis.speak(utterance);
    });
  }

  const { transcript, resetTranscript } = useSpeechRecognition({
    continuous: true,
    lang: 'en-US'
  });

  useEffect(() => {
    if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
      alert("This Browser doesn't support Speech-to-Text");
      return null;
    }
  }, []);

  return { textToSpeak, setTextToSpeak, speak, transcript, resetTranscript };
}
