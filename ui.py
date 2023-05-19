import tkinter.messagebox
from tkinter import *
from functools import partial
from quiz_brain import QuizBrain

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ COLOR CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Overall Theme
THEME_COLOR = "#375362"
WHITE = "#FFFFFF"
# Easy, Medium and Hard
YELLOW = "#d9c92b"
ORANGE = "#d98e2b"
RED = "#d92b2b"
# Correct or Not
GREEN = "#42DC46"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FONT CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
QUESTION_FONT = ("Ariel", 20, "italic")
SCORE_FONT = ("Ariel", 15, "italic")
LEVEL_FONT = ("Helvetica", 25, "bold")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ QuizGui Class ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class QuizGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("Fun Trivia Game")
        self.window.config(padx=20, pady=20, background=THEME_COLOR)

        self.get_difficulty()

        self.window.mainloop()

    def clear_screen(self):
        """A function that clears the screen from widgets."""
        widget_list = self.window.grid_slaves()
        for widget in widget_list:
            widget.destroy()

    def get_difficulty(self):
        """A function that gets the current difficulty and pushes the game forward."""

        # ~~~~~~~~~~~~~~~ Labels ~~~~~~~~~~~~~~~
        self.introduction = Label(text=f"Welcome to Our Trivia Game",
                                  font=LEVEL_FONT,
                                  bg=THEME_COLOR,
                                  fg=WHITE)
        self.introduction.grid(row=0, column=0, columnspan=3)

        self.question = Label(text=f"Up For a Challenge?",
                              font=SCORE_FONT,
                              bg=THEME_COLOR,
                              fg=WHITE)
        self.question.grid(row=1, column=0, columnspan=3)

        # ~~~~~~~~~~~~~~~ Buttons ~~~~~~~~~~~~~~~
        self.e_button = Button(text="EASY", font=LEVEL_FONT, highlightthickness=0,
                               bg=THEME_COLOR, fg=GREEN, command=partial(self.button_pressed, "easy"))
        self.e_button.grid(row=2, column=0)

        self.m_button = Button(text="MEDIUM", font=LEVEL_FONT, highlightthickness=0,
                               bg=THEME_COLOR, fg=ORANGE, command=partial(self.button_pressed, "medium"))
        self.m_button.grid(row=2, column=1)

        self.h_button = Button(text="HARD", font=LEVEL_FONT, highlightthickness=0,
                               bg=THEME_COLOR, fg=RED, command=partial(self.button_pressed, "hard"))
        self.h_button.grid(row=2, column=2)

        self.window.mainloop()

    def button_pressed(self, difficulty):
        """A function that registers the current difficulty chosen."""
        self.difficulty = difficulty
        self.quiz = QuizBrain(difficulty)

        self.clear_screen()
        self.window.quit()
        self.game_screen()

    def game_screen(self):
        """A function that initiates the main game screen."""
        self.window.update()

        # ~~~~~~~~~~~~~~~ A Label with Chosen Difficulty ~~~~~~~~~~~~~~~
        if self.difficulty == "easy":
            self.chosen_difficulty = Label(text=f"{self.difficulty.upper()}",
                                           font=LEVEL_FONT, bg=THEME_COLOR, fg=YELLOW)
        elif self.difficulty == "medium":
            self.chosen_difficulty = Label(text=f"{self.difficulty.upper()}",
                                           font=LEVEL_FONT, bg=THEME_COLOR, fg=ORANGE)
        else:
            self.chosen_difficulty = Label(text=f"{self.difficulty.upper()}",
                                           font=LEVEL_FONT, bg=THEME_COLOR, fg=RED)

        self.chosen_difficulty.grid(row=0, column=0, columnspan=2)

        # ~~~~~~~~~~ Score and Mistakes Labels ~~~~~~~~~~
        self.score_label = Label(text=f"Score: {self.quiz.score}", font=SCORE_FONT, bg=THEME_COLOR, fg=WHITE)
        self.score_label.grid(row=1, column=0, pady=10, sticky=W)

        self.mistakes_left = self.quiz.allowed_mistakes - self.quiz.mistakes
        self.mistakes_label = Label(text=f"Mistakes Left: {self.mistakes_left}",
                                    font=SCORE_FONT,
                                    bg=THEME_COLOR,
                                    fg=WHITE,
                                    anchor="ne")
        self.mistakes_label.grid(row=1, column=1, pady=10, sticky=W)

        # ~~~~~~~~~~ Central Canvas ~~~~~~~~~~
        self.question_gui = Canvas(width=300, height=250, bg=WHITE, highlightthickness=0)
        self.question_gui.grid(row=2, column=0, columnspan=2, pady=20)

        self.question_text = self.question_gui.create_text((150, 125), width=290, text=f"Sample", font=QUESTION_FONT,
                                                           fill=THEME_COLOR)

        # ~~~~~~~~~~ True and False Buttons ~~~~~~~~~~
        true_img = PhotoImage(file="images/true.png")
        self.b_true = Button(image=true_img, highlightthickness=0,
                             bg=THEME_COLOR, command=self.true_pressed)
        self.b_true.grid(row=3, column=0, padx=15, pady=15)

        false_img = PhotoImage(file="images/false.png")
        self.b_false = Button(image=false_img, highlightthickness=0,
                              bg=THEME_COLOR, command=self.false_pressed)
        self.b_false.grid(row=3, column=1, padx=15, pady=15)

        self.get_next_question()

        self.window.mainloop()

    def true_pressed(self):
        """A function that registers True has been pressed."""
        self.give_feedback(self.quiz.check_answer("true", self.quiz.current_question.answer))

    def false_pressed(self):
        """A function that registers False has been pressed."""
        self.give_feedback(self.quiz.check_answer("false", self.quiz.current_question.answer))

    def give_feedback(self, is_correct):
        """A function that gives feedback based on the answer."""
        if is_correct:
            self.question_gui.config(bg=GREEN)
        else:
            self.question_gui.config(bg=RED)
        self.is_end()
        self.window.after(500, self.get_next_question)

    def get_next_question(self):
        """A function that gets the next question."""
        self.question_gui.config(bg=WHITE)
        question = self.quiz.next_question()
        self.question_gui.itemconfig(self.question_text, text=question)
        self.change_score()

    def change_score(self):
        """A function that changes the score."""
        self.score_label.config(text=f"Score: {self.quiz.score}")
        self.mistakes_left = self.quiz.allowed_mistakes - self.quiz.mistakes
        self.mistakes_label.config(text=f"Mistakes Left: {self.mistakes_left}")

    def is_end(self):
        """A function that checks if it is the end of the game."""
        answer = self.quiz.is_end()
        if not answer:
            pass
        else:
            self.show_end_screen(answer)

    def show_end_screen(self, state):
        """A function that shows the end screen."""
        if state == "Ran Out of Mistakes":
            try_again = tkinter.messagebox.askyesno(title="Sorry.",
                                                    message="You've ran out of guesses. "
                                                            f"Your final score is {self.quiz.score}/10. "
                                                            "Would you like to try again?")
        else:
            try_again = tkinter.messagebox.askyesno(title=f"Congrats!",
                                                    message="You've finished all of the questions. "
                                                            f"Your final score is {self.quiz.score}/10. "
                                                            "Would you like to try again?")
        if try_again:
            self.clear_screen()
            self.get_difficulty()
        else:
            self.clear_screen()
            self.window.quit()
            self.window.destroy()
