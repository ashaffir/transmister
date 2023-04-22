const recordBtn = document.getElementById('record-button');
const stopBtn = document.getElementById('stop-btn');
const transcribeBtn = document.getElementById('runButton');
const loaderContainer = document.getElementById('loader-container');
const loaderText = document.getElementById('loader-text');

recordBtn.addEventListener('click', () => {
    showLoader('Recording');
    startRecording();
});

stopBtn.addEventListener('click', () => {
    stopRecording();
    recordBtn.style.display = 'block';
    hideLoader();
});


transcribeBtn.addEventListener('click', () => {
    showLoader('Transcribing');
});

function showLoader(text) {
    loaderText.textContent = text;
    loaderContainer.style.display = 'block';
    recordBtn.classList.add('hidden');
    if (text === 'Recording') {
        stopBtn.style.display = 'block';
    }
}

function hideLoader() {
    loaderContainer.style.display = 'none';
    stopBtn.style.display = 'none';
}