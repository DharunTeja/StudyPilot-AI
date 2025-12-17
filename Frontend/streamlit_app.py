import streamlit as st
import requests
from datetime import date
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="StudyPilot AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- LOAD EXTERNAL CSS ----------------
css_path = Path(__file__).parent / "styles.css"
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>StudyPilot AI</h1>
    <p>Your personal exam command center</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT PANEL ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    subject = st.text_input("📘 Subject", placeholder="Data Structures")

with c2:
    study_mode = st.selectbox(
        "📖 Study Mode",
        ["Concept Learning", "Exam Revision", "Practice-Focused"]
    )

with c3:
    exam_date = st.date_input("🗓 Exam Date")

hours = st.slider("⏱ Daily Study Hours", 1, 10, 2)
generate = st.button("🚀 Generate Study Plan")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ACTION ----------------
if generate:
    if not subject or exam_date <= date.today():
        st.warning("Please enter valid details.")
        st.stop()

    with st.spinner("Building your study command center..."):
        response = requests.post(
            "https://studypilot-ai.onrender.com/generate-plan",
            json={
                "subject": subject,
                "exam_date": str(exam_date),
                "hours": hours,
                "study_mode": study_mode
            },
            timeout=60
        )
        data = response.json()

    if "plan" not in data:
        st.error("Failed to generate plan.")
        st.stop()

    # ---------------- STATUS BAR ----------------
    days_left = (exam_date - date.today()).days

    st.markdown('<div class="card">', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)

    m1.markdown(f'<div class="metric">📅<br><b>{days_left}</b><br>Days Left</div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric">📖<br><b>{study_mode}</b></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric">⏱<br><b>{hours} hrs/day</b></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- SMART BREAK ----------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ☕ Smart Break Strategy")

    if hours <= 3:
        st.info("Light breaks • 5–10 min every hour")
    elif hours <= 6:
        st.info("Pomodoro • 25 min study + 5 min break")
    else:
        st.info("Deep focus • 50 min study + 10 min break")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- STUDY TIMELINE ----------------
    st.markdown("## 🧠 Study Timeline")

    text_lines = []

    for day in data["plan"]:
        revision = day.get("revision_type", "")
        is_revision = "Revision" in revision

        timeline_class = "timeline-day timeline-revision" if is_revision else "timeline-day"
        tag_class = "tag-revision" if is_revision else "tag-study"
        tag_text = revision if revision else "Study Day"

        with st.expander(f"{day.get('day')} • {day.get('focus')}"):
            st.markdown(f'<div class="{timeline_class}">', unsafe_allow_html=True)
            st.markdown(f'<span class="tag {tag_class}">{tag_text}</span>', unsafe_allow_html=True)

            st.markdown(f"**Objective:** {day.get('objective')}")
            st.markdown("**Concepts:**")
            for c in day.get("concepts", []):
                st.write(f"- {c}")

            ta = day.get("time_allocation", {})
            st.markdown(
                f"⏱ {ta.get('concepts_minutes','—')}m concepts | "
                f"{ta.get('practice_minutes','—')}m practice | "
                f"{ta.get('revision_minutes','—')}m revision"
            )

            st.markdown("**Activities:**")
            for a in day.get("activities", []):
                st.write(f"- {a}")

            st.markdown(f"**Outcome Check:** {day.get('outcome_check')}")
            st.markdown('</div>', unsafe_allow_html=True)

            text_lines.append(f"{day.get('day')} - {day.get('focus')}")

    # ---------------- DOWNLOAD ----------------
    st.download_button(
        "📥 Download Study Plan",
        data="\n".join(text_lines),
        file_name="StudyPilot_Study_Plan.txt"
    )

# ---------------- FOOTER ----------------
st.markdown(
    '<div class="footer">Built by <b>TriumphCoders</b> • Vibe Hack 2.0</div>',
    unsafe_allow_html=True
)
