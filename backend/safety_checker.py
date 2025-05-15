import google.generativeai as genai
from prompt_builder import build_prompt

class SafetyChecker:
    """Check ingredient safety using Gemini and ChromaDB."""
    def __init__(self, api_key, chromadb_manager):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.chromadb_manager = chromadb_manager

    def check_ingredient(self, ingredient_name):
        """Check the safety status of an ingredient."""
        retrieved_info = self.chromadb_manager.query(ingredient_name)
        prompt = build_prompt(ingredient_name, retrieved_info)
        print(f"\n🔬 Checking Ingredient: {ingredient_name}\n")
        try:
            response = self.model.generate_content(
                prompt,
                stream=True,
                generation_config={"response_mime_type": "text/plain"}
            )
            for chunk in response:
                print(chunk.text, end="")
            print("\n")
        except Exception as e:
            print(f"Error generating response: {e}")
            print(f"Raw Info: {retrieved_info[0]['details']}\n")