# -*- coding: utf-8 -*-

"""### Import necessary packages"""

import pandas as pd
import random
import gradio as gr
import sys
import io

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

#print("---- Imports are done.")

## to convert the output to markdown format
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

## setup your Google API Key

#GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')
#genai.configure(api_key=GOOGLE_API_KEY)

api_key = "your-api-key"
genai.configure(api_key=api_key)

"""### Read the data from CSV files
- Use prompts 2-8 from prompts.txt file to generate synthetic data and put that in csv files
- Here we are referring data from the csv files which have been already created using 2-8 prompts
- This data could be captured from the user themselves as well
"""

path_to_data_files = "synthetic_dataset/"

fin_situation_file = path_to_data_files + "synthetic_financial_situation_data_2.csv"
fin_situation_df = pd.read_csv(fin_situation_file)

fin_goals_file = path_to_data_files + "synthetic_financial_goals_data.csv"
fin_goals_df = pd.read_csv(fin_goals_file)

risk_tolerance_file = path_to_data_files + "synthetic_risk_tolerance_data.csv"
risk_tolerance_df = pd.read_csv(risk_tolerance_file)

additional_questions_file = path_to_data_files + "synthetic_additional_questions_data.csv"
additional_questions_df = pd.read_csv(additional_questions_file)

open_ended_questions_file = path_to_data_files + "synthetic_open_ended_questions_data.csv"
open_ended_questions_df = pd.read_csv(open_ended_questions_file)

#print("---- Synthetic data pertaining the financial profiles of the imaginary individuals has read.")

"""### form all the variables with the data from dataframes"""

random_number = random.randint(0, 19)

# Financial Situation:
income = fin_situation_df.iloc[random_number]['Income']
expenses = fin_situation_df.iloc[random_number]['Expenses']
assets = fin_situation_df.iloc[random_number]['Assets']
liabilities = fin_situation_df.iloc[random_number]['Liabilities']
net_worth = fin_situation_df.iloc[random_number]['Net Worth']

# Financial Goals:
short_term_goals = fin_goals_df.iloc[random_number]['Short-term goals']
long_term_goals = fin_goals_df.iloc[random_number]['Long-term goals']
priorities = fin_goals_df.iloc[random_number]['Priorities']

# Risk Tolerance:
investment_experience = risk_tolerance_df.iloc[random_number]['Investment Experience']
comfort_level = risk_tolerance_df.iloc[random_number]['Comfort Level']
risk_capacity = risk_tolerance_df.iloc[random_number]['Risk Capacity']

# Additional Questions:
financial_challenges = additional_questions_df.iloc[random_number]['Financial Challenges']
financial_habits = additional_questions_df.iloc[random_number]['Financial Habits']
financial_values = additional_questions_df.iloc[random_number]['Financial Values']

# Open-ended questions:
open_ended_etc = open_ended_questions_df.iloc[random_number]['Etc']
open_ended_expectations = open_ended_questions_df.iloc[random_number]['Expectations_for_fin_coach']

system_prompt = """
                  You are a personal virtual financial coach. Your primary goal
                  is to help the users improve their financial well-being. To
                  do this, you'll:
                    1. Understand the user's Financial Profile with the help of
                       some information which will be provided by the user.
                    2. Provide Personalized Financial Guidance:
                        - Budgeting: Help me create a realistic budget, track spending, and
                          identify areas where I can cut back or save more. Offer suggestions
                          based on my individual needs and spending habits.
                        - Saving: Suggest strategies to increase my savings rate, such as
                          automatic transfers or setting specific savings goals. Recommend
                          appropriate savings accounts or other tools.
                        - Investing: Explain different investment options (stocks, bonds,
                          ETFs, etc.) based on my risk tolerance and financial goals. Offer
                          guidance on diversifying my portfolio and rebalancing as needed.
                        - Debt Management: Help me develop a plan to pay off debt, prioritize
                          which debts to tackle first, and consider strategies like debt
                          consolidation or refinancing.
                        - Other Financial Topics: Offer advice on taxes, insurance, retirement
                          planning, estate planning, and other relevant areas based on my
                          specific questions and needs.


                  Example Questions/Requests:
                      - "Help me create a budget that I can actually stick to."
                      - "What are some good investment options for me?"
                      - "How can I pay off my credit card debt faster?"
                      - "What should I know about saving for retirement?"
                      - "tell me a good ratio in which i should invest my amount in different products"
                      - "suggest me some ways so that i remain disciplined with my spendings"
                      - "should i be investing in sharemarket securities or keep money in savings account"
                      - "should i go for investing in mutual funds or in direct equity shares"
                      - "given the tax implications is it wise to buy property from an investment perspective"
                      - "is investing in NPS good for the retirement in india"

                  Please note: I understand that you are not a licensed financial advisor
                    and cannot provide specific financial advice. I will consult with a
                    qualified professional for any financial decisions.
                """

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-001",
    #model_name="gemini-1.5-flash",
    system_instruction=[
        system_prompt
    ],
)

#print("---- Model has initialized with the system prompt.")

financial_profile = f"""
          - Financial Situation:
              - Income: {income}
              - Expenses: {expenses}
              - Assets: {assets}
              - Liabilities: {liabilities}
              - Net Worth: {net_worth}
          - Financial Goals:
              - Short-term goals: {short_term_goals}
              - Long-term goals: {long_term_goals}
              - Priorities: {priorities}
          - Risk Tolerance:
              - Investment Experience: {investment_experience}
              - Comfort Level: {comfort_level}
              - Risk Capacity: {risk_capacity}
          - Additional Things:
              - Financial Challenges: {financial_challenges}
              - Financial Habits: {financial_habits}
              - Financial Values: {financial_values}
          - Open-ended Things:
              - {open_ended_etc}
              - {open_ended_expectations}
"""

