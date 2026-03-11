import streamlit as st
import os
import sys
import tempfile
from PIL import Image

# Add project root and backend to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__)) # This is project_root/Frontend
project_root = os.path.dirname(current_dir)
backend_path = os.path.join(project_root, "backend")

if project_root not in sys.path:
    sys.path.append(project_root)
if backend_path not in sys.path:
    sys.path.append(backend_path)

# Mock some settings or load from env if needed
try:
    from app.services.ai_engine import ai_engine
    from app.services.document_processor import DocumentProcessor
    from app.config import settings
except ImportError:
    st.error("Could not load backend services. Please ensure the backend directory structure is correct.")
    st.stop()

import asyncio

# Page Configuration
st.set_page_config(
    page_title="StudyPilot AI 🎓",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4F46E5;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        border: none;
    }
    .card {
        padding: 20px;
        border-radius: 15px;
        background-white: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .title-text {
        font-size: 3rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 10px;
    }
    .subtitle-text {
        font-size: 1.2rem;
        color: #64748b;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Helper for async functions
def run_async(func):
    return asyncio.run(func)

# Sidebar
with st.sidebar:
    st.title("🎓 StudyPilot AI")
    st.markdown("---")
    menu = st.radio(
        "Navigation",
        ["Dashboard", "Summarize", "Quiz Generator", "Flashcards", "Study Plan"]
    )
    st.markdown("---")
    st.info("StudyPilot AI uses Gemini 2.0 Flash to help you study smarter, not harder.")

# Main Header
st.markdown('<div class="title-text">StudyPilot AI 🎓</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Transform your study materials into structured learning resources.</div>', unsafe_allow_html=True)

if menu == "Dashboard":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Welcome to StudyPilot AI</h3>
            <p>Upload your textbooks, PDFs, or lecture notes and let AI do the heavy lifting.</p>
            <ul>
                <li>Summarize long chapters</li>
                <li>Generate practice quizzes</li>
                <li>Create revision flashcards</li>
                <li>Build personalized study plans</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.write("### Get Started")
        uploaded_file = st.file_uploader("Upload study material (PDF, Image, TXT)", type=["pdf", "png", "jpg", "jpeg", "txt"])
        
        if uploaded_file:
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            if st.button("Process Document"):
                with st.spinner("Extracting text and analyzing..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    try:
                        file_type = uploaded_file.name.split('.')[-1].lower()
                        text = DocumentProcessor.process_file(tmp_path, file_type)
                        st.session_state['extracted_text'] = text
                        st.session_state['file_name'] = uploaded_file.name
                        st.success("Document processed! Navigate to other tabs to generate content.")
                    except Exception as e:
                        st.error(f"Error processing document: {e}")
                    finally:
                        if os.path.exists(tmp_path):
                            os.remove(tmp_path)

elif menu == "Summarize":
    if 'extracted_text' not in st.session_state:
        st.warning("Please upload and process a document in the Dashboard first.")
    else:
        st.write(f"### Summarizing: {st.session_state['file_name']}")
        if st.button("Generate Summary"):
            with st.spinner("AI is thinking..."):
                summary = run_async(ai_engine.generate_summary(st.session_state['extracted_text']))
                st.markdown(summary)
                st.download_button("Download Summary", summary, file_name=f"summary_{st.session_state['file_name']}.md")

elif menu == "Quiz Generator":
    if 'extracted_text' not in st.session_state:
        st.warning("Please upload and process a document in the Dashboard first.")
    else:
        st.write(f"### Generate Quiz: {st.session_state['file_name']}")
        num_q = st.slider("Number of questions", 5, 20, 10)
        
        if st.button("Generate Quiz"):
            with st.spinner("Creating your quiz..."):
                quiz = run_async(ai_engine.generate_quiz(st.session_state['extracted_text'], num_questions=num_q))
                st.session_state['current_quiz'] = quiz
        
        if 'current_quiz' in st.session_state:
            for i, q in enumerate(st.session_state['current_quiz']):
                with st.expander(f"Q{i+1}: {q.get('question', 'N/A')}"):
                    if q.get('type') == 'mcq':
                        for opt in q.get('options', []):
                            st.write(f"- {opt}")
                        st.info(f"Correct Answer: {q.get('correct_answer')}")
                    else:
                        st.info(f"Correct Answer: {q.get('correct_answer')}")
                    st.write(f"*Explanation:* {q.get('explanation')}")

elif menu == "Flashcards":
    if 'extracted_text' not in st.session_state:
        st.warning("Please upload and process a document in the Dashboard first.")
    else:
        st.write(f"### Flashcards: {st.session_state['file_name']}")
        num_cards = st.slider("Number of flashcards", 5, 30, 15)
        
        if st.button("Generate Flashcards"):
            with st.spinner("Crafting flashcards..."):
                flashcards = run_async(ai_engine.generate_flashcards(st.session_state['extracted_text'], num_cards=num_cards))
                st.session_state['flashcards'] = flashcards
        
        if 'flashcards' in st.session_state:
            cols = st.columns(2)
            for i, card in enumerate(st.session_state['flashcards']):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; height: 150px; display: flex; flex-direction: column; justify-content: center; align-items: center; background: white; margin-bottom: 15px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                        <div style="font-weight: bold; color: #4F46E5; margin-bottom: 5px;">{card.get('category', 'General')}</div>
                        <div style="text-align: center;">{card.get('front')}</div>
                        <hr style="width: 80%; margin: 10px 0;">
                        <div style="color: #64748b; font-size: 0.9em; text-align: center;">{card.get('back')}</div>
                    </div>
                    """, unsafe_allow_html=True)

elif menu == "Study Plan":
    if 'extracted_text' not in st.session_state:
        st.warning("Please upload and process a document in the Dashboard first.")
    else:
        st.write(f"### AI Study Plan: {st.session_state['file_name']}")
        days = st.number_input("Study days", 1, 30, 7)
        
        if st.button("Generate Plan"):
            with st.spinner("Planning your success..."):
                plan = run_async(ai_engine.generate_study_plan(st.session_state['extracted_text'], available_days=days))
                st.session_state['study_plan'] = plan
        
        if 'study_plan' in st.session_state:
            plan = st.session_state['study_plan']
            st.subheader(plan.get('title', 'Study Plan'))
            st.write(plan.get('overview', ''))
            
            for day_plan in plan.get('daily_plans', []):
                with st.expander(f"Day {day_plan.get('day')}: {day_plan.get('title')}"):
                    st.write("**Topics:** " + ", ".join(day_plan.get('topics', [])))
                    st.write("**Objectives:** " + ", ".join(day_plan.get('objectives', [])))
                    st.write("**Activities:** " + ", ".join(day_plan.get('activities', [])))
                    st.info(f"⏱️ Estimated Time: {day_plan.get('estimated_time')}")
                    st.write(f"*Tips:* {day_plan.get('tips')}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>Built with ❤️ by StudyPilot AI Team | Powered by Gemini 2.0 Flash</p>", unsafe_allow_html=True)
