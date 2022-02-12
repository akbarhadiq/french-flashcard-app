from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FLASHCARD_LANGUAGE_FONT = ("Ariel", 40, "italic")
FLASHCARD_VOCABULARY_FONT = ("Ariel", 60, "bold")
STARTING_FONT = ("Ariel", 20, "bold")

# ---------------------------- LANGUAGE DATA SETUP and TURNING THE FLASH CARD ------------------------------- #
# Language Data Setup

try:
    LANGUAGE_DATA_TO_LEARN = pandas.read_csv("data/words_to_learn.csv.csv")
except FileNotFoundError:
    LANGUAGE_DATA = pandas.read_csv("data/french_words.csv")
    LANGUAGE_DICTIONARY = LANGUAGE_DATA.to_dict(orient="records")
else:
    LANGUAGE_DICTIONARY = LANGUAGE_DATA_TO_LEARN.to_dict(orient="records")
    current_vocabulary = {}

# French


def generate_french_vocabulary():
    global current_vocabulary, flip_timer
    # cancel the flip timer
    window.after_cancel(flip_timer)

    current_vocabulary = random.choice(LANGUAGE_DICTIONARY)
    flash_card.itemconfig(card_title, text="French", fill="black")
    flash_card.itemconfig(card_word, text=current_vocabulary["French"], fill="black")
    flash_card.itemconfig(card_background, image=flash_card_front_image)

    # call the flip timer func flip_card
    flip_timer = window.after(3000, func=flip_card)

# English and flipping the cards


def flip_card():
    flash_card.itemconfig(card_title, text="English", fill="white")
    flash_card.itemconfig(card_word, text=current_vocabulary["English"], fill="white")
    flash_card.itemconfig(card_background, image=flash_card_back_image)


# Removing words if user click checkmark button to flag known French words
def is_known():
    LANGUAGE_DICTIONARY.remove(current_vocabulary)
    # print(len(LANGUAGE_DICTIONARY))
    data = pandas.DataFrame(LANGUAGE_DICTIONARY)
    data.to_csv("data/words_to_learn.csv", index=False)
    generate_french_vocabulary()


# ---------------------------- UI SETUP ------------------------------- #


# TkInter GUI
window = Tk()
window.title("Learn French with Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Create object image for images that are going to be used
flash_card_front_image = PhotoImage(file="images/card_front.png")
flash_card_back_image = PhotoImage(file="images/card_back.png")
check_button_image = PhotoImage(file="images/right.png")
x_button_image = PhotoImage(file="images/wrong.png")

# Create canvas
flash_card = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
# create the flash card front image
card_background = flash_card.create_image(400, 263, image=flash_card_front_image)
# create the flash card text
card_title = flash_card.create_text(400, 150, text="placeholder", font=FLASHCARD_LANGUAGE_FONT)
card_word = flash_card.create_text(400, 263, text="placeholder", font=STARTING_FONT,
                                   tags="vocabulary")
# Put the flash_card  on window
flash_card.grid(column=1, row=1, columnspan=2)


# Create the ✔ button and the ❌ button
known_button = Button(image=check_button_image, highlightthickness=0, command=is_known)
unknown_button = Button(image=x_button_image, highlightthickness=0, command=generate_french_vocabulary)
known_button.grid(column=1, row=2)
unknown_button.grid(column=2, row=2)


'''
Need to call the function generate_french_vocabulary() first to replace the
flash_card_front placeholder card_title and card_word text
'''

generate_french_vocabulary()

window.mainloop()
