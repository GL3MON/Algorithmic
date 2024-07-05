from dataclasses import dataclass
from pathlib import Path
from typing_extensions import TypedDict

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

class GraphState(TypedDict):
    question: str
    logic_code: str
    final_code: str
    error_check_count: int
    terminal_output: str
    required_output: str
    regenerate_count: int
    question_analysis: str
    math_analysis: str
    test_cases: str
    error: str