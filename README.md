# PDFMind.AI 🧠

PDF Summarizer + QnA powered by **Groq** (free, fast) + **FastAPI** + vanilla HTML frontend.

---

## Project Structure

```
pdfmind/
├── backend/
│   ├── main.py           ← FastAPI app
│   └── requirements.txt
└── frontend/
    └── index.html        ← Drop this anywhere (or serve with Live Server)
```

---

## Backend Setup

### 1. Get a free Groq API key
- Go to https://console.groq.com
- Sign up → API Keys → Create key
- Copy it

### 2. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Set your API key
**Windows:**
```cmd
set GROQ_API_KEY=your_key_here
```
**Mac/Linux:**
```bash
export GROQ_API_KEY=your_key_here
```

### 4. Run the server
```bash
uvicorn main:app --reload
```
Server starts at → http://localhost:8000

Auto docs available at → http://localhost:8000/docs

---

## Frontend Setup

Just open `frontend/index.html` in your browser.

If you get CORS errors, use VS Code **Live Server** extension to serve it.

The `BACKEND` variable at the top of the script is set to `http://localhost:8000`.
Change it to your deployed URL when you go live.

---

## Deploy for free

### Backend → Render.com
1. Push this project to GitHub
2. Go to https://render.com → New Web Service
3. Connect your repo, set root to `backend/`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
6. Add environment variable: `GROQ_API_KEY = your_key`

### Frontend → GitHub Pages or Netlify (drop the HTML file)
Update the `BACKEND` constant in `index.html` to your Render URL.

---

## Groq Free Tier Limits (as of 2025)
| Model | Requests/min | Tokens/min | Tokens/day |
|-------|-------------|------------|------------|
| llama3-8b-8192 | 30 | 30,000 | 500,000 |
| mixtral-8x7b | 30 | 5,000 | 500,000 |

Way more generous than OpenAI's free tier. To switch models, change the `MODEL` variable in `main.py`.

---

Made with 💟 by Trisha
