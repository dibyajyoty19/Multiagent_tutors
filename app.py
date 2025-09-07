import streamlit as st
from agents.planner_agent import create_study_plan
from agents.simplifier_agent import simplify_text
from agents.doubt_solver import solve_doubt
from agents.motivator_agent import motivate_student
from agents.resource_curator import suggest_resources
from agents.evaluator import create_quiz

st.title("EdTech Multi-Agent AI Tutor")

# Sidebar selection
agent_choice = st.sidebar.selectbox(
    "Select Agent",
    ["Planner", "Simplifier", "Doubt Solver", "Motivator", "Resource Curator", "Evaluator"]
)
if agent_choice == "Planner":
    topic = st.text_input("Enter topic to plan for:")
    if st.button("Generate Plan"):
        plan = create_study_plan(topic)
        st.write(plan)

elif agent_choice == "Simplifier":
    topic = st.text_input("Enter topic to simplify:")
    if st.button("Simplify"):
        explanation = simplify_text(topic)
        st.write(explanation)

elif agent_choice == "Doubt Solver":
    question = st.text_input("Enter your doubt:")
    if st.button("Solve Doubt"):
        answer = solve_doubt(question)
        st.write(answer)

elif agent_choice == "Motivator":
    if st.button("Motivate Me"):
        message = motivate_student()
        st.write(message)

elif agent_choice == "Resource Curator":
    topic = st.text_input("Enter topic to get resources for:")
    if st.button("Get Resources"):
        resources = suggest_resources(topic)
        st.write(resources)

elif agent_choice == "Evaluator":
    topic = st.text_input("Enter topic to quiz on:")
    if st.button("Generate Quiz"):
        quiz = create_quiz(topic)
        st.write(quiz)
