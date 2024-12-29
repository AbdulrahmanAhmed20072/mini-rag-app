from ..LLMInterface import LLMInterface
import cohere
import logging
from ..LLMEnums import CohereEnums, DocumentTypeEnum

class CoHereProvider(LLMInterface):

    def __init__(self, api_key: str ,
                       default_input_max_characters: int = 1000,
                       default_generation_max_output_tokens: int = 1000,
                       default_generation_temperature: float = 0.1):

        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.ClientV2(api_key = self.api_key)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):

        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):

        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
    
    def process_text(self, text):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list = [], max_output_token: int = None,
                            temperature: float = None):

        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Gereration model for OpenAI was not set")
            return None
        
        max_output_token = max_output_token if max_output_token else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt = prompt, role = CohereEnums.USER.value)
        )
        
        response = self.client.chat(
            model = self.generation_model_id,
            messages = chat_history,
            max_tokens = max_output_token,
            temperature = temperature,
            
            )
        
        if not response or not response.message or len(response.message.content) == 0 or not response.message.content[0].text:
            self.logger.error("Error while generation text with CoHere")
            return None

        return response.message.content[0].text
    
    def embed_text(self, text: str, document_type: str = None):

        if not self.client:
            self.logger.error("CoHere client was not set")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("embedding model for CoHere was not set")
            return None
        
        input_type = CohereEnums.DOCUMENT if document_type == DocumentTypeEnum.DOCUMENT else CohereEnums.QUERY

        response = self.client.embed(
            model = self.embedding_model_id,
            input_type = input_type,
            texts = [self.process_text(text)],
            embedding_types = ["float"]
        )

        if not response or not response.embeddings or not response.embeddings.float_:
            self.logger.error("Error while embedding text with CoHere")
            return None

        return response.embeddings.float_[0]

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role" : role,
            "content" : self.process_text(prompt)
        }