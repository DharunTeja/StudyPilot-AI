import streamlit as st
import requests
from datetime import date
from pathlib import Path
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import lightgrey

# ---------------- BACKEND CONFIG ----------------
BACKEND_URL = "http://127.0.0.1:5000/"

# ---------------- SESSION STATE ----------------
if "study_plan" not in st.session_state:
    st.session_state.study_plan = None
if "generated" not in st.session_state:
    st.session_state.generated = False
if "meta" not in st.session_state:
    st.session_state.meta = {}
# ---------------- MODULE PROGRESS STATE ----------------
if "day_progress" not in st.session_state:
    st.session_state.day_progress = {}  # e.g., {"Day 1": "completed"}

if "selected_day" not in st.session_state:
    st.session_state.selected_day = None


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="StudyPilot AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- LOAD CSS ----------------
css_path = Path(__file__).parent / "styles.css"
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- PDF GENERATOR ----------------
def generate_pdf(plan, meta):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setTitle(f"{meta['student_name']} Studyplan - {meta['subject']}")
    width, height = A4

    x = 40
    y = height - 40
    page = 1

    def watermark():
        c.saveState()
        c.setFont("Helvetica-Bold", 48)
        c.setFillColor(lightgrey)
        c.translate(width / 2, height / 2)
        c.rotate(45)
        c.drawCentredString(0, 0, "StudyPilot AI.pdf")
        c.restoreState()

    def footer():
        c.setFont("Helvetica", 9)
        c.setFillColor(lightgrey)
        c.drawCentredString(width / 2, 25, f"Page {page}")

    def new_page():
        nonlocal y, page
        footer()
        c.showPage()
        page += 1
        y = height - 40
        watermark()

    def line(text, bold=False, size=10):
        nonlocal y
        if y < 60:
            new_page()
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x, y, text)
        y -= 14

    watermark()

    c.setFont("Helvetica-Bold", 18)
    c.drawString(x, y, "STUDYPILOT AI – STUDY PLAN")
    y -= 26

    c.setFont("Helvetica", 12)
    c.drawString(x, y, f"Student Name: {meta['student_name']}")
    y -= 16
    c.drawString(x, y, f"Subject: {meta['subject']}")
    y -= 16
    c.drawString(x, y, f"Exam Date: {meta['exam_date']}")
    y -= 16
    c.drawString(x, y, f"Daily Study Hours: {meta['hours']}")
    y -= 22

    line("-" * 90)

    for day in plan:
        ta = day.get("time_allocation", {})

        line(day["day"], bold=True, size=12)
        line(f"Focus: {day['focus']}")
        line(f"Objective: {day['objective']}")

        line("Concepts:", bold=True)
        for cpt in day["concepts"]:
            line(f"- {cpt}")

        line("Activities:", bold=True)
        for act in day["activities"]:
            line(f"- {act}")

        concepts_m = ta.get("concepts_minutes", "—")
        practice_m = ta.get("practice_minutes", "—")
        revision_m = ta.get("revision_minutes", "—")

        line("Time Allocation:", bold=True)
        line(f"- Concepts: {concepts_m} min")
        line(f"- Practice: {practice_m} min")
        line(f"- Revision: {revision_m} min")


        line("-" * 90)

    footer()
    c.save()
    buffer.seek(0)
    return buffer

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>StudyPilot AI</h1>
    <p>Your personal exam command center</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT SECTION ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    student_name = st.text_input("👤 Student Name")
    subject = st.text_input("📘 Subject")

with c2:
    study_mode = st.selectbox("📖 Study Mode", [
        "Concept Learning", "Exam Revision", "Practice-Focused"
    ])
    exam_date = st.date_input("🗓 Exam Date")

hours = st.slider("⏱ Daily Study Hours", 1, 10, 2)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- GENERATE BUTTON ----------------
if st.button("🚀 Generate Study Plan"):
    if not student_name or not subject or exam_date <= date.today():
        st.warning("Please fill all details correctly.")
    else:
        with st.spinner("⏳ Generating your personalized study plan..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate-plan",
                    json={
                        "subject": subject,
                        "exam_date": str(exam_date),
                        "hours": hours,
                        "study_mode": study_mode
                    },
                    timeout=180
                )

                data = response.json()
                if "plan" in data:
                    st.session_state.study_plan = data
                    st.session_state.generated = True
                    st.session_state.meta = {
                        "student_name": student_name,
                        "subject": subject,
                        "exam_date": exam_date,
                        "hours": hours,
                        "study_mode": study_mode
                    }
                else:
                    st.error("Failed to generate study plan.")

            except requests.exceptions.ReadTimeout:
                st.error("Backend waking up. Please wait and try again.")
            except Exception as e:
                st.error(f"Error: {e}")

# ---------------- MAIN CONTENT ----------------
if st.session_state.generated:
    data = st.session_state.study_plan
    meta = st.session_state.meta

    # INSIGHTS
    st.markdown("## 📊 Insights")
    days_left = (meta["exam_date"] - date.today()).days

    a, b, c = st.columns(3)
    a.markdown(f'<div class="metric">📅<br><b>{days_left}</b><br>Days Left</div>', unsafe_allow_html=True)
    b.markdown(f'<div class="metric">📖<br><b>{meta["study_mode"]}</b></div>', unsafe_allow_html=True)
    c.markdown(f'<div class="metric">⏱<br><b>{meta["hours"]} hrs/day</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # SMART BREAK
    st.markdown("## ☕ Smart Break")
    if meta["hours"] <= 3:
        st.info("Light breaks • 5–10 min every hour")
    elif meta["hours"] <= 6:
        st.info("Pomodoro • 25 min study + 5 min break")
    else:
        st.info("Deep focus • 50 min study + 10 min break")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- STUDY PLAN ----------------
    st.markdown("## 🧠 Study Plan")

    for idx, day in enumerate(data["plan"]):
        day_label = day["day"]

        # Lock logic (same as before)
        if idx == 0:
            unlocked = True
        else:
            prev_day = data["plan"][idx - 1]["day"]
            unlocked = st.session_state.day_progress.get(prev_day) == "completed"

        status = st.session_state.day_progress.get(day_label)

        # Accordion
        with st.expander(f"{day_label} – {day['focus']}"):
            if status == "completed":
                st.success("✅ Module completed")

            if unlocked:
                if st.button(
                    "🔓 View Module",
                    key=f"view_{idx}"
                ):
                    st.session_state.selected_day = {
                        "day": day_label,
                        "focus": day["focus"],
                        "concepts": day.get("concepts", []),
                        "index": idx
                    }
                    st.switch_page("pages/modules.py")
            else:
                st.button(
                    "🔒 Locked",
                    disabled=True,
                    key=f"locked_{idx}"
                )

    # DOWNLOAD PDF
    st.markdown("## 📕 Download PDF")
    pdf = generate_pdf(data["plan"], meta)
    st.download_button(
        "Download Study Plan (PDF)",
        data=pdf,
        file_name=f"{meta['student_name']} Studyplan - {meta['subject']}.pdf",
        mime="application/pdf"
    )

# ---------------- FOOTER ----------------
st.markdown(
    '<div class="footer">Built by <b>TriumphCoders</b> • Vibe Hack 2.0</div>',
    unsafe_allow_html=True
)
