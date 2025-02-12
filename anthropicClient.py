import os
from anthropic import Anthropic
from typing import Dict, List


def prompt(
    prompt: str,
    model_name: str = "claude-3-opus-20240229",
    other_settings: Dict = None,
) -> str:
    client = Anthropic()

    # Merge default settings with provided settings
    settings = {
        "model": model_name,
        "max_tokens": 8192,
        "messages": [{"role": "user", "content": prompt}],
    }
    if other_settings:
        settings.update(other_settings)

    response = client.messages.create(**settings)
    return response.content[0].text


def allowedModels() -> List[str]:
    return [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-3-5-sonnet-20240620",
        "claude-3-haiku-20240307",
    ]


def listModels() -> List[str]:
    client = Anthropic()
    models = client.models.list()
    allowed = allowedModels()

    if not models:
        return []

    return [model.id for model in models if model.id in allowed]
