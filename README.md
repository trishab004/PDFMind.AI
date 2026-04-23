# PDFMind.AI 🧠

**Live Demo:** [https://pdfmind-ai.onrender.com](https://pdfmind-ai.onrender.com)

PDF Summarizer + QnA powered by **Groq** (free, fast Llama 3 models) + **FastAPI** + clean vanilla HTML frontend.

---

## Project Structure

Everything is neatly unified so it deploys as a single app:

```
pdfmind/
├── main.py                ← FastAPI app & Static Server
├── index.html             ← Frontend User Interface
├── requirements.txt       ← Python dependencies
└── .python-version        ← Forces Render to use stable Python length
```

---

## Local Setup

### 1. Get a free Groq API key
- Go to https://console.groq.com
- Sign up → API Keys → Create key
- Copy it

### 2. Configure Environment
Create a `.env` file in the same folder and add your key:
```env
GROQ_API_KEY=your_key_here
```

### 3. Install dependencies & Run
Open terminal in the `pdfmind` folder:
```bash
pip install -r requirements.txt
uvicorn main:app --reload --env-file .env
```
Open [http://localhost:8000](http://localhost:8000) in your browser!

---

## Deployment (Render.com)

This app is pre-configured to be deployed natively as a single Web Service on Render:
1. Push this project to GitHub
2. Go to https://dashboard.render.com → New Web Service
3. Connect the repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variable: `GROQ_API_KEY = your_key`

---

## Groq Free Tier Limits (as of 2025)
| Model | Requests/min | Tokens/min | Tokens/day |
|-------|-------------|------------|------------|
| llama-3.1-8b-instant | 30 | 30,000 | 500,000 |
| mixtral-8x7b-32768 | 30 | 5,000 | 500,000 |

Way more generous than OpenAI's free tier. To switch models, change the `MODEL` variable in `main.py`.

---

Made with 💟 by Trisha
