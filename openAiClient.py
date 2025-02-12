from openai import OpenAI
from typing import Dict, List


def prompt(
    prompt: str, model_name: str = "gpt-4o-mini", other_settings: Dict = None
) -> str:
    client = OpenAI()

    # Merge default settings with provided settings
    settings = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
    }
    if other_settings:
        settings.update(other_settings)

    response = client.chat.completions.create(**settings)
    return response.choices[0].message.content


def allowedModels() -> List[str]:
    return [
        "o1-mini-2024-09-12",
        "o1-mini",
        "o1",
        "o3-mini-2025-01-31",
        "o3-mini",
        "o1-2024-12-17",
        "gpt-4o-mini-2024-07-18",
        "gpt-4o-mini",
    ]


def listModels() -> List[str]:
    client = OpenAI()
    models = client.models.list()
    allowed = allowedModels()
    return [model.id for model in models.data if model.id in allowed]
