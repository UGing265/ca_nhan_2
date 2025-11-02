# /utils/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Class contains configuration settings."""

    # Set up Gemini API Key
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Setup for Agent Review
    REVIEW_MODEL = "gemini-2.5-flash"
    REVIEW_TEMPERATURE = 0.5

    # Settings for Agent Repair
    REPAIR_MODEL = "gemini-2.5-flash"
    REPAIR_TEMPERATURE = 0.2  # Low temperature to ensure accuracy

    # Streamlit configuration
    APP_TITLE = "AI Code Review and Repair Agent"


# Check the API key
if not Config.GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY is not set in environment variables.")

# Initialize client
from google import genai

GEMINI_CLIENT = genai.Client(api_key=Config.GEMINI_API_KEY)
