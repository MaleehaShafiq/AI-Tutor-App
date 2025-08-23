# 🎓 My Personalized AI Learning Tutor

![Image](https://github.com/user-attachments/assets/0753fdb7-9e27-4f06-b7e2-5d69b1fbc4fb)

Welcome! I'm excited to share my AI Learning Tutor, a project I built to explore the power of generative AI in creating adaptive and personalized educational experiences.

Instead of a one-size-fits-all approach, this app figures out what you know about a topic and then builds a custom learning plan just for you.

**👉 Try the live app here:** [**https://my-learning-tutor.streamlit.app/**](https://my-learning-tutor.streamlit.app/) <!-- IMPORTANT: Replace with your actual app URL! -->

---

## ✨ What does it do?

I designed the tutor to follow a logical, multi-step process that feels like a real conversation with a helpful guide:

1.  **It Starts by Asking Questions:** You tell the tutor what you want to learn, and it generates a quick diagnostic quiz to see where you're at.
2.  **You Get Honest Feedback:** Based on your answers, the AI evaluates your knowledge level—Beginner, Intermediate, or Advanced—and gives you constructive feedback.
3.  **A Custom Learning Plan is Born:** This is the core feature. The app creates a step-by-step learning plan with modules tailored specifically to your level.
4.  **It Finds Real-World Resources:** I didn't want the tutor to just give concepts; I wanted it to provide real help. So, I integrated a search tool that automatically finds and provides relevant links for each learning module.
5.  **Test Your Knowledge:** As you learn, you can click the "Quiz Me!" button on any module to get a fresh, 3-question MCQ to check your understanding and track your score.

---

## 🤖 Behind the Scenes: How the "Magic" Works

So, how does it seem so smart? The app's intelligence comes from **Google's Gemini LLM**, which acts as the expert "brain." My Python code's job is to be the "manager" that directs the conversation.

The whole process is an example of a simple AI agent. It follows a loop:
- It **perceives** the user's input (the topic and answers).
- It **thinks** by sending that information to the Gemini model with carefully crafted instructions (prompts) to make a decision or a plan.
- It **acts** by displaying the results (the evaluation, the learning plan, the quizzes) back to the user.

A key feature I'm proud of is the use of **Pydantic Parsers** from LangChain. This was a solution to a real-world problem I faced during development where the AI's output wasn't consistent. The parser forces the AI to provide a perfectly structured quiz every time, making the app much more reliable.

---

## 🛠️ My Tech Stack

I chose these technologies to build the app quickly and efficiently:

- **Frontend:** **Streamlit** - I used this because it's an amazing framework that let me build a beautiful and interactive UI right in Python.
- **AI "Plumbing":** **LangChain** - This was crucial for connecting all the different parts, from structuring the prompts to managing the AI's output.
- **The "Brain":** **Google Gemini API** - The powerful Large Language Model that provides the core intelligence.
- **Web Search Tool:** **Tavily API** - I integrated this to give the agent the ability to find live, up-to-date resources.
- **Deployment:** **Streamlit Community Cloud** - For hosting the app for free.

---

## 💡 What I'm Thinking of Adding Next

This project was a huge learning experience, and I have a few ideas for where to take it next:
- **More Learning Styles:** Letting the user ask for explanations with analogies or code examples.
- **Socratic Tutoring:** Instead of just giving quiz feedback, having the AI ask leading questions to help the user figure out the answer on their own.

Thanks for checking out my project!
