# 🧠 SQL Learning Assistant

An AI-powered chatbot that turns your plain English questions into SQL queries,
explains them, runs them, and shows the results  learn SQL by doing, not just reading.

---

## 💡 Why this project?

Most people learn SQL by watching videos or reading documentation.
This tool takes a different approach you ask a question in plain English, and the assistant:

1. Generates the correct SQL query
2. Explains what the query does in simple terms
3. Runs it on a real database and shows the results
4. Gives you a plain English answer

You don't just get an answer you understand how to get it yourself next time.

---

## 🛠️ Tech Stack

- **Python** — core language
- **Streamlit** — user interface
- **LangChain** — LLM chaining and prompt management
- **Groq API (LLaMA 3.1)** — SQL generation and explanation
- **SQLite** — sample online store database
- **Pandas** — query result handling

---

## ✨ Features

- Ask questions in plain English — no SQL knowledge needed to start
- Automatically generates the SQL query for your question
- Explains the query in simple beginner-friendly language
- Runs the query against a real database and displays the results
- Gives a short natural language answer to your question
- Chat history kept throughout the session

---

## 🗄️ About the Database

This app uses a small **online store database** with 4 tables:

- **customers** — customer information
- **products** — product catalog and prices
- **orders** — orders placed by customers
- **order_items** — products inside each order

Example questions you can ask:
- Which customers placed the most orders?
- What are the most expensive products?
- How many orders were placed per country?

---

## 🏗️ Architecture

![Architecture Diagram](https://raw.githubusercontent.com/sara-sgit/sql-ai-assistant/refs/heads/main/diagram.png)

---

## 🚀 How to Run Locally

1. Clone the repository
```bash
git clone https://github.com/sara-sgit/sql-ai-assistant
cd sql-ai-assistant
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up your environment variables
```bash
cp .env.example .env
```

4. Run the app
```bash
streamlit run app.py
```




