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
from pydantic import BaseModel, Field
from typing import List
from langchain.output_parsers import PydanticOutputParser




# --- Custom CSS for Styling ---
st.markdown("""
<style>
    /* Center the title */
    .st-emotion-cache-10trblm {
        text-align: center;
    }
    
    /* Style for the user's answers (green) */
    .user-answer {
        background-color: #2F4F4F; /* Dark Slate Gray - a nice dark green */
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #3E5F5F;
    }
    
    /* Style for the tutor's responses (blue) */
    .tutor-response {
        background-color: #2C3E50; /* Dark Slate Blue */
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #3A506B;
    }
    
    /* Simple popping/jumping animation */
    @keyframes pop-in {
        0% { transform: scale(0.9); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    .pop-in-animation {
        animation: pop-in 0.5s ease-out forwards;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Personalized AI Learning Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded" # Keep the sidebar open by default
)

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

# --- Pydantic Models for Structured Output ---
class QuizQuestion(BaseModel):
    question_text: str = Field(description="The text of the multiple-choice question.")
    options: List[str] = Field(description="A list of exactly four options for the question.")
    correct_answer: str = Field(description="The letter (a, b, c, or d) corresponding to the correct option.")

class Quiz(BaseModel):
    questions: List[QuizQuestion] = Field(description="A list of exactly three multiple-choice questions.")

quiz_parser = PydanticOutputParser(pydantic_object=Quiz)

# --- 4. CORE LOGIC FUNCTIONS ---
def generate_initial_assessment(topic):
    assessment_prompt = ChatPromptTemplate.from_template("Generate a 3-question diagnostic quiz for '{topic}'.")
    assessment_chain = assessment_prompt | llm | StrOutputParser()
    return assessment_chain.invoke({"topic": topic})

def evaluate_answers(questions, answers):
    evaluation_prompt = ChatPromptTemplate.from_template(
        "You are an expert AI Tutor. Evaluate these answers: {answers} for these questions: {questions}. Determine the user's level as [Beginner, Intermediate, Advanced]. Format with 'Feedback' and 'Knowledge Level' sections."
    )
    evaluation_chain = evaluation_prompt | llm | StrOutputParser()
    return evaluation_chain.invoke({"questions": questions, "answers": answers})

def generate_learning_plan(topic, knowledge_level):
    plan_prompt = ChatPromptTemplate.from_template(
        "Create a 3-module learning plan for a {knowledge_level} user on the topic of {topic}. For each module, provide a 'Module' title, 'Description', and a 'Search Query'."
    )
    plan_chain = plan_prompt | llm | StrOutputParser()
    return plan_chain.invoke({"topic": topic, "knowledge_level": knowledge_level})

def generate_module_quiz(module_title, module_description):
    quiz_prompt = ChatPromptTemplate.from_template(
        """
        Create a quiz with exactly 3 multiple-choice questions for the module: '{module_title}' - {module_description}.
        Each question must have four options.
        {format_instructions}
        """,
        partial_variables={"format_instructions": quiz_parser.get_format_instructions()}
    )
    quiz_chain = quiz_prompt | llm | quiz_parser
    return quiz_chain.invoke({"module_title": module_title, "module_description": module_description})

# ==============================================================================
# --- 5. STREAMLIT APP LAYOUT AND LOGIC (FINAL VERSION) ---
# ==============================================================================
st.title("🎓 Personalized AI Learning Tutor")
st.markdown("Welcome! I'm here to help you master any topic. Let's start by figuring out what you already know.")

with st.sidebar:
    st.header("About")
    st.markdown("""
    This is a personalized AI Learning Tutor built with Google Gemini, LangChain, and Streamlit.
    It assesses your knowledge and creates a tailored learning plan with resources and quizzes.
    """)
    st.divider()
    if st.button("Start a New Topic"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state.stage = 'topic_submission'
        st.rerun()

if 'stage' not in st.session_state:
    st.session_state.stage = 'topic_submission'

if st.session_state.stage == 'topic_submission':
    topic_input = st.text_input("What topic would you like to learn about today?", key="topic_input")
    if st.button("Start Assessment"):
        if topic_input:
            st.session_state.topic = topic_input
            with st.spinner("Asking the AI expert to write your assessment..."):
                st.session_state.questions = generate_initial_assessment(st.session_state.topic)
            st.session_state.stage = 'assessment_answering'
            st.rerun()

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

# --- STAGE 3: Display Plan & Interactive Quizzes (STYLED VERSION) ---
if st.session_state.stage == 'plan_display':
    
    # --- Tutor's Evaluation in a Blue Box ---
    with st.container():
        st.markdown('<div class="tutor-response pop-in-animation">', unsafe_allow_html=True)
        st.subheader("Here is your evaluation:")
        
        try:
            feedback_text = st.session_state.evaluation.split("Knowledge Level")[0]
            with st.expander("Click to see detailed feedback on your answers"):
                st.markdown(feedback_text)
            
            last_line = st.session_state.evaluation.strip().split('\n')[-1]
            knowledge_level = "Beginner" 
# Search for the correct line in the evaluation text
for line in st.session_state.evaluation.strip().split('\n'):
    if line.startswith("Knowledge Level:"):
        knowledge_level = line.split(':')[-1].strip()
        break # Stop searching once we've found it
        except Exception as e:
             st.error("Could not parse evaluation.")
        st.markdown('</div>', unsafe_allow_html=True)


    # --- Learning Plan Generation ---
    try:
        if 'plan' not in st.session_state:
             with st.spinner("Designing your personalized learning plan..."):
                st.session_state.plan = generate_learning_plan(st.session_state.topic, knowledge_level)
        
        st.subheader("Here is your Personalized Learning Plan!")
        
        modules = st.session_state.plan.strip().split('Module: ')[1:]
        for i, module_text in enumerate(modules):
            # ... (Parsing logic remains the same)
            title_match, desc_match, query_match = re.search(r"(.*?)\n", module_text), re.search(r"Description: (.*?)\n", module_text), re.search(r"Search Query: (.*)", module_text, re.DOTALL)
            
            if title_match and desc_match and query_match:
                title, description, query = title_match.group(1).strip(), desc_match.group(1).strip(), query_match.group(1).strip()

                with st.container(border=True):
                    # ... (Display Module title, desc, resources) ...
                    st.markdown(f"#### Module {i+1}: {title}")
                    st.markdown(f"**Description:** {description}")
                    # ...

                    st.divider()
                    if st.button(f"Quiz me on Module {i+1}", key=f"quiz_btn_{i}"):
                        with st.spinner(f"Generating a quiz for {title}..."):
                            st.session_state[f'quiz_for_module_{i}'] = generate_module_quiz(title, description)
                    
                    if f'quiz_for_module_{i}' in st.session_state:
                        # ... (Quiz form logic remains the same) ...
                        with st.form(key=f'quiz_form_{i}'):
                            # ...
                            submitted = st.form_submit_button("Submit Quiz")
                            if submitted:
                                # ... (Quiz submission logic) ...
                                st.rerun()

                # --- Quiz Results in a Green Box ---
                if f'quiz_feedback_for_module_{i}' in st.session_state:
                    with st.container():
                        st.markdown('<div class="user-answer pop-in-animation">', unsafe_allow_html=True)
                        st.markdown(st.session_state[f'quiz_feedback_for_module_{i}'])
                        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred. Please try again. Error: {e}")


