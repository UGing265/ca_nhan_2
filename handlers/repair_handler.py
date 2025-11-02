# /handlers/repair_handler.py

from agents.agent_repair import RepairAgent


def handle_repair_request(original_code: str, issue_description: str) -> str | None:
    """Process the debug request and return the corrected code."""

    if not issue_description or not original_code:
        return None

    agent = RepairAgent()

    # Logic can add Tool Use/Function Calling here.

    repaired_code = agent.repair(original_code, issue_description)

    # Post-processing logic: For example, check the syntax of repaired_code before returning it.

    return repaired_code