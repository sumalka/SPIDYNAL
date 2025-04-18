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
import subprocess
from datetime import datetime
import string
import ctypes
import contextlib

mode = "normal"  # global search mode default

def get_available_drives():
    """Return a list of currently connected and accessible drive letters."""
    drives = []
    bitmask = ctypes.cdll.kernel32.GetLogicalDrives()
    for i, letter in enumerate(string.ascii_uppercase):
        if bitmask & (1 << i):
            drives.append(f"{letter}:\\")
    return drives

# Function to play the exit sound and print the exit message
def exit_sequence():
    # Thread to play the exit sound
    thread1 = threading.Thread(target=play_sound, args=(spidy_sound,))
    # Thread to start the typewriter effect for exit message
    thread2 = threading.Thread(target=type_writer, args=("SPIDY BROZ SYSTEM OFFLINE 😴", Fore.YELLOW))

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()
    
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores files there
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Initialize pygame mixer
pygame.mixer.init()

# Function for typewriting effect
def type_writer(text, color, delay=0.01):
    for char in text:
        sys.stdout.write(f"{color}{char}{Fore.RESET}")
        sys.stdout.flush()
        sleep(delay)
    print("\n")


# Update the sound file paths
sound_path = resource_path("assets")  # Correct relative path

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
noresult_sound = os.path.join(sound_path, "noresult.mp3")

# Loader class to provide animation during the search
class Loader:
    def __init__(self, desc="Searching...", end="  Search Completed ✅", timeout=0.1):
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
        try:
            if "$Recycle.Bin" in drive:
                # 👇 Go through all Recycle Bin subfolders
                for root, _, filenames in os.walk(drive):
                    for filename in filenames:
                        if filename.lower().endswith(ext.lower()):
                            full_path = os.path.join(root, filename)
                            files.append(full_path)
            else:
                files.extend(glob.glob(search_pattern, recursive=True))
        except Exception:
            continue  # Ignore inaccessible folders

   
    total_items = len(files)
    
    # After counting files, push the total number of items to progress queue
    with lock:
        progress_queue.put(0)  # Start animation with 0 progress
        progress_queue.put(total_items)  # Set the total count for progress
    
    for file in files:
        if "$Recycle.Bin" in file:
            found_items.append(file)  # 🧟 Include recycled file regardless of name
        elif query.lower() in os.path.basename(file).lower():
            found_items.append(file)
        with lock:
            progress_queue.put(1)


