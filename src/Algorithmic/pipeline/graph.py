from typing_extensions import TypedDict
from Algorithmic.components.agents import Agents
from Algorithmic.components.tools import SandboxCodeExecutor
from langchain.globals import set_verbose, set_debug
from Algorithmic.components.llm import LLM
from Algorithmic.entity import GraphState
from Algorithmic.logging import logger
from Algorithmic.config.configuration import ConfigurationManager
from langgraph.graph import END, StateGraph

class Graph:
    
    def __init__(self):
        self.workflow = StateGraph(GraphState)
        
        config = ConfigurationManager()
        self.llm_config = config.get_llm_config()
        self.terminal_config = config.get_terminal_config()
        self.langchain_config= config.get_langchain_config()
        
        self.llm = LLM(config=self.llm_config)
        self.global_llm = self.llm.get_llm()
        self.coder = self.llm.get_llm(temperature=0.6)
        self.terminal = SandboxCodeExecutor(config=self.terminal_config)
        self.agents = Agents()
        
        logger.info("INITIATING QUESTION ANALYSER")
        self.question_analyser = self.agents.get_question_analyser(self.global_llm)
        
        logger.info("INITIATING MATH ANALYSER")
        self.math_analyser = self.agents.get_math_analyser(self.global_llm)
        
        logger.info("INITIATING PYTHON GENERATOR")
        self.python_generator = self.agents.get_python_generator(self.coder)
        
        logger.info("INITIATING IO HANDLER")
        self.io_handler = self.agents.get_io_handler(self.global_llm)
        
        logger.info("INITIATING ERROR HANDLER")
        self.error_handler = self.agents.get_error_handler(self.coder)
        
        logger.info("INITIATING OUTPUT ANALYSER")
        self.output_analyser = self.agents.get_output_analyser(self.global_llm)
        
    def analysis(self, state):
        logger.info("ANALYSING THE QUESTION")
        question = state['question']
        
        question_analysis = self.question_analyser.invoke({"question": question})
        math_analysis = self.math_analyser.invoke({"question": question})
        
        logger.info("ANALYSIS COMPLETED")
        return {"question_analysis": question_analysis, "math_analysis": math_analysis}
    
    def generation(self, state):
        logger.info("GENERATING LOGIC CODE")
        question_analysis = state['question_analysis']
        terminal_output = state['terminal_output']
        math_analysis = state['math_analysis']
        test_cases = state["test_cases"]
        error_check_count = state['error_check_count']
        question = state['question']
        error = state['error']
        error_check_count = 0
        
        generator_output = self.python_generator.invoke({"question_analysis": question_analysis,
                                                "math_analysis": math_analysis,
                                                "question": question,
                                                })
        
        logic_code = generator_output['code']
        
        logger.info("GENERATING IO CODE")
        io_output = self.io_handler.invoke({"logic_code": logic_code, "test_cases": test_cases, "question_analysis": question_analysis})
        final_code = io_output['code']
        
        logger.info("TESTING CODE")
        sandbox_states = self.terminal.run_llm_code(llm_code=final_code, test_cases=test_cases)
        error = sandbox_states['error']
        terminal_output = sandbox_states['output']
        
        logger.info("TESTING COMPLETED SUCCESSFULLY")
        return {"error": error, "logic_code": logic_code, "final_code": final_code, "terminal_output": terminal_output, "error_check_count": error_check_count}
        
    def decide_to_error_handle(self, state):
        logger.info("DECIDING WETHER TO ERROR HANDLE")
        error = state['error']
        error_check_count = state['error_check_count']
        
        if len(error):
            if error_check_count < 4:
                return "handle_error"
            else:
                return "regenerate"
        else:
            return "output_analysis"
    
    def error_handling(self, state):
        logger.info("FIXING ERROR")
        error_check_count = state['error_check_count']
        error = state['error']
        final_code = state['final_code']
        test_cases = state['test_cases']
        terminal_output = state['terminal_output']
        error_check_count +=1
        
        error_handler_output = self.error_handler.invoke({"final_code": final_code, "error": error})
        final_code = error_handler_output['code']
        
        logger.info("TESTING CODE")
        sandbox_states = self.terminal.run_llm_code(llm_code=final_code, test_cases=test_cases)
        error = sandbox_states['error']
        terminal_output = sandbox_states['output']
        
        logger.info(f"ERROR HANDLING COMPLETED: {error_check_count}")
        return {"final_code": final_code, "error": error, "terminal_output": terminal_output, "error_check_count": error_check_count}
     
    def output_analysis(self, state):
        logger.info("ANALYSING OUTPUT")
        terminal_output = state['terminal_output']
        question_analysis = state['question_analysis']
        math_analysis = state['math_analysis']
        error = state['error']
        final_code = state['final_code']
        logic_code = state['logic_code']
        required_output = state['required_output']
        test_cases = state['test_cases']
        regenerate_count = state['regenerate_count']  
        
        score = self.output_analyser.invoke({"test_cases": test_cases, "terminal_output": terminal_output, "required_output": required_output})['score']
        
        if score.lower() == "no":
            regenerate_count += 1
        else:
            regenerate_count = 0
        return {"regenerate_count": regenerate_count, "final_code": final_code, "logic_code": logic_code, "error": error, "terminal_output": terminal_output, "question_analysis": question_analysis, "math_analysis": math_analysis}
    
    def decide_to_regenerate(self, state):
        regenerate_count = state['regenerate_count']
        
        if regenerate_count > 5 or regenerate_count == 0:
            return "stop"
        else:
            return "regenerate"
    
    def app(self):
        logger.info(f"Lanchain Verbose:{self.langchain_config.set_verbose}")
        set_verbose(self.langchain_config.set_verbose)
        
        logger.info(f"Lanchain Debug:{self.langchain_config.set_debug}")
        set_debug(self.langchain_config.set_debug)
        
        logger.info("CONSTRUCTING NODES")
        self.workflow.add_node("analysis", self.analysis)
        self.workflow.add_node("generate", self.generation)
        self.workflow.add_node("error_handling", self.error_handling)
        self.workflow.add_node("output_analysis", self.output_analysis)
        
        logger.info("CONSTRUCTING GRAPH")
        self.workflow.set_entry_point("analysis")
        self.workflow.add_edge("analysis", "generate")
        self.workflow.add_conditional_edges(
            "generate",
            self.decide_to_error_handle,
            {
                "handle_error": "error_handling",
                "output_analysis": "output_analysis"
            },
        )

        self.workflow.add_conditional_edges(
            "error_handling",
            self.decide_to_error_handle,
            {
                "handle_error": "error_handling",
                "output_analysis": "output_analysis",
                "regenerate": "generate",
            }
        )

        self.workflow.add_conditional_edges(
            "output_analysis",
            self.decide_to_regenerate,
            {
                "stop": END,
                "regenerate": "generate"
            }
        )
        
        app = self.workflow.compile()
        return app