# agents/quiz_agent.py

import json
from openai import OpenAI, OpenAIError

# — Replace with your real API key —
API_KEY = "sk-proj-API=KEY"
client  = OpenAI(api_key=API_KEY)

class QuizAgent:
    """
    Generates a 5-question multiple-choice quiz on a given topic,
    then safely extracts the JSON from the model’s response.
    """
    def __init__(self, model: str = "gpt-4"):
        self.model = model

    def generate_quiz(self, topic: str) -> dict:
        prompt = f"""
You are a Kannada tutor. Create a 5-question multiple-choice quiz about this topic:
\"\"\"{topic}\"\"\"

For each question, provide:
1. "question": the question text in English.
2. "choices": an object mapping "A", "B", "C", "D" to four possible answers 
   (in Kannada script with a Latin transliteration in parentheses).
3. "correct": the letter (A–D) of the correct choice.

Respond **strictly** as JSON, for example:

{{
  "quiz": [
    {{
      "question": "…",
      "choices": {{"A":"…","B":"…","C":"…","D":"…"}},
      "correct": "A"
    }},
    … total 5 items …
  ]
}}
"""
        try:
            resp = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful Kannada tutor who creates quizzes."},
                    {"role": "user",   "content": prompt},
                ],
                temperature=0.7,
                max_tokens=600
            )
            raw = resp.choices[0].message.content.strip()

            # Extract the JSON object between the first '{' and the last '}'
            start = raw.find('{')
            end   = raw.rfind('}')
            if start == -1 or end == -1 or end < start:
                return {"error": "No JSON object found", "raw_output": raw}

            candidate = raw[start:end+1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                return {"error": "Failed to parse JSON", "raw_output": candidate}

        except OpenAIError as e:
            return {"error": f"OpenAI API error: {e}"}

if __name__ == "__main__":
    qa = QuizAgent()
    result = qa.generate_quiz("vehicles")
    print(json.dumps(result, ensure_ascii=False, indent=2))
