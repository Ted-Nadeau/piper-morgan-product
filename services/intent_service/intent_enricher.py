from typing import Optional
from services.domain.models import Intent
from services.file_context.file_resolver import FileResolver
from services.file_context.exceptions import AmbiguousFileReferenceError
from services.intent_service.pre_classifier import PreClassifier
from services.repositories.file_repository import FileRepository
import logging

logger = logging.getLogger(__name__)

class IntentEnricher:
    """Enriches intents with additional context like resolved files"""
    
    def __init__(self, db):
        self.db = db
        self.file_repository = FileRepository(db)
        self.file_resolver = FileResolver(self.file_repository)
    
    async def enrich_with_file_context(
        self, 
        intent: Intent, 
        session_id: str
    ) -> Intent:
        """Add resolved file references to intent context"""
        
        # Check if message contains file reference
        original_message = intent.context.get('original_message', '')
        if not PreClassifier.detect_file_reference(original_message):
            return intent
        
        try:
            # Resolve file reference
            file_id, confidence = await self.file_resolver.resolve_file_reference(
                intent, session_id
            )
            
            # Handle based on confidence
            if confidence > 0.8:
                # High confidence - proceed automatically
                intent.context['resolved_file_id'] = file_id
                intent.context['file_confidence'] = confidence
                logger.info(f"Resolved file with high confidence: {file_id} ({confidence:.2f})")
                
            elif confidence > 0.5:
                # Medium confidence - proceed but flag for confirmation
                intent.context['probable_file_id'] = file_id
                intent.context['file_confidence'] = confidence
                intent.context['needs_file_confirmation'] = True
                logger.info(f"Resolved file with medium confidence: {file_id} ({confidence:.2f})")
                
            else:
                # Low confidence - need clarification
                intent.context['needs_file_clarification'] = True
                logger.info("Low confidence file resolution - clarification needed")
                
        except AmbiguousFileReferenceError as e:
            # Multiple files matched - need disambiguation
            intent.context['needs_file_clarification'] = True
            intent.context['ambiguous_files'] = [
                {'id': f.id, 'filename': f.filename, 'upload_time': f.upload_time.isoformat()}
                for f in e.files
            ]
            logger.info(f"Ambiguous file reference: {len(e.files)} matches")
            
        except Exception as e:
            logger.error(f"Error during file resolution: {e}")
            # Don't fail the whole intent, just skip file resolution
            
        return intent
    
    async def enrich(self, intent: Intent, session_id: str) -> Intent:
        """Main enrichment method - can be extended for other enrichments"""
        # File context enrichment
        intent = await self.enrich_with_file_context(intent, session_id)
        
        # Future: Add other enrichments here
        # - Project context enrichment
        # - User preference enrichment
        # - Historical context enrichment
        
        return intent 