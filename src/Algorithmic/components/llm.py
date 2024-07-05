from langchain_google_genai import ChatGoogleGenerativeAI
from Algorithmic.constants import GOOGLE_API_KEY
from Algorithmic.logging import logger
from Algorithmic.entity import LLMConfig

class LLM:
    
    def __init__(self, config: LLMConfig):
        self.config = config
        if not GOOGLE_API_KEY:
            logger.info("GOOGLE API KEY NOT FOUND")
        
        self.llm = None
        
    def get_llm(self, temperature: int = 0):
        
        self.llm = ChatGoogleGenerativeAI(
            model = self.config.model,
            convert_system_message_to_human= self.config.convert_system_message_to_human,
            handle_parsing_errors = self.config.handle_parsing_errors,
            temperature = temperature,
            max_output_tokens= self.config.max_tokens,
            google_api_key = GOOGLE_API_KEY,
        )
        
        return self.llm