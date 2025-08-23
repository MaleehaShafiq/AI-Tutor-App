# 🎓 My Personalized AI Learning Tutor

![Image](https://github.com/user-attachments/assets/0753fdb7-9e27-4f06-b7e2-5d69b1fbc4fb)

Welcome! I'm excited to share my AI Learning Tutor, a project I built to explore the power of generative AI in creating adaptive and personalized educational experiences.

Instead of a one-size-fits-all approach, this app figures out what you know about a topic and then builds a custom learning plan just for you.

**👉 Try the live app here:** [**https://my-learning-tutor.streamlit.app/**](https://my-learning-tutor.streamlit.app/) 

### 🛠️ Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-100000?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgdmlld0JveD0iMCAwIDI1NiAyNTYiPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yMTguNTQgNzguNTNsLTMxLjA3IDMxLjA3bDMyLjgzIDMyLjgzYTEyIDEyIDAgMCAxIDAgMTYuOTdsLTQuMjQgNC4yNGExMiAxMiAwIDAgMS0xNi45NyAwTDExNi43IDEyMS4zbC0xMS4zMi0xMS4zMWE4IDggMCAwIDAtMTEuMzEgMGwtMTguMzggMTguMzhhOCA4IDAgMCAwIDAgMTEuMzFsMzYuNzggMzYuNzhhOCA4IDAgMCAwIDExLjMxIDBsMTguMzgtMTguMzhhOCA4IDAgMCAwIDAgMTEuMzFsLTExLjMyIDExLjMybDQxLjQgNDEuNGExMiAxMiAwIDAgMCAxNi45NyAwbDQuMjQtNC4yNGExMiAxMiAwIDAgMCAwLTE2Ljk3bC0zMi44My0zMi44M2wzMS4wNy0zMS4wN2ExMiAxMiAwIDAgMCAwLTE2Ljk3bC00LjI0LTQuMjRhMTIgMTIgMCAwIDAtMTYuOTcgMFptLTg0Ljg1IDM2Ljc4bDE4LjM4LTE4LjM4YTEyIDEyIDAgMCAwLTE2Ljk3LTE2Ljk3bC0zMS4wNyAzMS4wN2wtMzIuODMtMzIuODNhMTIgMTIgMCAwIDAtMTYuOTcgMGwtNC4yNCA0LjI0YTEyIDEyIDAgMCAwIDAgMTYuOTdsNDEuNCA0MS40bC0xMS4zMiAxMS4zMWExMiAxMiAwIDAgMC0zLjUyIDguNDljMCAzLjE4IDEuMjMgNi4yIDMuNTIgOC40OGwzNi43OCAzNi43OGExMiAxMiAwIDAgMCAxNi45NyAwbDQuMjQtNC4yNGExMiAxMiAwIDAgMCAwLTE2Ljk3bC0zMi4zMi0zMi4zM2wzMS4wNy0zMS4wN2ExMiAxMiAwIDAgMCAwLTE2Ljk3Wm0tMjUuNDYgNjIuMjJsMzYuNzggMzYuNzhhMTIgMTIgMCAwIDAgMTYuOTcgMGw0LjI0LTQuMjRhMTIgMTIgMCAwIDAgMC0xNi45N2wtMzIuODMtMzIuODNsMzEuMDctMzEuMDdhMTIgMTIgMCAwIDAgMC0xNi45N2wtNC4yNC00LjI0YTEyIDEyIDAgMCAwLTE2Ljk3IDBMMzcuNDYgMTQ2LjFsLTYuMjIgNi4yMmExMiAxMiAwIDAgMCAwIDE2Ljk3bDEzLjA5IDEzLjA5WiIvPjwvc3ZnPg==)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B9?style=for-the-badge&logo=google&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

---

## ✨ Key Features

-   🧠 **Dynamic Knowledge Assessment:** Starts with an AI-generated quiz to gauge the user's knowledge on any topic.
-   📊 **Intelligent Evaluation:** Provides constructive feedback and accurately classifies the user's knowledge level.
-   🚀 **Personalized Learning Plans:** Generates a custom, step-by-step curriculum tailored to the user's specific needs.
-   🔗 **Real-Time Web Resources:** Uses a search tool to find and provide relevant, live links for each learning module.
-   📝 **Interactive Quizzing:** Lets users test their comprehension with unique, on-demand quizzes for each module.

---

## 🤖 How it Works

The app acts as a simple AI agent. Here's the flow:

1.  **User Enters a Topic:** The journey begins.
2.  **AI Generates an Assessment:** The first AI call creates a quiz.
3.  **User Submits Answers:** The app perceives the user's input.
4.  **AI Evaluates and Assigns a Level:** The "brain" makes a judgment.
5.  **A Custom Plan is Generated:** Based on the level, a new plan is created.
6.  **The App Finds Resources & Offers Quizzes:** For each step in the plan, the app uses its tools to provide more value.

---

## 💡 What I Learned & Future Ideas

This project was a huge learning experience in prompt engineering and managing the reliability of LLM outputs. I solved a key challenge by using **Pydantic Parsers** to force the AI to return a perfectly structured quiz every time.

A few ideas for where to take this next:
- **More Learning Styles:** Letting the user ask for explanations with analogies or code examples.
- **Socratic Tutoring:** Having the AI ask leading questions instead of just giving quiz feedback.

Thanks for checking out my project!
- **More Learning Styles:** Letting the user ask for explanations with analogies or code examples.
- **Socratic Tutoring:** Instead of just giving quiz feedback, having the AI ask leading questions to help the user figure out the answer on their own.

Thanks for checking out my project!
