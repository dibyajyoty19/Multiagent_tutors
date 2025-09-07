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
    ["Doubt Solver", "Simplifier", "Resource Curator", "Evaluator", "Planner", "Motivator"]
)

# Doubt Solver
if agent_choice == "Doubt Solver":
    question = st.text_input("Enter your doubt:")
    if st.button("Solve Doubt"):
        answer = solve_doubt(question)
        st.write(answer)

# Simplifier
elif agent_choice == "Simplifier":
    topic = st.text_input("Enter topic to simplify:")
    if st.button("Simplify"):
        explanation = simplify_text(topic)
        st.write(explanation)

# Resource Curator
elif agent_choice == "Resource Curator":
    topic = st.text_input("Enter topic to get resources for:")
    if st.button("Get Resources"):
        resources = suggest_resources(topic)
        st.write(resources)

# Evaluator
elif agent_choice == "Evaluator":
    topic = st.text_input("Enter topic to quiz on:")
    if st.button("Generate Quiz"):
        quiz = create_quiz(topic)
        st.write(quiz)

# Planner
elif agent_choice == "Planner":
    goal = st.text_input("Enter your goal (e.g., Crack DSA interview)")
    topics_input = st.text_area("Enter topics (comma separated)", "Arrays, Strings, Recursion")
    hours_per_day = st.number_input("Hours per day", min_value=1, max_value=24, value=2)
    level = st.selectbox("Select level", ["beginner", "intermediate", "advanced"])
    deadline = st.date_input("Deadline (optional)", value=None)

    if st.button("Generate Plan"):
        if goal and topics_input:
            topics = [t.strip() for t in topics_input.split(",") if t.strip()]
            plan = create_study_plan(
                goal=goal,
                topics=topics,
                hours_per_day=hours_per_day,
                level=level,
                deadline=deadline.strftime("%Y-%m-%d") if deadline else None
            )
            st.markdown(plan["_markdown"])
        else:
            st.error("Please enter both a goal and at least one topic.")

# Motivator
elif agent_choice == "Motivator":
    if st.button("Motivate Me"):
        message = motivate_student()
        st.write(message)
