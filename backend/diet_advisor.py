import os
from openai import OpenAI

# Load your OpenRouter API key from an environment variable for safety
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_deepseek(condition):
    """Call the DeepSeek-R1 free API to get personalized advice."""
    if not OPENROUTER_API_KEY:
        return None

    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": "You are a friendly health advisor."},
                {"role": "user", "content": f"Suggest a healthy diet plan for {condition}."}
            ],
            stream=False
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("DeepSeek API error:", e)
        return None

def get_diet_advice(condition):
    rules = {
        "diabetes": "Focus on high-fiber foods, whole grains, vegetables. Avoid sugary drinks.",
        "weight loss": "Include lean protein, avoid junk food, stay hydrated, and exercise daily.",
        "heart health": "Eat omega-3 rich foods, reduce salt, avoid fried items."
    }

    key = condition.lower()
    if key in rules:
        return rules[key]

    # Fallback to DeepSeek LLM for custom advice
    advice = call_deepseek(condition)
    if advice:
        return advice

    # Final fallback if API isn't accessible
    return ("Here's general advice: maintain a balanced diet rich in vegetables, proteins, "
            "whole grains, and stay hydrated. Consult a nutritionist for tailored plans.")

# Example usage
if __name__ == "__main__":
    cond = "thyroid health"
    print(get_diet_advice(cond))
