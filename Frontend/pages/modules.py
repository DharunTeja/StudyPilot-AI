import streamlit as st
import time
from datetime import timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="StudyPilot AI | Modules",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CONSTANTS ----------------
MCQ_TIME_LIMIT = 10 * 60        # 10 minutes (soft)
THEORY_TIME_LIMIT = 20 * 60     # 20 minutes (soft)
TOTAL_TIME_LIMIT = 30 * 60      # 30 minutes (hard)

# ---------------- TEMP MCQ GENERATOR ----------------
def generate_dummy_mcqs(topics):
    mcqs = []
    topic = topics[0] if topics else "this topic"

    for i in range(10):
        mcqs.append({
            "question": f"MCQ {i+1}: Which statement about {topic} is correct?",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option B"
        })
    return mcqs

# ---------------- TEMP THEORY GENERATOR ----------------
def generate_dummy_theory(topics):
    theory = []
    topic = topics[0] if topics else "this topic"

    for i in range(5):
        theory.append({
            "question": f"Theory {i+1}: Explain {topic} in your own words.",
            "expected_points": [
                "Definition",
                "Use cases",
                "Advantages"
            ]
        })
    return theory



# ---------------- SESSION STATE INIT ----------------
if "module_started" not in st.session_state:
    st.session_state.module_started = False

if "module_start_time" not in st.session_state:
    st.session_state.module_start_time = None

if "module_completed" not in st.session_state:
    st.session_state.module_completed = False

# ---------------- MCQ STATE ----------------
if "module_phase" not in st.session_state:
    st.session_state.module_phase = "intro"  
    # intro → mcq → theory → completed

if "mcqs" not in st.session_state:
    st.session_state.mcqs = []

if "mcq_answers" not in st.session_state:
    st.session_state.mcq_answers = {}  # {index: selected_option}

if "current_mcq" not in st.session_state:
    st.session_state.current_mcq = 0

if "mcq_submitted" not in st.session_state:
    st.session_state.mcq_submitted = False
    
# ---------------- THEORY STATE ----------------
if "theory_questions" not in st.session_state:
    st.session_state.theory_questions = []

if "theory_answers" not in st.session_state:
    st.session_state.theory_answers = {}  # {index: answer text}

if "current_theory" not in st.session_state:
    st.session_state.current_theory = 0

if "theory_submitted" not in st.session_state:
    st.session_state.theory_submitted = False



# Required shared state check
if "selected_day" not in st.session_state or st.session_state.selected_day is None:
    st.warning("No module selected. Please return to Study Plan.")
    st.stop()

selected = st.session_state.selected_day
day_label = selected["day"]
focus = selected["focus"]
concepts = selected.get("concepts", [])

# ---------------- RESET MODULE ----------------
def reset_module():
    st.session_state.module_started = False
    st.session_state.module_start_time = None
    st.session_state.module_completed = False
    st.experimental_rerun()

# ---------------- TIMER LOGIC ----------------
def get_time_remaining():
    elapsed = time.time() - st.session_state.module_start_time
    remaining = TOTAL_TIME_LIMIT - elapsed
    return max(0, int(remaining))

# ---------------- HEADER ----------------
st.markdown(f"## 🧠 {day_label} – {focus}")

# ==================================================
# STATE 1 — MODULE INTRO
# ==================================================
if not st.session_state.module_started:

    st.markdown("### 📘 Module Overview")
    st.write("**Topics Covered:**")
    for c in concepts:
        st.write(f"- {c}")

    st.markdown("### 📜 Rules & Regulations")
    st.info(
        """
        1. Total duration: **30 minutes**
        2. MCQs should be completed within first **10 minutes**
        3. Theory questions should be completed within remaining **20 minutes**
        4. Timer starts only after clicking **Start Module**
        5. If time runs out:
           - Your attempt is discarded
           - New questions are generated
           - You must restart the module
        6. Copy-paste or AI-generated answers may not be accepted
        7. Completing this module unlocks the **next day**
        """
    )

    if st.button("▶ Start Module"):
        st.session_state.module_started = True
        st.session_state.module_start_time = time.time()

        # Initialize MCQs
        st.session_state.mcqs = generate_dummy_mcqs(concepts)
        st.session_state.mcq_answers = {}
        st.session_state.current_mcq = 0
        st.session_state.mcq_submitted = False
        st.session_state.module_phase = "mcq"

        st.rerun()


# ==================================================
# STATE 2 — ACTIVE MODULE
# ==================================================
else:
    remaining = get_time_remaining()

    # Time up → reset
    if remaining <= 0:
        st.error("⛔ Time’s up! Module has been reset with new questions.")
        reset_module()

    # Timer display
    mins, secs = divmod(remaining, 60)
    st.markdown(
        f"### ⏳ Time Remaining: `{mins:02d}:{secs:02d}`"
    )

    # Progress (placeholder)
    st.progress(0.3)  # Will be dynamic later

    st.divider()

    # ==================================================
                    # MCQ MODULE
    # ==================================================
