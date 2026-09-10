
# 📚 AI Personal Study Assistant

An AI-powered study assistant built using **Generative AI, RAG, and AI Agents**.

## 🚀 Features

* 💬 Ask questions from uploaded PDFs
* 👨‍🏫 AI Tutor
* 📝 AI Quiz Generator
* 📅 AI Study Planner
* 🔄 Revision Assistant
* 🤖 Multi-Agent AI Router
* 📊 Study Progress Tracking

## 🛠️ Tech Stack

* Python
* FastAPI
* Groq LLM
* LangChain
* ChromaDB
* Sentence Transformers
* SQLite
* SQLAlchemy
* Streamlit

## 🧠 Architecture

```text
User
 ↓
FastAPI
 ↓
AI Router
 ↓
┌────────┬────────┬─────────┐
Tutor    Quiz    Revision
 ↓        ↓         ↓
       RAG / Groq
           ↓
      Final Response
           ↓
        SQLite
```

## ⚙️ Setup

```bash
git clone https://github.com/YOUR_USERNAME/ai-personal-study-assistant.git
cd ai-personal-study-assistant

python -m venv venv
pip install -r requirements.txt
```

Create `.env`:

```env
GROQ_API_KEY=your_groq_api_key
LLM_MODEL=openai/gpt-oss-120b
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHROMA_DB_PATH=./data/chroma_db
```

## ▶️ Run

Backend:

```bash
python -m uvicorn app.main:app --reload
```

Frontend:

```bash
streamlit run frontend/streamlit_app.py
```

API Docs:

```text
http://127.0.0.1:8000/docs
```

## 👩‍💻 Author

**Priyanka Gupta**
B.Tech AI & Data Science
