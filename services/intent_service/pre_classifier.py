from typing import Optional
from services.domain.models import Intent
from services.shared_types import IntentCategory
import re
import string

class PreClassifier:
    """Rule-based pre-classification for common patterns"""
    
    # Greeting patterns
    GREETING_PATTERNS = [
        "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
        "greetings", "howdy", "hi there"
    ]
    
    # Farewell patterns  
    FAREWELL_PATTERNS = [
        "bye", "goodbye", "see you", "later", "farewell"
    ]
    
    # Thanks patterns
    THANKS_PATTERNS = [
        "thanks", "thank you", "thx", "ty", "much appreciated"
    ]
    
    # File reference patterns
    FILE_REFERENCE_PATTERNS = [
        r'\b(the file|that file|my file)\b',
        r'\b(the document|that document|my document)\b', 
        r'\b(what i uploaded|the upload|that upload)\b',
        r'\b(the csv|the pdf|the spreadsheet|the excel file)\b',
        r'\b(the report|that report|my report)\b',
        r'\b(the data file|that data file|my data file)\b'
    ]
    
    @staticmethod
    def pre_classify(message: str) -> Optional[Intent]:
        """Pre-classify message using rule-based patterns"""
        clean_msg = message.strip().lower()
        clean_for_matching = clean_msg.rstrip(string.punctuation + "!?.,;:😊🙂👋")
        
        # Check for greetings
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.GREETING_PATTERNS):
            return Intent(
                category=IntentCategory.CONVERSATION,
                action="greeting",
                confidence=1.0,
                context={"original_message": message}
            )
        
        # Check for farewells
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.FAREWELL_PATTERNS):
            return Intent(
                category=IntentCategory.CONVERSATION,
                action="farewell",
                confidence=1.0,
                context={"original_message": message}
            )
        
        # Check for thanks
        if clean_for_matching in PreClassifier.THANKS_PATTERNS:
            return Intent(
                category=IntentCategory.CONVERSATION,
                action="thanks",
                confidence=1.0,
                context={"original_message": message}
            )
        
        return None
    
    @staticmethod
    def detect_file_reference(message: str) -> bool:
        """Check if message references an uploaded file"""
        clean_msg = message.strip().lower()
        return PreClassifier._matches_patterns(clean_msg, PreClassifier.FILE_REFERENCE_PATTERNS)
    
    @staticmethod
    def _matches_patterns(message: str, patterns: list) -> bool:
        """Check if message matches any of the given patterns using regex"""
        for pattern in patterns:
            if re.search(pattern, message):
                return True
        return False 