if st.session_state.module_phase == "mcq":

    mcqs = st.session_state.mcqs
    idx = st.session_state.current_mcq
    total = len(mcqs)
    q = mcqs[idx]

    st.markdown(f"### 📝 MCQ {idx + 1} / {total}")
    st.markdown(q["question"])

    # Answer options
    selected = st.session_state.mcq_answers.get(idx)
    choice = st.radio(
        "Choose one option:",
        q["options"],
        index=q["options"].index(selected) if selected in q["options"] else None,
        key=f"mcq_radio_{idx}"
    )

    if choice:
        st.session_state.mcq_answers[idx] = choice

    # Navigation buttons
    c1, c2, c3 = st.columns([1, 2, 1])

    with c1:
        if st.button("◀ Previous", disabled=idx == 0):
            st.session_state.current_mcq -= 1
            st.rerun()

    with c3:
        if st.button("Next ▶", disabled=idx == total - 1):
            st.session_state.current_mcq += 1
            st.rerun()

    # Question jump buttons
    st.markdown("#### Questions")
    q_cols = st.columns(10)
    for i in range(total):
        label = f"{i+1}"
        answered = i in st.session_state.mcq_answers
        btn_label = f"✔ {label}" if answered else label

        if q_cols[i].button(btn_label, key=f"jump_{i}"):
            st.session_state.current_mcq = i
            st.rerun()

    # Submit MCQs
    all_attempted = len(st.session_state.mcq_answers) == total

    st.divider()
    if st.button("Submit MCQs", disabled=not all_attempted):
        st.session_state.mcq_submitted = True

        # Initialize Theory Module
        st.session_state.theory_questions = generate_dummy_theory(concepts)
        st.session_state.theory_answers = {}
        st.session_state.current_theory = 0
        st.session_state.theory_submitted = False

        st.session_state.module_phase = "theory"
        st.success("MCQs submitted successfully! Theory section unlocked.")
        st.rerun()



    # ---------------- THEORY SECTION (Placeholder) ----------------
    st.markdown("### ✍️ Theory Questions (5)")
    st.write("_Theory questions will appear here in the next step._")

    st.divider()

    # ---------------- COMPLETE MODULE (TEMPORARY) ----------------
    st.warning(
        "⚠️ This is a temporary completion button.\n"
        "In the next step, completion will depend on MCQs + theory evaluation."
    )

    if st.button("✅ Complete Module (Simulate)"):
        st.session_state.module_completed = True

        # Mark day as completed
        if "day_progress" not in st.session_state:
            st.session_state.day_progress = {}

        st.session_state.day_progress[day_label] = "completed"

        st.success("🎉 Module completed successfully! Next day unlocked.")

        if st.button("← Back to Study Plan"):
            reset_module()
            st.switch_page("streamlit_app.py")


def generate_dummy_mcqs(topics):
    mcqs = []
    for i in range(10):
        mcqs.append({
            "question": f"MCQ {i+1}: Which statement about {topics[0] if topics else 'this topic'} is correct?",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option B"
        })
    return mcqs

# ==================================================
# THEORY MODULE
# ==================================================
if st.session_state.module_phase == "theory":

    theory = st.session_state.theory_questions
    idx = st.session_state.current_theory
    total = len(theory)
    q = theory[idx]

    st.markdown(f"### ✍️ Theory Question {idx + 1} / {total}")
    st.markdown(q["question"])

    # Answer box
    existing_answer = st.session_state.theory_answers.get(idx, "")
    answer = st.text_area(
        "Your Answer:",
        value=existing_answer,
        height=180,
        key=f"theory_text_{idx}"
    )

    st.session_state.theory_answers[idx] = answer

    # Navigation buttons
    c1, c2, c3 = st.columns([1, 2, 1])

    with c1:
        if st.button("◀ Previous", disabled=idx == 0):
            st.session_state.current_theory -= 1
            st.rerun()

    with c3:
        if st.button("Next ▶", disabled=idx == total - 1):
            st.session_state.current_theory += 1
            st.rerun()

    # Jump buttons
    st.markdown("#### Questions")
    t_cols = st.columns(5)
    for i in range(total):
        answered = i in st.session_state.theory_answers and st.session_state.theory_answers[i].strip() != ""
        label = f"✔ {i+1}" if answered else f"{i+1}"

        if t_cols[i].button(label, key=f"theory_jump_{i}"):
            st.session_state.current_theory = i
            st.rerun()

    # Submit Theory
    all_answered = (
        len(st.session_state.theory_answers) == total and
        all(v.strip() for v in st.session_state.theory_answers.values())
    )

    st.divider()
    if st.button("Submit Theory", disabled=not all_answered):
        st.session_state.theory_submitted = True
        st.session_state.module_phase = "completed"
        st.rerun()

# ==================================================
# MODULE COMPLETED
# ==================================================
if st.session_state.module_phase == "completed":

    st.success("🎉 Module completed successfully!")

    # Temporary evaluation (placeholder)
    mcq_score = len(st.session_state.mcq_answers)  # mock
    theory_score = len(st.session_state.theory_answers) * 2  # mock

    st.markdown("### 📊 Evaluation Summary")
    st.write(f"MCQs: {mcq_score} / 10")
    st.write(f"Theory: {theory_score} / 10")
    st.write("Originality: Medium (placeholder)")

    # Mark day completed
    day_label = selected["day"]
    if "day_progress" not in st.session_state:
        st.session_state.day_progress = {}

    st.session_state.day_progress[day_label] = "completed"

    st.success("🔓 Next day unlocked!")

    if st.button("← Back to Study Plan"):
        # Reset module state for next use
        st.session_state.module_started = False
        st.session_state.module_start_time = None
        st.session_state.module_phase = "intro"
        st.rerun()
        st.switch_page("streamlit_app.py")
