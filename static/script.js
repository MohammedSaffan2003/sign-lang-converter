document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const resultText = document.getElementById('result-text');
    const uploadResultText = document.getElementById('upload-result-text');
    let stream;

    const init = () => {
        setupEventListeners();
    };

    const setupEventListeners = () => {
        document.getElementById('choose-capture').addEventListener('click', showCaptureSection);
        document.getElementById('choose-upload').addEventListener('click', showUploadSection);
        document.getElementById('choose-sign-words').addEventListener('click', showSignWordsSection);

        document.getElementById('start').addEventListener('click', startCamera);
        document.getElementById('capture').addEventListener('click', captureImage);
        document.getElementById('stop').addEventListener('click', stopCamera);
        document.getElementById('speak').addEventListener('click', () => speakText(resultText.innerText));
        document.getElementById('upload-speak').addEventListener('click', () => speakText(uploadResultText.innerText));
        document.getElementById('upload').addEventListener('click', uploadImage);
        document.getElementById('word-input').addEventListener('keydown', handleWordInput);
    };

    const showCaptureSection = () => {
        toggleVisibility('capture-section');
    };

    const showUploadSection = () => {
        toggleVisibility('upload-section');
    };

    const showSignWordsSection = () => {
        toggleVisibility('sign-words-section');
    };

    const toggleVisibility = (sectionId) => {
        const sections = ['capture-section', 'upload-section', 'sign-words-section'];
        sections.forEach(id => {
            document.getElementById(id).classList.toggle('hidden', id !== sectionId);
        });
    };

    const startCamera = async () => {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.style.display = 'block';
    };

    const captureImage = () => {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageDataUrl = canvas.toDataURL('image/png');

        fetchPrediction(imageDataUrl, resultText);
    };

    const stopCamera = () => {
        stream.getTracks().forEach(track => track.stop());
        video.style.display = 'none';
    };

    const speakText = (text) => {
        const msg = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(msg);
    };

    const uploadImage = () => {
        const file = document.getElementById('imageUpload').files[0];
        const reader = new FileReader();

        reader.onload = () => {
            const imageUrl = reader.result;
            document.getElementById('uploaded-image').src = imageUrl;
            document.getElementById('uploaded-image').style.display = 'block';

            fetchPrediction(imageUrl, uploadResultText);
        };

        if (file) {
            reader.readAsDataURL(file);
        }
    };

    const fetchPrediction = (imageDataUrl, resultElement) => {
        fetch('/predict', {
            method: 'POST',
            body: JSON.stringify({ image: imageDataUrl }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            resultElement.innerText = data.prediction;
        });
    };

    const handleWordInput = (event) => {
        if (event.key === 'Enter') {
            const wordInput = event.target;
            const word = wordInput.value.trim().toLowerCase();
            const signOutput = document.getElementById('sign-output');
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
    };

    init();
});
