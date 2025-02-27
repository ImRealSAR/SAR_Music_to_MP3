import os
import sys
import tkinter as tk
from tkinter import messagebox
import subprocess
import shutil

def get_yt_dlp_path():
    """Return the path to yt-dlp, bundled or system-installed."""
    if getattr(sys, 'frozen', False):  # Running as compiled EXE
        exe_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))

    yt_dlp_path = os.path.join(exe_dir, "yt-dlp.exe")  # For the bundled version

    if os.path.exists(yt_dlp_path):
        return yt_dlp_path  # Use the local version
    elif shutil.which("yt-dlp"):  # Check system-installed yt-dlp
        return "yt-dlp"
    else:
        return None  # Not found

def update_yt_dlp():
    """Automatically updates yt-dlp if it's available."""
    yt_dlp_path = get_yt_dlp_path()
    if yt_dlp_path and os.path.exists(yt_dlp_path):
        try:
            subprocess.run([yt_dlp_path, "-U"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            messagebox.showerror("Update Error", f"Could not update yt-dlp: {str(e)}")
    else:
        messagebox.showwarning("Warning", "yt-dlp not found! The program may not work.")

def download_mp3():
    """Downloads a YouTube video as MP3."""
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a valid YouTube URL")
        return

    yt_dlp_path = get_yt_dlp_path()
    if not yt_dlp_path:
        messagebox.showerror("Error", "yt-dlp not found! Ensure it's included or installed.")
        return

    try:
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "%(title)s.%(ext)s")

        command = [yt_dlp_path, "-x", "--audio-format", "mp3", "-o", output_path, url]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            messagebox.showinfo("Success", "Downloaded successfully! Check the 'downloads' folder.")
        else:
            messagebox.showerror("Download Error", result.stderr.decode("utf-8"))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("SAR's YouTube to MP3 Converter")
root.geometry("400x200")

# Run yt-dlp update on startup
update_yt_dlp()

tk.Label(root, text="Enter YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

download_button = tk.Button(root, text="Convert to MP3", command=download_mp3)
download_button.pack(pady=20)

root.mainloop()
