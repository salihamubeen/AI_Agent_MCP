# backend/config.py
from pathlib import Path

class Settings:
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Department keywords for guardrail
    DEPARTMENT_KEYWORDS: list = [
        "department", "faculty", "school", "program", "course",
        "engineering", "computer", "electrical", "mechanical",
        "civil", "chemical", "architecture", "business",
        "admission", "fee", "tuition", "lab", "facility",
        "requirement", "apply", "degree", "bachelor", "master"
    ]

settings = Settings()