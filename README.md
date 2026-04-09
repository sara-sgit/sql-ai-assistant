# 🧠 SQL Learning Assistant

An AI-powered assistant that turns your plain English questions into SQL 
queries and explains them so you actually learn. [ Learn by doing]

---

## 💡 Why this project?

Writing SQL from scratch is intimidating for beginners. This tool lets you
ask questions in plain English, automatically generates the correct SQL query,
runs it against a real database, and explains what each part of the query does.

You don't just get an answer — you understand how to get it yourself next time.

---

## ✨ Features

- Ask questions in plain English (no SQL knowledge needed to start)
- Automatically generates the SQL query for your question
- Runs the query against a real SQLite sample database
- Explains the query in simple beginner-friendly language
- Helps you learn SQL gradually through real examples

## 🚀 How to Run Locally

1. Clone the repository
   git clone https://github.com/sara-sgit/sql-ai-assistant
   cd sql-ai-assistant

2. Install dependencies
   pip install -r requirements.txt

3. Set up your environment variables
   Copy .env.example to .env and add your Groq API key
   GROQ_API_KEY=your-groq-api-key-here

4. Run the app
   streamlit run app.py




