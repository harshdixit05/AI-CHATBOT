# 🤖 AI-Powered MySQL Chatbot using Gemini API

This is an AI chatbot that takes user questions in natural language, converts them into SQL queries using **Gemini API**, executes them on a **MySQL database**, and returns friendly, human-readable answers.

---

## 🚀 Features

- 💬 Accepts user input via command line or UI
- 🧠 Uses Gemini (Google AI) API to translate natural language into SQL
- 🗃️ Connects to a live MySQL database
- 📊 Executes queries and formats answers
- 🔐 Secure and modular structure (with separate files for DB and Gemini logic)

---

## 🛠️ Tech Stack

- [Python 3.10+](https://www.python.org/)
- [MySQL](https://www.mysql.com/) — database backend
- [Gemini API](https://ai.google.dev/) — natural language understanding
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/) — DB driver

---

## 📁 Project Structure

```bash
.
├── main.py         # Entry point: handles user input/output
├── db.py           # Handles database connection and query execution
├── api.py          # Interacts with Gemini API to generate SQL and answers
├── .env            # Stores your Gemini API key and DB credentials (optional)
├── requirements.txt
└── README.md
