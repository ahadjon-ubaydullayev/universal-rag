# RAG Chatbot Backend

## 🚀 Overview
This is the **backend** for a **Retrieval-Augmented Generation (RAG) chatbot** designed to answer questions about various entities such as hospitals, universities, and agencies. It integrates **FastAPI, ChromaDB, and OpenAI’s GPT-3.5 Turbo** to provide accurate responses based on uploaded documents.

## 🛠 Features
- **Document-Based Q&A**: Answers questions using **PDF, DOC, CSV** files as context.
- **Fast & Scalable**: Built with **FastAPI** for high-performance API responses.
- **LLM Integration**: Uses **GPT-3.5 Turbo** for natural language responses.
- **Vector Search with ChromaDB**: Stores document embeddings for efficient retrieval.
- **Environment Configuration**: Uses **dotenv** for managing API keys and configurations.

## 📌 Tech Stack
- **FastAPI** - Backend framework
- **ChromaDB** - Vector database for retrieval
- **LangChain** - LLM and retrieval pipeline
- **OpenAI GPT-3.5 Turbo** - Chat model
- **Python-dotenv** - Environment variable management
- **pypdf** - PDF document parsing
- **SQLAlchemy** - Future database integration

## 📂 Project Structure
```
retrigenix/
│── backend/
│   ├── main.py            # FastAPI app
│   ├── retriever.py       # Runs document embedding and storage
│   ├── model.py           # LLM integration with OpenAI
│   ├── requirements.txt   # Backend dependencies
│── docs/                  # Uploaded documents
│── chroma_data/           # ChromaDB vector storage
│── .env                   # API keys and settings
```

## ⚡ Installation & Setup
1️⃣ **Clone the repository**
```sh
git clone https://github.com/yourusername/retrigenix.git
cd retrigenix/backend
```

2️⃣ **Create a virtual environment and install dependencies**
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3️⃣ **Set up environment variables**
Create a `.env` file and add your API keys:
```ini
OPENAI_API_KEY=your_openai_api_key
```

## ▶️ Running the Backend
Start the FastAPI server:
```sh
uvicorn main:app --reload
```
API will be available at: **`http://127.0.0.1:8000`**

## 📥 Adding Documents
**Every time you upload new documents, you must run `retriever.py`** to update the vector database:
```sh
python retriever.py
```

This ensures that newly uploaded documents are indexed for retrieval.

---
📌 **Stay tuned for more updates!** 🚀

