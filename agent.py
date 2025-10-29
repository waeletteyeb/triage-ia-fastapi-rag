# agent.py
# Streamlit Frontend for AI Triage System

import streamlit as st
import requests
import matplotlib.pyplot as plt
import os
API_URL = os.getenv("API_URL", "http://localhost:8000")



st.set_page_config(
    page_title="AI Triage Assistant",
    page_icon="🩺",
    layout="wide",
)

st.title("🩺 AI Triage Assistant")
st.markdown("Upload a report or enter symptoms to get triage results and recommendations.")

# =========================
# Helper: Score Circle
# =========================
def render_score_circle(level: str):
    """Render a circular gauge with transparent background and label under it."""
    levels = {
        "Level 1": ("Level 1 - Critical", "red", 1.0),
        "Level 2": ("Level 2 - High", "orange", 0.8),
        "Level 3": ("Level 3 - Moderate", "gold", 0.6),
        "Level 4": ("Level 4 - Low", "green", 0.4),
        "Level 5": ("Level 5 - Minimal", "lightgrey", 0.2),
        "Unknown": ("Unknown", "grey", 0.0),
    }
    label, color, value = levels.get(level, levels["Unknown"])

    fig, ax = plt.subplots(figsize=(1.8, 1.8), facecolor="none")
    ax.pie(
        [value, 1 - value],
        colors=[color, "none"],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.3, "edgecolor": "none"},
    )

    # Label under circle instead of inside
    ax.text(0, -1.2, label, ha="center", va="center", fontsize=10, weight="bold" , color="white")

    ax.set(aspect="equal")
    fig.patch.set_alpha(0.0)
    st.pyplot(fig, transparent=True)


# =========================
# Input Section
# =========================
st.subheader("📥 Patient Input")

patient_text = st.text_area("Enter patient symptoms or notes:")
uploaded_file = st.file_uploader("Or upload a report (.txt or .pdf)", type=["txt", "pdf"])

if "triage_result" not in st.session_state:
    st.session_state.triage_result = None

if st.button("Run Triage"):
    if uploaded_file:
        files = {"file": uploaded_file.getvalue()}
        resp = requests.post(f"{API_URL}/triage-upload", files={"file": uploaded_file})
    elif patient_text.strip():
        resp = requests.post(f"{API_URL}/triage", json={"text": patient_text})
    else:
        st.error("Please enter text or upload a file.")
        resp = None

    if resp and resp.status_code == 200:
        st.session_state.triage_result = resp.json()
    elif resp is not None:
        st.error(f"Triage failed: {resp.text}")

# =========================
# Triage Result
# =========================
if st.session_state.triage_result:
    triage = st.session_state.triage_result
    st.subheader("📊 Triage Result")

    col1, col2 = st.columns([1, 3])

    with col1:
        render_score_circle(triage.get("triage_level", "Unknown"))

    with col2:
        st.markdown(
            f"""
            <div style="padding: 1em; border-radius: 8px; background-color: #1e1e1e; margin-bottom: 1em; color: #f0f0f0;">
            <h4>📝 Explanation</h4>
            <p>{triage.get("explanation", "No explanation provided.")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        recs = triage.get("recommendations", [])
        if recs:
            st.markdown("### ✅ Recommendations")
            for r in recs:
                st.markdown(f"- {r}")

# =========================
# Chatbot
# =========================
st.subheader("💬 Chat with Assistant")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.text_input("Ask a question about the triage result:")
if st.button("Send"):
    if user_query.strip():
        history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
        history.append({"role": "system", "content": f"triage_result: {st.session_state.triage_result}"})
        payload = {"history": history, "query": user_query}
        resp = requests.post(f"{API_URL}/chat", json=payload)

        if resp.status_code == 200:
            reply = resp.json().get("reply", "No response.")
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        else:
            st.error("Chat failed.")

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"<div style='background:#333;padding:6px;border-radius:5px;margin:4px 0;'>👤 <b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div style='background:#222;padding:6px;border-radius:5px;margin:4px 0;'>🤖 <b>Assistant:</b> {msg['content']}</div>", unsafe_allow_html=True)

# =========================
# Handoff to n8n
# =========================
st.subheader("🔗 Send to Operations Agent (n8n)")
st.markdown("Enter patient details and instruction for n8n handoff:")

n8n_name = st.text_input("Patient Name")
n8n_email = st.text_input("Patient Email")
instruction = st.text_area("Instruction (e.g., 'book a doctor appointment')")

if st.button("Send to n8n"):
    if st.session_state.triage_result:
        payload = {
            "patient": {
                "name": n8n_name,
                "email": n8n_email,
                "notes": patient_text,
            },
            "triage": st.session_state.triage_result,
            "instruction": instruction,
        }
        resp = requests.post(f"{API_URL}/handoff-n8n", json=payload)
        if resp.status_code == 200:
            st.success("✅ Sent to n8n successfully.")
        else:
            st.error(f"n8n handoff failed: {resp.text}")
