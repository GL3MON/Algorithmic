from langchain_core.messages import AIMessage
from typing import List
from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeColors
from langgraph.graph.state import CompiledStateGraph
from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeColors

import re


def format_json(output: AIMessage) -> AIMessage:
    '''
    Converts the LLM output to fit into langchain JsonOutputParser.
    Args:
    =====
    output: AIMessage
    '''
    json_regex_expression = r'\{[^{}]*\}'
    output.content = re.findall(json_regex_expression, output.content)[0]
    return output


def display_graph(app: CompiledStateGraph) -> None:
    '''
    Displays the whole constructed graph.
    Args:
    =====
    app: CompliedStateGraph
    '''
    
    display(
        Image(
            app.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API,
            )
        )
    )

def write_python_to_file(main_code: str, function: str = None) -> None:
    '''
    Formats the python code and writes the code to a local file.
    Args:
    =====    
    main_code: str
    function: str
    '''
    
    
    with open("../llm_code.py", 'w') as llm_file:
        llm_file.write(main_code)

def json_quote_fixer(json_str: str) -> str:
    '''
    Replaces Json string single quotes to double quotes to fit the JsonOutParser 
    '''
    return json_str.replace('"', "```").replace("'", '"')