from pathlib import Path

prompts_path = Path(__file__).parent / 'prompts'

def read_prompt(name: str) -> str:
    with open(prompts_path / (name + '.txt')) as f:
        return f.read()
