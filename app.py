from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from pytube import YouTube
from pydub import AudioSegment
import zipfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    urls = [request.form[key] for key in request.form.keys()]
    output_dir = 'downloads'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mp3_files = []
    
    for url in urls:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_dir)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        AudioSegment.from_file(out_file).export(new_file, format='mp3')
        os.remove(out_file)
        mp3_files.append(new_file)

    zip_path = os.path.join(output_dir, 'mp3_files.zip')
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for mp3_file in mp3_files:
            zipf.write(mp3_file, os.path.basename(mp3_file))
            os.remove(mp3_file)

    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
