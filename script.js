const video = document.getElementById('video');
const startButton = document.getElementById('start');
const captureButton = document.getElementById('capture');
const stopButton = document.getElementById('stop');
const resultText = document.getElementById('result-text');
const speakButton = document.getElementById('speak');

let stream = null;

startButton.addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(s => {
            stream = s;
            video.srcObject = stream;
            video.style.display = 'block'; // Show the video element when the camera starts
        })
        .catch(err => {
            console.error('Error accessing the camera: ', err);
        });
});

captureButton.addEventListener('click', () => {
    if (!stream) {
        alert("Please start the camera first.");
        return;
    }
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/png');

    // Placeholder for sending image to backend for recognition
    // and getting the result
    // Assuming the result is returned as 'Recognized Sign'
    const recognizedText = 'Recognized Sign';  // Placeholder
    resultText.textContent = recognizedText;
});

stopButton.addEventListener('click', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        video.srcObject = null;
        video.style.display = 'none'; // Hide the video element when the camera stops
    }
});

speakButton.addEventListener('click', () => {
    const speech = new SpeechSynthesisUtterance(resultText.textContent);
    speechSynthesis.speak(speech);
});
