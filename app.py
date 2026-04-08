
import os
import streamlit as st
import pandas as pd

from langchain_community.utilities import SQLDatabase
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv

load_dotenv()

# ---------------- DATABASE ----------------

DATABASE_PATH = "learning_sql_store.db"

@st.cache_resource
def init_database():
    db_uri = f"sqlite:///{DATABASE_PATH}"

    # Disable sample rows to avoid date parsing errors
    return SQLDatabase.from_uri(
        db_uri,
        sample_rows_in_table_info=0
    )

db = init_database()

# ---------------- SQL GENERATION ----------------

def get_sql_chain(db):

    template = """
You are a data analyst helping a user explore a company database.

Based on the schema below, write a SQL query that answers the user's question.

<SCHEMA>{schema}</SCHEMA>

Write ONLY the SQL query.
Do not include explanations or backticks.

Example:

Question: Which customers placed the most orders?

SQL Query:
SELECT customer_id, COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC
LIMIT 5;

Question: {question}

SQL Query:
"""

    prompt = ChatPromptTemplate.from_template(template)

    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

    if not GROQ_API_KEY:
        st.error("GROQ_API_KEY missing. Add it to your .env file.")
        st.stop()

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )

    def get_schema(_):
        return db.get_table_info()[:6000]

    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

# ---------------- RESPONSE ----------------

def get_response(user_query: str, db: SQLDatabase):

    # 1️⃣ Generate SQL
    sql_chain = get_sql_chain(db)
    query = sql_chain.invoke({"question": user_query}).strip()

    # 2️⃣ Explain SQL
    explain_prompt = ChatPromptTemplate.from_template("""
Explain clearly and simply what the following SQL query does:

{query}
""")

    explain_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

    explain_chain = explain_prompt | explain_llm | StrOutputParser()

    explanation = explain_chain.invoke({"query": query})

    # 3️⃣ Execute SQL safely
    try:
        engine = db._engine
        df = pd.read_sql(query, engine)
        raw_result = df.to_string()

    except Exception as e:
        raw_result = str(e)
        df = pd.DataFrame({"error": [str(e)]})

    # 4️⃣ Generate final natural language answer
    nl_prompt = ChatPromptTemplate.from_template("""
You are a helpful SQL assistant.

Using the schema, SQL query, and SQL response,
write a SHORT factual answer to the user's question.

<SCHEMA>{schema}</SCHEMA>

Question: {question}
SQL Query: {query}
SQL Response: {response}
""")

    schema_text = db.get_table_info()[:4000]

    final_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

    final_chain = nl_prompt | final_llm | StrOutputParser()

    final_answer = final_chain.invoke({
        "schema": schema_text,
        "question": user_query,
        "query": query,
        "response": raw_result[:3000]
    })

    return {
        "query": query,
        "explanation": explanation,
        "answer": final_answer,
        "data": df
    }

# ---------------- STREAMLIT UI ----------------

if "chat_history" not in st.session_state:

    st.session_state.chat_history = [
        AIMessage(content=(
            "Hello! I'm your SQL assistant 👋\n\n"
            "I'm connected to an **online store database** with tables:\n"
            "`customers`, `products`, `orders`, and `order_items`.\n\n"
            "Try asking questions like:\n"
            "- Which customers placed the most orders?\n"
            "- What are the most expensive products?\n"
            "- How many orders were placed per country?"
        ))
    ]

st.image("p.jpg", width=100)

st.title("Learn SQL by Asking Questions")

st.write(
"Ask a question and the assistant will generate the SQL query, "
"explain it, run it on the database, and show the result."
)

with st.expander("About the database"):

    st.markdown("""
This app uses a small **online store database**.

Tables:

- **customers** – customer information  
- **products** – product catalog and prices  
- **orders** – orders placed by customers  
- **order_items** – products inside each order
""")

# ---------------- CHAT DISPLAY ----------------

for message in st.session_state.chat_history:

    if isinstance(message, AIMessage):

        with st.chat_message("AI", avatar="assistance.png"):
            st.markdown(message.content)

    elif isinstance(message, HumanMessage):

        with st.chat_message("Human", avatar="laptop.png"):
            st.markdown(message.content)

# ---------------- USER INPUT ----------------

user_query = st.chat_input("Ask a question about the database...")

if user_query and user_query.strip():

    st.session_state.chat_history.append(
        HumanMessage(content=user_query)
    )

    with st.chat_message("Human", avatar="laptop.png"):
        st.markdown(user_query)

    with st.chat_message("AI", avatar="assistance.png"):

        with st.spinner("Thinking..."):

            outputs = get_response(user_query, db)

        st.markdown("### Generated SQL Query")
        st.code(outputs["query"], language="sql")

        st.markdown("### SQL Explanation")
        st.info(outputs["explanation"])

        st.markdown("### Query Result")
        st.dataframe(outputs["data"])

        st.markdown("### Final Answer")
        st.success(outputs["answer"])

        st.session_state.chat_history.append(
            AIMessage(content=outputs["answer"])
        )