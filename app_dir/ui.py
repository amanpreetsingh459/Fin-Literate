# ui.py
def create_interface(questions):
    with gr.Blocks() as interface:
        question_index = gr.State(0)
        score = gr.State(0)

        gr.Markdown("## Multiple Choice Quiz")

        def display_question():
            return questions[question_index.value]["question"]

        def display_options():
            return questions[question_index.value]["options"]

        question_text = gr.Markdown(display_question())
        option_buttons = gr.Radio(display_options(), label="Options")
        check_button = gr.Button("Check Answer")
        result_text = gr.Markdown("")
        score_text = gr.Markdown(f"Score: {score.value}")

        def update_question(selected_option):
            nonlocal score
            result = check_answer(questions[question_index.value], selected_option)
            result_text.value = result
            if "Correct" in result:
                score.value += 1
            score_text.value = f"Score: {score.value}"
            question_index.value += 1
            if question_index.value < len(questions):
                question_text.value = display_question()
                option_buttons.choices = display_options()
            else:
                question_text.value = "Quiz completed!"
                option_buttons.visible = False
                check_button.visible = False

        check_button.click(update_question, inputs=[option_buttons], outputs=[result_text, question_text, option_buttons, check_button, score_text])

    return interface