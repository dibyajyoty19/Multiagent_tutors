#Doubt solver = it resolves the doubts of a student at the same given time without waiting for a real person to do it.
from agents.base_client import get_model

def solve_doubt(question: str) -> str:
    """
    This function takes a student's question and returns
    a clear, easy-to-understand explanation using Gemini AI.
    """
    model = get_model()
    # Ask Gemini AI in a conversational, student-friendly way
    prompt = f"""
    You are a friendly coding tutor. A student has asked this question:

    Question: {question}

    Please explain the answer clearly with examples if possible.
    Avoid jargon and keep it beginner-friendly.
    """
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    # Example test question
    test_question = "What is the difference between a list and a tuple in Python?"
    answer = solve_doubt(test_question)
    print("\nStudent Question:")
    print(test_question)
    print("\nTutor's Answer:")
    print(answer)
