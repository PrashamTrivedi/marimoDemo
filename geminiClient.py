from google import genai
from typing import Dict, List
import os

# Initialize the Gemini client
try:
    genai.configure()
except Exception as e:
    print(f"Warning: Failed to configure Gemini client: {str(e)}")


def prompt(
    prompt: str,
    model_name: str = "models/gemini-2.0-flash-exp",
    other_settings: Dict = None,
) -> str:
    # Initialize client
    client = genai.Client()

    # Merge default settings with provided settings
    settings = {
        "contents": prompt,
    }
    if other_settings:
        settings.update(other_settings)

    # Generate content using the client.models API
    response = client.models.generate_content(
        model=model_name.replace("models/", ""), **settings
    )
    return response.text


def allowedModels() -> List[str]:
    return [
        "models/gemini-2.0-flash-exp",
        "models/gemini-2.0-flash",
        "models/gemini-2.0-flash-001",
        "models/gemini-2.0-flash-lite-preview",
        "models/gemini-2.0-flash-lite-preview-02-05",
        "models/gemini-2.0-pro-exp",
        "models/gemini-2.0-pro-exp-02-05",
        "models/gemini-exp-1206",
        "models/gemini-2.0-flash-thinking-exp-01-21",
        "models/gemini-2.0-flash-thinking-exp",
        "models/gemini-2.0-flash-thinking-exp-1219",
    ]


def listModels() -> List[str]:
    if not os.getenv("GOOGLE_API_KEY"):
        print("GOOGLE_API_KEY is not set")
        return []

    try:
        allowed = allowedModels()
        models = []
        for m in genai.Client().models.list():
            if m.name in allowed:
                models.append(m.name)
        return models
    except Exception as e:
        print(f"Failed to list Gemini models: {str(e)}")
        return []


def getModelDetails(model_name: str) -> Dict:
    try:
        client = genai.Client()
        model_details = client.models.get(model_name)
        return {
            "name": model_details.name,
            "description": model_details.description,
            "version": model_details.version,
            "additional_info": (
                model_details.additional_info
                if hasattr(model_details, "additional_info")
                else None
            ),
        }
    except Exception as e:
        print(f"Failed to get details for model {model_name}: {str(e)}")
        return {}
