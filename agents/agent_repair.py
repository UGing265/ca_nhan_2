# ca_nhan_2\agents\agent_repair.py

from google.genai import types
from utils.config import GEMINI_CLIENT, Config
from prompts.repair_prompt import generate_repair_prompt, SYSTEM_INSTRUCTION_REPAIR
import re


class RepairAgent:
    def __init__(self):
        self.client = GEMINI_CLIENT
        self.model = Config.REPAIR_MODEL

    def repair(self, original_code: str, issue_description: str, language: str) -> str | None:
        prompt = generate_repair_prompt(original_code, issue_description, language)

        language_regex = language if language not in ['text', 'code'] else '.*?'

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION_REPAIR,
                    temperature=Config.REPAIR_TEMPERATURE
                )
            )

            code_block_match = re.search(rf"```({language_regex})\n(.*?)\n```", response.text, re.DOTALL)

            if code_block_match:
                return code_block_match.group(2).strip()
            else:
                print(f"Error: No code block found in Repair Agent response for language '{language}'. Response: {response.text[:100]}...")
                return None
        except Exception as e:
            print(f"Error calling Repair Agent: {e}")
            return None
