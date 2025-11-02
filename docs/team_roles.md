# Team Roles and Responsibilities

## Team Structure (5-Person Team)

### 1. Team Lead / ADK Architect
**Name**: [TBD]
**Primary Responsibilities**:
- Design and implement ADK pipelines (`agents/workflow.py`)
- Manage ADK SessionService integration (`utils/session_manager.py`)
- Configuration management (`utils/config.py`)
- Integration strategy in `streamlit_app.py`
- Architecture documentation

**Key Files**:
- `agents/workflow.py`
- `utils/session_manager.py`
- `utils/config.py`
- `docs/architecture.md`
- `tests/test_workflow.py`

---

### 2. AI Agent Specialist (Reviewer)
**Name**: [TBD]
**Primary Responsibilities**:
- Implement CodeReviewerAgent (`agents/agent_review.py`)
- Design review prompts (`prompts/review_prompt.py`)
- Define review output schema
- Unit testing for review agent

**Key Files**:
- `agents/agent_review.py`
- `prompts/review_prompt.py`
- `tests/test_agents.py` (review tests)

---

### 3. AI Agent Specialist (Repairer)
**Name**: [TBD]
**Primary Responsibilities**:
- Implement CodeRefactorerAgent (`agents/agent_repair.py`)
- Design repair prompts (`prompts/repair_prompt.py`)
- Implement state loading logic
- Unit testing for repair agent

**Key Files**:
- `agents/agent_repair.py`
- `prompts/repair_prompt.py`
- `tests/test_agents.py` (repair tests)

---

### 4. Frontend Lead (Streamlit UI)
**Name**: [TBD]
**Primary Responsibilities**:
- UI layout design in `streamlit_app.py`
- Monaco Editor integration
- Custom CSS styling (`static/styles.css`)
- Streamlit configuration (`.streamlit/config.toml`)
- UI helper functions (`utils/ui_helpers.py`)

**Key Files**:
- `streamlit_app.py` (UI components)
- `static/styles.css`
- `.streamlit/config.toml`
- `utils/ui_helpers.py`

---

### 5. Frontend Logic (Streamlit State)
**Name**: [TBD]
**Primary Responsibilities**:
- State management in `streamlit_app.py`
- Implement `handle_review()` function (`handlers/review_handler.py`)
- Implement `handle_repair()` function (`handlers/repair_handler.py`)
- ADK Runner integration
- Handler unit testing

**Key Files**:
- `streamlit_app.py` (state logic)
- `handlers/review_handler.py`
- `handlers/repair_handler.py`
- `tests/test_handlers.py`

---

## Collaboration Guidelines
1. All team members should be familiar with the overall architecture
2. Use clear commit messages referencing your role and file ownership
3. Coordinate with Team Lead for integration points
4. Follow the coding standards in `examples/sample_policies.md`
5. Write tests for all new functionality
