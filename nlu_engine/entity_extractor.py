# nlu_engine/entity_extractor.py
import re
from typing import Dict, List

class EntityExtractor:
    """Tiny regex-based entity extractor for testing."""

    AMOUNT_RE = re.compile(r"(?P<amount>\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b)")
    PHONE_RE = re.compile(r"\b\d{10}\b")
    EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        text = str(text)
        entities = {
            "amounts": self.AMOUNT_RE.findall(text),
            "phones": self.PHONE_RE.findall(text),
            "emails": self.EMAIL_RE.findall(text),
        }
        return entities

# Helper function for easier use
def extract_entities(text: str) -> Dict[str, List[str]]:
    ee = EntityExtractor()
    return ee.extract_entities(text)
