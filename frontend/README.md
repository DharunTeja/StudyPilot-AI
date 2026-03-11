# StudyPilot AI Frontend

This is the React TypeScript frontend for the StudyPilot AI platform. It provides a beautiful, modern, and responsive user interface for uploading study materials, viewing AI-generated summaries and quizzes, and tracking learning progress.

## Tech Stack
- **Framework**: React 18, Vite
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Routing**: React Router DOM v6
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Animations**: Framer Motion

## Setup Instructions

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Environment Variables**
   Create a `.env` file in this directory and configure your backend API URL (if different from default):
   ```env
   VITE_API_URL=http://localhost:8000/api
   ```

3. **Start the Development Server**
   ```bash
   npm run dev
   ```
   The application will be available at `http://localhost:5173`.

## Features
- **Auth Flow**: Uses Supabase Auth through the backend API.
- **Dashboard**: Track your progress and view learning analytics.
- **Materials Management**: Upload documents (PDF, image, text) for AI processing.
- **AI Generation UI**: View interactive quizzes, flashcards, summaries, and personalized study plans.
