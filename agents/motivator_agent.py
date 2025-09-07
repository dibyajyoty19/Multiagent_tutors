#Motivator agent - a emotional support, a motivator for the student, more like a mother touch.
from agents.base_client import get_model
import random

def motivate_student(feeling: str = "neutral") -> str:
    """
    This agent gives a motivational message based on the student's mood.
    If no mood is given, it provides a random uplifting message.
    """
    model = get_model()
    # Some preset fallback motivational messages
    fallback_quotes = [
        "Every coder was once a beginner. Keep pushing! 🚀",
        "Don’t give up. Debugging is just problem-solving in disguise.",
        "One step at a time. You’re making progress, even if it’s small.",
        "Consistency beats intensity. A little daily effort works wonders.",
    ]

    # Prompt for Gemini AI
    prompt = f"""
    You are a supportive mentor for coding students.
    The student is currently feeling: {feeling}.
    Give a short motivational message (2–3 lines).
    Keep it friendly, warm, and encouraging.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        # In case API fails, return a random fallback message
        return random.choice(fallback_quotes)


if __name__ == "__main__":
    # Example test runs
    print("\nNeutral Mood:")
    print(motivate_student("neutral"))

    print("\nTired Mood:")
    print(motivate_student("tired"))

    print("\nExcited Mood:")
    print(motivate_student("excited"))
