from langchain_core.messages import AIMessage
from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeColors
from langgraph.graph.state import CompiledStateGraph
from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeColors
from Algorithmic.logging import logger
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
import yaml
import re
import os

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")



@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"




@ensure_annotations
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


@ensure_annotations
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

@ensure_annotations
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
        

@ensure_annotations
def json_quote_fixer(json_str: str) -> str:
    '''
    Replaces Json string single quotes to double quotes to fit the JsonOutParser 
    '''
    return json_str.replace('"', "```").replace("'", '"')