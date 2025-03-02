import time
import os
import pygame
import sys
from colorama import init, Fore
import random
import threading
import glob
from colorama import Fore
from queue import Queue


# Function for typewriting effect
def type_writer(text, color, delay=0.5):
    sys.stdout.write(f"{color}{text}\n{Fore.RESET}")
    sys.stdout.flush()

# Function for loading animation with percentage and drive info
def loading_animation(total, current, lock, progress_queue, current_drive):
    animation = "|/-\\"
    idx = 0
    while current < total:
        try:
            current = progress_queue.get(timeout=0.1)  # Update from the queue with a timeout
        except:
            pass  # If no update, continue
        percentage = (current / total) * 100
        sys.stdout.write(f"\r{Fore.YELLOW}Searching on {current_drive}... {animation[idx % 4]}  {percentage:.2f}%")
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1

# Function to search for files and folders in each drive
def spidy_lens_search_drive(query, drive, extensions, found_items, current_item, total_items, lock, progress_queue):
    for ext in extensions:
        search_pattern = f"{drive}**/*{ext}"
        files = glob.glob(search_pattern, recursive=True)
        for file in files:
            if query.lower() in file.lower():
                found_items.append(file)
            with lock:
                current_item += 1
                progress_queue.put(current_item)
        with lock:
            total_items += len(files)

    search_pattern_folders = f"{drive}**/{query}*/"
    folders = glob.glob(search_pattern_folders, recursive=True)
    for folder in folders:
        found_items.append(folder)
        with lock:
            current_item += 1
            progress_queue.put(current_item)
    with lock:
        total_items += len(folders)

# Function to search for files and folders
def spidy_lens_search(query):
    extensions = [
        '.pdf', '.docx', '.doc', '.odt', '.txt', '.rtf', '.epub', '.md', '.html', '.xml', '.pptx', '.ppt', '.xlsx', '.xls', '.csv', '.tex', '.json', 
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ico', '.svg', '.webp', '.raw', '.heif', '.heic', 
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.alac', '.opus', 
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.mpg', '.mpeg', '.3gp', '.mts', '.vob', '.iso', 
        '.zip', '.tar', '.gz', '.rar', '.7z', '.xz', '.bz2', '.tar.gz', '.tar.bz2', '.tgz', 
        '.exe', '.bat', '.sh', '.cmd', '.msi', '.apk', '.app', '.dmg', '.jar', '.run', '.bin', 
        '.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.php', '.rb', '.swift', '.go', '.pl', '.ts', '.json', '.scala', '.lua', '.sh', 
        '.ttf', '.otf', '.woff', '.woff2', '.eot', '.svg', 
        '.db', '.sql', '.sqlite', '.mdb', '.accdb', '.json', '.xml', 
        '.dll', '.sys', '.ini', '.bak', '.log', '.dat', '.bin', 
        '.iso', '.dmg', '.vmdk', '.vdi', '.bak', '.backup', 
        '.vmdk', '.vhd', '.vdi', '.iso', '.ovf', 
        '.torrent', '.chm', '.md', '.xml', '.yml', '.json', '.ini', '.bak', '.log', '.dat', '.bin', '.apk', '.srt', 
        '.m4v', '.rmvb', '.mov', '.mpeg', '.mpg', '.ts', '.vob', '.m3u', '.cue'
    ]

    drives = ['C:\\', 'D:\\', 'E:\\']  # Adjust according to your system
    found_items = []
    total_items = 0  # Track total items to be searched
    current_item = 0  # Track the current item being processed

    lock = threading.Lock()  # Lock for thread-safe access
    progress_queue = Queue()  # Queue to update progress

    threads = []

    # Start a thread for each drive to search in parallel
    for drive in drives:
        thread = threading.Thread(target=spidy_lens_search_drive, args=(query, drive, extensions, found_items, current_item, total_items, lock, progress_queue))
        threads.append(thread)
        thread.start()

    # Start loading animation with percentage and drive info in a separate thread
    loading_thread = threading.Thread(target=loading_animation, args=(total_items, current_item, lock, progress_queue, drives[0]))  # Default to 'C:'
    loading_thread.daemon = True
    loading_thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return found_items, total_items, current_item

