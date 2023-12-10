from pathlib import Path

instructions_path = Path(__file__).parent / 'instructions'

def read_prompt(name: str) -> str:
    with open(instructions_path / (name + '.txt')) as f:
        return f.read()
