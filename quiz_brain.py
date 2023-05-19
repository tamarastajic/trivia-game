import html
from data import get_easy, get_medium, get_hard
from question_model import Question


# ~~~~~~~~~~~~~~~~~~~ QuizBrain Class ~~~~~~~~~~~~~~~~~~~
class QuizBrain:
    def __init__(self, mode):
        self.current_question = None
        self.question_number = 0
        self.score = 0
        self.mistakes = 0

        self.question_list = []

        # Branching out based on difficulty
        if mode == "easy":
            self.allowed_mistakes = 7
            self.question_data_easy = get_easy()
            for question in self.question_data_easy:
                self.question_list.append(Question(question["question"], question["correct_answer"]))
        elif mode == "medium":
            self.allowed_mistakes = 5
            self.question_data_medium = get_medium()
            for question in self.question_data_medium:
                self.question_list.append(Question(question["question"], question["correct_answer"]))
        else:
            self.allowed_mistakes = 2
            self.question_data_hard = get_hard()
            for question in self.question_data_hard:
                self.question_list.append(Question(question["question"], question["correct_answer"]))

    def still_has_questions(self):
        """A function that checks if there are still questions left."""
        return self.question_number < len(self.question_list)

    def next_question(self):
        """A function that gets and returns the next question."""
        self.current_question = self.question_list[self.question_number]
        # ~------------------------------~ Removes Odd HTML Entities ~------------------------------~
        self.current_question.text = html.unescape(self.current_question.text)

        self.question_number += 1
        return f"Q.{self.question_number}: {self.current_question.text}"

    def check_answer(self, u_answer, c_answer):
        """A function that checks if the answer was correct."""
        if u_answer.lower() == c_answer.lower():
            self.score += 1
            return True
        else:
            self.mistakes += 1
            return False

    def is_end(self):
        """A function that checks if it's the end of the game."""
        if self.mistakes == self.allowed_mistakes:
            return "Ran Out of Mistakes"
        elif self.question_number == len(self.question_list):
            return "Finished All Questions"
        else:
            return False