def spidy_lens():
    type_writer("Welcome to SPIDY LENS! You can search for files by name with extensions (.pdf, .docx, etc.). Please note that this process may take some time as it involves searching and analyzing the system. Type 'close lens' to exit the lens.", Fore.GREEN)

    while True:
        # Change color for user input
        query = input(f"{Fore.CYAN}Enter the file name or keyword to search (minimum 2 characters, or type 'close lens' to exit): {Fore.RESET}")

        if query.lower() == "close lens":
            type_writer("Closing SPIDY LENS.", Fore.RED)
            break  # Exit the loop and close the program

        # Ensure the input is at least 2 characters long
        if len(query) < 2:
            type_writer("Please enter at least 2 characters for the search query.", Fore.RED)
            continue  # Ask for input again without exiting

        # Start searching and loading in a separate thread
        type_writer(f"Searching for '{query}'...", Fore.YELLOW)

        found_items, total_items, current_item = spidy_lens_search(query)

        # After search is completed, stop the loading animation by clearing the line
        sys.stdout.write("\r                                      \r")

        # Display results
        if found_items:
            type_writer(f"Found {len(found_items)} items related to '{query}':", Fore.GREEN)
            for result in found_items:
                print(result)
        else:
            type_writer(f"No results found for '{query}'.", Fore.RED)
        
# Initialize pygame mixer
pygame.mixer.init()

# Initialize colorama
init()

# ASCII Art for branding
from termcolor import colored
def print_spidy_art():
    spidy_art1 = """
    
    
    
    
    
   ▄████████    ▄███████▄  ▄█  ████████▄  ▄██   ▄        
  ███    ███   ███    ███ ███  ███   ▀███ ███   ██▄      
  ███    █▀    ███    ███ ███▌ ███    ███ ███▄▄▄███      
  ███          ███    ███ ███▌ ███    ███ ▀▀▀▀▀▀███      
▀███████████ ▀█████████▀  ███▌ ███    ███ ▄██   ███      
         ███   ███        ███  ███    ███ ███   ███      
   ▄█    ███   ███        ███  ███   ▄███ ███   ███      
 ▄████████▀   ▄████▀      █▀   ████████▀   ▀█████▀        
 
 
"""
    spidy_art2 = """
    
    
    
                                                     ⠀⠀⢀⡟⢀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣧⠈⣧⠀⠀
                                                     ⠀⠀⣼⠀⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡆⢸⡆⠀
⠀⢰⣿⠀⠻⠧⣤⡴⣦⣤⣤⣤⣠⡶⣤⣤⠾⠗⠈⣿⠀
⠀⠺⣷⡶⠖⠛⣩⣭⣿⣿⣿⣿⣿⣯⣭⡙⠛⠶⣶⡿⠃
⠀⠀⠀⢀⣤⠾⢋⣴⠟⣿⣿⣿⡟⢷⣬⠙⢷⣄⠀⠀⠀
⢀⣠⡴⠟⠁⠀⣾⡇⠀⣿⣿⣿⡇⠀⣿⡇⠀⠙⠳⣦⣀
⢸⡏⠀⠀⠀⠀⢿⡇⠀⢸⣿⣿⠁⠀⣿⡇⠀⠀⠀⠈⣿
⠀⣷⠀⠀⠀⠀⢸⡇⠀⠀⢻⠇⠀⠀⣿⠇⠀⠀⠀⠀⣿
⠀⢿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⢸⡏
⠘⡇⠀⠀⠀⠈⣷⠀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⡾⠀
                                                        ⠀⠀⠹⠀⠀⠀⠀⢻⠀⠀⠀⠀⠀⢸⠇⠀⠀⠀⢰⠁⠀
                                                        ⠀⠀⠀⠁⠀⠀⠀⠈⢇⠀⠀⠀⠀⡞⠀⠀⠀⠀⠁⠀⠀

"""
 #Ensure both arts have the same number of lines by padding with empty lines
    lines_spidy_art1 = spidy_art1.split('\n')
    lines_spidy_art2 = spidy_art2.split('\n')

    max_lines = max(len(lines_spidy_art1), len(lines_spidy_art2))

    # Pad the shorter art with empty lines
    while len(lines_spidy_art1) < max_lines:
        lines_spidy_art1.append("")
    while len(lines_spidy_art2) < max_lines:
        lines_spidy_art2.append("")

    # Margin to be added (e.g., 10 spaces)
    margin = 35

    # Add margin only to spidy_art1
    lines_spidy_art1 = [(" " * margin) + line for line in lines_spidy_art1]

    # Create a shorter horizontal border with alternating colors
    horizontal_border = ""
    for i in range(156):  # Length of border, set to 150 characters
        if i % 2 == 0:
            horizontal_border += colored("═", "blue")
        else:
            horizontal_border += colored("═", "red")

    # Print the shorter horizontal border at the top
    print(horizontal_border)

    # Printing the two Spidy Art side by side with a horizontal blue and red border
    for line1, line2 in zip(lines_spidy_art1, lines_spidy_art2):
        print(f"{colored(line1, 'blue')}{colored(line2, 'red')}")

    # Print the shorter horizontal border at the bottom
    print(horizontal_border)

