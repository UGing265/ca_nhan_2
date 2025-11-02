# /prompts/repair_prompt.py

SYSTEM_INSTRUCTION_REPAIR = """
You are an AI Code Repairer. Your task is to receive a piece of broken code and a description of the problem, then propose a Python code fix.

IMPORTANT REQUIREMENTS:
- You will only be returned the final fix.

- Wrap the fix in a single Python Markdown block (```python...```).
- NO explanation, NO greeting, NO other text outside the code block.
"""


def generate_repair_prompt(original_code: str, issue_description: str) -> str:
    """Create specific prompts for code repair."""
    return f"""
    Original code snippet:
    ---
    {original_code}
    ---

    Problem needs fixing: {issue_description}

    Please provide the complete fixed code (not just the changed part) and ensure it complies with the output requirement (code block only).
    """