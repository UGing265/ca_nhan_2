# /agents/workflow.py

from agents.agent_review import ReviewAgent
from agents.agent_repair import RepairAgent


def run_code_review_workflow(code_input: str, language: str) -> tuple[list, str | None]:
    """
    Run the review and repair flow:
        1. Run ReviewAgent to find the problem.
        2. If there is a problem, select the most serious problem and run RepairAgent.
    """

    review_agent = ReviewAgent()
    repair_agent = RepairAgent()

    # 1. Run Review
    review_results = review_agent.review(code_input, language)

    repaired_code = None

    if review_results:
        # Suppose we just fix the first problem we find.
        first_issue = review_results[0]
        issue_desc = f"Issue: {first_issue['description']} at line {first_issue['line']}."

        # 2. Run Repair
        repaired_code = repair_agent.repair(code_input, issue_desc, language)

    return review_results, repaired_code
