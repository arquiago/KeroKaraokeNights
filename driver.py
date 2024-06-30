import re
import time
from collections import deque
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from pydub import AudioSegment
from pydub.playback import play
import threading
class Session:
  def __init__(self, songs):
    self.playlist = deque(songs)
    self.play_event = threading.Event()

  def playFirstInQueue(self):
    song = self.playlist[0]
    self.play(song)

  def play(self, song):
    for secs in range(1, 4):
      print(f'começando em {secs}...')
      time.sleep(1)
      

    audio_thread = threading.Thread(target=self.playAudio, args=(song.audioFile,))
    audio_thread.start()

    root = tk.Tk()
    root.title("karaoke")
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, font=("Arial", 12))
    text_area.pack(pady=10, padx=10)

    text_area.tag_configure("pink", foreground="blue")

    for line in song.lyrics:
      text_area.insert(tk.END, line[0] + "\n")
      text_area.see(tk.END)
      text_area.update()
      time.sleep(line[1])
    
    audio_thread.join()
  
  def playEverything(self):
    while self.playlist:
      self.playFirstInQueue()
      self.playlist.popleft()
      self.play_event.wait()

  def playAudio(self, audioFile):
    audio = AudioSegment.from_file(audioFile)
    play(audio)
    self.play_event.set()

class Song:
  def __init__(self, lyrics, duration, audioFile):
    self.lyrics = lyrics
    self.time = duration
    self.audioFile = audioFile

def lyricsToSong(lyricsFile, audioFile, minutes=0, seconds=0):
  lyrics = open(lyricsFile)
  listaT = []
  for linha in lyrics:
    if re.search('^\s*$', linha): continue
    matchL = re.match('^\d+(\.\d+)?\s+(.*)', linha)
    linhaSeparada = linha.split()
    tempo = float(linhaSeparada[0])
    listaT.append((matchL.group(2), tempo))

  return Song(listaT, 60 * minutes + seconds, audioFile)

def convertSongs(files):
  songs = []
  for file in files:
    songs.append(lyricsToSong(file[0], file[1]))
  
  return songs

print("----------------------\nWelcome to the karaoke(˶˃ ᴗ ˂˶)!!! lets goooo\n----------------------")
time.sleep(4.5)


lista = [('OnlyActing.txt', 'OnlyActing.mp3'), ('360.txt', '360.mp3')]

listaSongs = convertSongs(lista)
session = Session(listaSongs)
session.playEverything()