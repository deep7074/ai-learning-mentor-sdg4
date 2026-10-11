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

    model = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
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
        return r.json()["message"]["content"]
    except Exception as e:
        return (
            "I could not connect to the LLM. Make sure Ollama is running "
            "and the selected model is installed. "
            f"Technical detail: {e}"
        )

def mentor_answer(profile, question, retrieved_context=""):
    system = """
You are an AI Learning Mentor for college students and a teaching assistant.
Explain concepts clearly and accurately using simple English.
You may use the student's uploaded notes when relevant.
If note context is provided, prioritize it and say when the notes do not contain enough information.
Do not invent citations or claim to know facts that are absent from the notes.
Do not shame students. Give practical next steps.
"""
    context = f"""
Student profile:
Name: {profile.get('name', 'Student')}
Course: {profile.get('course', 'College')}
Attendance: {profile.get('attendance', 75)}%
Study hours/week: {profile.get('study_hours', 8)}
Pending assignments: {profile.get('pending', 1)}
Recent quiz score: {profile.get('quiz_score', 60)}%

Uploaded-note context:
{retrieved_context or 'No uploaded notes were selected.'}
"""
    return ask_llm(system, context + "\n\nStudent question:\n" + question)

def generate_study_plan(profile, subjects, days):
    system = """
Create a realistic personalized study plan for a college student.
Use simple English. Include revision, practice, breaks, and small daily goals.
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
    text = re.sub(r"```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"```\s*", "", text)

    # First, try parsing the complete response.
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Otherwise, extract the first complete JSON object or array.
    decoder = json.JSONDecoder()

    for i, char in enumerate(text):
        if char in "[{":
            try:
                value, _ = decoder.raw_decode(text[i:])
                return value
            except json.JSONDecodeError:
                continue

    raise ValueError("No valid JSON object or array found")



def generate_quiz(topic, difficulty, num_q):
    system = f"""
You are a quiz generator for college students.
Create exactly {num_q} multiple-choice questions about: {topic}
Difficulty: {difficulty}

Return ONLY a valid JSON ARRAY.
Every array item must have exactly these keys:
"question", "options", "answer".

Rules:
- "question" must be a string.
- "options" must contain exactly 4 different answer strings.
- "answer" must be the FULL TEXT of one of the 4 options.
- Do not use A, B, C, or D as the answer.
- Do not include Markdown or explanations outside the JSON.
- Make all questions relevant to the requested topic.
"""
    for attempt in range(2):
        raw = ask_llm(
            system,
            f"Generate {num_q} {difficulty} quiz questions about {topic}. "
            "Return a JSON array only."
        )
        try:
            data = _extract_json(raw)

            if isinstance(data, dict):
                if isinstance(data.get("questions"), list):
                    data = data["questions"]
                else:
                    data = [data]

            if not isinstance(data, list):
                continue

            cleaned = []
            for item in data:
                if not isinstance(item, dict):
                    continue

                question = item.get("question")
                options = item.get("options")
                answer = item.get("answer")

                if not isinstance(question, str) or not isinstance(options, list):
                    continue

                options = [
                    option.strip()
                    for option in options
                    if isinstance(option, str) and option.strip()
                ]

                if len(options) != 4 or len(set(options)) != 4:
                    continue

                if not isinstance(answer, str):
                    continue

                answer = answer.strip()
                matched = next(
                    (option for option in options
                     if option.casefold() == answer.casefold()),
                    None
                )

                if matched is None:
                    continue

                cleaned.append({
                    "question": question.strip(),
                    "options": options,
                    "answer": matched
                })

                if len(cleaned) == num_q:
                    return cleaned

        except (ValueError, TypeError, KeyError):
            continue

    return []


def generate_revision_summary(topic, context):
    system = """
Create a concise exam revision sheet from the supplied study material.
Use headings, bullet points, key definitions, and 5 likely exam questions.
Do not add unsupported facts.
"""
    return ask_llm(system, f"Topic: {topic}\n\nStudy material:\n{context}")
