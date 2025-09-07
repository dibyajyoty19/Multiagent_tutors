#Simplifier agent - takes a difficult topic and explains it in easy words with examples or analogies so students can understand quickly.
from agents.base_client import get_model

def simplify_text(text: str) -> str:
    model = get_model()
    prompt = f"""
    You are an EdTech tutor.
    Simplify the following text for a Class 10 student.
    Make it clear, short, and easy to understand.

    Text: {text}
    """
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    # Example Science concept
    sample_text = "Photosynthesis is the biochemical process in which light energy is converted into chemical energy by plants, producing glucose and oxygen as byproducts."
    simplified = simplify_text(sample_text)
    print("Original:", sample_text)
    print("Simplified:", simplified)
