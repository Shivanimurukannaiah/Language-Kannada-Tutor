# agents/translate_agent.py

import json
from openai import OpenAI

# — Use your working key here —
API_KEY = "ssk-proj"
client  = OpenAI(api_key=API_KEY)

class TranslateAgent:
    def __init__(self, model: str = "gpt-4"):
        self.model = model

    def translate(self, text: str) -> dict:
        prompt = f"""
Translate the following English sentence into Kannada.
Provide:
- Kannada (Kannada script)
- Transliteration (Latin script)

Text: "{text}"

Respond as JSON:
{{"kannada":"...", "transliteration":"..."}}
"""
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role":"system",  "content":"You are an accurate Kannada translator."},
                {"role":"user",    "content":prompt},
            ],
            temperature=0,
            max_tokens=100
        )
        output = resp.choices[0].message.content.strip()
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return {"error":"JSON parse failed","raw_output":output}

if __name__ == "__main__":
    print(json.dumps(TranslateAgent().translate("Where is the library?"), ensure_ascii=False, indent=2))
