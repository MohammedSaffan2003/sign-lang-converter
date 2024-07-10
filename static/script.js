document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const startButton = document.getElementById('start');
    const captureButton = document.getElementById('capture');
    const stopButton = document.getElementById('stop');
    const resultText = document.getElementById('result-text');
    const speakButton = document.getElementById('speak');
    const imageUpload = document.getElementById('imageUpload');
    const uploadButton = document.getElementById('upload');
    const uploadedImage = document.getElementById('uploaded-image');
    const uploadResultText = document.getElementById('upload-result-text');
    const uploadSpeakButton = document.getElementById('upload-speak');

    const captureSection = document.getElementById('capture-section');
    const uploadSection = document.getElementById('upload-section');
    const signWordsSection = document.getElementById('sign-words-section');
    const chooseCaptureButton = document.getElementById('choose-capture');
    const chooseUploadButton = document.getElementById('choose-upload');
    const chooseSignWordsButton = document.getElementById('choose-sign-words');
    const wordInput = document.getElementById('word-input');
    const signOutput = document.getElementById('sign-output');

    

    

    let stream;

    // Toggle sections
    chooseCaptureButton.addEventListener('click', () => {
        captureSection.classList.remove('hidden');
        uploadSection.classList.add('hidden');
        signWordsSection.classList.add('hidden');
    });

    chooseUploadButton.addEventListener('click', () => {
        uploadSection.classList.remove('hidden');
        captureSection.classList.add('hidden');
        signWordsSection.classList.add('hidden');
    });

    chooseSignWordsButton.addEventListener('click', () => {
        signWordsSection.classList.remove('hidden');
        captureSection.classList.add('hidden');
        uploadSection.classList.add('hidden');
    });

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

    uploadSpeakButton.addEventListener('click', () => {
        const msg = new SpeechSynthesisUtterance(uploadResultText.innerText);
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
                uploadResultText.innerText = data.prediction;
            });
        };

        if (file) {
            reader.readAsDataURL(file);
        }
    });

    // Handle word input for sign language display

    
    const inputField = document.getElementById('text-input');
    const textForm = document.getElementById('text-form');
    const wordOutputContainer = document.getElementById('word-output-container');

    textForm.addEventListener('submit', (event) => {
        event.preventDefault();
        wordOutputContainer.innerHTML = '';

        const text = inputField.value;
        const words = text.split(' ');

        const colors = ['#FFD700', '#ADFF2F', '#FF69B4', '#87CEEB', '#FF4500'];
        let colorIndex = 0;

        words.forEach(word => {
            const wordDiv = document.createElement('div');
            wordDiv.classList.add('word-frame');
            wordDiv.style.border = `1px solid ${colors[colorIndex % colors.length]}`;
            wordDiv.style.backgroundColor = colors[colorIndex % colors.length];
            colorIndex++;

            for (let char of word) {
                if (/[a-zA-Z0-9]/.test(char)) {
                    const img = document.createElement('img');
                    img.src = `static/letters/${char.toLowerCase()}.png`;
                    img.alt = char;
                    wordDiv.appendChild(img);
                } else {
                    const span = document.createElement('span');
                    span.textContent = char;
                    span.classList.add('non-alphanumeric');
                    wordDiv.appendChild(span);
                }
            }

            wordOutputContainer.appendChild(wordDiv);
        });

        inputField.value = '';
    });


    wordInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const word = wordInput.value.trim().toLowerCase();
            signOutput.innerHTML = '';
            for (let char of word) {
                if (char.match(/[a-z0-9]/)) {
                    const img = document.createElement('img');
                    img.src = `static/letters/${char}.png`;
                    img.alt = char;
                    img.className = 'sign-letter';
                    signOutput.appendChild(img);
                } else if (char === ' ') {
                    const space = document.createElement('div');
                    space.className = 'sign-space';
                    signOutput.appendChild(space);
                }
            }
        }
    });
});

// for General Sign Feature
document.addEventListener('DOMContentLoaded', () => {
    const generalVideo = document.getElementById('general-video');
    const generalStartButton = document.getElementById('general-start');
    const generalStopButton = document.getElementById('general-stop');
    const generalResultText = document.getElementById('general-result-text');

    const generalSignsSection = document.getElementById('general-signs-section');
    const chooseGeneralSignsButton = document.getElementById('choose-general-signs');

    let generalStream;
    let recognitionTimeout;
    let lastRecognizedSign = '';
    let lastRecognizedTime = 0;

    // Toggle sections
    chooseGeneralSignsButton.addEventListener('click', () => {
        generalSignsSection.classList.remove('hidden');
    });

    // Camera functions
    generalStartButton.addEventListener('click', async () => {
        generalStream = await navigator.mediaDevices.getUserMedia({ video: true });
        generalVideo.srcObject = generalStream;
        generalVideo.style.display = 'block';

        recognitionTimeout = setInterval(() => {
            recognizeSign();
        }, 1000);
    });

    generalStopButton.addEventListener('click', () => {
        generalStream.getTracks().forEach(track => track.stop());
        generalVideo.style.display = 'none';
        clearInterval(recognitionTimeout);
    });

    const recognizeSign = () => {
        // Capture the frame from the video
        const canvas = document.createElement('canvas');
        canvas.width = generalVideo.videoWidth;
        canvas.height = generalVideo.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(generalVideo, 0, 0, canvas.width, canvas.height);

        const imageDataUrl = canvas.toDataURL('image/png');
        fetch('/general_sign_predict', {
            method: 'POST',
            body: JSON.stringify({ image: imageDataUrl }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            const currentTime = Date.now();
            if (data.prediction !== lastRecognizedSign || currentTime - lastRecognizedTime > 5000) {
                generalResultText.innerText = data.prediction;
                lastRecognizedSign = data.prediction;
                lastRecognizedTime = currentTime;
                const msg = new SpeechSynthesisUtterance(data.prediction);
                window.speechSynthesis.speak(msg);
            }
        });
    };
});
