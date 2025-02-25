import os
from anthropic import Anthropic
from typing import Dict, List


def prompt(
    prompt: str,
    model_name: str = "claude-3-opus-20240229",
    other_settings: Dict = None,
) -> str:
    client = Anthropic()

    if "-reasoning" in model_name:
        model_name = model_name.replace("-reasoning", "")

    # Merge default settings with provided settings
    settings = {
        "model": model_name,
        "max_tokens": 8192,
        "messages": [{"role": "user", "content": prompt}],
    }
    if other_settings:
        settings.update(other_settings)

    print(settings)
    response = client.messages.create(**settings)
    if "3-7-sonnet" in model_name and other_settings.get("thinking"):
        return f"<thoughts>{response.content[0].thinking}</thoughts>\n{response.content[1].text}"
    else:
        return response.content[0].text


def allowedModels() -> List[str]:
    return [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-3-5-sonnet-20240620",
        "claude-3-haiku-20240307",
        "claude-3-7-sonnet-20250219",
        "claude-3-7-sonnet-20250219-reasoning",
        "claude-3-7-sonnet-latest",
        "claude-3-7-sonnet-latest-reasoning",
    ]


def listModels() -> List[str]:
    client = Anthropic()
    models = client.models.list()
    allowed = allowedModels()

    if not models:
        return []
    else:
        result = [model.id for model in models if model.id in allowed]
        # Add reasoning suffix for 3-7-sonnet models
        for model_id in result.copy():
            if "3-7-sonnet" in model_id:
                result.append(f"{model_id}-reasoning")
        return result
