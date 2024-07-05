from pathlib import Path

CONFIG_PATH = Path("config/config.yaml")

PYTHON_CODE_EXECUTION_COMMAND = 'bash -c "python /mnt/llm_code.py < /mnt/test_cases.txt"'