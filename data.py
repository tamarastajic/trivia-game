import requests


# --------------------------- Functions for Different Difficulties ---------------------------
def get_easy():
    """A function that gets and returns easy questions."""
    response = requests.get("https://opentdb.com/api.php?amount=10&difficulty=easy&type=boolean")
    response.raise_for_status()
    data = response.json()["results"]
    question_data_easy = data
    return question_data_easy


def get_medium():
    """A function that gets and returns medium difficulty questions."""
    response = requests.get("https://opentdb.com/api.php?amount=10&difficulty=medium&type=boolean")
    response.raise_for_status()
    data = response.json()["results"]
    question_data_medium = data
    return question_data_medium


def get_hard():
    """A function that gets and returns hard questions."""
    response = requests.get("https://opentdb.com/api.php?amount=10&difficulty=hard&type=boolean")
    response.raise_for_status()
    data = response.json()["results"]
    question_data_hard = data
    return question_data_hard