# High-end Linux-style loader animation with progress bar and unique colors
def linux_loader_animation():
    loading_text = "System Initializing..."
    total_steps = 50  # Number of steps to simulate the system loading
    bar_length = 50  # Length of the progress bar
    spinner = ['|', '/', '-', '\\']
    count = 0

    for step in range(total_steps):
        progress = int((step / total_steps) * bar_length)
        bar = "█" * progress + " " * (bar_length - progress)
        
        # Customizing the colors for different parts
        sys.stdout.write(f"\r{colored(loading_text, 'yellow')} "
                         f"[{colored(bar, 'white')}] "
                         f"{colored(str(step * 2) + '%', 'green')} "
                         f"{colored(spinner[count % 4], 'green')}")
        sys.stdout.flush()
        time.sleep(0.1)
        count += 1

    sys.stdout.write("\r" + " " * 80 + "\r")  # Clear the line after completion
    
    # Different color for the completion text and progress bar
    print(f"{colored(loading_text, 'yellow')} "
          f"[{colored('█████████████████████████', 'white')}] "
          f"{colored('100% Complete', 'green')}")


# Call the function to print ASCII art
print_spidy_art()

# Call the Linux-style loader animation after the ASCII art
print("\n")
linux_loader_animation()

# Update the paths to include the full path to the files
sound_path = r"E:\SPIDY BROZ SYSTEM™ V1.0\\"
spidy_sound = os.path.join(sound_path, "assets/spidy_sound.mp3")
wake_up_spidy = os.path.join(sound_path, "assets/ake_up_spidy.mp3")
start = os.path.join(sound_path, "assets/start.mp3")
middle = os.path.join(sound_path, "assets/middle.mp3")
dady_home = os.path.join(sound_path, "assets/dady_home.mp3")
spidy_online = os.path.join(sound_path, "assets/spidy_online.mp3")
hacker_mode = os.path.join(sound_path, "assets/hacker_mode.mp3")
voice_mode = os.path.join(sound_path, "assets/voice_mode.mp3")

# Function to simulate typing effect
def type_writer(text, color=Fore.GREEN, delay=0.02, end_line=True):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    if end_line:
        print()  # To move to the next line if needed

# Function to play sound
def play_sound(sound):
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the sound to finish
            time.sleep(1)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Random Spidy Quotes
spidy_quotes = [
    "I am your friendly neighborhood Spidy! 🕷️",
    "With great power comes great responsibility! ⚡",
    "Web-slinging through the streets...💨",
    "I’m always watching... 😏",
    "Spidy is always ready for action! 🔥"
]

# Function to get a random Spidy quote
def get_random_spidy_quote():
    return random.choice(spidy_quotes)

# Function to simulate typing effect
def type_writer(text, color=Fore.GREEN, delay=0.02, end_line=True):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    if end_line:
        print()  # To move to the next line if needed

# Function to play sound
def play_sound(sound):
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the sound to finish
            time.sleep(1)
    except Exception as e:
        print(f"Error playing sound: {e}")
        

import threading
import random
from colorama import Fore

# Function to play the sound (Make sure 'dady_home' is a valid path to a sound file)
def play_daddy_home_sound():
    play_sound(dady_home)  # Make sure 'dady_home' is the correct sound file

# Function to simulate the typing effect
def type_daddy_home_message():
    type_writer("Daddy is Home Wake Up Spidy 🔥😏", random.choice([Fore.RED, Fore.YELLOW, Fore.LIGHTCYAN_EX]))

# Function to play the sound (Make sure to define the play_sound function)
def play_sound(sound):
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the sound to finish
            time.sleep(1)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Function for the typewriter effect (Ensure this is defined)
def type_writer(text, color=Fore.GREEN, delay=0.02, end_line=True):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    if end_line:
        print()  # To move to the next line if needed

spidy_quotes = [
    "I am your friendly neighborhood Spidy! 🕷️",
    "With great power comes great responsibility! ⚡",
    "Web-slinging through the streets...💨",
    "I’m always watching... 😏",
    "Spidy is always ready for action! 🔥"
]

# Function to simulate typing effect
def type_writer(text, color=Fore.GREEN, delay=0.02, end_line=True):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    if end_line:
        print()  # To move to the next line if needed

# Function to play sound
def play_sound(sound):
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the sound to finish
            time.sleep(1)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Function to get a random Spidy quote
def get_random_spidy_quote():
    return random.choice(spidy_quotes)

# Welcome Spidynal Forever
def spidy_online_system():
    print(Fore.CYAN)
    threading.Thread(target=play_sound, args=(spidy_online,)).start()
    type_writer("🔥 SPIDYNAL V2.0 SYSTEM ONLINE 💀🕸️", Fore.LIGHTCYAN_EX)
    type_writer("[🤝] GPT Private Server Connected...", Fore.MAGENTA)
    type_writer("[💀] Spidynal Security System ONLINE...", Fore.RED)
    type_writer("✅ DADDY IS HOME WAKE UP SPIDY!", Fore.YELLOW)

