var tts = window.speechSynthesis;
var voices = [];


function getVoices() {
    voices = tts.getVoices();
    console.log(voices);
}

