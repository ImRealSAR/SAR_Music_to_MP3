import os
import tkinter as tk
from tkinter import messagebox
import subprocess

def update_yt_dlp():
    """Automatically updates yt-dlp to the latest version."""
    try:
        subprocess.run("yt-dlp -U", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        messagebox.showerror("Update Error", f"Could not update yt-dlp: {str(e)}")

def download_mp3():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a valid YouTube URL")
        return
    
    try:
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "%(title)s.%(ext)s")
        
        command = f'yt-dlp -x --audio-format mp3 -o "{output_path}" "{url}"'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            messagebox.showinfo("Success", "Downloaded successfully! Check the 'downloads' folder.")
        else:
            messagebox.showerror("Download Error", result.stderr.decode("utf-8"))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("YouTube to MP3 Converter")
root.geometry("400x200")

# Run yt-dlp update on startup
update_yt_dlp()

tk.Label(root, text="Enter YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

download_button = tk.Button(root, text="Convert to MP3", command=download_mp3)
download_button.pack(pady=20)

root.mainloop()
