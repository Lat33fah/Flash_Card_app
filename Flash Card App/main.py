from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title('Flash Card App')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_back = PhotoImage(file='images/card_back.png')
card_front = PhotoImage(file='images/card_front.png')
right_img = PhotoImage(file='images/right.png')
wrong_img = PhotoImage(file='images/wrong.png')
current_word = {}
dict_words = {}
# Reading CSV file
try:
    words = pd.read_csv('data/Words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('data/french_words.csv')
    dict_words = original_data.to_dict(orient='records')
else:
    dict_words = words.to_dict(orient='records')


# Canvas
canvas = Canvas(width=800, height=526)
image_color = canvas.create_image(400, 263, image=card_front)
title = canvas.create_text(400, 150, text="Title", fill="black", font='Ariel 40 italic')
card_word = canvas.create_text(400, 263, text='Word', fill="black", font='Ariel 60 bold')
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)


# Clicking buttons
def click():
    global current_word, change_time
    window.after_cancel(change_time)
    current_word = random.choice(dict_words)
    canvas.itemconfig(title, text='French', fill='black')
    canvas.itemconfig(card_word, text=current_word['French'], fill='black')
    canvas.itemconfig(image_color, image=card_front)
    change_time = window.after(3000, change)


# Flip cards
def change():
    canvas.itemconfig(title, text='English', fill='white')
    canvas.itemconfig(card_word, text=current_word['English'], fill='white')
    canvas.itemconfig(image_color, image=card_back)


change_time = window.after(3000, change)


def known_word():
    dict_words.remove(current_word)
    print(len(dict_words))
    data = pd.DataFrame(dict_words)
    data.to_csv("data/Words_to_learn.csv", index=False)
    click()


# Buttons
right_button = Button(image=right_img, highlightthickness=0, command=known_word)
right_button.grid(column=1, row=1)

wrong_button = Button(image=wrong_img, highlightthickness=0, command=click)
wrong_button.grid(column=0, row=1)

click()

window.mainloop()
