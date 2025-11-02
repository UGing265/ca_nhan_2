# Deployment Guide

## Local Development

### Prerequisites
- Python 3.9+
- Google Cloud account with Gemini API access
- Git

### Setup Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd copilot_review_project
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

5. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

6. Open browser to: `http://localhost:8501`

---

## Cloud Deployment

### Option 1: Streamlit Community Cloud
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add secrets in Streamlit Cloud dashboard:
   - `GOOGLE_API_KEY`
   - `GEMINI_MODEL_NAME`
5. Deploy

### Option 2: Google Cloud Run
1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8080
   CMD streamlit run streamlit_app.py --server.port=8080
   ```

2. Build and deploy:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/copilot-review
   gcloud run deploy copilot-review \
     --image gcr.io/PROJECT_ID/copilot-review \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### Option 3: Docker Compose (Local)
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    env_file:
      - .env
```

---

## Environment Variables
Required:
- `GOOGLE_API_KEY`: Your Google AI API key
- `GEMINI_MODEL_NAME`: Model to use (default: gemini-2.0-flash-exp)

Optional:
- `STREAMLIT_SERVER_PORT`: Port number (default: 8501)
- `STREAMLIT_THEME`: Theme configuration

---

## Monitoring and Logs
- Streamlit logs: Check console output
- ADK session tracking: Implemented in `utils/session_manager.py`
- Error handling: See `handlers/` for error capture logic
