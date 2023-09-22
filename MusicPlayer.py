import tkinter as tk
import os
import pygame
from tkinter import Scale, StringVar

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("960x540")

        pygame.init()
        pygame.mixer.init()

        self.playlist = []
        self.current_track = 0
        self.paused = False
        self.volume = 0.5  # Initial volume (0.0 to 1.0)
        # Flags for repeat and shuffle modes
        self.repeat_mode = False
        self.shuffle_mode = False
        self.create_ui()
        self.load_songs()

        # Variables for progress bar and song length
        self.song_length = 0
        self.update_interval = 1000  # Update every 1 second
        self.progress_timer = None  # Timer for updating progress bar and duration label

        self.song_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.song_label.pack()

        self.duration_label = tk.Label(self.root, text="0:00 / 0:00", font=("Arial", 12))
        self.duration_label.pack()

        self.progress_bar = Scale(self.root, from_=0, to=100, orient="horizontal", label="", showvalue=0)
        self.progress_bar.pack(fill="x")

    def create_ui(self):
        # Create a custom font for the listbox
        listbox_font = ("Arial", 12)

        # Song listbox with custom font
        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=60, height=20, font=listbox_font)
        self.listbox.pack(pady=10)

        # Buttons frame
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack()

        # Play, Pause, Previous, Next buttons
        self.play_button = tk.Button(buttons_frame, text="Play", command=self.play_music)
        self.play_button.pack(side=tk.LEFT, padx=10)
        self.pause_button = tk.Button(buttons_frame, text="Pause", command=self.pause_music)
        self.pause_button.pack(side=tk.LEFT, padx=10)
        self.prev_button = tk.Button(buttons_frame, text="Previous", command=self.prev_track)
        self.prev_button.pack(side=tk.LEFT, padx=10)
        self.next_button = tk.Button(buttons_frame, text="Next", command=self.next_track)
        self.next_button.pack(side=tk.LEFT, padx=10)

        # Volume control
        self.volume_slider = Scale(self.root, from_=0, to=100, orient="horizontal", label="Volume", command=self.update_volume)
        self.volume_slider.set(50)
        self.volume_slider.pack()

        # Volume label
        self.volume_label_var = StringVar()  # Create a StringVar for volume label
        self.volume_label_var.set(f"Volume: {int(self.volume * 100)}%")
        self.volume_label = tk.Label(self.root, textvariable=self.volume_label_var, font=("Arial", 12))
        self.volume_label.pack(pady=5)

        # Repeat and Shuffle buttons
        self.repeat_button = tk.Button(self.root, text="Repeat", command=self.toggle_repeat)
        self.repeat_button.pack(pady=5)
        self.shuffle_button = tk.Button(self.root, text="Shuffle", command=self.toggle_shuffle)
        self.shuffle_button.pack(pady=5)

    def update_volume(self, value):
        self.volume = int(value) / 100
        pygame.mixer.music.set_volume(self.volume)
        self.volume_label_var.set(f"Volume: {int(self.volume * 100)}%")

    def load_songs(self):
        music_folder = "C:\\Users\\subha\\Music\\"  # Replace with the path to your music folder
        for filename in os.listdir(music_folder):
            if filename.endswith(".mp3"):
                self.playlist.append(os.path.join(music_folder, filename))
                self.listbox.insert(tk.END, filename)

    def play_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            track_path = self.playlist[self.current_track]
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            self.song_length = pygame.mixer.Sound(track_path).get_length()
            self.update_song_label()  # Update the song label
            self.update_duration_label()  # Update the duration label
            self.start_progress_timer()  # Start the progress timer

    def update_duration_label(self):
        def format_time(seconds):
            minutes, seconds = divmod(int(seconds), 60)
            return f"{minutes}:{seconds:02}"

        current_time = pygame.mixer.music.get_pos() / 1000
        duration_text = f"{format_time(current_time)} / {format_time(self.song_length)}"
        self.duration_label.config(text=duration_text)
        self.root.after(self.update_interval, self.update_duration_label)

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def prev_track(self):
        # Stop the progress timer
        self.stop_progress_timer()

        self.current_track = (self.current_track - 1) % len(self.playlist)
        self.play_music()

    def next_track(self):
        # Stop the progress timer
        self.stop_progress_timer()

        self.current_track = (self.current_track + 1) % len(self.playlist)
        self.play_music()

    def update_song_label(self):
        current_song = os.path.basename(self.playlist[self.current_track])
        self.song_label.config(text="Now Playing: " + current_song)

    def toggle_repeat(self):
        self.repeat_mode = not self.repeat_mode
        if self.repeat_mode:
            print("Repeat mode is ON")
        else:
            print("Repeat mode is OFF")

    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        if self.shuffle_mode:
            print("Shuffle mode is ON")
            # Shuffle the playlist if needed
            self.shuffle_playlist()
        else:
            print("Shuffle mode is OFF")
            # Restore the original playlist order if needed
            self.load_songs()

    def shuffle_playlist(self):
        # Shuffle the playlist randomly
        import random
        random.shuffle(self.playlist)
        self.listbox.delete(0, tk.END)
        for filename in self.playlist:
            self.listbox.insert(tk.END, os.path.basename(filename))

    def start_progress_timer(self):
        self.progress_timer = self.root.after(self.update_interval, self.update_progress_bar)

    def stop_progress_timer(self):
        if self.progress_timer:
            self.root.after_cancel(self.progress_timer)
            self.progress_timer = None

    def update_progress_bar(self):
        current_time = pygame.mixer.music.get_pos() / 1000  # Get current time in seconds
        progress = (current_time / self.song_length) * 100
        self.progress_bar.set(progress)
        self.progress_timer = self.root.after(self.update_interval, self.update_progress_bar)

if __name__ == "__main__":
    root = tk.Tk()
    music_player = MusicPlayer(root)
    root.mainloop()
