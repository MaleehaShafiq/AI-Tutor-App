# ==============================================================================
#                      Personalized AI Learning Tutor
# ==============================================================================
# Filename: tutor_app.py
# Final Version with Robust, Structured Output for Quizzes
# ==============================================================================

import streamlit as st
import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults

# --- NEW: Import Pydantic and Parser for robust, structured output ---
from pydantic import BaseModel, Field
from typing import List
from langchain.output_parsers import PydanticOutputParser


# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Personalized AI Learning Tutor", page_icon="🎓", layout="wide")


# --- 2. API KEY SETUP ---
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
except FileNotFoundError:
    st.error("Secrets file not found. For local development, please create a .streamlit/secrets.toml file.")
    st.stop()


# --- 3. AI & TOOL INITIALIZATION ---
@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

@st.cache_resource
def get_search_tool():
    return TavilySearchResults(max_results=3)

llm = get_llm()
search_tool = get_search_tool()


# --- NEW: Pydantic Models for Structured Output ---
class QuizQuestion(BaseModel):
    question_text: str = Field(description="The text of the multiple-choice question.")
    options: List[str] = Field(description="A list of exactly four options for the question.")
    correct_answer: str = Field(description="The letter (a, b, c, or d) of the correct option.")

class Quiz(BaseModel):
    questions: List[QuizQuestion] = Field(description="A list of exactly three multiple-choice questions.")

# --- Set up a parser for the quiz ---
quiz_parser = PydanticOutputParser(pydantic_object=Quiz)


# --- 4. CORE LOGIC FUNCTIONS ---
def generate_initial_assessment(topic):
    # ... (This function remains the same) ...
    assessment_prompt = ChatPromptTemplate.from_template("...")
    return assessment_chain.invoke({"topic": topic})

def evaluate_answers(questions, answers):
    # ... (This function remains the same) ...
    evaluation_prompt = ChatPromptTemplate.from_template("...")
    return evaluation_chain.invoke({"questions": questions, "answers": answers})

def generate_learning_plan(topic, knowledge_level):
    # ... (This function remains the same) ...
    plan_prompt = ChatPromptTemplate.from_template("...")
    return plan_chain.invoke({"topic": topic, "knowledge_level": knowledge_level})


# --- UPGRADED QUIZ GENERATOR USING STRUCTURED OUTPUT ---
def generate_module_quiz(module_title, module_description):
    """Generates a 3-MCQ quiz using a structured Pydantic parser for reliability."""
    quiz_prompt = ChatPromptTemplate.from_template(
        """
        You are an AI Learning Tutor. Create a quiz with exactly 3 multiple-choice questions for the learning module below.
        Module Title: {module_title}
        Module Description: {module_description}

        The questions should test the key concepts in the module description.
        Each question must have four options.

        {format_instructions}
        """,
        partial_variables={"format_instructions": quiz_parser.get_format_instructions()}
    )
    quiz_chain = quiz_prompt | llm | quiz_parser
    return quiz_chain.invoke({"module_title": module_title, "module_description": module_description})

# (The separate evaluate_quiz_answers function is no longer needed, as we can check the answers directly in Python)


# ==============================================================================
# --- 5. STREAMLIT APP LAYOUT AND LOGIC (FINAL VERSION) ---
# ==============================================================================
st.title("🎓 Personalized AI Learning Tutor")
st.markdown("Welcome! I'm here to help you master any topic. Let's start by figuring out what you already know.")

with st.sidebar:
    st.header("About")
    st.markdown("...") # About text here
    if st.button("Start a New Topic"):
        # ... (Reset logic) ...

if 'stage' not in st.session_state:
    st.session_state.stage = 'topic_submission'

# --- STAGE 1: Get Topic ---
if st.session_state.stage == 'topic_submission':
    topic_input = st.text_input("What topic would you like to learn about today?", key="topic_input")
    if st.button("Start Assessment"):
        if topic_input:
            st.session_state.topic = topic_input
            with st.spinner("Asking the AI expert to write your assessment... (This can take a few seconds)"):
                st.session_state.questions = generate_initial_assessment(st.session_state.topic)
            st.session_state.stage = 'assessment_answering'
            st.rerun()

