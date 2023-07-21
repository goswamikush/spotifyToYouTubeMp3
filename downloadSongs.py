from pytube import YouTube
import os

def download_songs(songIds):
    destination = "/Users/kushgoswami/Desktop/music"
    for songId in songIds:
        url = f"https://www.youtube.com/watch?v={songId}"
        video = YouTube(url).streams.filter(only_audio=True).first()
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
    
