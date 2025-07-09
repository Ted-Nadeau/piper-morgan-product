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
    
    # File reference patterns (with variations and typo tolerance)
    FILE_REFERENCE_PATTERNS = [
        # Direct references
        r'\b(the file|that file|my file|this file)\b',
        r'\b(the document|that document|my document|this document)\b',
        r'\b(the doc|that doc|my doc|this doc)\b',
        r'\b(what i uploaded|the upload|that upload|this upload)\b',
        
        # File types
        r'\b(the csv|that csv|my csv|this csv)\b',
        r'\b(the pdf|that pdf|my pdf|this pdf)\b',
        r'\b(the spreadsheet|that spreadsheet|my spreadsheet|this spreadsheet)\b',
        r'\b(the excel file|that excel file|my excel file|this excel file)\b',
        r'\b(the report|that report|my report|this report)\b',
        r'\b(the data file|that data file|my data file|this data file)\b',
        r'\b(the text file|that text file|my text file|this text file)\b',
        r'\b(the markdown file|that markdown file|my markdown file|this markdown file)\b',
        r'\b(the json file|that json file|my json file|this json file)\b',
        
        # Abbreviated forms
        r'\b(the txt|that txt|my txt|this txt)\b',
        r'\b(the md|that md|my md|this md)\b',
        r'\b(the xlsx|that xlsx|my xlsx|this xlsx)\b',
        r'\b(the docx|that docx|my docx|this docx)\b',
        
        # Generic patterns with adjectives
        r'\b(that \w+(?:\s+\w+)* file|the \w+(?:\s+\w+)* file|my \w+(?:\s+\w+)* file|this \w+(?:\s+\w+)* file)\b',
        r'\b(that \w+(?:\s+\w+)* document|the \w+(?:\s+\w+)* document|my \w+(?:\s+\w+)* document|this \w+(?:\s+\w+)* document)\b',
        r'\b(that \w+(?:\s+\w+)* doc|the \w+(?:\s+\w+)* doc|my \w+(?:\s+\w+)* doc|this \w+(?:\s+\w+)* doc)\b',
        
        # Common typos and variations
        r'\b(teh file|taht file|th file)\b',
        r'\b(documnet|docuemnt|docment)\b',
        r'\b(fiel|fils|fille)\b',
        r'\b(uploded|uplaoded|uploadd)\b',
        r'\b(reprot|reoprt|raport)\b',
        r'\b(excell|exel|excel)\b',
        r'\b(spreedsheet|spredsheet|spreadsheat)\b',
        
        # Integration-related typos (from handoff doc)
        r'\b(intregration|integartion|intergration)\b',
        r'\b(analys[ei]s|analisys|anlyze)\b',
        r'\b(summar[iy]ze|summerize|summarise)\b'
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
    def get_file_reference_confidence(message: str) -> float:
        """Calculate confidence score for file reference detection"""
        clean_msg = message.strip().lower()
        
        # Different patterns have different confidence weights
        high_confidence_patterns = [
            r'\b(the file|that file|my file|this file)\b',
            r'\b(the document|that document|my document|this document)\b',
            r'\b(what i uploaded|the upload|that upload|this upload|my upload)\b',
        ]
        
        medium_confidence_patterns = [
            r'\b(the csv|that csv|my csv|this csv)\b',
            r'\b(the pdf|that pdf|my pdf|this pdf)\b',
            r'\b(the doc|that doc|my doc|this doc)\b',
            r'\b(the report|that report|my report|this report)\b',
        ]
        
        low_confidence_patterns = [
            r'\b(teh file|taht file|th file)\b',
            r'\b(documnet|docuemnt|docment)\b',
            r'\b(fiel|fils|fille)\b',
            r'\b(uploded|uplaoded|uploadd)\b',
        ]
        
        # Check for matches and return highest confidence
        if PreClassifier._matches_patterns(clean_msg, high_confidence_patterns):
            return 0.9
        elif PreClassifier._matches_patterns(clean_msg, medium_confidence_patterns):
            return 0.7
        elif PreClassifier._matches_patterns(clean_msg, low_confidence_patterns):
            return 0.5
        elif PreClassifier._matches_patterns(clean_msg, PreClassifier.FILE_REFERENCE_PATTERNS):
            return 0.6  # Generic patterns
        else:
            return 0.0
    
    @staticmethod
    def _matches_patterns(message: str, patterns: list) -> bool:
        """Check if message matches any of the given patterns using regex"""
        for pattern in patterns:
            if re.search(pattern, message):
                return True
        return False 