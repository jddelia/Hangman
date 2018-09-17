#! /usr/bin/python3

# This is a game of hangman with a GUI.

from tkinter import *
from random import choice

class Hangman:
    WORD_LIST = []

    def __init__(self, root):
        """ Populate WORD LIST with words from
            txt file. """
        with  open("words.txt") as fp:
            for word in fp:
                self.WORD_LIST.append(word.strip())

        self.root = root
        root.title("Hangman")

        self.strikes = 0
        self.word = choice(self.WORD_LIST).upper()
        self.word_underscored = ["_"] * len(self.word)
        self.guess = ""
        self.guessed = "GUESSES: "
        self.photo = PhotoImage(file="/home/jddelia/python/Tkinter/Hangman/images/hangman01.png")

        # Canvas where image will be put.
        self.canvas = Canvas(root, width=600, height=500)
        self.canvas.grid(row=0, columnspan=3)
        self.canvas.create_image(340, 240, image=self.photo)

        # Displays word with underscores for characters.
        self.word_blank = StringVar()
        self.word_blank.set(" _ " * len(self.word))
        self.word_blank_label = Label(root, textvariable=self.word_blank)
        self.word_blank_label.grid(row=1, column=0, sticky=W+E)

        self.enter_letter_label = Label(root, text="ENTER LETTER: ")
        self.enter_letter_label.grid(row=1, column=1, sticky=W+E)

        # Entry field to accept letters.
        letterfield = root.register(self.validate)

        self.entry = Entry(root, validate="key", validatecommand=(letterfield, "%P"))
        self.entry.grid(row=1, columnspan=4, column=2, sticky=W+E)

        # Displays the guesses that have been made
        self.guesses = StringVar()
        self.guesses.set(self.guessed)
        self.guesses_label = Label(root, textvariable=self.guesses)
        self.guesses_label.grid(row=2, column=3, sticky=W)

        # New game, with values reset.
        self.new = Button(root, text="New Game", command=self.new_game)
        self.new.grid(row=2, column=0, sticky=W+E)

        self.add = Button(root, text="HINT", state=DISABLED)
        self.add.grid(row=2, column=1, sticky=W+E)

        # Submit button, calls check_guess() function.
        self.submit = Button(root, text="Submit", command=self.check_guess)
        self.submit.grid(row=2, column=2, sticky=W+E)

    def change_image(self):
        """ This function updates the image based
            on strikes. """
        image_lst = ["/home/jddelia/python/Tkinter/Hangman/images/hangman01.png",
                    "/home/jddelia/python/Tkinter/Hangman/images/hangman02.png",
                    "/home/jddelia/python/Tkinter/Hangman/images/hangman03.png",
                    "/home/jddelia/python/Tkinter/Hangman/images/hangman04.png",
                    "/home/jddelia/python/Tkinter/Hangman/images/hangman05.png",
                    "/home/jddelia/python/Tkinter/Hangman/images/hangman06.png",
                    "/home/jddelia/python/Tkinter/Hangman/images/hangman07.png"]
        self.strikes = self.strikes % len(image_lst)
        self.photo = PhotoImage(file=image_lst[self.strikes])
        self.canvas.create_image(340, 240, image=self.photo)

    def validate(self, text):
        # Validates input into entry field.
        if not text:
            return True
        else:
            try:
                self.guess = text.upper()
                return True
            except:
                return False

    def new_game(self):
        """ This function resets all the attributes,
            and selects a new word to start a new game. """
        self.strikes = 0
        self.change_image()
        self.word = choice(self.WORD_LIST).upper()
        self.word_blank.set(" _ " * len(self.word))
        self.word_underscored = ["_"] * len(self.word)
        self.guessed = "GUESSES: "
        self.guesses.set(self.guessed)

    def check_guess(self):
        """ This function checks if guess was correct.
            It also updates attributes accordingly. """
        if self.guess in self.guessed[8:]:
            self.entry.delete(0, END)
            return
        self.guessed += self.guess
        self.guesses.set(self.guessed)
        if self.guessed[-1] not in self.word:
            self.strikes += 1
            self.change_image()
        else:
            self.word_form()

        if "_" in self.word_underscored:
            if self.strikes == 6:
                self.word_blank.set(self.word)
                self.guesses.set("HANGMAN. YOU LOSE.")

        if ''.join(self.word_underscored) == self.word:
            self.guesses.set("You WIN!")
            self.word_blank.set(self.word)

        self.entry.delete(0, END)

    def word_form(self):
        """ This function updates the display of underscored
            word. """
        if self.guessed[-1] in self.word:
            for index, letter in enumerate(self.word_underscored):
                if self.word[index] == self.guessed[-1]:
                    self.word_underscored[index] = self.word[index]
        self.word_blank.set(str(self.word_underscored))

def main():
    root = Tk()

    app = Hangman(root)

    root.mainloop()

if __name__ == "__main__":
    main()
