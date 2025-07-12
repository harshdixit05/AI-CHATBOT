# Gym Fitness AI Chatbot 💪🤖

This is an intelligent chatbot designed to interact with a **gym management database**. The chatbot uses Retrieval-Augmented Generation (RAG) to generate SQL queries from user questions and provide insightful, user-friendly answers. It's capable of working with multiple vector stores and integrates semantic caching and LLMs for smart query generation.

---

## 💡 Features

- 🔍 Converts natural language questions into SQL queries using a Gemini LLM
- 🧠 Uses schema-based vector search (supports FAISS, Chroma, Milvus, Qdrant)
- 🗂️ Retrieves the most relevant schema context before query generation
- 🛢️ Connects to an SQL database to fetch actual data
- 📊 Returns answers in natural language if result rows ≤ 20
- 📚 Supports semantic caching to speed up repeated queries
- ⚙️ Modular structure for easy swapping of vector databases
- 🐳 Milvus and Qdrant integrations use Docker

---
## 🔍 Models Used

- **Embedding Model**: `all-MiniLM-L6-v2` (default in many sentence-transformers, efficient and fast)
- **LLM for SQL Generation & Answering**: Google **Gemini** model (model name configurable via `GEMINI_MODEL` in `.env` file)


## 📁 Folder Structure

```
Agentic_AI/
│
├── main.py                      
├── README.md                    # Docs on how to run, configure, and use
├── requirements.txt             # Dependencies
├── .env                         # API keys, DB URIs, secrets
├── config/ 
├── data        
│   ├── CSV files
│
├── logs/                       
│   
│
├── src/                         # All source code
│   ├── api/                     
│   │   ├── api.py               #LLM Connection (Gemini)
│   │   └── __init__.py
│   │
│   ├── database/                # DB connection & queries
│   │   ├── db.py
│   │   └── __init__.py
│   │
│   ├── vector_store/            # Vector DB wrappers
│   │   ├── faiss_store.py
│   │   ├── qdrant_store.py
│   │   ├── chroma_store.py
│   │   ├── milvus_store.py
│   │   └── __init__.py
│   │
│   ├── cache/                   # Caching layer (e.g.,semanticCache)
│   │   ├── cache.py
│   │   └── __init__.py             
│   │     
│   │
│   ├── utils/                   # Helper functions (SQL)
│       ├── sql_utils.py      
│       └── __init__.py
│   
│      
│
└── .gitignore    
```

---

## 🔧 Environment Variables

Create a `.env` file in your root directory with the following:

```env
# API
GEMINI_API_KEY=
GEMINI_MODEL=

# Vector
EMBEDDING_MODEL=
EMBEDDING_DIM=
FAISS_INDEX_TYPE=

# Database
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=


#Milvus

MILVUS_HOST=localhost
MILVUS_PORT=19530
MILVUS_COLLECTION=schema_store
```

---

## 🧪 Setup and Run

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```



## 📦 Database Setup & Import Instructions

This project uses a MySQL database to store gym-related data. A pre-configured `.sql` dump file is provided in the `data/` folder to help users set up the database quickly.

### ✅ Prerequisites

- MySQL should be installed and configured on your system.
- Ensure `mysql` command-line tool is available in your terminal (i.e., MySQL is added to your system's PATH).

---

### 💾 Steps to Restore the Database

1. **Open your terminal** (Command Prompt, PowerShell, or Bash).

2. **Create a new MySQL database** named `chatbot`:
   ```bash
   mysql -u your_username -p -e "CREATE DATABASE chatbot;"

Import the SQL dump into the chatbot database:
   ```bash
  mysql -u your_username -p chatbot < data/mydb_backup.sql
   ```


🔁 Replace your_username with your actual MySQL username (e.g., root).

🔑 You’ll be prompted to enter your MySQL password.

📁 SQL Dump Location
The SQL file is stored here in your project:
```
project-root/
├── data/
│   └── mydb_backup.sql

```
⚙️ Final Step
Ensure your .env file contains the correct database configuration:
```
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=chatbot
```
Once this is done, you're ready to run the chatbot with access to the full gym database!

2. **Run Vector DBs (if using Milvus or Qdrant)**

Make sure [Docker](https://www.docker.com/) is installed.

##  Start Milvus (Vector Store)

Milvus is one of the supported vector databases in this project. Follow the appropriate instructions based on your OS to start Milvus in **standalone mode using Docker**.

---
###  For Linux /  For macOS (with Docker & Bash)

Make sure Docker is running. Then run the following commands in your terminal:

```bash
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh
bash standalone_embed.sh start
```

To stop Milvus later:

```bash
bash standalone_embed.sh stop
```

 ### For Windows (PowerShell)
If you're on Windows and using PowerShell, do the following:

```bash
Invoke-WebRequest https://raw.githubusercontent.com/milvus-io/milvus/refs/heads/master/scripts/standalone_embed.bat -OutFile standalone.bat
.\standalone.bat start
```

To stop Milvus:
```bash
.\standalone.bat stop
```

## 🔍 Start Qdrant (Vector Store)

Qdrant is one of the supported vector databases in this project. It can be run easily using Docker.

---

### 🐳 For All OS (Linux / macOS / Windows)

Make sure Docker is installed and running. Then run the following command in your terminal or PowerShell:

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```


3. **Start the Bot**

```bash
python main.py
```

---

## ✅ Example Questions

```txt
-Which members have not renewed their subscriptions?
-List all members attending Zumba classes.
-Delete all records.
```

---

## 🧠 How it Works (Architecture)

1. User inputs a question.
2. Schema is searched via embeddings (using chosen vector store).
3. Relevant schema is passed to LLM to generate SQL.
4. SQL is executed; if rows ≤ 20, full result is passed to LLM to summarize.
5. Result is returned in friendly format.

---

## 📌 Notes

- Replace placeholders in `.env` before running.
- Currently supports FAISS, Chroma, Milvus, and Qdrant as vector databases.
- All logic is modular, allowing easy extensions or swap of components.

---


Made by Harsh Dixit.
