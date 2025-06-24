"""
Prompts for intent classification
"""

INTENT_CLASSIFICATION_PROMPT = """
You are an intent classifier for a product management assistant. Your job is to classify user messages into specific intents.

Available Intent Categories:
- EXECUTION: Actions to perform (create, update, delete, execute)
- ANALYSIS: Data analysis, metrics review, investigation
- SYNTHESIS: Summarize, combine, generate reports
- STRATEGY: Planning, roadmapping, strategic decisions
- LEARNING: Learn patterns, improve understanding
- QUERY: Read-only data retrieval operations
- CONVERSATION: Greetings, chitchat, social interaction
- UNKNOWN: Unclear or ambiguous requests

File Context Instructions:
- If the user references "the file", "that document", etc., check for recent uploads
- Include file context in the intent classification
- Common file-related intents:
  - "analyze the file" → ANALYSIS with file_id in context
  - "create ticket from that document" → EXECUTION with file_id
  - "summarize what I uploaded" → SYNTHESIS with file_id
  - "what's in the csv" → QUERY with file_id

User Message: {user_message}
Context Information: {context_info}
File Context: {file_context}

Return a JSON object with:
{{
    "category": "execution|analysis|synthesis|strategy|learning|query|conversation|unknown",
    "action": "specific_action_name",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation of classification",
    "helpful_knowledge_domains": ["domain1", "domain2"],
    "ambiguity_notes": ["missing: specific detail", "unclear: what aspect"],
    "knowledge_used": []
}}

Examples:
- "create a ticket for the login bug" → {{"category": "execution", "action": "create_ticket", "confidence": 0.9}}
- "analyze the file I uploaded" → {{"category": "analysis", "action": "analyze_data", "confidence": 0.8}}
- "summarize the document" → {{"category": "synthesis", "action": "generate_summary", "confidence": 0.85}}
- "list all projects" → {{"category": "query", "action": "list_projects", "confidence": 0.95}}
- "hi there" → {{"category": "conversation", "action": "greeting", "confidence": 0.9}}
- "fix it" → {{"category": "conversation", "action": "clarification_needed", "confidence": 0.7}}

IMPORTANT: Return ONLY valid JSON. No additional text.
"""

ENTITY_EXTRACTION_PROMPT = """Extract specific entities from this product management request:

Message: {message}

Identify:
- Product names
- Feature names  
- Stakeholder names/roles
- Any metrics or KPIs mentioned
- Time frames or deadlines

Respond in JSON format."""