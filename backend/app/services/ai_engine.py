import json
import re
from typing import Optional, List
import google.generativeai as genai
from app.config import settings


class AIEngine:
    """AI-powered content generation engine using Google Gemini."""

    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None

    def _safe_parse_json(self, text: str) -> dict | list:
        """Safely parse JSON from AI response, handling markdown code blocks."""
        # Remove markdown code blocks if present
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON in the response
            json_match = re.search(r'[\[{].*[\]}]', text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            return {}

    async def generate_summary(self, text: str) -> str:
        """Generate a concise summary of the given text."""
        if not self.model:
            return self._fallback_summary(text)

        prompt = f"""You are an expert academic summarizer. Create a comprehensive yet concise summary of the following study material.

The summary should:
1. Capture all key concepts and main ideas
2. Be organized with clear headings using markdown (##)
3. Include bullet points for important details
4. Highlight key terms in **bold**
5. Be around 300-500 words

Study Material:
{text[:8000]}

Provide the summary in clean markdown format."""

        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_summary(text)

    async def generate_quiz(self, text: str, num_questions: int = 10) -> list:
        """Generate quiz questions from the study material."""
        if not self.model:
            return self._fallback_quiz(text)

        prompt = f"""You are an expert quiz creator for academic content. Generate exactly {num_questions} quiz questions from the following study material.

Create a mix of:
- Multiple Choice Questions (MCQ) with 4 options
- True/False questions
- Short Answer questions

Return ONLY a valid JSON array with this exact format:
[
  {{
    "type": "mcq",
    "question": "What is...?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "explanation": "Brief explanation why this is correct"
  }},
  {{
    "type": "true_false",
    "question": "Statement to evaluate",
    "correct_answer": "True",
    "explanation": "Brief explanation"
  }},
  {{
    "type": "short_answer",
    "question": "Explain...",
    "correct_answer": "Expected key points in the answer",
    "explanation": "Detailed correct answer"
  }}
]

Study Material:
{text[:8000]}

Return ONLY valid JSON, no other text."""

        try:
            response = await self.model.generate_content_async(prompt)
            result = self._safe_parse_json(response.text)
            if isinstance(result, list):
                return result
            return self._fallback_quiz(text)
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_quiz(text)

    async def generate_flashcards(self, text: str, num_cards: int = 15) -> list:
        """Generate flashcards from the study material."""
        if not self.model:
            return self._fallback_flashcards(text)

        prompt = f"""You are an expert educator. Create exactly {num_cards} flashcards from the following study material.

Each flashcard should have:
- A clear, concise front (question/term)
- A comprehensive back (answer/definition)

Return ONLY a valid JSON array with this format:
[
  {{
    "front": "Term or Question",
    "back": "Definition or Answer",
    "category": "Topic Category"
  }}
]

Study Material:
{text[:8000]}

Return ONLY valid JSON, no other text."""

        try:
            response = await self.model.generate_content_async(prompt)
            result = self._safe_parse_json(response.text)
            if isinstance(result, list):
                return result
            return self._fallback_flashcards(text)
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_flashcards(text)

    async def generate_study_plan(self, text: str, available_days: int = 7) -> dict:
        """Generate a personalized study plan from the material."""
        if not self.model:
            return self._fallback_study_plan(text)

        prompt = f"""You are an expert academic planner. Create a detailed {available_days}-day study plan based on the following material.

The plan should:
1. Break content into manageable daily topics
2. Include specific learning objectives for each day
3. Suggest study techniques for each topic
4. Include revision sessions
5. Estimate time needed per topic

Return ONLY a valid JSON object with this format:
{{
  "title": "Study Plan Title",
  "total_days": {available_days},
  "overview": "Brief overview of the plan",
  "daily_plans": [
    {{
      "day": 1,
      "title": "Day 1 Title",
      "topics": ["Topic 1", "Topic 2"],
      "objectives": ["Objective 1", "Objective 2"],
      "activities": ["Read chapter X", "Practice problems"],
      "estimated_time": "2 hours",
      "tips": "Study tip for this day"
    }}
  ],
  "key_topics": ["Main Topic 1", "Main Topic 2"],
  "recommended_resources": ["Resource 1", "Resource 2"]
}}

Study Material:
{text[:8000]}

Return ONLY valid JSON, no other text."""

        try:
            response = await self.model.generate_content_async(prompt)
            result = self._safe_parse_json(response.text)
            if isinstance(result, dict):
                return result
            return self._fallback_study_plan(text)
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_study_plan(text)

    async def extract_key_concepts(self, text: str) -> list:
        """Extract key concepts and topics from the text."""
        if not self.model:
            return self._fallback_key_concepts(text)

        prompt = f"""Extract the top 10-15 key concepts, terms, and topics from this study material.

Return ONLY a valid JSON array of strings:
["Concept 1", "Concept 2", "Concept 3"]

Study Material:
{text[:6000]}

Return ONLY valid JSON, no other text."""

        try:
            response = await self.model.generate_content_async(prompt)
            result = self._safe_parse_json(response.text)
            if isinstance(result, list):
                return result
            return self._fallback_key_concepts(text)
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_key_concepts(text)

    # ---- Fallback methods (when API key is not available) ----

    def _fallback_summary(self, text: str) -> str:
        """Generate a basic summary without AI."""
        sentences = text.split('.')
        key_sentences = sentences[:min(10, len(sentences))]
        summary = '. '.join(s.strip() for s in key_sentences if s.strip())
        return f"## Summary\n\n{summary}.\n\n*Note: This is a basic summary. Configure your Gemini API key for AI-powered summaries.*"

    def _fallback_quiz(self, text: str) -> list:
        """Generate basic quiz without AI."""
        return [
            {
                "type": "short_answer",
                "question": "Summarize the main topic of this study material.",
                "correct_answer": "Refer to the study material for the answer.",
                "explanation": "Review the material to identify the main theme."
            },
            {
                "type": "true_false",
                "question": "This material covers a single topic only.",
                "correct_answer": "False",
                "explanation": "Most study materials cover multiple related topics."
            }
        ]

    def _fallback_flashcards(self, text: str) -> list:
        """Generate basic flashcards without AI."""
        words = text.split()
        return [
            {
                "front": "What is the main topic of this material?",
                "back": " ".join(words[:30]) + "...",
                "category": "General"
            }
        ]

    def _fallback_study_plan(self, text: str) -> dict:
        """Generate basic study plan without AI."""
        return {
            "title": "Study Plan",
            "total_days": 7,
            "overview": "A basic 7-day study plan for your material.",
            "daily_plans": [
                {
                    "day": i,
                    "title": f"Day {i}",
                    "topics": ["Review material"],
                    "objectives": ["Understand key concepts"],
                    "activities": ["Read and take notes"],
                    "estimated_time": "1-2 hours",
                    "tips": "Focus on understanding rather than memorizing"
                }
                for i in range(1, 8)
            ],
            "key_topics": ["Main concepts"],
            "recommended_resources": ["Your uploaded material"]
        }

    def _fallback_key_concepts(self, text: str) -> list:
        """Extract basic key concepts without AI."""
        words = text.split()
        # Get unique longer words as potential key terms
        key_words = list(set(w.strip('.,;:!?') for w in words if len(w) > 6))
        return key_words[:10] if key_words else ["General concepts"]


# Singleton instance
ai_engine = AIEngine()
