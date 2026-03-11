# StudyPilot AI 🎓

StudyPilot AI is an intelligent academic assistant designed to help students convert learning materials into structured study content such as summaries, quizzes, flashcards, and learning plans using Artificial Intelligence.

## 🚀 Features

- **Smart Content Processing**: Upload PDFs, images, or text and extract clean content.
- **AI Summarization**: Automatically generate concise and clear summaries from long materials.
- **Adaptive Quizzes**: Generate MCQs, True/False, and Short Answer questions to test your knowledge.
- **Flashcard Generation**: Instantly create revision flashcards for key terms and definitions.
- **Personalized Study Plans**: Get a structured roadmap for your studying over multiple days.
- **Learning Analytics**: Track your progress, study streaks, weak topics, and study time.

## 🏗️ Architecture

- **Frontend**: React (TypeScript), Vite, Tailwind CSS, Framer Motion
- **Backend**: Python, FastAPI
- **Database & Auth**: Supabase (PostgreSQL, Supabase Auth)
- **AI Engine**: Google Gemini API (gemini-2.0-flash)
- **Document Processing**: PyPDF2, Pytesseract (OCR)

## 📁 Repository Structure

- `/frontend` - React TypeScript application
- `/backend` - FastAPI Python server
- `Algorithm Explanation.txt` - Step-by-step logic of the AI processing
- `System Architecture Explanation.txt` - High-level system design
- `Implementation Roadmap.txt` - Development phases
- `Project Description.txt` - Core concept and problem statement

## 🏁 Getting Started

### Prerequisites
- Node.js (v18+)
- Python 3.10+
- Supabase Project (Database & Auth)
- Google Gemini API Key

### Setting up the Database
1. Create a project in [Supabase](https://supabase.com).
2. Go to the SQL Editor and paste the contents of `backend/supabase_schema.sql` to create the required tables and security policies.

### Running the Backend
1. Navigate to the `backend` directory: `cd backend`
2. Configure your environment variables in a `.env` file (see `backend/.env.example`).
3. Follow the instructions in the [Backend README](./backend/README.md) to install dependencies and start the server.

### Running the Frontend
1. Navigate to the `frontend` directory: `cd frontend`
2. Follow the instructions in the [Frontend README](./frontend/README.md) to install dependencies and start the UI.