# Main Search Function
def spidy_lens_search(query, extensions):
    drives = get_available_drives()

    custom_paths = [
        # 💬 Known Active Caches & Temp
        os.path.expandvars(r"%APPDATA%\WhatsApp\Cache"),
        os.path.expandvars(r"%LOCALAPPDATA%\Packages"),
        os.path.expanduser(r"~\AppData\Local\Temp"),

        # 🧠 Startup locations
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"),     # Per-user startup
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup",                    # Global startup

        # 🔍 Windows Performance & Search
        r"C:\Windows\Prefetch",
        r"C:\ProgramData\Microsoft\Search\Data\Applications\Windows",

        # 📦 Shared Resources
        r"C:\Program Files\Common Files",
        r"C:\Program Files (x86)\Common Files",

        # 📂 Public / Default Profiles
        r"C:\Users\Public\Documents",
        r"C:\Users\Default\AppData",
        r"C:\Users\Default\NTUSER.DAT",

        # 🛡️ Defender & AV
        r"C:\ProgramData\Microsoft\Windows Defender",

        # 🔥 Boot & Recovery
        r"C:\$WinREAgent",
        r"C:\$Windows.~WS",
        r"C:\$Windows.~BT",
        r"C:\Recovery",
        r"C:\System Volume Information",

        # 🧱 System Service Profiles
        r"C:\Windows\ServiceProfiles\LocalService",
        r"C:\Windows\ServiceProfiles\NetworkService",

        # 🧪 Scheduled Tasks, System Logs
        r"C:\Windows\Tasks",
        r"C:\Windows\System32\Tasks",
        r"C:\Windows\System32\LogFiles",
        r"C:\Windows\debug",
        r"C:\Windows\Logs",
        r"C:\Windows\Temp",

        # 🕵️ Hidden from Explorer but exists
        r"C:\Documents and Settings",  # Link on modern OS, legacy profiles
        r"C:\ProgramData\Microsoft\Crypto\RSA\MachineKeys",  # Private certs
        r"C:\Windows\System32\config",  # SYSTEM, SAM, SECURITY hives
        r"C:\Windows\CSC",  # Offline files cache
        r"C:\Windows\System32\DriverStore",  # Drivers DB

        # 💾 Potential malware drop zones
        r"C:\Intel\Logs",
        r"C:\PerfLogs",
        r"C:\Config.Msi",
        r"C:\MSOCache",
    ]

    if mode == "hell":
        all_paths = drives + custom_paths
        loader_msg = f"  🔍 [HELL MODE] Scanning drives + system folders for '{query} {extensions}'..."
    else:
        all_paths = drives
        loader_msg = f"  🔍 Scanning drives for '{query} {extensions}'..."

    found_items = []
    lock = threading.Lock()
    progress_queue = Queue()
    threads = []

    with Loader(loader_msg):
        for path in all_paths:
            thread = threading.Thread(
                target=spidy_lens_search_drive,
                args=(query, path, extensions, found_items, progress_queue, lock)
            )
            threads.append(thread)
            thread.start()

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
    global mode  # 🛠️ Fixes UnboundLocalError
    sys.stdout.write("\r\n")
    sys.stdout.write("\r\n")
    sys.stdout.write("\r\n")
    welcome_message = (
        "╔══════════════════════ SPIDY LENS™ ══════════════════════╗\n"
        "║                                                         ║\n"
        "║                  Advanced File Search                   ║\n"
        "║       ─────── Type 'close lens' to exit ───────         ║\n"
        "║                                                         ║\n"
        "╚═════════════════════════════════════════════════════════╝"
    )
    type_writer(welcome_message, Fore.GREEN)  # Let type_writer apply the color
    sys.stdout.write("\r\n")

    while True:
        # ---- Input validation for file extension ----
        while True:
            file_ext = input(f"{Fore.CYAN}  🕷️ Enter the file extension : {Fore.RESET}").strip()

            if file_ext.lower() == "close lens":
                type_writer("   Closing SPIDY LENS...", Fore.RED)
                return

            if file_ext.lower() == "lens mode":
                type_writer(f"\r\n  🧭 Current Mode: {mode.upper()}", Fore.BLUE)
                continue

            if file_ext.lower() == "lens reset":
                type_writer("  🔁 Resetting SPIDY LENS input form...", Fore.CYAN)
                continue  # Restart extension prompt

            if file_ext.lower() in ["mode hell", "mode normal"]:
                mode = "hell" if "hell" in file_ext.lower() else "normal"
                type_writer(f"\r\n  🛠️ Switched to {mode.upper()} MODE", Fore.YELLOW)
                continue

            # 🚫 Extension must start with dot like .exe, .mp3
            if not file_ext.startswith("."):
                type_writer(" ❌ Invalid extension format! Use something like `.mp3`, `.bat`, `.jpg`", Fore.RED)
                continue

            if file_ext:
                break

            type_writer(" Please enter a valid file extension!", Fore.RED)
            sys.stdout.write("\r\n")

        # ---- Input validation for file name/keyword ----
        while True:
            query = input(f"{Fore.CYAN}  🕷️ Enter the file name or keyword : {Fore.RESET}").strip()

            if query.lower() == "close lens":
                type_writer("   Closing SPIDY LENS...", Fore.RED)
                return

            if query.lower() == "lens mode":
                type_writer(f"\r\n  🧭 Current Mode: {mode.upper()}", Fore.BLUE)
                continue

            if query.lower() == "lens reset":
                type_writer("  🔁 Resetting SPIDY LENS input form...", Fore.CYAN)
                # 👇 This is the fix: break to OUTER while True, restarting both prompts!
                break

            if query.lower() in ["mode hell", "mode normal"]:
                mode = "hell" if "hell" in query.lower() else "normal"
                type_writer(f"\r\n  🛠️ Mode switched to {mode.upper()} MODE", Fore.MAGENTA)
                continue

            if query and len(query) >= 1:
                break

            type_writer("Please enter a valid file name or keyword (at least 1 character)!", Fore.RED)
            sys.stdout.write("\r\n")

        # If query is 'lens reset', break out to extension prompt
        if query.lower() == "lens reset":
            continue

        # Normal search below
        type_writer(f"  Searching for '{query}' files with extension '{file_ext}'... ", Fore.YELLOW)
        found_items = spidy_lens_search(query, [file_ext])

        # ... Rest of your results logic stays the same


        sys.stdout.write("\r\n")
        if found_items:
            thread1 = threading.Thread(target=play_sound, args=(notify_sound,))
            thread1.start()
            
            type_writer(f" Found {len(found_items)} results 🕷️:", Fore.GREEN)
            
            for idx, item in enumerate(found_items, 1):
                print(f"  {idx}. {item}")  # Indent results for alignment
                if "$Recycle.Bin" in item:
                    print(f"     ⚠️ This file may be renamed. It's from Recycle Bin.")
                sys.stdout.write("\r\n")  
                # Improved UI with consistent spacing and alignment
                action_prompt = (
                    f"{Fore.MAGENTA}┌─ Options for '{os.path.basename(item)}' 🕷️ ───────────────\n"  # Header with border
                    f"{Fore.MAGENTA}|\n"
                    f"{Fore.YELLOW}│  [1] Open File          [2] Open Location          [3] Next\n"  # Single-item options
                    f"{Fore.GREEN}│  [4] Open All Files     [5] Open All Locations     [6] Show All\n"
                    f"{Fore.GREEN}│  [7] Close Lens\n"  # All-item options
                    f"{Fore.MAGENTA}└────────────────────────────────────────────────────────────────────────────\n"  # Footer border
                    f"{Fore.CYAN}  Enter your choice: "  # Prompt aligned with options
                )
                action = input(action_prompt + Fore.RESET).strip()

                if action == '1':  # Open single file
                    try:
                        if os.name == 'nt':  # Windows
                            os.startfile(item)
                        elif os.name == 'posix':  # Linux or macOS
                            subprocess.run(['xdg-open' if os.uname().sysname == 'Linux' else 'open', item])
                        type_writer(f"Opening '{item}'...", Fore.YELLOW)
                    except Exception as e:
                        type_writer(f"Error opening file: {e}", Fore.RED)
                elif action == '2':  # Open single location
                    try:
                        dir_path = os.path.dirname(item)
                        if os.name == 'nt':  # Windows
                            os.startfile(dir_path)
                        elif os.name == 'posix':  # Linux or macOS
                            subprocess.run(['xdg-open' if os.uname().sysname == 'Linux' else 'open', dir_path])
                        type_writer(f"   Opening location of '{item}'...",Fore.YELLOW)
                    except Exception as e:
                        type_writer(f"Error opening location: {e}",Fore.RED)
                elif action == '3':  # Skip single item
                    type_writer("Skipping...", Fore.CYAN)
                elif action == '4':  # Open all files
                    for all_item in found_items:
                        try:
                            if os.name == 'nt':
                                os.startfile(all_item)
                            elif os.name == 'posix':
                                subprocess.run(['xdg-open' if os.uname().sysname == 'Linux' else 'open', all_item])
                            type_writer(f"   Opening '{all_item}'...", Fore.YELLOW)
                        except Exception as e:
                            type_writer(f"Error opening file: {e}",Fore.RED)
                    break  # Exit loop after processing all
                elif action == '5':  # Open all locations
                    for all_item in found_items:
                        try:
                            dir_path = os.path.dirname(all_item)
                            if os.name == 'nt':
                                os.startfile(dir_path)
                            elif os.name == 'posix':
                                subprocess.run(['xdg-open' if os.uname().sysname == 'Linux' else 'open', dir_path])
                            type_writer(f"   Opening location of '{all_item}'...",Fore.YELLOW)
                        except Exception as e:
                            type_writer(f"Error opening location: {e}", Fore.RED)
                    break  # Exit loop after processing all
                elif action == '6':  # Show all items
                    type_writer(" All found locations:", Fore.GREEN)
                    for index, item in enumerate(found_items, start=1):
                        print(f"  {index}. {item}")  # Indent locations for alignment
                    sys.stdout.write("\r\n")  # Extra line after locations
                    sys.stdout.write("\r\n")  # Extra line after locations
                    break  # Exit loop without further processing
                elif action == '7':  # Close lens
                    type_writer("  Closing SPIDY LENS...", Fore.RED)
                    sys.stdout.write("\r\n")  # Extra line after locations
                    return
                else:  # Invalid input defaults to skip
                    type_writer("Invalid option, skipping...", Fore.CYAN)
                sys.stdout.write("\r\n")
        else:
            thread1 = threading.Thread(target=play_sound, args=(noresult_sound,))
            thread1.start()
            type_writer(f"   No results found for '{query}' with extension '{file_ext}'.", Fore.RED)
            sys.stdout.write("\r\n")
            
# Initialize colorama
init()

# Run the program
if __name__ == "__main__":
    try:
        spidy_lens()
    except KeyboardInterrupt:
        now = datetime.now().strftime("%H:%M:%S")
        type_writer(f"\n🕷️ [{now}] SPIDY LENS interrupted by user. pressed Ctrl + C. Exiting SPIDYNAL safely...", Fore.RED)
        exit_sequence()
        sys.exit(0)
