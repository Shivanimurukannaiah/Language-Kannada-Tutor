# agents/flashcard_agent.py

from openai import OpenAI

# — Use your working key here —
API_KEY = "sk-proj-A"
client  = OpenAI(api_key=API_KEY)

class FlashcardAgent:
    def __init__(self, model: str = "dall-e-3", size: str = "1024x1024"):
        self.model = model
        self.size  = size

    def create_flashcard(self, word: str, style: str = "cartoon") -> str:
        """
        Returns the URL of a generated illustration for the given Kannada word.
        """
        prompt = f"Create a {style}-style illustration of the Kannada word '{word}'."
        resp = client.images.generate(
            model=self.model,
            prompt=prompt,
            n=1,
            size=self.size
        )
        return resp.data[0].url

if __name__ == "__main__":
    url = FlashcardAgent().create_flashcard("ಮನೆ", style="watercolor")
    print("Image URL:", url)
