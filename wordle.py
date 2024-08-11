import random
import string
import tkinter as tk
from bs4 import BeautifulSoup
import requests

root = tk.Tk()
root.title("Wordle Game")

label = tk.Label(root, text="", font=("Arial", 24))
label.pack()

guesses_left_label = tk.Label(root, text="Guesses Left: 6", font=("Arial", 18))
guesses_left_label.pack()

difficulty_label = tk.Label(root, text="Difficulty: Easy", font=("Arial", 18))
difficulty_label.pack()

entry = tk.Entry(root, font=("Arial", 24), width=20)
entry.pack()


url = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")
all_text = soup.get_text()
word_list = all_text.split()
five_letter_words = [word for word in word_list if len(word) == 5]

letterValues = {
  'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
}

attempts = 0
previous_guesses = []
difficulty_level = "easy"
random_word = None

def select_five_letter_word():
    global random_word
    if difficulty_level == "easy":
        easy_words = [word for word in five_letter_words if sum(letterValues[letter.upper()] for letter in word) <= 15]
        random_word = random.choice(easy_words)
    elif difficulty_level == "medium":
        medium_words = [word for word in five_letter_words if 15 < sum(letterValues[letter.upper()] for letter in word) <= 25]
        random_word = random.choice(medium_words)
    else:
        hard_words = [word for word in five_letter_words if sum(letterValues[letter.upper()] for letter in word) > 25]
        random_word = random.choice(hard_words)

def check_guess():
    global attempts,  easy_button, medium_button, hard_button
    guess = entry.get().lower()
    entry.delete(0, tk.END)

    if not all(char in string.ascii_lowercase for char in guess):
        label.config(text="Please enter only letters.")
        return

    if len(guess) != 5:
        label.config(text="Please enter a 5-letter word.")
        return

    if guess not in five_letter_words:
        label.config(text="Please input a real 5-letter word.")
        return

    # Check if the guess has already been made
    if guess in previous_guesses:
        label.config(text="You've already guessed that word.")
        return

    clue_labels = []
    clue_frame = tk.Frame(root)
    clue_frame.pack()

    for i, letter in enumerate(guess):
        clue_label = tk.Label(clue_frame, text=letter.upper(), fonr=("Arial", 18),  width=2, padx=5, pady=5)
        if letter == random_word[i]:
            clue_label.config(bg="green", fg="white")
        elif letter == random_word:
            clue_label.config(bg="yellow", fg="black")
        else:
            clue_label.config(bg="gray", fg="white")
        clue_label.pack(side=tk.LEFT)
        clue_labels.append(clue_label)

    previous_guesses.append(guess)
    attempts += 1
    guesses_left_label.config(text=f"Attempts Left: {6 - attempts}")

    if attempts == 1:
        easy_button.config(state=tk.DISABLED)
        medium_button.config(state=tk.DISABLED)
        hard_button.config(state=tk.DISABLED)

    if guess == random_word:
        label.config(text=f"You Win! The word was {random_word}.")
        for clue_label in clue_labels:
            clue_label.config(bg="green", fg="white")
            return True
    elif attempts == 6:
        label.config(text=f"You have run out of attempts, the word was {random_word}.")
        return True
    else:
        return False

def set_difficulty(level):
    global difficulty_level
    difficulty_level = level
    difficulty_label.config(text=f"Difficulty: {level.capitalize()}")

easy_button = tk.Button(root, text="Easy", command=lambda: set_difficulty("easy"), font=("Arial", 18))
easy_button.pack(side=tk.LEFT, padx=10)

medium_button = tk.Button(root, text="Medium", command=lambda: set_difficulty("medium"), font=("Arial", 18))
medium_button.pack(side=tk.LEFT, padx=10)

hard_button = tk.Button(root, text="Hard", command=lambda: set_difficulty("hard"), font=("Arial", 18))
hard_button.pack(side=tk.LEFT, padx=10)

submit_button = tk.Button(root, text="Submit", command=check_guess, font=("Arial", 18))
submit_button.pack()

select_five_letter_word()
root.mainloop()
