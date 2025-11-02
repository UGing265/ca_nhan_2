# /agents/agent_review.py

from google.genai import types
from utils.config import GEMINI_CLIENT, Config
from prompts.review_prompt import generate_review_prompt, SYSTEM_INSTRUCTION_REVIEW
import json


class ReviewAgent:
    def __init__(self):
        self.client = GEMINI_CLIENT
        self.model = Config.REVIEW_MODEL

    def review(self, code_snippet: str, language: str) -> list:
        """Perform source code review and return JSON results."""
        prompt = generate_review_prompt(code_snippet, language)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION_REVIEW,
                    temperature=Config.REVIEW_TEMPERATURE,
                    response_mime_type="application/json", # Request JSON output
                    response_schema={
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "issue_type": {"type": "string"},
                                "severity": {"type": "string", "enum": ["Critical", "Major", "Minor", "Hint"]},
                                "line": {"type": "integer"},
                                "context": {"type": "string"},
                                "description": {"type": "string"}
                            }
                        }
                    }
                )
            )
            return json.loads(response.text)

        except Exception as e:
            print(f"Lỗi khi gọi Review Agent: {e}")
            return []