from pathlib import Path

PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"

def load_prompt(version: str) -> str:
    path = PROMPT_DIR / f"{version}_answer_with_sources.txt"
    if not path.exists():
        raise FileNotFoundError(f"Prompt version not found: {path.name}")
    return path.read_text(encoding="utf-8")

def render_prompt(template: str, *, question: str, context: str) -> str:
    return template.format(question=question, context=context)
