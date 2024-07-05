from Algorithmic.logging import logger
from Algorithmic.utils.common import read_yaml, create_directories
from Algorithmic.constants import *
from Algorithmic.entity import (
    LangchainConfig,
    TerminalConfig,
    LLMConfig,
)

class ConfigurationManager:
    def __init__(self, config_path= CONFIG_PATH):
        self.config = read_yaml(config_path)
        create_directories([self.config.artifacts_root])
        
    def get_langchain_config(self) -> LangchainConfig:
        config = self.config.langchain_config
        
        langchain_config = LangchainConfig(
            set_debug = config.set_debug,
            set_verbose = config.set_verbose,
            recursion_limit = config.recursion_limit,
        )
        
        return langchain_config
    
    def get_terminal_config(self):
        config = self.config.terminal_config
        create_directories([config.root_dir])
        
        terminal_config = TerminalConfig(
            python_image = config.python_image,
            terminal_output_file = config.terminal_output_file,
        )
        
        return terminal_config
    
    def get_llm_config(self):
        config = self.config.llm_config
        
        llm_config = LLMConfig(
            model= config.model,
            convert_system_message_to_human= config.convert_system_message_to_human,
            handle_parsing_errors= config.handle_parsing_errors,
            max_tokens= config.max_tokens,
        )
        
        return llm_config
        
        