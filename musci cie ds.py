import tkinter as tk
from tkinter import filedialog 
import os
import random
import pygame
from tkinter import font

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player (By- Atharva Gaikwad)")
        self.playlist = []
        self.current_song_index = 0
        self.is_playing = False 
        self.current_song = None  # Store the currently playing song
        self.is_shuffled = False  # Flag to track whether the playlist is shuffled

        self.now_playing_label = tk.Label(root, text="Now Playing: No song selected")
        self.now_playing_label.pack(pady=10)

        self.status_text = tk.Text(root, wrap=tk.WORD, width=40, height=1,)
        self.status_text.pack(pady=5)

        self.song_list_label = tk.Label(root, text="List of Songs (Sorted)")
        self.song_list_label.pack(pady=5)

        self.song_list_text = tk.Text(root, wrap=tk.WORD, width=50, height=15,  borderwidth=9, relief="ridge")
        self.song_list_text.pack(pady=5)

        self.button_frame = tk.Frame(self.root, borderwidth=5, relief="ridge")
        self.button_frame.pack(pady=15)

        self.pair_1_frame = tk.Frame(self.button_frame)
        self.pair_1_frame.pack(side=tk.LEFT, padx=15)

        self.play_pause_button = tk.Button(self.pair_1_frame, text="⏯️", font=("helvetica", 20),command=self.toggle_play_pause , height=1, width=3,borderwidth=3 ,relief="solid")
        self.play_pause_button.pack(pady=5)

        self.pair_2_frame = tk.Frame(self.button_frame)
        self.pair_2_frame.pack(side=tk.LEFT, padx=15, pady=(10, 10))

        self.next_button = tk.Button(self.pair_2_frame, text="⏭️",font=("Arial", 12), command=self.next_song)
        self.next_button.pack(pady=5)

        self.prev_button = tk.Button(self.pair_2_frame, text="⏮️",font=("Arial", 12), command=self.prev_song)
        self.prev_button.pack(pady=5)
        
        self.pair_3_frame = tk.Frame(self.button_frame)
        self.pair_3_frame.pack(side=tk.LEFT, padx=15)

        self.shuffle_button = tk.Button(self.pair_3_frame, text="🔀" ,font=("Arial", 12), command=self.shuffle_playlist)
        self.shuffle_button.pack(pady=5)

        self.sort_button = tk.Button(self.pair_3_frame, text="🔁" ,font=("Arial", 12), command=self.sort_playlist)
        self.sort_button.pack(pady=5)
        
        self.pair_4_frame = tk.Frame(self.button_frame)
        self.pair_4_frame.pack(side=tk.LEFT, padx=15)

        self.add_button = tk.Button(self.pair_4_frame, text="➕" ,font=("Arial", 12), command=self.add_song)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(self.pair_4_frame, text="➖" ,font=("Arial", 12), command=self.delete_song)
        self.delete_button.pack(pady=5)


    def update_song_label(self):
        if self.current_song is not None:
            song_name = os.path.basename(self.current_song)
            self.now_playing_label.config(text="Now Playing: " + song_name)
        else:
            self.now_playing_label.config(text="Now Playing: No song selected")
    
    def play_music(self):
        if not self.playlist:
            self.update_status("No songs in the playlist")
            return
        
        else:
            song = self.playlist[self.current_song_index]
            self.current_song = song  # Set the current song
            self.update_song_label()  # Update the "Now Playing" label
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            self.paused = False
            self.update_status("Song playing")
    
    def toggle_play_pause(self):
        if not self.playlist:
            self.update_status("No songs in the playlist")
            return

        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.update_status("Song paused")
        else:
            if self.current_song is None:
                # If there's no current song, start playing the first song in the playlist
                song = self.playlist[0]
                self.current_song_index = 0
                self.current_song = song
            else:
                song = self.playlist[self.current_song_index]

            self.update_song_label()
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            self.is_playing = True
            self.update_status("Song playing")

    def next_song(self):
        if not self.playlist:
            self.update_status("No songs in the playlist")
            return

        if self.current_song_index < len(self.playlist) - 1:
            self.current_song_index += 1
            self.play_music()
        else:
            self.update_status("End of playlist")

    def prev_song(self):
        if not self.playlist:
            self.update_status("No songs in the playlist")
            return

        if self.current_song_index > 0:
            self.current_song_index -= 1
            self.play_music()
        else:
            self.update_status("Beginning of playlist")

    def shuffle_playlist(self):
        random.shuffle(self.playlist)
        self.current_song_index = 0
        self.is_shuffled = True
        self.update_song_list_label()
        self.update_song_list()

    def sort_playlist(self):
        self.playlist.sort()
        self.current_song_index = 0
        self.is_shuffled = False
        self.update_song_list_label()
        self.update_song_list()

    def update_song_list_label(self):
        label_text = "List of Songs"
        if self.is_shuffled:
            label_text += " (Shuffled)"
        else:
            label_text += " (Sorted)"
        self.song_list_label.config(text=label_text)

    def update_song_list(self):
        song_list = "\n\n".join([os.path.basename(song) for song in self.playlist])
        self.song_list_text.delete(1.0, tk.END)
        self.song_list_text.insert(tk.END, song_list)

    def add_song(self):
        if len(self.playlist) < 10:
            file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
            if file_path:
                self.playlist.append(file_path)
                self.update_song_list()
            self.update_status("Song added to the playlist")
        else:
            self.update_status("Maximum of 10 songs reached.")

    def delete_song(self):
        if not self.playlist:
            self.update_status("No songs in the playlist")
            return

        del self.playlist[self.current_song_index]

        if self.current_song_index >= len(self.playlist):
            self.current_song_index = 0
        elif self.current_song_index < 0:
            self.current_song_index = 0

        if not self.playlist:
            self.current_song = None
        elif self.current_song_index < len(self.playlist):
            self.current_song = self.playlist[self.current_song_index]

        self.update_song_list()
        self.update_song_label()
        self.update_status("Song deleted from the playlist")


    def update_status(self, text):
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, text)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("610x580")
    root.configure(bg="lightblue",borderwidth=25, relief="ridge")
    pygame.mixer.init()
    player = MusicPlayer(root)
    player.run()
