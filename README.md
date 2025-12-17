# 📘 StudyPilot AI  
**Your Intelligent Co-Pilot for Structured, Stress-Free Exam Preparation**

---

## 🚀 Overview

**StudyPilot AI** is an AI-powered study planning assistant that generates **personalized, science-based study schedules** for students preparing for exams.

Unlike generic timetables, StudyPilot AI applies **time allocation logic, spaced repetition, and adaptive study modes** to help students study effectively, reduce overwhelm, and improve retention.

Built as part of **Vibe Hack 2.0 (Open Innovation)** by **TriumphCoders**.

---

## 🎯 Problem Statement

Students often struggle not with *what* to study, but with:

- Planning realistic daily schedules  
- Managing time efficiently  
- Knowing when and how to revise  
- Avoiding burnout close to exams  

Most existing solutions provide static timetables that ignore learning science and individual preferences.

---

## 💡 Solution

StudyPilot AI solves this by generating a **day-wise, outcome-driven study plan** that:

- Starts from **today’s date**, not arbitrary timelines  
- Adapts to different **study modes**  
- Allocates time scientifically  
- Includes **micro-revisions** and **final revisions**  
- Provides clear daily objectives and outcome checks  

---

## ✨ Key Features

### 🧠 Intelligent Study Planning
- Personalized plan based on subject, exam date, and daily availability
- Starts from the **current day** and ends exactly on the exam date

### 📖 Study Mode Toggle
Choose how you want to prepare:
- **Concept Learning** – focus on understanding fundamentals  
- **Exam Revision** – summaries, recall, quick notes  
- **Practice-Focused** – problem solving and mock tests  

### ⏱️ Time Allocation Logic
Each day’s study time is split intelligently:
- 40% Concepts  
- 40% Practice  
- 20% Revision  

This removes guesswork and improves consistency.

### 🔁 Micro-Revision System
- **Every 3rd day** includes a micro-revision  
- **Last 2 days** are reserved for final revision  
- Implements spaced repetition for better retention

### 🎯 Outcome-Driven Daily Structure
Each day includes:
- Objective  
- Concepts to cover  
- Activities  
- Time breakdown  
- Revision type  
- Outcome check  

### ☕ Smart Break Suggestions
Break strategies based on daily study hours:
- Light breaks  
- Pomodoro technique  
- Deep focus cycles  

### 📥 Downloadable Study Plan
- Export the complete plan for offline use  
- Useful for real-world adoption

### 🌙 Premium Dark UI
- Modern, eye-friendly dark theme  
- Glassmorphism-style cards  
- Clean, distraction-free layout

---

## 🛠️ Tech Stack

### Frontend
- **Streamlit**
- Custom CSS (dark theme, glass UI)

### Backend
- **Python**
- **Flask**

### AI
- **Groq API**
- **LLaMA-3.1-8B-Instant**

---

## 🧩 System Architecture

User (Streamlit UI)
↓
Flask Backend
↓
Groq LLM (AI)
↓
Structured Study Plan
↓
Streamlit Rendering 


---

## 🧪 How It Works

1. User enters subject, exam date, daily study hours, and study mode  
2. Backend calculates valid study window (today → exam date)  
3. AI generates a structured, day-wise plan using learning science rules  
4. Backend normalizes and validates AI output  
5. Frontend displays a polished, interactive study plan  

---

## ▶️ Running the Project Locally

### Prerequisites
- Python 3.9+
- Groq API Key

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py

### Frontend Setup
``` bash
cd frontend
pip install -r requirements.txt
python -m streamlit run streamlit_app.py

🔐 Environment Variables

Create a .env file inside the backend folder:

GROQ_API_KEY=your_groq_api_key_here


#🏆 Hackathon Details

Event: Vibe Hack 2.0

Theme: Open Innovation

Mode: Virtual

Team: TriumphCoders

#🌱 Future Enhancements

Weekly summary view

Today’s focus widget

Progress persistence

Calendar integration

Multi-subject planning

#📌 Why StudyPilot AI Stands Out

Applies learning science, not just AI

Focuses on real student problems

Clean architecture and defensive AI handling

Product-ready UI and UX

Built end-to-end within hackathon constraints

#👨‍💻 Team

TriumphCoders
Built with passion during Vibe Hack 2.0 🚀

#📜 License

This project is for educational and hackathon use.