import os
import json
import re
import requests

def _provider():
    return os.getenv("LLM_PROVIDER", "ollama").lower().strip()

def ask_llm(system_prompt, user_prompt):
    provider = _provider()

    if provider == "openai":
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
            response = client.responses.create(
                model=model,
                instructions=system_prompt,
                input=user_prompt
            )
            return response.output_text
        except Exception as e:
            return f"LLM error: {e}"

    # Default: local Ollama
    model = os.getenv("OLLAMA_MODEL", "llama3.2")
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    }

    try:
        r = requests.post(url, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        return data["message"]["content"]
    except Exception as e:
        return (
            "I could not connect to the LLM. "
            "If you are using Ollama, make sure Ollama is running and the model is downloaded. "
            f"Technical detail: {e}"
        )

def generate_study_plan(profile, subjects, days):
    system = """
You are an AI learning mentor for college students.
Create a realistic, supportive study plan. Use simple English.
Do not shame the student. Keep sessions manageable and include revision,
practice, breaks, and a small daily goal.
Return a clean Markdown table followed by 3 short tips.
"""
    user = f"""
Student: {profile['name']}
Course: {profile['course']}
Attendance: {profile['attendance']}%
Study hours/week: {profile['study_hours']}
Pending assignments: {profile['pending']}
Recent quiz score: {profile['quiz_score']}%
Subjects/topics: {subjects}
Plan duration: {days} days
"""
    return ask_llm(system, user)

def _extract_json(text):
    text = text.strip()
    text = re.sub(r"```json\s*", "", text, flags=re.I)
    text = re.sub(r"```\s*", "", text)
    start = text.find("[")
    end = text.rfind("]")
    if start >= 0 and end > start:
        text = text[start:end+1]
    return json.loads(text)

def generate_quiz(topic, difficulty, num_q):
    system = """
Create a multiple-choice educational quiz.
Return ONLY valid JSON: a list of objects with exactly these keys:
question, options, answer.
Each options list must contain 4 strings and answer must exactly match one option.
No Markdown and no extra text.
"""
    user = f"Topic: {topic}\nDifficulty: {difficulty}\nQuestions: {num_q}"
    raw = ask_llm(system, user)
    try:
        data = _extract_json(raw)
        cleaned = []
        for item in data[:num_q]:
            if (
                isinstance(item, dict)
                and isinstance(item.get("question"), str)
                and isinstance(item.get("options"), list)
                and len(item["options"]) == 4
                and item.get("answer") in item["options"]
            ):
                cleaned.append(item)
        return cleaned
    except Exception:
        return []

def evaluate_answer(question, student_answer):
    system = """
Give short, encouraging feedback on a student's answer.
State whether it is correct, then explain the concept in simple terms.
"""
    return ask_llm(system, f"Question: {question}\nStudent answer: {student_answer}")
