# \ca_nhan_2\prompts\repair_prompt.py

SYSTEM_INSTRUCTION_REPAIR = """
You are an AI Code Repairer. Your task is to receive a piece of broken code and a description of the problem, then propose a code fix in the original language.
IMPORTANT REQUIREMENTS:
- You will only be returned the final fix.
- Wrap the fix in a single Markdown block (e.g., ```python...``` or ```javascript...```).
- NO explanation, NO greeting, NO other text outside the code block.
"""


def generate_repair_prompt(original_code: str, issue_description: str, language: str = "code") -> str:
    """Create specific prompts for code repair."""
    return f"""
Original {language} code snippet:
---
{original_code}
---
Problem needs fixing: {issue_description}
Please provide the complete fixed code (not just the changed part) and ensure it complies with the output requirement (code block only).
""".strip()  # Dùng .strip()
