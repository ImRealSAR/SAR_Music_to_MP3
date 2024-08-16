
document.getElementById('convert-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const youtubeUrl = document.getElementById('youtube-url').value;
    const resultDiv = document.getElementById('result');

    // Simulate an API request to a third-party service
    fetch(`https://example-api.com/convert?url=${encodeURIComponent(youtubeUrl)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                resultDiv.innerHTML = `<a href="${data.downloadLink}" download>Download MP3</a>`;
            } else {
                resultDiv.textContent = "Error converting video.";
            }
        })
        .catch(error => {
            resultDiv.textContent = "An error occurred. Please try again.";
        });
});
