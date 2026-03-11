# StudyPilot AI Backend

This is the Python FastAPI backend for StudyPilot AI. It handles file parsing (PDF, OCR), AI generation using Google Gemini, and database interactions using Supabase.

## Tech Stack
- **Framework**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **AI Model**: Google Generative AI (Gemini 2.0 Flash)
- **Document Processing**: PyPDF2, Pytesseract, Pillow
- **Authentication**: JWT & Supabase Auth

## Setup Instructions

1. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**
   Copy `.env.example` to `.env` and fill in your credentials:
   ```env
   SUPABASE_URL=YOUR_SUPABASE_PROJECT_URL
   SUPABASE_KEY=YOUR_SUPABASE_ANON_KEY
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY
   ```

4. **Initialize Database**
   Copy the contents of `supabase_schema.sql` and run it in your Supabase project's SQL Editor to set up the necessary tables, triggers, and Row Level Security (RLS) policies.

5. **Run the Server**
   ```bash
   python main.py
   # Or using uvicorn directly:
   # uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   The API will be available at `http://localhost:8000`. You can view the automatically generated Swagger documentation at `http://localhost:8000/docs`.

## Key Modules
- `/app/routes/materials.py`: Handles file uploads and document processing.
- `/app/routes/ai.py`: Connects processed documents to the Gemini AI to generate summaries, quizzes, and flashcards.
- `/app/routes/progress.py`: Tracks student performance and calculates analytics.
- `/app/services/document_processor.py`: Uses standard libraries to extract clean text from PDFs and images.
