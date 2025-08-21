# ==============================================================================
#                      Personalized AI Learning Tutor
# ==============================================================================
# Filename: tutor_app.py
# Final Version with Interactive Quizzes and Improved UI
# ==============================================================================

import streamlit as st
import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Personalized AI Learning Tutor",
    page_icon="🎓",
    layout="wide"
)

# --- 2. API KEY SETUP ---
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
except FileNotFoundError:
    st.error("Secrets file not found. For local development, please create a .streamlit/secrets.toml file.")
    st.info("The secrets.toml file should contain your GOOGLE_API_KEY and TAVILY_API_KEY.")
    st.stop()

# --- 3. AI & TOOL INITIALIZATION ---
@st.cache_resource
def get_llm():
    """Initializes and returns the Gemini LLM instance."""
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

@st.cache_resource
def get_search_tool():
    """Initializes and returns the Tavily Search tool instance."""
    return TavilySearchResults(max_results=3)

llm = get_llm()
search_tool = get_search_tool()

# --- 4. CORE LOGIC FUNCTIONS ---
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
    """Generates a short quiz for a specific learning module."""
    quiz_prompt = ChatPromptTemplate.from_template(
        """
        You are an AI Learning Tutor. Create a short, 2-question quiz to test understanding of a learning module.
        The module is: Title: {module_title} ; Description: {module_description}
        Generate two questions: 1. A multiple-choice question. 2. A short-answer question. Format the output clearly.
        """
    )
    quiz_chain = quiz_prompt | llm | StrOutputParser()
    return quiz_chain.invoke({"module_title": module_title, "module_description": module_description})


# ==============================================================================
# --- 5. STREAMLIT APP LAYOUT AND LOGIC ---
# ==============================================================================
st.title("🎓 Personalized AI Learning Tutor")
st.markdown("Welcome! I'm here to help you master any topic. Let's start by figuring out what you already know.")

# --- SIDEBAR ---
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

# --- Initialize session state ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'topic_submission'

# --- STAGE 1: Get Topic ---
if st.session_state.stage == 'topic_submission':
    topic_input = st.text_input("What topic would you like to learn about today?", key="topic_input")
    if st.button("Start Assessment"):
        if topic_input:
            st.session_state.topic = topic_input
            with st.spinner("Generating your personalized assessment..."):
                st.session_state.questions = generate_initial_assessment(st.session_state.topic)
            st.session_state.stage = 'assessment_answering'
            st.rerun()
        else:
            st.warning("Please enter a topic to begin.")

# --- STAGE 2: Get Answers ---
if st.session_state.stage == 'assessment_answering':
    st.subheader(f"Assessment for: {st.session_state.topic}")
    st.markdown(st.session_state.questions)
    user_answers = st.text_area("Please enter your answers here:", height=200, key="answers_input")
    if st.button("Submit Answers"):
        if user_answers:
            with st.spinner("Evaluating your answers... This may take a moment."):
                st.session_state.evaluation = evaluate_answers(st.session_state.questions, user_answers)
            st.session_state.stage = 'plan_display'
            st.rerun()
        else:
            st.warning("Please provide your answers before submitting.")

# --- STAGE 3: Display Plan & Interactive Quizzes ---
if st.session_state.stage == 'plan_display':
    st.subheader("Here is your evaluation:")

    try:
        feedback_text = st.session_state.evaluation.split("Knowledge Level")[0]
        with st.expander("Click to see detailed feedback on your answers"):
            st.markdown(feedback_text)
        
        last_line = st.session_state.evaluation.strip().split('\n')[-1]
        knowledge_level = last_line.split(':')[-1].strip()
        st.success(f"Based on your answers, your knowledge level is: **{knowledge_level}**")
        
        # This check prevents re-generating the plan on every button click
        if 'plan' not in st.session_state:
             with st.spinner("Creating your personalized learning plan with resources..."):
                st.session_state.plan = generate_learning_plan(st.session_state.topic, knowledge_level)

        st.subheader("Here is your Personalized Learning Plan!")
        
        modules = st.session_state.plan.strip().split('Module: ')[1:]
        for i, module_text in enumerate(modules):
            title_match = re.search(r"(.*?)\n", module_text)
            desc_match = re.search(r"Description: (.*?)\n", module_text)
            query_match = re.search(r"Search Query: (.*)", module_text, re.DOTALL)

            if title_match and desc_match and query_match:
                title = title_match.group(1).strip()
                description = desc_match.group(1).strip()
                query = query_match.group(1).strip()

                with st.container(border=True):
                    st.markdown(f"#### Module {i+1}: {title}")
                    st.markdown(f"**Description:** {description}")
                    
                    search_results = search_tool.invoke(query)
                    
                    st.markdown("**Recommended Resources:**")
                    if isinstance(search_results, list) and len(search_results) > 0:
                        for result in search_results:
                            if isinstance(result, dict) and 'title' in result and 'url' in result:
                                st.markdown(f"- [{result['title']}]({result['url']})")
                    else:
                        st.markdown("No online resources found for this module.")

                    st.divider()
                    if st.button(f"Quiz me on Module {i+1}", key=f"quiz_btn_{i}"):
                        with st.spinner(f"Generating a quiz for {title}..."):
                            quiz_questions = generate_module_quiz(title, description)
                            st.session_state[f'quiz_for_module_{i}'] = quiz_questions
                    
                    if f'quiz_for_module_{i}' in st.session_state:
                        st.markdown("---")
                        st.write(st.session_state[f'quiz_for_module_{i}'])

    except Exception as e:
        st.error(f"An error occurred while generating your plan. Please try again. Error: {e}")



