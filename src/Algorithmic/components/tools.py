from Algorithmic.constants import PYTHON_CODE_EXECUTION_COMMAND
from Algorithmic.entity import TerminalConfig
import json
import tempfile
import docker
import os

class SandboxCodeExecutor:

    def __init__(self, config: TerminalConfig):
        self.client = docker.from_env()
        self.config = config
        
    def run_llm_code(self, llm_code: str, test_cases: str):
        
        with tempfile.TemporaryDirectory() as temp_dir:
            llm_code_file_path = os.path.join(temp_dir, 'llm_code.py')
            test_cases_file_path = os.path.join(temp_dir, 'test_cases.txt')
            
            with open(llm_code_file_path, 'w') as llm_code_file:
                llm_code_file.write(llm_code)
            
            with open(test_cases_file_path, 'w') as test_cases_file:
                test_cases_file.write(test_cases)
            
            try:
                container = self.client.containers.run(
                    self.config.python_image,
                    PYTHON_CODE_EXECUTION_COMMAND,
                    volumes = {temp_dir: {'bind': '/mnt', 'mode': 'rw'}},
                    detach = True,
                    stderr =  True,
                    stdout = True,
                )
                result = container.wait(timeout=10)
                terminal_output = container.logs().decode('utf-8')
                container.remove()
                
                terminal_out_json_fp = open(self.config.terminal_output_file, 'w', encoding='utf-8')
                terminal_output = {
                    "output": terminal_output if result['StatusCode'] == 0 else "", 
                    "error": terminal_output if result['StatusCode'] != 0 else "",
                }

                json.dump(terminal_output, terminal_out_json_fp, ensure_ascii=False, indent=4)
                
                return terminal_output
                
            except Exception as e:
                return {"error": str(e)}