# --- STAGE 2: Get Answers ---
if st.session_state.stage == 'assessment_answering':
    st.subheader(f"Assessment for: {st.session_state.topic}")
    st.markdown(st.session_state.questions)
    user_answers = st.text_area("Please enter your answers here:", height=200, key="answers_input")
    if st.button("Submit Answers"):
        if user_answers:
            with st.spinner("Evaluating your answers..."):
                st.session_state.evaluation = evaluate_answers(st.session_state.questions, user_answers)
            st.session_state.stage = 'plan_display'
            st.rerun()

# --- STAGE 3: Display Plan & Robust Quizzes ---
if st.session_state.stage == 'plan_display':
    st.subheader("Here is your evaluation:")
    
    try:
        feedback_text = st.session_state.evaluation.split("Knowledge Level")[0]
        with st.expander("Click to see detailed feedback"):
            st.markdown(feedback_text)
        
        knowledge_level = st.session_state.evaluation.strip().split('\n')[-1].split(':')[-1].strip()
        st.success(f"Based on your answers, your knowledge level is: **{knowledge_level}**")
        
        # ... (Total Score logic remains the same) ...
        
        if 'plan' not in st.session_state:
             with st.spinner("Designing your personalized learning plan..."):
                st.session_state.plan = generate_learning_plan(st.session_state.topic, knowledge_level)

        st.subheader("Here is your Personalized Learning Plan!")
        
        modules = st.session_state.plan.strip().split('Module: ')[1:]
        for i, module_text in enumerate(modules):
            # ... (Parsing logic for title, desc, query remains the same) ...

            with st.container(border=True):
                # ... (Display Module title, desc, resources) ...

                st.divider()
                if st.button(f"Quiz me on Module {i+1}", key=f"quiz_btn_{i}"):
                    with st.spinner(f"Generating a quiz for {title}... This is an AI-powered process and may take a moment."):
                        # The new function returns a structured Quiz object
                        quiz_object = generate_module_quiz(title, description)
                        st.session_state[f'quiz_for_module_{i}'] = quiz_object
                
                if f'quiz_for_module_{i}' in st.session_state:
                    quiz: Quiz = st.session_state[f'quiz_for_module_{i}']
                    
                    with st.form(key=f'quiz_form_{i}'):
                        user_answers = []
                        for q_idx, question in enumerate(quiz.questions):
                            st.markdown(f"**Question {q_idx+1}:** {question.question_text}")
                            # The options are now a reliable list from our object
                            user_choice = st.radio("Select an answer:", question.options, key=f"mc_{i}_{q_idx}", index=None, label_visibility="collapsed")
                            user_answers.append(user_choice)
                        
                        submitted = st.form_submit_button("Submit Quiz")

                        if submitted:
                            score = 0
                            feedback_list = ["**Quiz Results:**"]
                            for q_idx, question in enumerate(quiz.questions):
                                user_ans = user_answers[q_idx]
                                correct_ans_text = question.options[ord(question.correct_answer) - ord('a')]
                                
                                if user_ans == correct_ans_text:
                                    score += 1
                                    feedback_list.append(f"✅ **Question {q_idx+1}: Correct!**")
                                else:
                                    feedback_list.append(f"❌ **Question {q_idx+1}: Incorrect.** The correct answer was: **{correct_ans_text}**")
                            
                            st.session_state[f'quiz_feedback_for_module_{i}'] = "\n".join(feedback_list)
                            st.session_state[f'quiz_score_for_module_{i}'] = (score, 3)
                            st.rerun()

                if f'quiz_feedback_for_module_{i}' in st.session_state:
                    st.info(st.session_state[f'quiz_feedback_for_module_{i}'])

    except Exception as e:
        st.error(f"An error occurred. Please try again. Error: {e}")
