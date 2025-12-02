# 🧠 LangGraph Research Assistant (GraphRAG Edition)

> **Your AI-Powered Second Brain that "Connects the Dots"**

![Graph View](https://raw.githubusercontent.com/GEEGEEGOOGOO/LangGraph-Research-Assistant/main/assets/graph_view_demo.png)

---

## 📖 What is this? (In Simple English)

Imagine you have a super-smart research assistant who reads every document you give them. But instead of just memorizing the words, they **draw a giant mind map** connecting every person, concept, and idea.

When you ask a question, they don't just look for matching keywords (like a standard search engine). Instead, they look at the **connections** on their mind map to give you a deeper, smarter answer.

### 🍎 An Analogy
*   **Standard Search (Google/Ctrl+F):** You search for "Apple". It gives you a list of pages with the word "Apple".
*   **This Assistant (GraphRAG):** You search for "Apple". It tells you: *"Apple released the iPhone in 2007, which was founded by Steve Jobs, who also founded Pixar."* It understands the **relationships**.

### 🌍 Why is this useful today?
We are drowning in information. We have thousands of PDFs, notes, and docs. Finding *specific* facts is easy, but understanding **how things connect** is hard. This tool solves that by turning your scattered documents into a structured **Knowledge Graph**.

---

## 🛠️ Technical Details (Under the Hood)

This project is a sophisticated **Graph Retrieval-Augmented Generation (GraphRAG)** system.

### Core Technologies
1.  **GraphRAG Engine**: Instead of storing text in a simple list (Vector Store), we extract entities and relationships to build a **Knowledge Graph** using `NetworkX`.
2.  **Google Gemini 2.5 Flash**: The brain of the operation. We use this latest, ultra-fast AI model to:
    *   **Read** your documents and extract triplets (e.g., `Entity A -> Related To -> Entity B`).
    *   **Synthesize** answers based on the graph data.
3.  **LangGraph**: The "manager" that coordinates different AI agents (Planner, Retriever, Synthesizer) to work together.
4.  **React Frontend**: A beautiful, futuristic dashboard to visualize your knowledge graph interactively using D3.js.

### How it Works (The Pipeline)
1.  **Ingestion**: You upload a document.
2.  **Extraction**: Gemini reads it and identifies key concepts (Nodes) and how they relate (Edges).
3.  **Graph Construction**: These are added to a persistent network graph.
4.  **Querying**: When you ask a question, the system traverses the graph to find related concepts (even if they don't use the exact same keywords).
5.  **Synthesis**: Gemini writes a clear answer using this rich context.

---

## 🚀 Use Cases

### 1. Academic Research
*   **Scenario**: You have 50 papers on "Climate Change".
*   **Benefit**: Ask *"How does ocean acidification affect coral reefs?"* and get an answer synthesizing findings from *all* papers, showing the chain of cause-and-effect.

### 2. Legal & Compliance
*   **Scenario**: Analyzing hundreds of contracts.
*   **Benefit**: Instantly see how "Clause X" in Contract A relates to "Regulation Y" in a government PDF.

### 3. Personal Knowledge Management (PKM)
*   **Scenario**: You have years of messy notes.
*   **Benefit**: Turn your Obsidian/Notion dump into a queryable brain. Discover that a book you read 3 years ago connects to a project you're working on today.

### 4. Investigative Journalism
*   **Scenario**: Connecting dots between people, companies, and events.
*   **Benefit**: The graph automatically highlights that "Person A" worked at "Company B" which funded "Event C".

---

## 🏆 The Competitive Edge

Why use this over ChatGPT or standard RAG tools?

| Feature | Standard RAG / ChatGPT | **LangGraph Research Assistant** |
| :--- | :--- | :--- |
| **Understanding** | Matches keywords (Vector Search) | **Understands Relationships (Graph Search)** |
| **Context** | Limited to text chunks | **Traverses connected concepts (Multi-hop)** |
| **Transparency** | "Black box" answer | **Visual Graph** (See the connections) |
| **Discovery** | Finds what you search for | **Finds what you didn't know you needed** |
| **Cost** | High (if using GPT-4) | **Low** (Optimized with Gemini 2.5 Flash) |

---

## ⚡ Quick Start

### Prerequisites
*   Python 3.11+
*   Node.js & npm
*   Google Gemini API Key

### 1. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Set your API Key in .env
# GEMINI_API_KEY=your_key_here
```

### 2. Frontend Setup
```bash
cd frontend
npm install
```

### 3. Run Everything
Double-click `start_all.bat` (Windows) or run:
```bash
# Terminal 1 (Backend)
uvicorn app.main:app --reload

# Terminal 2 (Frontend)
npm run dev
```

---

**Built with ❤️ using LangGraph, Gemini, and React.**
