import os
import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
from moviepy.editor import AudioFileClip
import requests

def download_video_as_mp3():
    # Get the YouTube URL from the input field
    youtube_url = url_entry.get().strip()
    if not youtube_url:
        messagebox.showerror("Error", "Please enter a valid YouTube URL.")
        return

    output_path = "downloads"  # Folder to save MP3 files
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        # Fetch the YouTube page content using requests
        response = requests.get(youtube_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        # Initialize YouTube object with the fetched content
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        download_path = audio_stream.download(output_path=output_path)

        # Convert to MP3
        mp3_path = os.path.splitext(download_path)[0] + ".mp3"
        with AudioFileClip(download_path) as audio_clip:
            audio_clip.write_audiofile(mp3_path)

        # Remove original file
        os.remove(download_path)

        messagebox.showinfo("Success", f"Downloaded and saved as MP3:\n{mp3_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# Setting up the Tkinter GUI window
app = tk.Tk()
app.title("YouTube to MP3 Converter")

# Adding input field and button
tk.Label(app, text="YouTube URL:").pack(pady=10)
url_entry = tk.Entry(app, width=50)
url_entry.pack(pady=5)
download_button = tk.Button(app, text="Download as MP3", command=download_video_as_mp3)
download_button.pack(pady=20)

app.mainloop()