from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from Algorithmic.constants import (
    PROBLEM_ANALYSER_PROMPT,
    MATH_ANALYSER_PROMPT,
    PYTHON_GENERATOR_PROMPT,
    IO_HANDLER_PROMPT,
    ERROR_HANDLER_PROMPT,
    OUTPUT_ANALYSER_PROMPT,
)

class Agents:
    
    def __init__(self):
        self.question_analyser = None
        self.math_analyser = None
        self.python_generator = None
        self.io_handler = None
        self.error_handler = None
        self.output_analyser = None
    
    def get_question_analyser(self, llm):
        prompt = PromptTemplate(
            template=PROBLEM_ANALYSER_PROMPT,
            input_variables=["question"],
        )
        
        self.question_analyser = prompt | llm | StrOutputParser()
        return self.question_analyser
    
    def get_math_analyser(self, llm):
        prompt = PromptTemplate(
            template=MATH_ANALYSER_PROMPT,
            input_variables=["question"],
        )
        
        self.math_analyser = prompt | llm | StrOutputParser()
        return self.math_analyser
        
    def get_python_generator(self, llm):
        prompt = PromptTemplate(
            template= PYTHON_GENERATOR_PROMPT,
            input_variables=["question_analysis", "math_analysis", "question"],
        )
        
        self.python_generator = prompt | llm | JsonOutputParser()
        return self.python_generator
    
    def get_io_handler(self, llm):
        prompt = PromptTemplate(
            template= IO_HANDLER_PROMPT,
            input_variables= ["test_cases", "logic_code", "question_analysis"],
        )
        
        self.io_handler = prompt | llm | JsonOutputParser()
        return self.io_handler
    
    def get_error_handler(self, llm):
        prompt = PromptTemplate(
            template= ERROR_HANDLER_PROMPT,
            input_variables= ["final_code", "error"]
        )
        
        self.error_handler = prompt | llm | JsonOutputParser()
        return self.error_handler
        
    def get_output_analyser(self, llm):
        prompt = PromptTemplate(
            template= OUTPUT_ANALYSER_PROMPT,
            input_variables= ["test_cases", "terminal_output", "required_output"]
        )
        
        self.output_analyser = prompt | llm | JsonOutputParser()
        return self.output_analyser