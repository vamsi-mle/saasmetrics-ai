"""
saasmetrics.ai  |  Frontend  v5
Streaming responses, AI router visualizer, file upload panel.
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path

import requests
import sseclient
import streamlit as st

# ── Config ────────────────────────────────────────────────────────────────────
import os
from dotenv import load_dotenv
load_dotenv()

BACKEND = f"http://{os.getenv('BACKEND_HOST','localhost')}:{os.getenv('BACKEND_PORT','8000')}"

st.set_page_config(
    page_title="saasmetrics.ai",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
.stApp { background:#0d1117; color:#e6edf3; }
header[data-testid="stHeader"] { background:#0d1117; }
section[data-testid="stSidebar"] {
    background:#010409;
    border-right:1px solid #21262d;
}
div[data-testid="stSidebarContent"] { padding-top: 1rem; }

/* ── Inputs ── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background:#161b22 !important;
    color:#e6edf3 !important;
    border:1px solid #30363d !important;
    border-radius:6px !important;
    font-size:14px !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color:#388bfd !important;
    box-shadow:0 0 0 3px rgba(56,139,253,0.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    background:#21262d !important;
    color:#e6edf3 !important;
    border:1px solid #30363d !important;
    border-radius:6px !important;
    font-size:13px !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background:#30363d !important;
    border-color:#8b949e !important;
}
button[kind="primary"] {
    background:#238636 !important;
    border-color:#238636 !important;
    color:#fff !important;
}
button[kind="primary"]:hover {
    background:#2ea043 !important;
    border-color:#2ea043 !important;
}

/* ── Messages ── */
.msg-user {
    background:#161b22;
    border-left:3px solid #388bfd;
    padding:12px 18px;
    border-radius:0 8px 8px 0;
    margin:10px 0;
    font-size:14px;
    color:#e6edf3;
}
.msg-bot {
    background:#0d1117;
    border:1px solid #21262d;
    border-left:3px solid #3fb950;
    padding:16px 20px;
    border-radius:0 8px 8px 0;
    margin:10px 0;
    font-size:14px;
    line-height:1.7;
    color:#e6edf3;
}
.msg-streaming {
    background:#0d1117;
    border:1px solid #21262d;
    border-left:3px solid #e3b341;
    padding:16px 20px;
    border-radius:0 8px 8px 0;
    margin:10px 0;
    font-size:14px;
    line-height:1.7;
    color:#e6edf3;
}

/* ── Source badges ── */
.badge {
    display:inline-block;
    padding:3px 10px;
    border-radius:12px;
    font-size:11px;
    font-weight:600;
    margin:2px 3px 8px 0;
    letter-spacing:0.2px;
}
.b-bq     { background:#0c2d6b; color:#79c0ff; border:1px solid #1f6feb; }
.b-excel  { background:#0a3622; color:#56d364; border:1px solid #238636; }
.b-pdf    { background:#3d1c1c; color:#ff7b72; border:1px solid #8b2020; }
.b-word   { background:#1c1c3d; color:#a5a5ff; border:1px solid #3030a0; }
.b-upload { background:#2d1c3d; color:#d2a8ff; border:1px solid #8957e5; }

/* ── Confidence ── */
.conf-high   { color:#56d364; font-size:11px; font-weight:700; }
.conf-medium { color:#e3b341; font-size:11px; font-weight:700; }
.conf-low    { color:#ff7b72; font-size:11px; font-weight:700; }

/* ── Router panel ── */
.router-panel {
    background:#161b22;
    border:1px solid #30363d;
    border-radius:8px;
    padding:10px 14px;
    margin:6px 0;
    font-size:12px;
    color:#8b949e;
}
.router-step {
    color:#e3b341;
    font-size:11px;
    font-weight:600;
    letter-spacing:0.5px;
    margin-bottom:4px;
}

/* ── Disambig + SQL ── */
.disambig-note {
    background:#161b22;
    border:1px solid #30363d;
    border-left:3px solid #e3b341;
    border-radius:0 6px 6px 0;
    padding:6px 12px;
    font-size:12px;
    color:#8b949e;
    margin-top:8px;
}
.sql-block {
    background:#010409;
    border:1px solid #21262d;
    border-radius:6px;
    padding:10px 14px;
    font-size:11px;
    font-family:'Courier New', monospace;
    color:#79c0ff;
    margin-top:8px;
    white-space:pre-wrap;
    word-break:break-all;
}

/* ── Upload panel ── */
.upload-file-item {
    background:#161b22;
    border:1px solid #30363d;
    border-radius:6px;
    padding:8px 12px;
    margin:4px 0;
    font-size:12px;
    color:#8b949e;
    display:flex;
    align-items:center;
    justify-content:space-between;
}
.source-status {
    display:inline-block;
    width:8px; height:8px;
    border-radius:50%;
    margin-right:6px;
}
.dot-green  { background:#3fb950; }
.dot-yellow { background:#e3b341; }
.dot-red    { background:#ff7b72; }

/* ── Demo questions ── */
.demo-q-btn button {
    background:#0d1117 !important;
    border:1px solid #21262d !important;
    text-align:left !important;
    font-size:12px !important;
    padding:6px 10px !important;
    color:#8b949e !important;
    height:auto !important;
    white-space:normal !important;
    line-height:1.4 !important;
}
.demo-q-btn button:hover {
    border-color:#388bfd !important;
    color:#79c0ff !important;
}

/* ── Empty state ── */
.empty-state {
    text-align:center;
    padding:100px 20px;
    color:#484f58;
}

/* ── Streamlit overrides ── */
.stSpinner > div { border-top-color:#388bfd !important; }
div[data-testid="stFileUploader"] {
    background:#161b22 !important;
    border:1px dashed #30363d !important;
    border-radius:8px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [
    ("messages", []),
    ("pending_question", ""),
    ("show_sql", False),
    ("show_routing", True),
    ("uploads", []),
]:
    if k not in st.session_state:
        st.session_state[k] = v


# ── Helpers ───────────────────────────────────────────────────────────────────
def source_badge(s: str) -> str:
    sl = s.lower()
    if "upload" in sl or "uploaded" in sl:
        return '<span class="badge b-upload">📎 Uploaded</span>'
    if any(k in sl for k in ["bigquery", "bq", "customer", "revenue", "subscription"]):
        return '<span class="badge b-bq">🗄 BigQuery</span>'
    if any(k in sl for k in ["excel", "sheet", "pipeline", "q4"]):
        return '<span class="badge b-excel">📊 Sheets</span>'
    if any(k in sl for k in ["pdf", "board", "report", "q3"]):
        return '<span class="badge b-pdf">📄 Board Report</span>'
    if any(k in sl for k in ["word", "policy", "commercial"]):
        return '<span class="badge b-word">📝 Policy</span>'
    return f'<span class="badge b-bq">📦 {s[:15]}</span>'

def conf_html(c: str) -> str:
    c = (c or "").lower()
    cls = {"high": "conf-high", "medium": "conf-medium", "low": "conf-low"}.get(c, "conf-medium")
    icon = {"high": "✓", "medium": "≈", "low": "⚠"}.get(c, "≈")
    return f'<span class="{cls}">{icon} {c.upper()} confidence</span>'

def intent_icon(tag: str) -> str:
    return {
        "revenue": "💰", "pipeline": "🔮", "churn": "⚠️",
        "policy": "📋", "pricing": "💲", "account_health": "❤️",
        "usage": "📈", "save_playbook": "🆘", "comparison": "⚖️",
    }.get(tag, "🔍")

def refresh_uploads():
    try:
        r = requests.get(f"{BACKEND}/uploads", timeout=10)
        if r.status_code == 200:
            st.session_state.uploads = r.json().get("files", [])
    except Exception:
        pass

def get_health():
    try:
        r = requests.get(f"{BACKEND}/health", timeout=5)
        return r.json() if r.status_code == 200 else {}
    except Exception:
        return {}


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ saasmetrics.ai")
    st.markdown("<small style='color:#484f58'>Enterprise Data Assistant</small>", unsafe_allow_html=True)

    # System health dots
    health = get_health()
    def dot(ok): return '<span class="source-status dot-green"></span>' if ok else '<span class="source-status dot-red"></span>'

    st.markdown(
        f"<div style='font-size:11px;color:#8b949e;margin:8px 0 12px'>"
        f"{dot(health.get('gemini'))} Gemini &nbsp;"
        f"{dot(health.get('bigquery'))} BigQuery &nbsp;"
        f"{dot(health.get('gcs'))} GCS"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Upload panel ──────────────────────────────────────────────────────
    st.markdown("**📎 Data Sources**")
    st.markdown(
        "<small style='color:#8b949e'>Upload Excel, PDF, Word or CSV to add as a live source.</small>",
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload",
        type=["xlsx", "xls", "pdf", "docx", "csv"],
        label_visibility="collapsed",
        key="file_uploader_widget",
    )
    if uploaded_file and uploaded_file.name != st.session_state.get("_last_uploaded"):
        st.session_state["_last_uploaded"] = uploaded_file.name
        with st.spinner(f"Indexing {uploaded_file.name}..."):
            try:
                r = requests.post(
                    f"{BACKEND}/upload",
                    files={"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)},
                    timeout=30,
                )
                if r.status_code == 200:
                    st.success(f"✓ {uploaded_file.name} — ready to query")
                    refresh_uploads()
                else:
                    st.error(r.json().get("detail", "Upload failed"))
            except Exception as e:
                st.error(f"Upload error: {e}")

    refresh_uploads()
    if st.session_state.uploads:
        for f in st.session_state.uploads:
            c1, c2 = st.columns([5, 1])
            with c1:
                icon = {"Excel": "📊", "PDF": "📄", "Word": "📝", "CSV": "📋"}.get(f["source_type"], "📎")
                st.markdown(
                    f"<div class='upload-file-item'>"
                    f"{icon} <b>{f['filename']}</b><br>"
                    f"<span style='font-size:10px'>{f['source_type']} · {f['size_kb']} KB</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            with c2:
                if st.button("✕", key=f"rm_{f['filename']}", help="Remove"):
                    try:
                        requests.delete(f"{BACKEND}/upload/{f['filename']}", timeout=10)
                        refresh_uploads()
                        st.rerun()
                    except Exception:
                        pass
    else:
        st.markdown("<small style='color:#30363d'>No uploads yet.</small>", unsafe_allow_html=True)

    st.divider()

    # ── Built-in sources status ───────────────────────────────────────────
    st.markdown("**Built-in Sources**")
    bs = health.get("builtin_sources", {})
    for name, key, icon in [("BigQuery", "bigquery", "🗄"), ("Pipeline (Sheets)", "excel", "📊"),
                              ("Board Report (PDF)", "pdf", "📄"), ("Policy Doc (Word)", "word", "📝")]:
        if key == "bigquery":
            ok = health.get("bigquery", False)
        else:
            ok = bs.get(key, False)
        d = '<span class="source-status dot-green"></span>' if ok else '<span class="source-status dot-yellow"></span>'
        st.markdown(f"<small>{d}{icon} {name}</small>", unsafe_allow_html=True)

    st.divider()

    # ── Settings ──────────────────────────────────────────────────────────
    st.session_state.show_routing = st.toggle("Show routing decisions", value=st.session_state.show_routing)
    st.session_state.show_sql     = st.toggle("Show SQL queries",       value=st.session_state.show_sql)

    st.divider()

    # ── Demo questions ────────────────────────────────────────────────────
    st.markdown("**Demo Questions**")

    DEMO = {
        "💰 Revenue & ARR": [
            "What is our current ARR?",
            "Show me the ARR trend for the past 6 months",
            "What is our NRR and how has it trended?",
        ],
        "⚠️ At-Risk & Churn": [
            "Who are our at-risk accounts and what is the total ARR at risk?",
            "Why did NordBank churn and what would we charge them to return?",
            "What is the full save playbook for Meridian Trading?",
        ],
        "🔀 Multi-Source": [
            "What discount can we offer Meridian Trading and who needs to approve it?",
            "Which at-risk accounts qualify for the RIIP promotion?",
            "How does Q3 ARR compare to Q4 weighted pipeline coverage?",
        ],
        "🔍 Disambiguation": [
            "How many seats does Apex Financial have?",
            "What is the price for Meridian Trading's subscription?",
            "Who owns the Pinnacle Wealth account?",
        ],
        "📎 Upload Demo": [
            "Summarize what's in my uploaded files",
            "What does my uploaded data show about churn risk?",
            "Cross-reference my upload against our at-risk accounts",
        ],
        "⬇️ LOW Confidence Demo": [
            "What was the average deal cycle length for Enterprise accounts closed in Q2 FY2024, and how does it compare to our industry benchmark?",
        ],
    }

    for cat, questions in DEMO.items():
        with st.expander(cat):
            for q in questions:
                st.markdown('<div class="demo-q-btn">', unsafe_allow_html=True)
                if st.button(q, key=f"dq_{hash(q)}", use_container_width=True):
                    st.session_state.pending_question = q
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑 Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🔄 Reload", use_container_width=True):
            try:
                requests.post(f"{BACKEND}/reload", timeout=5)
                _source_cache = {}
                st.success("Sources reloaded")
            except Exception:
                st.error("Backend offline")

    n_turns = len([m for m in st.session_state.messages if m["role"] == "user"])
    if n_turns:
        st.markdown(
            f"<small style='color:#484f58'>🧠 {n_turns} turn{'s' if n_turns != 1 else ''} in memory</small>",
            unsafe_allow_html=True,
        )


# ── Main chat area ────────────────────────────────────────────────────────────
st.markdown("## Enterprise Data Assistant")

chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:56px;margin-bottom:12px">🛡️</div>
            <div style="font-size:20px;color:#8b949e;font-weight:600">Ask anything about your data</div>
            <div style="font-size:14px;margin-top:8px">
                Revenue · Customers · Pipeline · Policy · Board Reports · Your Uploads
            </div>
            <div style="font-size:12px;margin-top:6px;color:#30363d">
                Powered by Gemini · Grounded in live BigQuery · Source-cited answers
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="msg-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                # Routing info
                routing_html = ""
                if st.session_state.show_routing and msg.get("routing"):
                    r = msg["routing"]
                    srcs = " → ".join(r.get("sources", []))
                    reasoning = r.get("reasoning", "")
                    q_type = r.get("query_type", "")
                    i_tag = r.get("intent_tag", "")
                    routing_html = (
                        f'<div class="router-panel">'
                        f'<div class="router-step">🔀 ROUTER — {q_type.upper()} {intent_icon(i_tag)} {i_tag}</div>'
                        f'Sources selected: <b>{srcs}</b><br>'
                        f'<span style="color:#484f58">{reasoning}</span>'
                        f'</div>'
                    )

                # Source badges + confidence
                badges = "".join(source_badge(s) for s in msg.get("sources_used", []))
                conf = conf_html(msg.get("confidence", "high"))

                # Disambiguation note
                disambig = msg.get("disambiguation_notes", "")
                disambig_html = (
                    f'<div class="disambig-note">🔀 {disambig}</div>'
                    if disambig else ""
                )

                # SQL
                sql_html = ""
                if st.session_state.show_sql and msg.get("sql"):
                    sql_html = f'<div class="sql-block">{msg["sql"]}</div>'

                # Strip metadata line from answer text
                answer_text = re.sub(r"\nMETADATA::\{.*\}", "", msg["content"], flags=re.DOTALL).strip()

                st.markdown(
                    f'{routing_html}'
                    f'<div class="msg-bot">'
                    f'<div style="margin-bottom:8px">{badges} &nbsp; {conf}</div>'
                    f'{answer_text}'
                    f'{disambig_html}'
                    f'{sql_html}'
                    f'<div style="font-size:10px;color:#30363d;margin-top:8px">{msg.get("ts","")}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )


# ── Input bar ─────────────────────────────────────────────────────────────────
st.divider()
col_input, col_btn = st.columns([7, 1])
with col_input:
    user_input = st.text_input(
        "question",
        value=st.session_state.pending_question,
        placeholder="Ask anything — 'What is our ARR?', 'Save playbook for Meridian?', 'Cross-reference my upload...'",
        label_visibility="collapsed",
        key="chat_input",
    )
with col_btn:
    send = st.button("Send →", type="primary", use_container_width=True)

if st.session_state.pending_question:
    q = st.session_state.pending_question
    st.session_state.pending_question = ""
    st.session_state["_pending_stream"] = q
    st.session_state.messages.append({
        "role": "user",
        "content": q,
        "ts": datetime.now().strftime("%H:%M"),
    })
    st.rerun()


# ── Send & stream ─────────────────────────────────────────────────────────────
def send_query(question: str):
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": question,
        "ts": datetime.now().strftime("%H:%M"),
    })
    st.rerun()


def stream_response(question: str):
    """Call backend SSE stream, accumulate tokens, update UI live."""
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]  # exclude the user message just added
    ]

    routing_data = {}
    sql_data = None
    accumulated = ""
    metadata = {}

    # Streaming placeholder
    placeholder = st.empty()

    try:
        with requests.post(
            f"{BACKEND}/query",
            json={"question": question, "history": history},
            stream=True,
            timeout=120,
        ) as response:
            client = sseclient.SSEClient(response)

            for event in client.events():
                if not event.data:
                    continue
                try:
                    d = json.loads(event.data)
                except json.JSONDecodeError:
                    continue

                evt = d.get("event")

                if evt == "routing":
                    routing_data = d
                    if st.session_state.show_routing:
                        srcs = " → ".join(d.get("sources", []))
                        placeholder.markdown(
                            f'<div class="router-panel">'
                            f'<div class="router-step">🔀 ROUTING → {srcs}</div>'
                            f'{d.get("reasoning","")}'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

                elif evt == "sql":
                    sql_data = d.get("sql")

                elif d.get("done"):
                    metadata = d.get("metadata", {})
                    break

                elif "token" in d:
                    accumulated += d["token"]
                    clean = re.sub(r"\nMETADATA::\{.*\}", "", accumulated, flags=re.DOTALL).strip()
                    placeholder.markdown(
                        f'<div class="msg-streaming">'
                        f'<div style="color:#e3b341;font-size:11px;margin-bottom:6px">⚡ Generating...</div>'
                        f'{clean}▌'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

    except Exception as e:
        accumulated = f"⚠️ Stream error: {e}\n\nMake sure the backend is running: `uvicorn backend.main:app --reload`"
        metadata = {}

    placeholder.empty()

    # Finalise and store message
    clean_answer = re.sub(r"\nMETADATA::\{.*\}", "", accumulated, flags=re.DOTALL).strip()

    st.session_state.messages.append({
        "role": "assistant",
        "content": clean_answer,
        "sources_used": metadata.get("sources_used", routing_data.get("sources", [])),
        "confidence": metadata.get("confidence", "medium"),
        "disambiguation_notes": metadata.get("disambiguation_notes", ""),
        "routing": routing_data,
        "sql": sql_data,
        "ts": datetime.now().strftime("%H:%M"),
    })
    st.rerun()


# ── Trigger logic ─────────────────────────────────────────────────────────────
# Only fire when Send button is explicitly clicked OR a demo question was selected
if send and user_input.strip():
    q = user_input.strip()
    st.session_state["_pending_stream"] = q
    st.session_state.messages.append({
        "role": "user",
        "content": q,
        "ts": datetime.now().strftime("%H:%M"),
    })
    st.rerun()

elif st.session_state.get("_pending_stream"):
    q = st.session_state.pop("_pending_stream")
    stream_response(q)