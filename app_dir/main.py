# main.py (or your main application file)
from questions import get_questions
from quiz_logic import check_answer
from ui import create_interface

if __name__ == "__main__":
    questions = get_questions()
    interface = create_interface(questions)
    interface.launch()