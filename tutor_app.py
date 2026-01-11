# ==============================================================================
#                      Personalized AI Learning Tutor
# ==============================================================================
import streamlit as st
import os
import re
from typing import List
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults

from pydantic import BaseModel, Field
from typing import List
from langchain.output_parsers import PydanticOutputParser


# Custom CSS Styling
st.markdown("""
<style>
    h1 {
        text-align: center;
    }
    .tutor-response {
        background-color: #2C3E50;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #3A506B;
    }
    @keyframes pop-in {
        0% { transform: scale(0.95); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    .pop-in-animation {
        animation: pop-in 0.5s ease-out forwards;
    }
</style>
""", unsafe_allow_html=True)

# Page Configuration
st.set_page_config(page_title="Personalized AI Learning Tutor", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# API Key Setup
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
except (FileNotFoundError, KeyError):
    st.error("Secrets file not found or keys are missing. Please create a .streamlit/secrets.toml file for local development.")
    st.stop()

# llm and search tool initialization
@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

@st.cache_resource
def get_search_tool():
    return TavilySearchResults(max_results=3)

llm = get_llm()
search_tool = get_search_tool()

# Pydantic Model for Structured Output
class QuizQuestion(BaseModel):
    question_text: str = Field(description="The text of the multiple-choice question.")
    options: List[str] = Field(description="A list of exactly four options for the question.")
    correct_answer: str = Field(description="The letter (a, b, c, or d) corresponding to the correct option.")

class Quiz(BaseModel):
    questions: List[QuizQuestion] = Field(description="A list of exactly three multiple-choice questions.")

quiz_parser = PydanticOutputParser(pydantic_object=Quiz)

# Core Logic
def generate_initial_assessment(topic):
    """Generates a 3-question diagnostic quiz for a given topic."""
    assessment_prompt = ChatPromptTemplate.from_template(
        "You are a friendly AI Tutor. Generate a 3-question diagnostic quiz for the topic '{topic}', with questions ranging from easy to hard."
    )
    assessment_chain = assessment_prompt | llm | StrOutputParser()
    return assessment_chain.invoke({"topic": topic})

def evaluate_answers(questions, answers):
    """Evaluates user's answers and determines their knowledge level."""
    evaluation_prompt = ChatPromptTemplate.from_template(
        """
        You are an expert AI Tutor. Evaluate the user's answers to the following quiz.
        Quiz Questions: --- {questions} --- ; User's Answers: --- {answers} ---
        Based on the answers, provide brief, constructive feedback. Acknowledge any skipped questions.
        Then, determine the user's overall knowledge level as one of these exact three options: [Beginner, Intermediate, Advanced].
        Structure your output with a "Feedback" section and end with a "Knowledge Level" section.
        """
    )
    evaluation_chain = evaluation_prompt | llm | StrOutputParser()
    return evaluation_chain.invoke({"questions": questions, "answers": answers})

def generate_learning_plan(topic, knowledge_level):
    """Generates a personalized learning plan with searchable queries."""
    plan_prompt = ChatPromptTemplate.from_template(
        """
        You are an AI curriculum designer. Create a personalized learning plan for a user.
        Topic: {topic} ; User's Assessed Level: {knowledge_level}
        Create a step-by-step learning plan with 3 concise modules.
        For each module, provide: A clear "Module" title, a brief 1-sentence "Description", and a simple "Search Query".
        Format each module exactly like this:
        Module: [Module Title]\nDescription: [Module Description]\nSearch Query: [Effective Search Query]
        """
    )
    plan_chain = plan_prompt | llm | StrOutputParser()
    return plan_chain.invoke({"topic": topic, "knowledge_level": knowledge_level})

def generate_module_quiz(module_title, module_description):
    """Generates a 3-MCQ quiz using a structured Pydantic parser for reliability."""
    quiz_prompt = ChatPromptTemplate.from_template(
        """
        You are an AI Tutor. Create a quiz with exactly 3 multiple-choice questions for the learning module below.
        Module Title: {module_title}
        Module Description: {module_description}

        **RULES:**
        1.  Create exactly 3 multiple-choice questions.
        2.  Each question MUST have four options.
        3.  The questions must be relevant to the module's topic.

        {format_instructions}
        """,
        partial_variables={"format_instructions": quiz_parser.get_format_instructions()}
    )
    return (quiz_prompt | llm | quiz_parser).invoke({"module_title": module_title, "module_description": module_description})
    

# ==============================================================================
#                      Streamlit App logic and Layout
# ==============================================================================
st.title("🎓 Personalized AI Learning Tutor")
st.markdown("Welcome! I'm here to help you master any topic. Let's start by figuring out what you already know.")

with st.sidebar:
    st.header("About")
    st.markdown("This is a personalized AI Learning Tutor built with Google Gemini, LangChain, and Streamlit.")
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

if st.session_state.stage == 'plan_display':
    st.subheader("Here is your evaluation:")
    try:
        feedback_text = st.session_state.evaluation.split("Knowledge Level")[0]
        with st.expander("Click to see detailed feedback"):
            st.markdown(feedback_text)
        
        knowledge_level = "Beginner"
        for line in st.session_state.evaluation.strip().split('\n'):
            if line.startswith("Knowledge Level:"):
                knowledge_level = line.split(':')[-1].strip()
                break
        st.success(f"Based on your answers, your knowledge level is: **{knowledge_level}**")

        total_score, total_possible = 0, 0
        for i in range(3):
            if f'quiz_score_for_module_{i}' in st.session_state:
                score, possible = st.session_state[f'quiz_score_for_module_{i}']
                total_score += score
                total_possible += possible
        if total_possible > 0:
            st.metric(label="Your Total Score", value=f"{total_score} / {total_possible}")

        if 'plan' not in st.session_state:
             with st.spinner("Designing your personalized learning plan..."):
                st.session_state.plan = generate_learning_plan(st.session_state.topic, knowledge_level)

        st.subheader("Here is your Personalized Learning Plan!")
        
        modules = st.session_state.plan.strip().split('Module: ')[1:]
        for i, module_text in enumerate(modules):
            title_match = re.search(r"(.*?)\n", module_text)
            desc_match = re.search(r"Description: (.*?)\n", module_text)
            query_match = re.search(r"Search Query: (.*)", module_text, re.DOTALL)
            
            if title_match and desc_match and query_match:
                title, description, query = title_match.group(1).strip(), desc_match.group(1).strip(), query_match.group(1).strip()
                
                with st.container(border=True):
                    st.markdown(f"#### Module {i+1}: {title}")
                    st.markdown(f"**Description:** {description}")
                    
                    st.markdown("**Recommended Resources:**")
                    search_results = search_tool.invoke(query)
                    if isinstance(search_results, list) and len(search_results) > 0:
                        for result in search_results:
                            if isinstance(result, dict) and 'title' in result and 'url' in result:
                                st.markdown(f"- [{result['title']}]({result['url']})")
                    else:
                        st.markdown("No online resources found.")

                    st.divider()
                    if st.button(f"Quiz me on Module {i+1}", key=f"quiz_btn_{i}"):
                        with st.spinner(f"Generating a quiz for {title}..."):
                            quiz_object = generate_module_quiz(title, description)
                            st.session_state[f'quiz_for_module_{i}'] = quiz_object
                    
                    if f'quiz_for_module_{i}' in st.session_state:
                        quiz: Quiz = st.session_state[f'quiz_for_module_{i}']
                        
                        with st.form(key=f'quiz_form_{i}'):
                            user_answers = []
                            for q_idx, question in enumerate(quiz.questions):
                                st.markdown(f"**Question {q_idx+1}:** {question.question_text}")
                                user_choice = st.radio("Select an answer:", question.options, key=f"mc_{i}_{q_idx}", index=None, label_visibility="collapsed")
                                user_answers.append(user_choice)
                            
                            submitted = st.form_submit_button("Submit Quiz")

                            if submitted:
                                score = 0
                                feedback_list = ["**Quiz Results:**"]
                                for q_idx, question in enumerate(quiz.questions):
                                    user_ans = user_answers[q_idx]
                                    correct_ans_index = ord(question.correct_answer.lower()) - ord('a')
                                    correct_ans_text = question.options[correct_ans_index]
                                    
                                    if user_ans == correct_ans_text:
                                        score += 1
                                        feedback_list.append(f"✅ **Question {q_idx+1}: Correct!**")
                                    else:
                                        feedback_list.append(f"❌ **Question {q_idx+1}: Incorrect.** The correct answer was: **'{correct_ans_text}'**")
                                
                                st.session_state[f'quiz_feedback_for_module_{i}'] = "\n\n".join(feedback_list)
                                st.session_state[f'quiz_score_for_module_{i}'] = (score, 3)
                                st.rerun()

                    if f'quiz_feedback_for_module_{i}' in st.session_state:
                        st.info(st.session_state[f'quiz_feedback_for_module_{i}'])

    except Exception as e:
        st.error(f"An error occurred during the planning stage. Please try again. Error: {e}")
# =================================================================================================================================================================

