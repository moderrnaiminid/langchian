"""Configuration settings for LangChain LLM with long-term memory."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for LLM settings."""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # LLM Model Settings
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    
    # Memory Settings
    MEMORY_KEY = "chat_history"
    CONVERSATION_BUFFER_SIZE = int(os.getenv("CONVERSATION_BUFFER_SIZE", "10"))
    
    # Vector Store Settings
    CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "long_term_memory")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    
    # Retrieval Settings
    RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "5"))
    
    @classmethod
    def validate(cls):
        """Validate that required configurations are set."""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not set. Please set it in .env file or environment variables."
            )
        return True
