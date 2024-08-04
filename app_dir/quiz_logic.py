# quiz_logic.py
def check_answer(question, selected_option):
    if question["options"][selected_option] == question["answer"]:
        return f"Correct! The answer is {question['answer']}"
    else:
        return f"Incorrect. The correct answer is {question['answer']}"
