from typing import Dict, List, Tuple
import openAiClient
import geminiClient
import anthropicClient

# Global model cache
_model_provider_map: Dict[str, str] = {}


def _initialize_model_map():
    """Initialize the model to provider mapping"""
    global _model_provider_map
    _model_provider_map.clear()

    # OpenAI Models
    try:
        models = openAiClient.listModels()
        print("\nOpenAI Models:")
        for model in models:
            print(f"  - {model}")
            _model_provider_map[model] = "openai"
    except Exception as e:
        print(f"Error retrieving OpenAI models: {str(e)}")
        pass

    # Gemini Models
    try:
        models = geminiClient.listModels()
        print("\nGemini Models:")
        for model in models:
            print(f"  - {model}")
            _model_provider_map[model] = "gemini"
    except Exception as e:
        print(f"Error retrieving Gemini models: {str(e)}")
        pass

    # Anthropic Models
    try:
        models = anthropicClient.listModels()
        print("\nAnthropic Models:")
        for model in models:
            print(f"  - {model}")
            _model_provider_map[model] = "anthropic"
    except Exception as e:
        print(f"Error retrieving Anthropic models: {str(e)}")
        pass

    if not _model_provider_map:
        print("\nWarning: No models were successfully retrieved from any provider")


def listModels() -> List[Tuple[str, str]]:
    """
    List all available models from all providers.
    Returns a list of tuples containing (provider, model_name)
    """
    _initialize_model_map()
    return [(provider, model) for model, provider in _model_provider_map.items()]


def prompt(prompt: str, model_name: str, other_settings: Dict = None) -> str:
    """
    Route the prompt to the appropriate provider based on the model name using the cached mapping
    """
    # Initialize model map if empty
    if not _model_provider_map:
        _initialize_model_map()

    # Get provider from the map
    provider = _model_provider_map.get(model_name)
    if not provider:
        raise ValueError(
            f"Unknown model: {model_name}. Please call listModels() to see available models."
        )

    # Route to appropriate provider
    if provider == "openai":
        return openAiClient.prompt(prompt, model_name, other_settings)
    elif provider == "gemini":
        return geminiClient.prompt(prompt, model_name, other_settings)
    elif provider == "anthropic":
        return anthropicClient.prompt(prompt, model_name, other_settings)
    else:
        raise ValueError(f"Unknown provider: {provider} for model: {model_name}")
