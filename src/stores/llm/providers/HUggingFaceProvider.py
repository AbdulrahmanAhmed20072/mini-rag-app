from ..LLMInterface import LLMInterface
from transformers import pipeline
import logging
from enum import Enum
from ..LLMEnums import HuggingFaceEnums, DocumentTypeEnum
from transformers import pipeline
from sentence_transformers import SentenceTransformer

class HuggingFaceProvider(LLMInterface):

    def __init__(self, default_input_max_characters: int = 1000,
                       default_generation_max_output_tokens: int = 1000,
                       default_generation_temperature: float = 0.1):

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.generation_pipeline = None
        self.sentence_transformer = None

        self.enums = HuggingFaceEnums
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id
        self.generation_pipeline = pipeline("text-generation", model=model_id, tokenizer=model_id)

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

        self.sentence_transformer = SentenceTransformer(self.embedding_model_id, trust_remote_code=True)

    def process_text(self, text):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list = [], max_output_token: int = None,
                            temperature: float = None):
        
        if not self.generation_model_id:
            self.logger.error("Generation model for Hugging Face was not set")
            return None
        
        if not self.generation_pipeline:
            self.logger.error("Generation pipeline for Hugging Face was not set")
            return None
        
        max_output_token = max_output_token if max_output_token else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt, role=self.enums.USER.value)
        )

        response = self.generation_pipeline(
            chat_history,
            max_length=max_output_token,
            temperature=temperature,
            return_full_text=False
        )

        if not response or len(response) == 0 or not response[0]['generated_text']:
            self.logger.error("Error while generating text with Hugging Face")
            return None

        return response[0]['generated_text']

    def embed_text(self, text: str, document_type: str = None):

        if not self.embedding_model_id or not self.sentence_transformer:
            self.logger.error("Embedding model id or sentence_transformer for Hugging Face was not set")
            return None

        embedded_text = self.sentence_transformer.encode(
            sentences = text,
        )

        if len(embedded_text) == 0:
            self.logger.error("Error while embedding text with Hugging Face")
            return None

        return embedded_text.tolist()

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role.value if isinstance(role, Enum) else role,
            "content": self.process_text(prompt)
        }