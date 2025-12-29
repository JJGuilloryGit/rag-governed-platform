import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .schemas import AskRequest, AskResponse
from .service import answer

INDEX_DIR = os.getenv("RAG_UI_INDEX", "./data/index")

app = FastAPI(title="Governed RAG Demo", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/ask", response_model=AskResponse)
def api_ask(req: AskRequest) -> AskResponse:
    if not Path(INDEX_DIR).exists():
        raise HTTPException(
            status_code=400,
            detail=f"Index not found at '{INDEX_DIR}'. Run the ingest step first.",
        )

    try:
        return answer(req, index_dir=INDEX_DIR)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to process request.") from exc

@app.get("/", response_class=HTMLResponse)
def root() -> HTMLResponse:
    return HTMLResponse(content=HTML_CONTENT)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Governed RAG Demo</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: radial-gradient(120% 120% at 20% 20%, #0f172a 0%, #05060b 40%, #0a0c1d 100%);
      --panel: rgba(16, 24, 40, 0.8);
      --accent: #7cf3c5;
      --muted: #c4c9d4;
      --border: rgba(255, 255, 255, 0.08);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: white;
      font-family: 'Space Grotesk', 'Segoe UI', sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 32px;
    }
    .grid {
      width: min(1200px, 100%);
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 24px;
    }
    .card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 24px;
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.55);
      backdrop-filter: blur(6px);
    }
    h1 {
      font-size: 32px;
      margin: 0 0 12px 0;
      letter-spacing: -0.02em;
    }
    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: var(--accent);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 12px;
      letter-spacing: 0.08em;
      padding: 8px 12px;
      border: 1px solid var(--border);
      border-radius: 999px;
      background: rgba(124, 243, 197, 0.06);
    }
    p.lead {
      margin: 12px 0 20px 0;
      color: var(--muted);
      font-size: 16px;
      line-height: 1.6;
    }
    label {
      display: block;
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 6px;
    }
    textarea, select, button, input {
      width: 100%;
      border-radius: 12px;
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.04);
      color: white;
      font-size: 15px;
      padding: 12px 14px;
      outline: none;
      transition: border 0.2s ease, transform 0.2s ease;
    }
    textarea {
      resize: vertical;
      min-height: 140px;
      line-height: 1.5;
    }
    select { appearance: none; }
    button {
      cursor: pointer;
      border: none;
      background: linear-gradient(120deg, #4de1af, #74f5ff);
      color: #04151f;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      box-shadow: 0 12px 35px rgba(116, 245, 255, 0.3);
    }
    button:hover { transform: translateY(-1px); }
    button:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
    .row { display: flex; gap: 12px; align-items: flex-end; }
    .row > div { flex: 1; }
    .pill {
      display: inline-flex;
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid var(--border);
      font-size: 12px;
      color: var(--muted);
      gap: 8px;
      align-items: center;
    }
    .stat {
      display: flex;
      gap: 8px;
      align-items: center;
      color: var(--muted);
      font-size: 13px;
    }
    .answer {
      white-space: pre-wrap;
      line-height: 1.6;
      color: #f4f7fb;
    }
    .surface {
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 16px;
      background: rgba(255, 255, 255, 0.02);
    }
    ul {
      padding-left: 18px;
      color: var(--muted);
      margin: 8px 0 0 0;
      line-height: 1.5;
    }
    .badge { color: var(--accent); font-weight: 600; }
    @media (max-width: 960px) {
      body { padding: 18px; }
      .grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="grid">
    <div class="card">
      <div class="eyebrow">Governed RAG</div>
      <h1>Ask your policy questions</h1>
      <p class="lead">Grounded answers with prompt governance, logging, and citations</p>
      <div class="surface" style="margin-bottom: 14px;">
        <label style="margin-bottom: 4px;">How to use (non-technical)</label>
        <ul style="margin: 0;">
          <li>Type a plain-English question (e.g., “What is the refund policy?”).</li>
          <li>Keep “Prompt version” on the default unless you’re asked to switch.</li>
          <li>Click “Run RAG” and wait a couple of seconds.</li>
          <li>Read the answer and scan the citations to see where it came from.</li>
        </ul>
      </div>
      <form id="ask-form">
        <label for="question">Question</label>
        <textarea id="question" name="question" placeholder="e.g., What is the refund policy for premium users?" required></textarea>
        <div class="row" style="margin-top: 14px;">
          <div>
            <label for="prompt">Prompt version</label>
            <select id="prompt" name="prompt">
              <option value="v1">v1 (default)</option>
              <option value="v2">v2</option>
            </select>
          </div>
          <div style="max-width: 180px;">
            <button type="submit" id="submit">Run RAG</button>
          </div>
        </div>
      </form>
      <div style="margin-top: 14px;" class="stat">
        <span class="pill"><span style="width: 10px; height: 10px; background: var(--accent); border-radius: 50%;"></span>Local index demo</span>
        <span class="pill">Backend: FAISS</span>
        <span class="pill">Prompt governance ready</span>
      </div>
    </div>
    <div class="card">
      <div class="surface">
        <div class="stat" style="margin-bottom: 6px;">
          <span class="badge" id="status">Ready</span>
          <span id="chars" aria-live="polite"></span>
        </div>
        <div class="answer" id="answer">Run a query to see the grounded response here.</div>
        <div id="citations-wrap" style="margin-top: 14px;">
          <label>Citations</label>
          <ul id="citations">
            <li>No citations yet.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <script>
    const form = document.getElementById('ask-form');
    const submitBtn = document.getElementById('submit');
    const status = document.getElementById('status');
    const chars = document.getElementById('chars');
    const answerBlock = document.getElementById('answer');
    const citationsList = document.getElementById('citations');

    async function askRag(event) {
      event.preventDefault();
      const question = document.getElementById('question').value.trim();
      const prompt_version = document.getElementById('prompt').value;
      if (!question) return;

      submitBtn.disabled = true;
      status.textContent = 'Thinking...';
      answerBlock.textContent = 'Collecting context and crafting a grounded answer...';
      citationsList.innerHTML = '<li>Loading...</li>';
      chars.textContent = '';

      try {
        const resp = await fetch('/api/ask', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question, prompt_version })
        });

        const data = await resp.json();
        if (!resp.ok) {
          throw new Error(data.detail || 'Request failed');
        }

        status.textContent = 'Answer ready';
        answerBlock.textContent = data.answer;
        chars.textContent = `Context chars used: ${data.context_chars}`;

        citationsList.innerHTML = '';
        if (data.citations && data.citations.length) {
          data.citations.forEach((c) => {
            const li = document.createElement('li');
            li.textContent = c;
            citationsList.appendChild(li);
          });
        } else {
          citationsList.innerHTML = '<li>No citations returned.</li>';
        }
      } catch (err) {
        status.textContent = 'Error';
        answerBlock.textContent = err.message || 'Something went wrong.';
        citationsList.innerHTML = '<li>Check the server logs for details.</li>';
      } finally {
        submitBtn.disabled = false;
      }
    }

    form.addEventListener('submit', askRag);
  </script>
</body>
</html>
"""