# Hacker Mode Activation
def hacker_mode_activation():
    threading.Thread(target=play_sound, args=(hacker_mode,)).start()
    type_writer("[💀] SPIDYNAL DARK HACKER MODE ACTIVATED...", Fore.RED)
    for i in range(5):
        type_writer(random.choice(spidy_quotes), random.choice([Fore.RED, Fore.CYAN, Fore.YELLOW]))
        time.sleep(0.5)

# Voice System
def voice_mode_system():
    threading.Thread(target=play_sound, args=(voice_mode,)).start()
    type_writer("🎙️ SPIDYNAL VOICE SYSTEM ONLINE...", Fore.LIGHTCYAN_EX)
    time.sleep(2)
    type_writer("Hello Daddy... Welcome back to your Private AI 🔥😏💀", Fore.YELLOW)

# Play 'DADDY HOME' sound and display message
def play_daddy_home_sound():
    play_sound(dady_home)  # Make sure 'dady_home' is the correct sound file

def type_daddy_home_message():
    type_writer("Daddy is Home Wake Up Spidy 🔥😏", random.choice([Fore.RED, Fore.YELLOW, Fore.LIGHTCYAN_EX]))


# Print ASCII Art with color
def print_ascii_art():
    print(Fore.CYAN )

# Play sound in background using threading
def play_start_sound():
    play_sound(start)

# Run both the ASCII art and sound concurrently
thread1 = threading.Thread(target=print_ascii_art)
thread2 = threading.Thread(target=play_start_sound)

# Start both threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

time.sleep(1)  # Add a small delay after both actions have completed

# Display system startup message
# Function to play sound in a separate thread
def play_middle_sound():
    play_sound(wake_up_spidy)

# Run both the sound and type_writer concurrently
thread1 = threading.Thread(target=play_middle_sound)
thread2 = threading.Thread(target=type_writer, args=("🔥 SPIDY X SYSTEM ONLINE 🕸️", Fore.CYAN))

# Start both threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

time.sleep(2)
# Function to play the sound for middle
def play_middle_sound():
    play_sound(middle)

# Run both the sound and type_writer concurrently
thread1 = threading.Thread(target=play_middle_sound)
thread2 = threading.Thread(target=type_writer, args=("[🤝] Connecting to ~SPIDY Private Server...", Fore.MAGENTA))

# Start both threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()
type_writer("✅ SPIDY SYSTEM ACTIVATED..!", Fore.GREEN)
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

# Play the intro sound in a separate thread
# thread = threading.Thread(target=play_sound, args=(middle,))
# thread.start()

while True:
    
    # Get command input from user with a dynamic typing effect
   
    type_writer(" ", Fore.LIGHTCYAN_EX)
    type_writer("SPIDYNAL™ 🕷️: ", Fore.CYAN, delay=0.02, end_line=False)
    command = input()

    import threading

# Assuming you are in the main command loop
    if command.lower() == "spidy":
        # Start both the sound and the typewriter effect concurrently using threads
        thread1 = threading.Thread(target=play_daddy_home_sound)
        thread2 = threading.Thread(target=type_daddy_home_message)

        # Start both threads
        thread1.start()
        thread2.start()

        # Wait for both threads to finish
        thread1.join()
        thread2.join()


    elif command.lower() == "whats today":
        # Display a random Spidy quote and change color
        type_writer(get_random_spidy_quote(), random.choice([Fore.LIGHTGREEN_EX, Fore.CYAN, Fore.MAGENTA]))
        
    elif command.lower() == "spidy hacks":
        hacker_mode_activation()
            
    elif command.lower() == "spidynal voice":
        voice_mode_system()
    elif command.lower() == "whats today":
        # Display a random Spidy quote
        type_writer(get_random_spidy_quote(), random.choice([Fore.LIGHTGREEN_EX, Fore.CYAN, Fore.MAGENTA]))

    elif command.lower() == "spidy lens":
        spidy_lens()  # Call the spidy_lens function when the user enters this command
        
    elif command.lower() == "exit":
        exit_sequence()
        break  # Exit the loop after the exit sequence is completed

    elif command.lower() == "help":
            type_writer("Available Commands: spidy, spidy hacks, spidynal voice, whats today, exit, help", Fore.GREEN)
        

    else:
        # Randomly change the color for an "Invalid Command"
        invalid_colors = [Fore.RED, Fore.YELLOW, Fore.MAGENTA, Fore.LIGHTCYAN_EX]
        type_writer(f"Invalid Command... Try Again 😏", random.choice(invalid_colors))
