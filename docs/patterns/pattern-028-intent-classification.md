# Pattern-028: Intent Classification

## Status
Experimental (Original vision from May 28, 2025)

## Context
When users interact with Piper Morgan through natural language, their intent needs to be classified to route to appropriate handlers. This pattern transforms ambiguous natural language into actionable intent types.

## Pattern

### Core Intent Types (May 28 Vision)
```python
class IntentType(Enum):
    CREATE_ISSUE = "create_issue"      # User wants to create a new GitHub issue
    REVIEW_ISSUE = "review_issue"      # User wants to review/update existing issue
    QUERY_KNOWLEDGE = "query_knowledge" # User asking about project knowledge
    ANALYZE_DATA = "analyze_data"      # User requesting data analysis
    CLARIFY = "clarify"               # User needs clarification/multi-turn
    CHAT = "chat"                     # General conversation
```

### Simple Classification Approach
```python
class IntentClassifier:
    """
    Map natural language to intent types using pattern matching
    initially, evolving to ML-based classification.
    """

    def classify(self, user_input: str) -> IntentType:
        """
        Phase 1: Keyword-based classification
        Phase 2: LLM-based classification
        Phase 3: Fine-tuned model
        """
        input_lower = user_input.lower()

        # Phase 1 Implementation (Current)
        if any(word in input_lower for word in ['create', 'new', 'add', 'issue', 'ticket']):
            return IntentType.CREATE_ISSUE
        elif any(word in input_lower for word in ['review', 'update', 'check', 'status']):
            return IntentType.REVIEW_ISSUE
        elif any(word in input_lower for word in ['what', 'how', 'explain', 'tell me']):
            return IntentType.QUERY_KNOWLEDGE
        elif any(word in input_lower for word in ['analyze', 'trends', 'metrics', 'data']):
            return IntentType.ANALYZE_DATA
        elif '?' in user_input and len(user_input.split()) < 5:
            return IntentType.CLARIFY
        else:
            return IntentType.CHAT
```

### Integration with Workflow Router
```python
# In services/queries/router.py
async def route_query(self, query: QueryModel) -> QueryResponse:
    # First classify intent
    intent = self.intent_classifier.classify(query.text)

    # Then route to appropriate handler
    if intent == IntentType.CREATE_ISSUE:
        return await self.github_service.create_issue_workflow(query)
    elif intent == IntentType.QUERY_KNOWLEDGE:
        return await self.knowledge_service.query(query)
    # ... etc
```

## Benefits
- **Natural interaction**: Users don't need to learn commands
- **Progressive enhancement**: Start simple, evolve to sophisticated
- **Universal entry point**: All interactions flow through intent classification
- **Learning opportunity**: Every classification can improve the model

## Trade-offs
- **Initial accuracy**: Keyword-based approach has limitations
- **Context loss**: Single-turn classification misses conversation history
- **Training data**: Needs accumulated interactions to improve
- **Ambiguity**: Some inputs may have multiple valid intents

## Implementation Strategy

### Phase 1: Basic Classification (Week 1)
- Implement keyword-based classifier
- Log all classifications for training data
- Add to query router

### Phase 2: LLM Enhancement (Week 2)
- Use Claude for classification
- Compare with keyword approach
- A/B test for accuracy

### Phase 3: Learning Integration (Week 3)
- Store classification results
- Build training dataset
- Implement feedback loop

## Related Patterns
- [Pattern-006: Query Router](pattern-006-query-router.md)
- [Pattern-017: Multi-Agent Coordination](pattern-017-multi-agent-coordination.md)
- [Pattern-029: Plugin Interface](pattern-029-plugin-interface.md)

## References
- Original vision: May 28, 2025 genesis documents
- Related issue: #96 (FEAT-INTENT)
- Implementation location: services/queries/intent_classifier.py (to be created)
