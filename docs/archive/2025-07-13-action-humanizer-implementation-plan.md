# Action Humanizer Implementation Plan

## Objective
Implement a smart caching system to convert technical action strings (e.g., `investigate_crash`) into natural language (e.g., "investigate a crash") for user-facing messages.

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   UI Messages   │────▶│ Action Humanizer │────▶│   Cache Store   │
│    Templates    │     │     Service      │     │   (Database)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │   LLM Client     │
                        │ (Generate if new)│
                        └──────────────────┘
```

## Implementation Steps for Cursor Assistant

### Step 1: Create Database Table for Cache

**File**: New migration in `alembic/versions/`

```python
"""add action humanization cache table

Revision ID: [generated]
Create Date: [generated]
"""

def upgrade():
    op.create_table(
        'action_humanizations',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('action', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('human_readable', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('usage_count', sa.Integer(), default=0),
        sa.Column('last_used', sa.DateTime(), nullable=True)
    )

def downgrade():
    op.drop_table('action_humanizations')
```

### Step 2: Create Domain Model

**File**: `services/domain/models.py` (add to existing)

```python
@dataclass
class ActionHumanization:
    """Cached human-readable version of technical action strings"""
    id: str = field(default_factory=lambda: str(uuid4()))
    action: str = ""  # e.g., "investigate_crash"
    category: Optional[str] = None  # e.g., "ANALYSIS"
    human_readable: str = ""  # e.g., "investigate a crash"
    created_at: datetime = field(default_factory=datetime.now)
    usage_count: int = 0
    last_used: Optional[datetime] = None
```

### Step 3: Create Database Model

**File**: `services/persistence/models.py` (add to existing)

```python
class ActionHumanizationDB(Base):
    __tablename__ = "action_humanizations"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    action = Column(String(255), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=True)
    human_readable = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime, nullable=True)

    def to_domain(self) -> ActionHumanization:
        return ActionHumanization(
            id=self.id,
            action=self.action,
            category=self.category,
            human_readable=self.human_readable,
            created_at=self.created_at,
            usage_count=self.usage_count,
            last_used=self.last_used
        )
```

### Step 4: Create Repository

**File**: `services/persistence/repositories/action_humanization_repository.py`

```python
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from services.domain.models import ActionHumanization
from services.persistence.models import ActionHumanizationDB

class ActionHumanizationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_action(self, action: str) -> Optional[ActionHumanization]:
        """Get humanization by action string"""
        result = await self.session.execute(
            select(ActionHumanizationDB).where(
                ActionHumanizationDB.action == action
            )
        )
        db_obj = result.scalar_one_or_none()
        return db_obj.to_domain() if db_obj else None

    async def create(self, humanization: ActionHumanization) -> ActionHumanization:
        """Store new humanization"""
        db_obj = ActionHumanizationDB(
            id=humanization.id,
            action=humanization.action,
            category=humanization.category,
            human_readable=humanization.human_readable,
            created_at=humanization.created_at
        )
        self.session.add(db_obj)
        await self.session.commit()
        return humanization

    async def increment_usage(self, action: str) -> None:
        """Track usage for analytics"""
        await self.session.execute(
            update(ActionHumanizationDB)
            .where(ActionHumanizationDB.action == action)
            .values(
                usage_count=ActionHumanizationDB.usage_count + 1,
                last_used=datetime.utcnow()
            )
        )
        await self.session.commit()
```

### Step 5: Create Humanizer Service

**File**: `services/ui_messages/action_humanizer.py`

```python
import re
from typing import Optional
from services.domain.models import ActionHumanization
from services.persistence.repositories.action_humanization_repository import ActionHumanizationRepository
from services.llm.client import LLMClient

class ActionHumanizer:
    """Service to convert technical action strings to natural language"""

    def __init__(self, repo: ActionHumanizationRepository, llm_client: LLMClient):
        self.repo = repo
        self.llm_client = llm_client

    async def humanize(self, action: str, category: Optional[str] = None) -> str:
        """Convert technical action to human-readable format"""

        # Check cache first
        cached = await self.repo.get_by_action(action)
        if cached:
            await self.repo.increment_usage(action)
            return cached.human_readable

        # Try rule-based conversion first
        human_readable = self._apply_rules(action)

        # If rules don't produce good result, use LLM
        if human_readable == action or '_' in human_readable:
            human_readable = await self._generate_with_llm(action, category)

        # Cache the result
        humanization = ActionHumanization(
            action=action,
            category=category,
            human_readable=human_readable
        )
        await self.repo.create(humanization)

        return human_readable

    def _apply_rules(self, action: str) -> str:
        """Simple rule-based conversion for common patterns"""
        # Handle common verb patterns
        if '_' not in action:
            return action

        parts = action.split('_')

        # Common patterns: verb_noun → verb a noun
        if len(parts) == 2:
            verb, noun = parts
            if verb in ['create', 'investigate', 'analyze', 'review', 'update', 'delete']:
                return f"{verb} a {noun}"
            elif verb in ['list', 'count']:
                return f"{verb} {noun}s"  # pluralize

        # Default: just replace underscores
        return action.replace('_', ' ')

    async def _generate_with_llm(self, action: str, category: Optional[str] = None) -> str:
        """Use LLM to generate natural language version"""

        prompt = f"""Convert this technical action identifier to natural conversational English.

Technical action: {action}
{"Category: " + category if category else ""}

Examples:
- investigate_crash → investigate a crash
- create_github_issue → create a GitHub issue
- analyze_performance → analyze performance
- review_pull_request → review a pull request
- update_user_story → update a user story

Important:
- Keep it concise (2-5 words)
- Use proper articles (a, an, the) where appropriate
- Recognize common abbreviations (github → GitHub, api → API, db → database)
- Maintain the action verb

Natural language version:"""

        response = await self.llm_client.complete(
            prompt,
            max_tokens=20,
            temperature=0.3  # Low temperature for consistency
        )

        return response.strip()
```

### Step 6: Integrate with Message Templates

**File**: Update `services/ui_messages/templates.py`

```python
# Add to existing template module

from services.ui_messages.action_humanizer import ActionHumanizer

class TemplateRenderer:
    """Enhanced template rendering with action humanization"""

    def __init__(self, humanizer: ActionHumanizer):
        self.humanizer = humanizer

    async def render_template(
        self,
        template: str,
        intent_action: str,
        intent_category: Optional[str] = None,
        **kwargs
    ) -> str:
        """Render template with humanized action"""

        # Humanize the action if it appears in the template
        if "{action}" in template or "{human_action}" in template:
            human_action = await self.humanizer.humanize(intent_action, intent_category)
            kwargs['action'] = intent_action  # Keep original
            kwargs['human_action'] = human_action  # Add humanized

        return template.format(**kwargs)
```

### Step 7: Update Main.py Integration

**File**: Update response handling in `main.py`

```python
# In the dependency injection setup
action_humanizer = ActionHumanizer(
    repo=ActionHumanizationRepository(db_session),
    llm_client=llm_client
)
template_renderer = TemplateRenderer(humanizer=action_humanizer)

# In response formatting
if workflow.status == WorkflowStatus.RUNNING:
    # Use humanized action in the message
    message = await template_renderer.render_template(
        "I understand you want to {human_action}. I've started a workflow to handle this.",
        intent_action=intent.action,
        intent_category=intent.category.value
    )
```

### Step 8: Add Pre-populated Common Actions (Optional)

**File**: `scripts/seed_humanizations.py`

```python
# Script to pre-populate common action humanizations

COMMON_ACTIONS = [
    ("investigate_issue", "investigate an issue"),
    ("investigate_crash", "investigate a crash"),
    ("create_ticket", "create a ticket"),
    ("create_github_issue", "create a GitHub issue"),
    ("analyze_performance", "analyze performance"),
    ("analyze_metrics", "analyze metrics"),
    ("review_code", "review code"),
    ("update_requirements", "update requirements"),
    # Add more as needed
]

async def seed_humanizations():
    # Implementation to pre-populate cache
    pass
```

## Testing Plan

1. **Unit Tests**: Test rule-based conversion
2. **Integration Tests**: Test cache hit/miss scenarios
3. **LLM Mock Tests**: Test LLM generation with mocked responses
4. **End-to-End**: Verify messages show humanized actions

## Success Criteria

- No more snake_case strings in user messages
- Consistent translations for same actions
- Fast response times (cache hits)
- Graceful handling of new actions
- Natural, conversational output

## Non-blocking Implementation

This can be implemented incrementally:
1. Start with rule-based only (no LLM) for testing
2. Add database/cache layer
3. Add LLM generation
4. Gradually roll out to different message types

The system will work at each stage, getting progressively better.
