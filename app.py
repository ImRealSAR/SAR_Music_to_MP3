from flask import Flask, request, send_file, render_template
from pytube import YouTube
from io import BytesIO
from pydub import AudioSegment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    yt = YouTube(url)
    video_url = yt.video_id
    stream = yt.streams.filter(only_audio=True).first()
    buffer = BytesIO()
    stream.stream_to_buffer(buffer)
    buffer.seek(0)
    audio = AudioSegment.from_file(buffer, format="mp4")
    output_buffer = BytesIO()
    audio.export(output_buffer, format="mp3")
    output_buffer.seek(0)
    return send_file(output_buffer, as_attachment=True, download_name=f"{yt.title}.mp3", mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)
