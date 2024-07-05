from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain.globals import set_verbose, set_debug
from utils.common import format_json, display_graph, json_quote_fixer

GOOGLE_API_KEY = "AIzaSyBO5I5F5VDjPxcTNTWD8SY0oH3X7eeDxbw"


class Agents:
    
    