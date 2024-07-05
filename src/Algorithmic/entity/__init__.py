from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class LangchainConfig:
    set_debug: bool
    set_verbose: True
    recursion_limit: int

@dataclass(frozen=True)
class TerminalConfig:
    python_image: str
    terminal_output_file: Path

@dataclass(frozen=True)
class LLMConfig:
    model: str
    convert_system_message_to_human: True
    handle_parsing_errors: True
    max_tokens: 1000