from enum import Enum

class LLMEnums(Enum):

    OPENAI = "OPENAI"
    COHERE = "COHERE"
    HUGGING_FACE = "HUGGING_FACE"

class OpenAIEnums(Enum):

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class CohereEnums(Enum):

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    DOCUMENT = "search_document"
    QUERY = "search_query"

class HuggingFaceEnums(Enum):

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class DocumentTypeEnum(Enum):

    DOCUMENT = "document"
    QUERY = "query"