# agents/lesson_agent.py

import json
from openai import OpenAI

# — Your hard-coded key for now —
API_KEY = "sk-proj"
client  = OpenAI(api_key=API_KEY)

class LessonAgent:
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.prompt = """
Generate Kannada interrogative sentences on a given theme.
For each sentence, return:
1. Kannada (Kannada script)
2. Transliteration (Latin script)
3. English translation.

Respond **only** with a JSON array of objects, e.g.:

[
  {"kannada":"…","transliteration":"…","english":"…"},
  …
]
"""

    def create_lesson(self, theme: str, count: int = 5) -> list[dict]:
        user_msg = (
            f'{self.prompt}\nNow generate {count} questions on the theme "{theme}".'
        )
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role":"system", "content":"You are a concise Kannada tutor."},
                {"role":"user",   "content":user_msg},
            ],
            temperature=0.7,
            max_tokens=768
        )

        raw = resp.choices[0].message.content.strip()

        # Attempt to slice out the JSON array from the raw text
        start = raw.find('[')
        end   = raw.rfind(']')
        if start != -1 and end != -1 and end > start:
            candidate = raw[start:end+1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass  # fall back to error below

        # If we get here, parsing failed
        print("RAW OUTPUT (truncated or malformed):\n", raw)
        return [{"error": "Failed to parse JSON", "raw_output": raw}]


if __name__ == "__main__":
    lesson = LessonAgent().create_lesson(theme="ಫಲಗಳು (fruits)", count=5)
    print(json.dumps(lesson, ensure_ascii=False, indent=2))
