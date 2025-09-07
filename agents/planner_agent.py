#Planner agent - helps students build a study plan
import json
import re
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from agents.base_client import get_model 

# JSON format we expect from Gemini
PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "overview": {"type": "string"},
        "assumptions": {"type": "array", "items": {"type": "string"}},
        "daily_plan": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "day": {"type": "integer"},
                    "date": {"type": "string"},
                    "hours": {"type": "number"},
                    "topics": {"type": "array", "items": {"type": "string"}},
                    "tasks": {"type": "array", "items": {"type": "string"}},
                    "milestone": {"type": "string"}
                },
                "required": ["day", "date", "hours", "topics", "tasks"]
            }
        },
        "checkpoints": {"type": "array", "items": {"type": "string"}},
        "resources": {"type": "array", "items": {"type": "object"}},
        "tips": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["overview", "daily_plan"]
}

# helper to calculate days till deadline
def days_left(today: datetime, deadline: Optional[str]) -> Optional[int]:
    if not deadline:
        return None
    try:
        end = datetime.strptime(deadline, "%Y-%m-%d")
        return max((end - today).days, 1)
    except:
        return None

# helper to pull JSON out of Gemini response
def extract_json(text: str) -> str:
    block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if block:
        return block.group(1)
    # fallback: take first {...}
    first, last = text.find("{"), text.rfind("}")
    if first != -1 and last != -1:
        return text[first:last+1]
    raise ValueError("No JSON found in response")

# convert plan dict into a nice markdown for console/UI
def make_markdown(plan: Dict[str, Any]) -> str:
    out = []
    out.append("# Study Plan\n")
    if "overview" in plan:
        out.append("**Overview:** " + plan["overview"] + "\n")

    # assumptions
    if plan.get("assumptions"):
        out.append("**Assumptions:**")
        for a in plan["assumptions"]:
            out.append("- " + a)
        out.append("")

    # daily schedule
    out.append("## Daily Plan")
    for d in plan.get("daily_plan", []):
        out.append(f"### Day {d.get('day')} – {d.get('date')} ({d.get('hours')} hrs)")
        if d.get("topics"):
            out.append("**Topics:** " + ", ".join(d["topics"]))
        if d.get("tasks"):
            out.append("**Tasks:**")
            for t in d["tasks"]:
                out.append("- " + t)
        if d.get("milestone"):
            out.append("**Milestone:** " + d["milestone"])
        out.append("")

    # checkpoints
    if plan.get("checkpoints"):
        out.append("## Checkpoints")
        for c in plan["checkpoints"]:
            out.append("- " + c)
        out.append("")

    # resources
    if plan.get("resources"):
        out.append("## Resources")
        for r in plan["resources"]:
            title = r.get("title", "Resource")
            topic = r.get("topic", "")
            link = r.get("link", "")
            out.append(f"- {title} ({topic}) {link}")
        out.append("")

    # tips
    if plan.get("tips"):
        out.append("## Tips")
        for t in plan["tips"]:
            out.append("- " + t)

    return "\n".join(out)

# main function
def create_study_plan(
    goal: str,
    topics: List[str],
    hours_per_day: float,
    level: str = "beginner",
    deadline: Optional[str] = None,
    start_date: Optional[str] = None,
    include_resources: bool = True
) -> Dict[str, Any]:

    model = get_model()

    # start date defaults to today
    today = datetime.today() if not start_date else datetime.strptime(start_date, "%Y-%m-%d")
    available_days = days_left(today, deadline)

    # if no deadline, estimate length
    if not available_days:
        est_days = max(len(topics) * 2, 5)
    else:
        est_days = available_days

    schema_text = json.dumps(PLAN_SCHEMA, indent=2)

    prompt = f"""
Make a study plan for a student.

Goal: {goal}
Level: {level}
Hours per day: {hours_per_day}
Topics: {topics}
Start date: {today.strftime("%Y-%m-%d")}
Deadline: {"None" if not deadline else deadline}
Total days (estimate): {est_days}

Rules:
- Plan must be JSON only, following this schema:
{schema_text}
- Dates should start from the start date.
- Daily tasks must be realistic, not vague.
- Include resources only if include_resources = {include_resources}.
    """

    response = model.generate_content(prompt)
    raw = response.text.strip()

    try:
        plan_json = extract_json(raw)
        plan = json.loads(plan_json)
    except:
        plan = {"overview": "Could not parse JSON", "daily_plan": [], "raw": raw}

    # fix missing dates
    if plan.get("daily_plan"):
        for i, d in enumerate(plan["daily_plan"], start=1):
            if not d.get("date"):
                d["date"] = (today + timedelta(days=i-1)).strftime("%Y-%m-%d")

    # also return markdown version
    plan["_markdown"] = make_markdown(plan)
    return plan

# test run
if __name__ == "__main__":
    topics = ["Arrays", "Strings", "Recursion", "Graphs", "DP"]
    plan = create_study_plan(
        goal="Prepare for DSA interview",
        topics=topics,
        hours_per_day=3,
        level="intermediate",
        deadline=None
    )
    print(plan["_markdown"])
