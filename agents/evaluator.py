#Evaluator - creates short quizzes or tests to check a student’s understanding of a topic.

from agents.base_client import get_model

def create_quiz(topic: str, num_questions: int = 3) -> str:
    """
    This agent prepares a short quiz to test the student's understanding.
    It acts like a teacher giving practice questions for revision.
    """

    model = get_model()
    prompt = f"""
    You are a quiz master.
    Create {num_questions} multiple-choice questions on the topic: {topic}.
    Each question should have 4 options (A, B, C, D).
    Clearly mark the correct answer.
    Keep questions simple and student-friendly.
    """
    response = model.generate_content(prompt)
    return response.text.strip()


if __name__ == "__main__":
    sample_topic = "Python Data Types"
    print("\nQuiz on Topic:")
    print(sample_topic)

    print("\nGenerated Quiz:")
    print(create_quiz(sample_topic))
