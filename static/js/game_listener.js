function captureFrame() {
    fetch('/process-frame', {
        method: 'POST',
        body: JSON.stringify({ game: game }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
    // .then(data => {
    //     if (data.scoreChanged) {
    //         changeLights();
    //     }
    // })
    // .catch(error => console.error('Error processing frame:', error));
}

function changeLights() {
    console.log("Score changed! Triggering light change...");
}

setInterval(captureFrame, 1000);
