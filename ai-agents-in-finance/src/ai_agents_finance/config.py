import os

from dotenv import load_dotenv

load_dotenv()

def load_config():
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "openai_model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "gemini_api_key": os.getenv("GEMINI_API_KEY"),
        "gemini_model": os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
        "gemini_fallback_model": os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.6-flash"),
        "financial_modeling_prep_api_key": os.getenv("FINANCIAL_MODELING_PREP_API_KEY"),
        "langsmith_tracing": os.getenv("LANGSMITH_TRACING"),
        "langsmith_endpoint": os.getenv("LANGSMITH_ENDPOINT"),
        "langsmith_api_key": os.getenv("LANGSMITH_API_KEY"),
        "langsmith_project": os.getenv("LANGSMITH_PROJECT"),
        "hf_token": os.getenv("HF_TOKEN")
    }
