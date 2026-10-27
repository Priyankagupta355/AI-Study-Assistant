# 📚 AI Personal Study Assistant

An AI-powered study companion built using Generative AI, Retrieval-Augmented Generation (RAG), and AI Agents to make learning more interactive and personalized.

The application helps students interact with study materials, practice questions, plan their learning, and track study progress through AI-powered features.

## ✨ Features

### 💬 PDF Question Answering

Ask questions about uploaded PDF study materials and get AI-generated responses based on the available document context.

### 👨‍🏫 AI Tutor

Get learning assistance and explanations through an AI-powered tutoring experience.

### 📝 AI Quiz Generator

Generate practice quizzes to revise concepts and test your understanding.

### 📅 AI Study Planner

Use AI-assisted planning features to organize your study activities.

### 🔄 Revision Assistant

Get support for revising concepts and preparing for assessments.

### 🤖 Multi-Agent AI Router

Route requests to appropriate AI workflows based on the task, supporting different learning activities.

### 📊 Study Progress Tracking

Track study-related progress through the application's progress-tracking functionality.

## 🛠️ Tech Stack

| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| Python                | Core application development |
| FastAPI               | Backend API development      |
| Groq LLM              | Language model integration   |
| LangChain             | LLM application components   |
| ChromaDB              | Vector storage for retrieval |
| Sentence Transformers | Text embeddings              |
| SQLite                | Database storage             |
| SQLAlchemy            | Database interaction         |
| Streamlit             | User interface               |

## 🧠 Architecture

The application follows a modular architecture that connects the user interface, backend API, AI workflows, retrieval components, and database.

```text
                 User
                   |
                   v
              Streamlit UI
                   |
                   v
                FastAPI
                   |
                   v
                AI Router
                   |
          +--------+--------+
          |        |        |
          v        v        v
        Tutor     Quiz    Revision
          |        |        |
          +--------+--------+
                   |
                   v
             RAG / Groq LLM
                   |
                   v
             AI Response
                   |
                   v
              SQLite DB
```

*Note: This diagram represents the documented high-level architecture. The exact execution flow depends on the implementation.*

## 🔄 How It Works

1. The user interacts with the application through the Streamlit interface.
2. Requests are processed by the FastAPI backend.
3. The AI router directs requests to the relevant learning workflow.
4. Retrieval components can provide relevant document context for supported PDF question-answering tasks.
5. The Groq language model generates a response using the information supplied to the workflow.
6. Study-related information is stored or retrieved through the application's database functionality where implemented.

## 📁 Project Structure

```text
AI-Study-Assistant/
│
├── app/
│   └── Backend application
│
├── frontend/
│   └── Streamlit interface
│
├── requirements.txt
├── README.md
└── .gitignore
```

The repository contains the `app/` and `frontend/` directories. The exact internal structure may evolve as the project develops.

## ⚙️ Installation and Setup

### Prerequisites

- Python installed on your system
- Git
- A Groq API key

### 1. Clone the Repository

```bash
git clone https://github.com/Priyankagupta355/AI-Study-Assistant.git
cd AI-Study-Assistant
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add the configuration required by your application.

```env
GROQ_API_KEY=your_groq_api_key
LLM_MODEL=openai/gpt-oss-120b
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHROMA_DB_PATH=./data/chroma_db
```

Replace `your_groq_api_key` with your own API key.

<<<<<<< Updated upstream
**Important:** Never commit your actual API key to GitHub. Keep `.env` excluded through `.gitignore`.

### 5. Run the Backend

=======
Start the backend first in one terminal:

>>>>>>> Stashed changes
>>>>>>>
>>>>>>
>>>>>
>>>>
>>>
>>

```bash
python -m uvicorn app.main:app --reload
```


**Important:** Never commit your actual API key to GitHub. Keep `.env` excluded through `.gitignore`.

### 5. Run the Backend

Start the backend first in one terminal:

```bash
python -m uvicorn app.main:app --reload
```

The backend should be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Run the Frontend

Open a second terminal, activate the same virtual environment, and run:

```bash
streamlit run frontend/streamlit_app.py
```

If any command fails, verify the project structure, installed dependencies, environment variables, and the relevant entry-point file.

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Run the Frontend

Open a second terminal, activate the same virtual environment, and run:

```bash
streamlit run frontend/streamlit_app.py
```

If any command fails, verify the project structure, installed dependencies, environment variables, and the relevant entry-point file.

## 🔐 Environment and Security

- Store API credentials in environment variables.
- Never upload private keys or credentials to a public repository.
- Keep dependencies documented in `requirements.txt`.
- Avoid committing generated databases, local environment files, or unnecessary temporary files.

## 🚀 Future Improvements

Potential improvements include:

- Add automated tests for backend endpoints and AI workflows.
- Improve error handling for failed model requests.
- Add document-processing and retrieval tests.
- Add application screenshots and example outputs.
- Improve API documentation with request and response examples.
- Add deployment instructions and a live demo when available.

These are potential improvements, not claims that the features are already implemented.

## 👩‍💻 Author

**Priyanka Gupta**

B.Tech in Artificial Intelligence and Data Science

- GitHub: [Priyankagupta355](https://github.com/Priyankagupta355)
- Project Repository: [AI Personal Study Assistant](https://github.com/Priyankagupta355/AI-Study-Assistant)

---

⭐ If you find this project interesting, feel free to explore the repository.
