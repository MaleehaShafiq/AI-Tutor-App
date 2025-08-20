# ==============================================================================
#                      Personalized AI Learning Tutor
# ==============================================================================
# Filename: tutor_app.py
#
# Instructions:
# 1. Save this code in a file named `tutor_app.py`.
# 2. Create a `requirements.txt` file with the necessary libraries.
# 3. Create a `.streamlit/secrets.toml` file for your API keys.
# 4. Run from your terminal: `streamlit run tutor_app.py`
# ==============================================================================

import streamlit as st
import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
# NOTE: The new, recommended way to import Tavily for web searches
from langchain_community.tools.tavily_search import TavilySearchResults

# --- 1. PAGE CONFIGURATION ---
# Set the page title, icon, and layout for a professional look.
st.set_page_config(
    page_title="Personalized AI Learning Tutor",
    page_icon="🎓",
    layout="wide"
)

# --- 2. API KEY SETUP ---
# For Streamlit deployment, we use `st.secrets` to securely manage API keys.
# This prevents you from ever hardcoding secrets in your script.
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
except FileNotFoundError:
    st.error("Secrets file not found. For local development, please create a .streamlit/secrets.toml file.")
    st.info("The secrets.toml file should contain your GOOGLE_API_KEY and TAVILY_API_KEY.")
    st.stop()


# --- 3. AI & TOOL INITIALIZATION ---
# Using `@st.cache_resource` is a Streamlit best practice. It ensures that these
# heavyweight objects (the LLM and the search tool) are created only once per
# session, which significantly improves performance.
@st.cache_resource
def get_llm():
    """Initializes and returns the Gemini LLM instance."""
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

@st.cache_resource
def get_search_tool():
    return TavilySearchResults(max_results=3)

# Initialize the resources for the app
llm = get_llm()
search_tool = get_search_tool()

# --- 4. CORE LOGIC FUNCTIONS ---
# These functions encapsulate the AI's "thinking" process.

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
        Quiz Questions:
        ---
        {questions}
        ---
        User's Answers:
        ---
        {answers}
        ---
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
        Topic: {topic}
        User's Assessed Level: {knowledge_level}

        Create a step-by-step learning plan with 3 concise modules.
        For each module, provide three things:
        1. A clear "Module" title (e.g., "Module 1: The Core Intuition").
        2. A brief 1-sentence "Description" of the key concepts.
        3. A simple, effective "Search Query" to find resources for this module.

        **IMPORTANT**: Format each module exactly like this example, with no extra text:
        Module: [Module Title]
        Description: [Module Description]
        Search Query: [Effective Search Query]
        """
    )
    plan_chain = plan_prompt | llm | StrOutputParser()
    return plan_chain.invoke({"topic": topic, "knowledge_level": knowledge_level})


# --- 5. STREAMLIT APP LAYOUT AND LOGIC ---
st.title("🎓 Personalized AI Learning Tutor")
st.markdown("Welcome! I'm here to help you master any topic. Let's start by figuring out what you already know.")

# Initialize session state variables to manage the multi-step conversation flow.
# This is the "memory" of the app.
if 'stage' not in st.session_state:
    st.session_state.stage = 'topic_submission'

# --- STAGE 1: Get the Topic from the User ---
if st.session_state.stage == 'topic_submission':
    topic_input = st.text_input("What topic would you like to learn about today?", key="topic_input")
    if st.button("Start Assessment"):
        if topic_input:
            st.session_state.topic = topic_input
            with st.spinner("Generating your personalized assessment..."):
                st.session_state.questions = generate_initial_assessment(st.session_state.topic)
            st.session_state.stage = 'assessment_answering'
            st.rerun() # Rerun the script to move to the next stage
        else:
            st.warning("Please enter a topic to begin.")

# --- STAGE 2: Display Assessment and Get Answers ---
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

# --- STAGE 3: Display Evaluation and Generate/Display Plan with Resources ---
if st.session_state.stage == 'plan_display':
    st.subheader("Here is your evaluation:")
    st.markdown(st.session_state.evaluation)

    try:
        # This part is safe and can be in a try block
        last_line = st.session_state.evaluation.strip().split('\n')[-1]
        knowledge_level = last_line.split(':')[-1].strip()

        st.success(f"Based on your answers, your knowledge level is: **{knowledge_level}**")
        
        with st.spinner("Creating your personalized learning plan with resources..."):
            conceptual_plan = generate_learning_plan(st.session_state.topic, knowledge_level)

            st.subheader("Here is your Personalized Learning Plan!")
            
            modules = conceptual_plan.strip().split('Module: ')[1:]
            for module_text in modules:
                title_match = re.search(r"(.*?)\n", module_text)
                desc_match = re.search(r"Description: (.*?)\n", module_text)
                query_match = re.search(r"Search Query: (.*)", module_text, re.DOTALL)

                if title_match and desc_match and query_match:
                    title = title_match.group(1).strip()
                    description = desc_match.group(1).strip()
                    query = query_match.group(1).strip()

                    with st.container(border=True):
                        st.markdown(f"#### Module: {title}")
                        st.markdown(f"**Description:** {description}")
                        
                        # This search part is now safer
                        search_results = search_tool.invoke(query)
                        
                        st.markdown("**Recommended Resources:**")
                        if isinstance(search_results, list) and len(search_results) > 0:
                            for result in search_results[:3]: # Show top 3
                                if isinstance(result, dict) and 'title' in result and 'url' in result:
                                    st.markdown(f"- [{result['title']}]({result['url']})")
                                else:
                                    st.markdown(f"- {result}")
                        else:
                            st.markdown("No online resources found for this module.")

    except Exception as e:
        st.error(f"An error occurred while generating your plan. Please try again. Error: {e}")

    if st.button("Start a New Topic"):
        st.session_state.clear()
        st.session_state.stage = 'topic_submission'
        st.rerun()



