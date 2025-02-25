from openai import OpenAI
from typing import Dict, List


def _should_format(model_name: str) -> bool:
    return model_name.startswith(("o1", "o3"))


def prompt(
    prompt: str, model_name: str = "gpt-4o-mini", other_settings: Dict = None
) -> str:
    client = OpenAI()

    # Add formatting text for o1 and o3 models
    content = (
        f"Formatting re-enabled. {prompt}" if _should_format(model_name) else prompt
    )

    # Merge default settings with provided settings
    settings = {
        "model": model_name,
        "messages": [{"role": "user", "content": content}],
    }

    print(other_settings.get("reasoning_effort", None))

    response = client.chat.completions.create(
        model=model_name,
        messages=settings["messages"],
        reasoning_effort=other_settings.get("reasoning_effort", None),
    )
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
