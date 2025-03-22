import glob
import os
import sys
from queue import Queue
import threading
import time
from colorama import Fore, init
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep
import pygame 


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores files there
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Initialize pygame mixer
pygame.mixer.init()

# Function for typewriting effect
def type_writer(text, color, delay=0.05):
    for char in text:
        sys.stdout.write(f"{color}{char}{Fore.RESET}")
        sys.stdout.flush()
        sleep(delay)
    print("\n")


# Update the sound file paths
sound_path = resource_path("build/spidy/mound/assets")  # Correct relative path

# Use os.path.join to build the full paths
spidy_sound = os.path.join(sound_path, "spidy_sound.mp3")
wake_up_spidy = os.path.join(sound_path, "wake_up_spidy.mp3")
start = os.path.join(sound_path, "start.mp3")
middle = os.path.join(sound_path, "middle.mp3")
dady_home = os.path.join(sound_path, "dady_home.mp3")
spidy_online = os.path.join(sound_path, "spidy_online.mp3")
hacker_mode = os.path.join(sound_path, "hacker_mode.mp3")
voice_mode = os.path.join(sound_path, "voice_mode.mp3")
notify_sound = os.path.join(sound_path, "xnotify.mp3")


# Loader class to provide animation during the search
class Loader:
    def __init__(self, desc="Searching...", end="Search Completed ✅", timeout=0.1):
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_value, tb):
        self.stop()

# Function to search for files with specified extensions
def spidy_lens_search_drive(query, drive, extensions, found_items, progress_queue, lock):
    total_items = 0
    files = []
    for ext in extensions:
        search_pattern = f"{drive}**/*{ext}"
        files.extend(glob.glob(search_pattern, recursive=True))
    total_items = len(files)
    
    # After counting files, push the total number of items to progress queue
    with lock:
        progress_queue.put(0)  # Start animation with 0 progress
        progress_queue.put(total_items)  # Set the total count for progress
    
    for file in files:
        if query.lower() in os.path.basename(file).lower():
            found_items.append(file)
        with lock:
            progress_queue.put(1)  # Increment progress for each file processed

# Main Search Function
def spidy_lens_search(query, extensions):
    drives = ['C:\\', 'D:\\', 'E:\\']
    found_items = []
    lock = threading.Lock()
    progress_queue = Queue()
    threads = []
    total_items = 0

    # Start search threads for each drive
    for drive in drives:
        thread = threading.Thread(target=spidy_lens_search_drive, args=(query, drive, extensions, found_items, progress_queue, lock))
        threads.append(thread)
        thread.start()
        total_items += 1  # Increase total_items for each drive processed

    # Start animation thread
    with Loader(f"Searching for '{query} {extensions}' on all drives..."):
        # Wait for threads to finish
        for thread in threads:
            thread.join()

    return found_items

# Updated play_sound function to match spidy.py
# Function to play sound
def play_sound(sound):
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the sound to finish
            time.sleep(1)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Main Function
def spidy_lens():
    type_writer("Welcome to SPIDY LENS™ — Your Smart File Finder!", Fore.GREEN)
    type_writer("Type 'close lens' to exit.", Fore.CYAN)

    while True:
        file_ext = input(f"{Fore.CYAN}Enter the file extension 🕷️: {Fore.RESET}")
        if file_ext.lower() == "close lens":
            type_writer("Closing SPIDY LENS...", Fore.RED)
            break
        
        query = input(f"{Fore.CYAN}Enter the file name or keyword: {Fore.RESET}")
        if query.lower() == "close lens":
            type_writer("Closing SPIDY LENS...", Fore.RED)
            break

        type_writer(f"Searching for '{query}' files with extension '{file_ext}'...", Fore.YELLOW)
        found_items = spidy_lens_search(query, [file_ext])

        sys.stdout.write("\r\n")
        if found_items:
            thread1 = threading.Thread(target=play_sound, args=(notify_sound,))
            thread1.start()
            
            type_writer(f"Found {len(found_items)} results:", Fore.GREEN)
            for item in found_items:
                print(item)
        else:
            type_writer(f"No results found for '{query}' with extension '{file_ext}'.", Fore.RED)


# Initialize colorama
init()

# Run the program
spidy_lens()