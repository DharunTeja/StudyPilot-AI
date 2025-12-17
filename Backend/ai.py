from groq import Groq
import json
import os
from dotenv import load_dotenv
from datetime import date, timedelta

# ---------------- ENV SETUP ----------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- MAIN FUNCTION ----------------
def generate_study_plan(subject, exam_date, hours, study_mode):
    today = date.today()
    exam = date.fromisoformat(exam_date)
    days_left = (exam - today).days

    if days_left <= 0:
        return {"plan": []}

    total_minutes = hours * 60

    # ---------------- PROMPT ----------------
    prompt = f"""
You are an expert academic study planner.

Generate study content ONLY. Do NOT number days.
Return ONLY valid JSON. No markdown. No explanations.

SUBJECT: {subject}
STUDY MODE: {study_mode}
TOTAL DAYS: {days_left}
DAILY STUDY MINUTES: {total_minutes}

RULES:
- Generate exactly {days_left} day objects
- Each object represents ONE day of study
- Do NOT include dates or day numbers
- Focus on logical topic progression
- Use realistic time allocation

FORMAT:
{{
  "plan": [
    {{
      "focus": "Topic name",
      "objective": "Learning goal",
      "concepts": ["Concept A", "Concept B"],
      "activities": ["Read", "Practice", "Recall"],
      "time_allocation": {{
        "concepts_minutes": 60,
        "practice_minutes": 60,
        "revision_minutes": 30
      }},
      "outcome_check": "Verification method"
    }}
  ]
}}
"""

    # ---------------- AI CALL ----------------
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You output strict JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    try:
        raw_plan = json.loads(response.choices[0].message.content)
        ai_days = raw_plan.get("plan", [])
    except Exception:
        return {"plan": []}

    # ---------------- FORCE SEQUENTIAL DAYS ----------------
    final_plan = []
    current_date = today

    for idx in range(days_left):
        # If AI gave fewer days, safely reuse last topic
        ai_day = ai_days[idx] if idx < len(ai_days) else ai_days[-1]

        day_number = idx + 1
        day_data = {
            "day": f"Day {day_number} ({current_date.isoformat()})",
            "focus": ai_day.get("focus", "Revision / Practice"),
            "objective": ai_day.get("objective", ""),
            "concepts": ai_day.get("concepts", []),
            "activities": ai_day.get("activities", []),
            "time_allocation": ai_day.get("time_allocation", {
                "concepts_minutes": total_minutes // 2,
                "practice_minutes": total_minutes // 3,
                "revision_minutes": total_minutes // 6
            }),
            "outcome_check": ai_day.get("outcome_check", "")
        }

        # ---------------- REVISION LOGIC ----------------
        if idx >= days_left - 2:
            day_data["revision_type"] = "Final Revision"
        elif (idx + 1) % 3 == 0:
            day_data["revision_type"] = "Micro Revision"
        else:
            day_data["revision_type"] = "Study Day"

        final_plan.append(day_data)
        current_date += timedelta(days=1)

    return {"plan": final_plan}
