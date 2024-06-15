document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const startButton = document.getElementById('start');
    const captureButton = document.getElementById('capture');
    const stopButton = document.getElementById('stop');
    const resultText = document.getElementById('result-text');
    const speakButton = document.getElementById('speak');
    const imageUpload = document.getElementById('imageUpload');
    const uploadButton = document.getElementById('upload');
    const uploadedImageContainer = document.getElementById('uploaded-image-container');
    const uploadedImage = document.getElementById('uploaded-image');

    let stream;

    // Camera functions
    startButton.addEventListener('click', async () => {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.style.display = 'block';
    });

    captureButton.addEventListener('click', () => {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageDataUrl = canvas.toDataURL('image/png');

        fetch('/predict', {
            method: 'POST',
            body: JSON.stringify({ image: imageDataUrl }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            resultText.innerText = data.prediction;
        });
    });

    stopButton.addEventListener('click', () => {
        stream.getTracks().forEach(track => track.stop());
        video.style.display = 'none';
    });

    // Speak function
    speakButton.addEventListener('click', () => {
        const msg = new SpeechSynthesisUtterance(resultText.innerText);
        window.speechSynthesis.speak(msg);
    });

    // Image upload functions
    uploadButton.addEventListener('click', () => {
        const file = imageUpload.files[0];
        const reader = new FileReader();

        reader.onload = () => {
            uploadedImage.src = reader.result;
            uploadedImage.style.display = 'block';

            fetch('/predict', {
                method: 'POST',
                body: JSON.stringify({ image: reader.result }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                resultText.innerText = data.prediction;
            });
        };

        if (file) {
            reader.readAsDataURL(file);
        }
    });
});


// JS to handle the options
