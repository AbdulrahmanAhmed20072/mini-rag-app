from .LLMEnums import LLMEnums
from .providers import OpenAIProvider, CoHereProvider, HuggingFaceProvider

class LLMProviderFactory:

    def __init__(self, config: dict):
        self.config = config

    def create(self, provider):

        if provider == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key = self.config.OPENAI_API_KEY,
                api_url = self.config.OPENAI_API_URL,
                default_input_max_characters = self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens = self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature = self.config.GENERATION_DEFAULT_TEMPERATURE
            )

        elif provider == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key = self.config.COHERE_API_KEY,
                default_input_max_characters = self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens = self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature = self.config.GENERATION_DEFAULT_TEMPERATURE
            )
        
        elif provider == LLMEnums.HUGGING_FACE.value:
            return HuggingFaceProvider(
                default_input_max_characters = self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens = self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature = self.config.GENERATION_DEFAULT_TEMPERATURE
            )

        else:
            return None