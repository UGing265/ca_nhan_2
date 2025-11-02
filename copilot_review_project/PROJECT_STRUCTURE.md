# Copilot Review Project - File Structure

```
/copilot_review_project/
│
├── .env
│   # (Team-wide) Stores environment variables and API keys (e.g., GOOGLE_API_KEY, GEMINI_MODEL_NAME).
│
├── .gitignore
│   # (Team-wide) Specifies files/folders to exclude from version control (e.g., .env, __pycache__, .streamlit/).
│
├── requirements.txt
│   # (Team-wide) Lists Python dependencies: google-adk, streamlit, streamlit-monaco-editor, python-dotenv.
│
├── README.md
│   # (Team-wide) Project documentation: setup instructions, architecture overview, and usage guide.
│
├── streamlit_app.py
│   # (Role: Team Lead + Frontend Lead + Frontend Logic) Main Streamlit application entry point. Integrates Monaco editor, manages st.session_state (workflow steps, session_id), calls ADK pipelines, and renders the UI layout.
│
├── .streamlit/
│   └── config.toml
│       # (Role: Frontend Lead) Streamlit configuration file for theme, layout settings, and custom styling.
│
├── /agents/
│   │
│   ├── __init__.py
│   │   # (Role: Team Lead) Makes the agents directory a Python package. Exports key agents for easy imports.
│   │
│   ├── workflow.py
│   │   # (Role: Team Lead / ADK Architect) Defines the two main ADK SequentialAgent pipelines: root_agent_review and root_agent_repair. Orchestrates sub-agents and manages ADK SessionService.
│   │
│   ├── agent_review.py
│   │   # (Role: AI Agent Specialist - Reviewer) Implements the CodeReviewerAgent (LlmAgent). Contains the review prompt, instructions, and output_key configuration to save review results to session.state.
│   │
│   └── agent_repair.py
│       # (Role: AI Agent Specialist - Repairer) Implements the CodeRefactorerAgent (LlmAgent). Contains the repair prompt, instructions, and logic to load code/comments from session.state and generate repaired_code.
│
├── /prompts/
│   │
│   ├── __init__.py
│   │   # (Team-wide) Makes the prompts directory a Python package.
│   │
│   ├── review_prompt.py
│   │   # (Role: AI Agent Specialist - Reviewer) Contains the system prompt template for the code review agent. Defines how to analyze code against policies and return structured feedback.
│   │
│   └── repair_prompt.py
│       # (Role: AI Agent Specialist - Repairer) Contains the system prompt template for the code repair agent. Defines how to read review comments and refactor code while preserving functionality.
│
├── /utils/
│   │
│   ├── __init__.py
│   │   # (Team-wide) Makes the utils directory a Python package.
│   │
│   ├── config.py
│   │   # (Role: Team Lead) Loads environment variables from .env (using python-dotenv). Exports configuration constants like MODEL_NAME, API_KEY, etc.
│   │
│   ├── session_manager.py
│   │   # (Role: Team Lead / ADK Architect) Initializes and manages the ADK SessionService (InMemorySessionService). Provides helper functions to create/retrieve ADK sessions.
│   │
│   └── ui_helpers.py
│       # (Role: Frontend Lead) Contains reusable UI helper functions for Streamlit (e.g., render_code_editor, render_review_result, apply_custom_css).
│
├── /handlers/
│   │
│   ├── __init__.py
│   │   # (Team-wide) Makes the handlers directory a Python package.
│   │
│   ├── review_handler.py
│   │   # (Role: Frontend Logic) Implements the handle_review() function. Invokes the root_agent_review pipeline via ADK Runner, stores session_id in st.session_state, and returns review results.
│   │
│   └── repair_handler.py
│       # (Role: Frontend Logic) Implements the handle_repair() function. Invokes the root_agent_repair pipeline using the stored session_id, retrieves repaired code, and updates UI state.
│
├── /static/
│   │
│   ├── styles.css
│   │   # (Role: Frontend Lead) Custom CSS for styling the Streamlit app to achieve a "VSCode-like" appearance (dark theme, Monaco editor styling, button styles).
│   │
│   └── logo.png
│       # (Team-wide) Optional project logo displayed in the Streamlit sidebar or header.
│
├── /tests/
│   │
│   ├── __init__.py
│   │   # (Team-wide) Makes the tests directory a Python package.
│   │
│   ├── test_agents.py
│   │   # (Role: AI Agent Specialists) Unit tests for agent_review.py and agent_repair.py. Tests agent initialization, prompt validation, and output format.
│   │
│   ├── test_workflow.py
│   │   # (Role: Team Lead) Integration tests for workflow.py. Tests the full review and repair pipelines end-to-end.
│   │
│   ├── test_handlers.py
│   │   # (Role: Frontend Logic) Unit tests for review_handler.py and repair_handler.py. Tests state management and ADK Runner invocation.
│   │
│   └── test_utils.py
│       # (Team-wide) Unit tests for utility functions in /utils/ (config loading, session management, UI helpers).
│
├── /examples/
│   │
│   ├── sample_code.py
│   │   # (Team-wide) Example Python code file for testing the review system (contains intentional issues to trigger review comments).
│   │
│   └── sample_policies.md
│       # (Team-wide) Example policy document with coding standards and rules (e.g., "All functions must have docstrings", "No hardcoded credentials").
│
└── /docs/
    │
    ├── architecture.md
    │   # (Role: Team Lead) Technical architecture documentation. Describes the ADK pipeline design, Streamlit state flow, and Human-in-the-Loop workflow.
    │
    ├── team_roles.md
    │   # (Team-wide) Defines the 5-person team structure, responsibilities, and file ownership for each role.
    │
    └── deployment.md
        # (Role: Team Lead) Deployment guide for running the Streamlit app locally and deploying to cloud platforms (Streamlit Cloud, Cloud Run, etc.).
```

## Key Architecture Notes

### State Management Flow:
1. **Streamlit Session State (`st.session_state`):**
   - `workflow_step`: Tracks UI state ('input', 'review_complete', 'awaiting_decision', 'repair_complete')
   - `adk_session_id`: Stores the ADK session ID for continuity between review and repair
   - `code_input`: User's input code
   - `policy_input`: User's input policies
   - `review_result`: Output from review agent
   - `repaired_code`: Output from repair agent

2. **ADK Session State (`session.state`):**
   - `current_code`: The code being reviewed/repaired
   - `review_comments`: Structured feedback from the reviewer agent
   - `policies`: The policies used for review
   - Used by agents to maintain context between review and repair operations

### ADK Pipeline Architecture:
- **root_agent_review**: SequentialAgent → CodeReviewerAgent → saves to session.state
- **root_agent_repair**: SequentialAgent → loads session.state → CodeRefactorerAgent → returns repaired_code

### Team Ownership Summary:
1. **Team Lead / ADK Architect**: workflow.py, session_manager.py, config.py, architecture docs
2. **AI Agent Specialist (Reviewer)**: agent_review.py, review_prompt.py, related tests
3. **AI Agent Specialist (Repairer)**: agent_repair.py, repair_prompt.py, related tests
4. **Frontend Lead (Streamlit UI)**: UI layout in streamlit_app.py, styles.css, ui_helpers.py, config.toml
5. **Frontend Logic (Streamlit State)**: State management in streamlit_app.py, review_handler.py, repair_handler.py
