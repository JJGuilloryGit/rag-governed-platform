"""Prompt regression tests.

Run:
  python -m evaluation.prompt_regression_tests
"""
from pathlib import Path
import difflib

PROMPTS = ["v1", "v2"]

def test_prompts_exist():
    base = Path(__file__).resolve().parents[1] / "prompts"
    for v in PROMPTS:
        fp = base / f"{v}_answer_with_sources.txt"
        assert fp.exists(), f"Missing prompt: {fp.name}"

def test_no_unbounded_instructions():
    base = Path(__file__).resolve().parents[1] / "prompts"
    for v in PROMPTS:
        txt = (base / f"{v}_answer_with_sources.txt").read_text(encoding="utf-8").lower()
        assert "ignore previous" not in txt, "Potential prompt injection anti-pattern in template"

if __name__ == "__main__":
    test_prompts_exist()
    test_no_unbounded_instructions()
    print("All prompt governance tests passed.")
