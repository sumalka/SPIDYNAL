import requests
import json
import pygame
from colorama import Fore, init
from time import sleep

# Function to simulate file search in a public index
def spidy_lens_search_global(query):
    # Simulated response from a public index
    public_files = [
        {"name": "Sample File 1", "link": "https://drive.google.com/file/d/1234567890", "platform": "Google Drive"},
        {"name": "Example Report", "link": "https://onedrive.live.com/view.aspx?cid=abcd1234", "platform": "OneDrive"},
        {"name": "Image File", "link": "https://www.icloud.com/icloud-drive/file/56789abcd", "platform": "iCloud"}
    ]

    found_items = []
    for file in public_files:
        if query.lower() in file['name'].lower():
            found_items.append(file)

    return found_items


# Function to play sound
def play_sound(file_path):
    pygame.mixer.init()  # Initialize the mixer for sound
    pygame.mixer.music.load(file_path)  # Load your sound file (e.g., 'sound.mp3')
    pygame.mixer.music.play()  # Play the sound


# Function for typewriting effect
def type_writer(text, color, delay=0.05):
    for char in text:
        print(f"{color}{char}{Fore.RESET}", end="", flush=True)
        sleep(delay)
    print()


# Main function
def spidy_lens():
    type_writer("Welcome to SPIDY LENS™ — Global Search System!", Fore.GREEN)
    type_writer("Search globally for files shared on Google Drive, OneDrive, and iCloud.", Fore.CYAN)
    type_writer("Type 'close lens' to exit.", Fore.CYAN)

    while True:
        query = input(f"{Fore.CYAN}Enter the file name or keyword to search globally: {Fore.RESET}")
        if query.lower() == "close lens":
            type_writer("Closing SPIDY LENS...", Fore.RED)
            break

        type_writer(f"Searching for '{query}' in public files...", Fore.YELLOW)

        # Simulate searching the public file index
        found_items = spidy_lens_search_global(query)

        if found_items:
            type_writer(f"Found {len(found_items)} results:", Fore.GREEN)
            for item in found_items:
                print(f"{item['platform']}: {item['name']} - {item['link']}")
        else:
            type_writer(f"No results found for '{query}'.", Fore.RED)

        # Play sound after search is completed
        play_sound("assets/notify.mp3")  # Path to the notification sound


# Initialize colorama
init()

# Run the program
spidy_lens()
