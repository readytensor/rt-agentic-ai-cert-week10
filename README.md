# Ready Tensor Agentic AI Certification – Week 10

This repository contains lesson materials and code examples for **Week 10** of the [Agentic AI Developer Certification Program](https://app.readytensor.ai/publications/HrJ0xWtLzLNt) by Ready Tensor. This is about **packaging agentic AI systems** for different audiences — from portfolio demos to production handoffs.

⚠️ **Note**: This is a work-in-progress. We're actively adding code examples and documentation to this repository. Stay tuned for updates!

---

## What You'll Learn

- **Lessons 1a-1b**: **FastAPI & Render** — Build professional APIs and deploy them as scalable services
- **Lesson 2**: **Gradio & Hugging Face** — Create intuitive demos and share them instantly
- **Lesson 3**: **Streamlit & Cloud** — Build interactive showcases for stakeholders and employers
- **Lesson 4**: **Building Resilience** — Handle real-world failures gracefully when APIs go down
- **Lesson 5**: **Production Documentation** — Technical docs and compliance materials for professional handoffs

---

## Getting Started

### Prerequisites

- Python 3.10+
- Groq API key (for Lesson 1). You can get your API key from [Groq](https://console.groq.com/).

---

## API Key Setup

Create a `.env` file in the root directory and add your API key:

```
GROQ_API_KEY=your-api-key-here
```

## Usage

### Lesson 1a: FastAPI Service - Example 1 (Simple Service)

1. `cd code/lesson1a_fastapi/`
2. `python -m venv venv` (if not already created)
3. `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt`
5. `python example/main.py` for example 1 (simple service)
6. Open your browser and go to `http://localhost:8000/docs` to interact with the API.

### Lesson 1a: FastAPI Service - Example 2 (RAG-based Service)

1. `cd code/lesson1a_fastapi/`
2. `python -m venv venv` (if not already created)
3. `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt` (if not already installed)
5. `python example2_rag/setup_data.py` to ingest data into the RAG database (one-time only)
6. `python example2_rag/main.py` to run the RAG service
7. Open your browser and go to `http://localhost:8000/docs` to interact with the API.

### Lesson 2: Gradio App

1. `cd code/lesson2_gradio/`
2. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
3. `python -m venv venv` (if not already created)
4. `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. `pip install -r requirements.txt`
6. `python main.py` to run the Gradio app
7. Open your browser and go to `http://localhost:7860` to interact with the app.

### Lesson 3: Streamlit App

1. `cd code/lesson3_streamlit/`
2. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
3. `python -m venv venv` (if not already created)
4. `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. `pip install -r requirements.txt`
6. `streamlit run main.py` to run the Streamlit app
7. Open your browser and go to `http://localhost:8501` to interact with the app.

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## Contact

**Ready Tensor, Inc.**

- Email: contact at readytensor dot com
- Issues & Contributions: Open an issue or PR on this repo
- Website: [https://readytensor.ai](https://readytensor.ai)
