from datetime import datetime, timedelta
from typing import List, Optional


class AnalyticsService:
    """Service for computing learning analytics and progress insights."""

    @staticmethod
    def calculate_study_streak(activities: List[dict]) -> int:
        """Calculate consecutive study days streak."""
        if not activities:
            return 0

        # Get unique dates with activity
        dates = set()
        for activity in activities:
            created = activity.get("created_at")
            if isinstance(created, datetime):
                dates.add(created.date())
            elif isinstance(created, str):
                try:
                    dates.add(datetime.fromisoformat(created).date())
                except ValueError:
                    pass

        if not dates:
            return 0

        # Sort dates in reverse order
        sorted_dates = sorted(dates, reverse=True)
        today = datetime.utcnow().date()

        # Check if the most recent activity is today or yesterday
        if sorted_dates[0] < today - timedelta(days=1):
            return 0

        streak = 1
        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] == sorted_dates[i - 1] - timedelta(days=1):
                streak += 1
            else:
                break

        return streak

    @staticmethod
    def identify_weak_topics(quiz_results: List[dict]) -> List[str]:
        """Identify topics where the student needs improvement."""
        topic_scores = {}

        for result in quiz_results:
            topic = result.get("subject", "General")
            score = result.get("score", 0)

            if topic not in topic_scores:
                topic_scores[topic] = {"total": 0, "count": 0}

            topic_scores[topic]["total"] += score
            topic_scores[topic]["count"] += 1

        weak_topics = []
        for topic, data in topic_scores.items():
            avg_score = data["total"] / data["count"] if data["count"] > 0 else 0
            if avg_score < 0.6:  # Below 60% threshold
                weak_topics.append(topic)

        return weak_topics

    @staticmethod
    def identify_strong_topics(quiz_results: List[dict]) -> List[str]:
        """Identify topics where the student excels."""
        topic_scores = {}

        for result in quiz_results:
            topic = result.get("subject", "General")
            score = result.get("score", 0)

            if topic not in topic_scores:
                topic_scores[topic] = {"total": 0, "count": 0}

            topic_scores[topic]["total"] += score
            topic_scores[topic]["count"] += 1

        strong_topics = []
        for topic, data in topic_scores.items():
            avg_score = data["total"] / data["count"] if data["count"] > 0 else 0
            if avg_score >= 0.8:  # 80% and above
                strong_topics.append(topic)

        return strong_topics

    @staticmethod
    def calculate_average_score(quiz_results: List[dict]) -> float:
        """Calculate overall average quiz score."""
        if not quiz_results:
            return 0.0

        total = sum(r.get("score", 0) for r in quiz_results)
        return round(total / len(quiz_results) * 100, 1)

    @staticmethod
    def get_study_time_breakdown(activities: List[dict]) -> dict:
        """Get study time breakdown by day of week."""
        breakdown = {
            "Monday": 0, "Tuesday": 0, "Wednesday": 0,
            "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0
        }

        for activity in activities:
            created = activity.get("created_at")
            time_spent = activity.get("time_spent", 0)

            if isinstance(created, datetime):
                day_name = created.strftime("%A")
            elif isinstance(created, str):
                try:
                    day_name = datetime.fromisoformat(created).strftime("%A")
                except ValueError:
                    continue
            else:
                continue

            if day_name in breakdown:
                breakdown[day_name] += time_spent // 60  # Convert to minutes

        return breakdown

    @staticmethod
    def generate_recommendations(
        weak_topics: List[str],
        strong_topics: List[str],
        study_streak: int,
        average_score: float
    ) -> List[str]:
        """Generate personalized study recommendations."""
        recommendations = []

        if weak_topics:
            recommendations.append(
                f"📚 Focus on improving: {', '.join(weak_topics[:3])}. "
                "Try reviewing flashcards and taking practice quizzes on these topics."
            )

        if strong_topics:
            recommendations.append(
                f"🌟 Great progress in: {', '.join(strong_topics[:3])}! "
                "Consider teaching these topics to reinforce your understanding."
            )

        if study_streak >= 7:
            recommendations.append(
                f"🔥 Amazing {study_streak}-day study streak! Keep it up!"
            )
        elif study_streak >= 3:
            recommendations.append(
                f"👍 Good {study_streak}-day streak. Stay consistent!"
            )
        else:
            recommendations.append(
                "💪 Try to study every day to build a habit. Consistency is key!"
            )

        if average_score >= 80:
            recommendations.append(
                "🎯 Your average score is excellent! Try more challenging material."
            )
        elif average_score >= 60:
            recommendations.append(
                "📈 Good scores! Focus on your weak areas to push above 80%."
            )
        else:
            recommendations.append(
                "📖 Review your study materials more thoroughly before taking quizzes."
            )

        return recommendations


analytics_service = AnalyticsService()
