# Architecture Documentation

## System Overview
The Copilot Review Project is a Streamlit-based AI code review tool powered by Google ADK.

## Architecture Diagram
```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI Layer                    │
│  (streamlit_app.py + Monaco Editor + st.session_state)  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ├──> handle_review() ──> root_agent_review
                 │                         (ADK Pipeline)
                 │                              │
                 │                              ├──> CodeReviewerAgent
                 │                              │    (saves to session.state)
                 │                              └──> Returns review_result
                 │
                 └──> handle_repair() ──> root_agent_repair
                                           (ADK Pipeline)
                                                │
                                                ├──> Loads session.state
                                                ├──> CodeRefactorerAgent
                                                └──> Returns repaired_code
```

## State Management

### Streamlit Session State
- `workflow_step`: UI state tracking ('input', 'review_complete', 'awaiting_decision', 'repair_complete')
- `adk_session_id`: ADK session identifier for continuity
- `code_input`: User's code
- `policy_input`: User's policies
- `review_result`: Review output
- `repaired_code`: Repair output

### ADK Session State
- `current_code`: Code being analyzed
- `review_comments`: Structured feedback
- `policies`: Applied policies

## Workflow Flow
1. User inputs code + policies
2. Click "Review" → handle_review() → root_agent_review
3. UI displays results + "Repair" / "Stop" buttons
4. If "Repair" clicked → handle_repair() → root_agent_repair
5. UI displays repaired code

## Technology Stack
- **Frontend/Backend**: Streamlit
- **Code Editor**: streamlit-monaco
- **AI Framework**: Google ADK
- **Session Management**: InMemorySessionService
- **LLM**: Gemini 2.0 Flash
