import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "degistir-bunu")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")

    # Veritabanı
    DATABASE_PATH = os.path.join("instance", "app.db")

    # Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
