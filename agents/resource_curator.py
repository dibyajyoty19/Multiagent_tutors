#Resource curator - finds and suggests the best learning resources (articles, tutorials, videos) for a given topic.
from agents.base_client import get_model

def suggest_resources(topic: str) -> str:
    """
    This agent recommends useful study resources for a given topic.
    Resources can be tutorials, articles, or videos.
    It acts like a mentor who guides students towards trusted materials.
    """
    model = get_model()
    prompt = f"""
    You are a helpful study assistant.
    A student is learning the topic: {topic}.
    Suggest 3-5 useful resources (articles, tutorials, or videos).
    Keep recommendations short, clear, and add why they are useful.
    Avoid broken links, suggest popular or reliable platforms only.
    """

    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    # Example test topic
    sample_topic = "Object-Oriented Programming in Python"
    print("\nTopic:")
    print(sample_topic)

    print("\nSuggested Resources:")
    print(suggest_resources(sample_topic))
