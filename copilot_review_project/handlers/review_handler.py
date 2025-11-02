# /handlers/review_handler.py

from agents.agent_review import ReviewAgent


def handle_review_request(code_input: str) -> list:
    """Process review requests and return standardized results."""

    if not code_input.strip():
        return []

    agent = ReviewAgent()

    # Here you can add source code preprocessing logic (e.g. run linter, check syntax)

    review_results = agent.review(code_input)

    # Here post-processing logic can be added (e.g. filtering, sorting results)

    return review_results