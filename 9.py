import random
import time
import tkinter as tk
import threading
import requests
from PIL import Image, ImageTk
import winsound  # For playing sounds (Windows)

# Fetch the word list from the provided URL
def fetch_word_list(url):
    response = requests.get(url)
    if response.status_code == 200:
        return set(response.text.splitlines())
    return set()

# Create a set of valid words (English only) from the given URL
word_list_url = "https://www.mit.edu/~ecprice/wordlist.10000"
word_list = fetch_word_list(word_list_url)

# Global variables to store current word, found words, found anagrams, and timers
current_word = ""
found_words_sequence = []  # Store found words and anagrams
timer_count = 0
word_timer_count = 0
is_word_found = False

# Layers to show the last letters
layers = [[] for _ in range(12)]  # Increased to 12 layers

# Create the main application window
app = tk.Tk()
app.title("Black Knight Moon Delay Simulator Base 9 ")

# Set the background image
bg_image = Image.open("moon.jpg")  # Use the path to the downloaded image
bg_image_width, bg_image_height = bg_image.size
app.geometry(f"{bg_image_width}x{bg_image_height}")  # Set window size to match the image dimensions

# Set the black background behind the background image
app.configure(bg='black')

bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(app, image=bg_photo)
background_label.place(relwidth=1, relheight=1)  # Cover entire window

# Create labels to display the current letter, word, timers, and found words
letter_label = tk.Label(app, font=('Helvetica', 24), fg='white', bg='black')
letter_label.pack(pady=20)

word_label = tk.Label(app, font=('Helvetica', 20), fg='white', bg='black')
word_label.pack(pady=20)

found_words_label = tk.Label(app, font=('Helvetica', 14), fg='white', bg='black', wraplength=380)  # Set wraplength for word wrapping
found_words_label.pack(anchor='nw')

timer_label = tk.Label(app, font=('Helvetica', 14), fg='white', bg='black')
timer_label.pack(anchor='nw')

word_timer_label = tk.Label(app, font=('Helvetica', 14), fg='white', bg='black')
word_timer_label.pack(anchor='nw')

# Create the signal indicator light in the specified position
signal_label = tk.Label(app, text="•", font=('Helvetica', 24), fg='red', bg='black')
signal_label.place(x=bg_image_width - 40, y=20)  # Positioned 40 pixels from the right and 20 pixels down
signal_label.pack_forget()

# Create labels for layers
layer_labels = []
for i in range(12):  # Increased to 12 layers
    label = tk.Label(app, font=('Helvetica', 14), fg='white', bg='black')
    label.pack(anchor='nw')
    layer_labels.append(label)

# Letter frequencies as percentages
letter_frequencies = {
    'E': 11.1607, 'A': 8.4966, 'R': 7.5809, 'I': 7.5448,
    'O': 7.1635, 'T': 6.9509, 'N': 6.6544, 'S': 5.7351,
    'L': 5.4893, 'C': 4.5388, 'U': 3.6308, 'D': 3.3844,
    'P': 3.1671, 'M': 3.0129, 'H': 3.0034, 'G': 2.4705,
    'B': 2.0720, 'F': 1.8121, 'Y': 1.7779, 'W': 1.2899,
    'K': 1.1016, 'V': 1.0074, 'X': 0.2902, 'Z': 0.2722,
    'J': 0.1965, 'Q': 0.1962
}

# Create a list of letters according to their frequencies
letters = []
for letter, frequency in letter_frequencies.items():
    letters.extend([letter] * int(frequency * 100))

# Define tones for A-Z
def play_tone(letter):
    frequencies = [
        261, 294, 329, 349, 392, 440, 494, 523, 587, 659, 698, 784,
        880, 988, 1047, 1175, 1319, 1397, 1568, 1760, 1976, 2093,
        2349, 2637, 2794, 3136, 3520, 3951  # C4 to B5
    ]
    index = ord(letter) - ord('A')  # Get the index from A-Z
    if 0 <= index < len(frequencies):
        winsound.Beep(frequencies[index], 200)  # Play tone for 200ms

def generate_random_base9(length=1):
    return ''.join(str(random.randint(0, 8)) for _ in range(length))

def get_letter_from_frequencies():
    return random.choice(letters)

def update_layers():
    for i in range(12):  # Update to handle 12 layers
        if len(current_word) >= (i + 1):
            layers[i] = current_word[-(i + 1):]
        else:
            layers[i] = ""

    for i in range(12):  # Update to display 12 layers
        layer_labels[i].config(text=f"Layer {i + 1}: {layers[i]}")

def update_timers():
    global timer_count, word_timer_count, is_word_found
    while True:
        time.sleep(0.1)
        timer_count += 1
        timer_label.config(text=f"Time Since Last Letter: {timer_count / 10:.1f} seconds")
        
        if not is_word_found:
            word_timer_count += 1
        word_timer_label.config(text=f"Time Since Last Word: {word_timer_count / 10:.1f} seconds")

def reset_word_flag():
    global is_word_found
    time.sleep(2)
    is_word_found = False

def show_signal():
    signal_label.pack()
    app.after(1000, signal_label.pack_forget)  # Hide after 1 second

def is_anagram(word1, word2):
    return sorted(word1.lower()) == sorted(word2.lower())

def find_valid_anagrams(input_string):
    valid_anagrams = []
    for word in word_list:
        if len(word) == len(input_string) and is_anagram(word, input_string):
            valid_anagrams.append(word)
    return valid_anagrams

def check_and_display_letter():
    global current_word, found_words_sequence, timer_count, word_timer_count, is_word_found
    while True:
        random_time = random.uniform(2.000, 10.000)
        time.sleep(random_time)

        letter = get_letter_from_frequencies()
        current_word += letter
        timer_count = 0

        # Play tone for the current letter
        play_tone(letter)

        for i in range(1, 13):  # Check for 12 layers
            display_word = current_word[-i:]
            if len(display_word) >= 2:
                # Ensure that the display_word is strictly in English
                if display_word.lower() in word_list:
                    found_words_sequence.append(display_word.lower())
                    if len(found_words_sequence) > 12:  # Limit to last 12 found words
                        found_words_sequence.pop(0)  # Remove the oldest entry
                    word_label.config(text=f"Found Word: {display_word}", fg='red')
                    is_word_found = True
                    word_timer_count = 0
                    threading.Thread(target=reset_word_flag).start()
                
                # Check for valid anagrams in all layers
                for layer in layers:
                    if layer and len(layer) == len(display_word):
                        valid_anagrams = find_valid_anagrams(layer)
                        if valid_anagrams:
                            for anagram in valid_anagrams:
                                if anagram not in found_words_sequence:
                                    found_words_sequence.append(anagram)
                                    if len(found_words_sequence) > 12:  # Limit to last 12 found anagrams
                                        found_words_sequence.pop(0)  # Remove the oldest entry
                                    word_label.config(text=f"Found Anagram: {anagram}", fg='cyan')
                                    break  # Exit the loop after finding a valid anagram

        if not is_word_found:
            word_label.config(text=f"Current Word: {current_word}", fg='white')

        letter_label.config(text=letter)
        update_layers()
        found_words_label.config(text=f"Found Words:\n{' '.join(found_words_sequence)}")
        show_signal()  # Show the flashing signal

# Run the timer and letter checking functions in separate threads
timer_thread = threading.Thread(target=update_timers)
timer_thread.daemon = True
timer_thread.start()

letter_thread = threading.Thread(target=check_and_display_letter)
letter_thread.daemon = True
letter_thread.start()

app.mainloop()