def get_input_with_default(prompt, default):
    user_input = input(f"{prompt}")
    return user_input if user_input.strip() else default

#user_query = f"""Explain me in 4 points or less that should I go for investing in mutual funds or in direct equity shares?"""

default_query = f"""Explain me in 4 points or less that should I go for investing in mutual funds or in direct equity shares?"""
initial_message = f"""
Welcome to FinLiterate app. We appreciate your step towards enhancing your knowledge about finances. 

Input your query to address:-
- Any financial challenges you might have
- To get insights about your portfolio
- To get tailored financial advice
- To just have some fun and playing with the app.

Few example to start with:-
- Help me create a budget that I can actually stick to.
- What are some good investment options for me?
- How can I pay off my credit card debt faster?
- What should I know about saving for retirement?
- tell me a good ratio in which i should invest my amount in different products.
- suggest me some ways so that i remain disciplined with my spendings.
- should i be investing in sharemarket securities or keep money in savings account.
- should i go for investing in mutual funds or in direct equity shares.
- given the tax implications is it wise to buy property from an investment perspective.
- is investing in NPS good for the retirement in india.

With your provided details of financial profile we have tailored a query for you
 to address. If you don't wanna write on your own just hit and we will populate 
 the query for you and provide you the necessary information.

Tailored query for you: {default_query}
"""
print(initial_message)

user_query = get_input_with_default("Input your query(hit enter to input default)", default_query)
print(f"\nUser query: {user_query}!\nApp response goes below:--------\n\n")

submit_prompt = f"""
User input: Understand My Financial Profile with the below information which has
 been supplied by me and answer the query I ask after this:- {financial_profile}

Query: {user_query}
Answer:

"""


contents = [submit_prompt]
response_financial_profile = model.generate_content(contents)
print(response_financial_profile.text)


print("""
\n### Based on above suggestions we have designed a quiz for you to 
strengthen your financial skills. A further step towards being FinLiterate. 
\nClick the below public URL to access the same:-\n
""")


"""### Based on above suggestions below we have designed a quiz for you to strengthen your financial skills. A further step towards being FinLiterate."""

def get_questions_list():
  path_to_data_files = "synthetic_dataset/"
  qa_file = path_to_data_files + "financial_literacy_quiz.csv"
  qa_df = pd.read_csv(qa_file)
  questions_list = []
  for row in qa_df.itertuples():
    question = row.Question
    options = [row.optionA, row.optionB, row.optionC, row.optionD]
    if row.Answer == "A":
      answer = row.optionA
    elif row.Answer == "B":
      answer = row.optionB
    elif row.Answer == "C":
      answer = row.optionC
    elif row.Answer == "D":
      answer = row.optionD

    questions_list.append({
              "question": question,
              "options": options,
              "answer": answer
          })
  return questions_list

def quiz():
    questions = get_questions_list()

    def check_answer(question_index, selected_option):
        if selected_option == questions[question_index]["answer"]:
            return f"#### Correct! The answer is {questions[question_index]['answer']}"
        else:
            return f"#### Incorrect. The correct answer is {questions[question_index]['answer']}"


    with gr.Blocks() as interface:

        question_index = gr.State(0)
        score = gr.State(0)

        gr.Markdown("## Financial Literacy...")

        def display_question():
            return "#### " + questions[question_index.value]["question"]

        def display_options():
            return questions[question_index.value]["options"]

        question_text = gr.Markdown(display_question())
        #sys.stdout.write(f"\nquestion_text.value: {question_text.value}")

        option_buttons = gr.Radio(display_options(), label="Options")
        #sys.stdout.write(f"\noption_buttons.value: {option_buttons.value}")

        check_button = gr.Button("Check Answer")
        #sys.stdout.write(f"\ncheck_button.value: {check_button.value}")

        result_text = gr.Markdown("")
        #sys.stdout.write(f"\nresult_text.value: {result_text.value}")

        score_text = gr.Markdown(f"### Score: {score.value}")
        #sys.stdout.write(f"\nscore_text.value: {score_text.value}")


        def update_question(selected_option):

            #sys.stdout.write(f"Selected option index: {selected_option}")  # Print the selected option index
            #sys.stdout.write(f"\nCurrent question index: {question_index.value}")  # Print the current question index

            result = check_answer(question_index.value, selected_option)
            #sys.stdout.write(f"\nResult from check_answer: {result}")  # Print the result of answer checking

            result_text.value = result
            #sys.stdout.write(f"\nresult_text.value: {result_text.value}")
            if "Correct" in result:
                score.value += 1
            score_text.value = f"Score: {score.value}"
            question_index.value += 1

            #sys.stdout.write(f"\nUpdated question index: {question_index.value}")  # Print the updated question index
            #sys.stdout.write(f"\nscore_text.value: {score_text.value}")

            if question_index.value < len(questions):
              return(
                result,
                "#### " + questions[question_index.value]["question"],
                gr.update(choices=questions[question_index.value]["options"]),  # Update choices here
                check_button.value,
                "### " + score_text.value
              )
            else:
              question_index.value = 0
              return(
                  result,
                  "#### " + questions[question_index.value]["question"],
                  gr.update(choices=questions[question_index.value]["options"]),  # Update choices here
                  check_button.value,
                  "### " + score_text.value
              )

        check_button.click(update_question, inputs=[option_buttons], outputs=[result_text, question_text, option_buttons, check_button, score_text])

    interface.launch(share=True, show_error=True)

quiz()

