// Obtener todos los videos que se están reproduciendo en la página
const videos = document.querySelectorAll('video');

const recordButton = document.createElement('button');
recordButton.textContent = 'Grabar Video';
recordButton.style.position = 'absolute';
recordButton.style.backgroundColor = 'blue'; 
recordButton.style.color = 'white'; 
recordButton.style.padding = '5px 10px';
recordButton.style.border = 'none';
recordButton.style.cursor = 'pointer';
recordButton.className = 'Dowloader'; 

let recordingInProgress = false;
let mediaRecorder;

// Función para agregar el botón de grabación a un video
const addRecordButtonToVideo = (video) => {
    const button = recordButton.cloneNode(true);
    button.style.position = 'absolute'; 
    button.style.top = '50%';
    button.style.left = '50%';
    button.style.transform = 'translate(-50%, -50%)'; 

    button.addEventListener('click', async () => {
        if (recordingInProgress) {
            return;
        }

        const windowHeight = window.innerHeight;
        const videoTopOffset = video.getBoundingClientRect().top + window.scrollY; 
        const videoHeight = video.offsetHeight;
        const scrollOffset = videoTopOffset - (windowHeight / 2) + (videoHeight / 2);
        window.scrollTo({ top: scrollOffset, behavior: 'smooth' });

        if (!recordingInProgress && video.readyState === 4) {
            recordingInProgress = true;

            button.textContent = 'Grabando Video';
            button.style.backgroundColor = 'red'; 

            video.currentTime = 0;

            // Activar el sonido si el video está silenciado
            if (video.muted) {
                video.muted = false;
            }

            const stream = video.captureStream();
            mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
            const recordedChunks = [];

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const blob = new Blob(recordedChunks, { type: 'video/webm' });
                const url = URL.createObjectURL(blob);

                const downloadLink = document.createElement('a');
                downloadLink.href = url;
                downloadLink.download = 'grabacion_video.webm'; 
                downloadLink.click();

                URL.revokeObjectURL(url);

                recordingInProgress = false;
                button.textContent = 'Listo'; 
                button.style.backgroundColor = 'blue'; 
            };

            mediaRecorder.start();

            video.play();

            video.addEventListener('pause', () => {
                if (mediaRecorder && mediaRecorder.state === 'recording') {
                    mediaRecorder.pause();
                }
            });

            video.addEventListener('play', () => {
                if (mediaRecorder && mediaRecorder.state === 'paused') {
                    mediaRecorder.resume();
                }
            });
        }
    });

    video.parentNode.appendChild(button);
};

// Agregar el botón
videos.forEach(video => addRecordButtonToVideo(video));
