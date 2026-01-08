"""
Shared Types
Common enums and types used across services
"""

from enum import Enum


class IntentCategory(Enum):
    EXECUTION = "execution"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    STRATEGY = "strategy"
    PLANNING = "planning"  # For planning and design activities
    REVIEW = "review"  # For review and validation activities
    LEARNING = "learning"
    QUERY = "query"  # CQRS-lite: For read-only data retrieval operations
    CONVERSATION = "conversation"  # For greetings, chitchat, social interaction
    IDENTITY = "identity"  # For identity queries - "What's your name and role?"
    TEMPORAL = "temporal"  # For temporal queries - "What day is it?"
    STATUS = "status"  # For status queries - "What am I working on?"
    PRIORITY = "priority"  # For priority queries - "What's my top priority?"
    GUIDANCE = "guidance"  # For guidance queries - "What should I focus on?"
    UNKNOWN = "unknown"  # For unclear or ambiguous requests


class WorkflowType(Enum):
    CREATE_FEATURE = "create_feature"
    ANALYZE_METRICS = "analyze_metrics"
    CREATE_TICKET = "create_ticket"
    CREATE_TASK = "create_task"
    REVIEW_ITEM = "review_item"
    GENERATE_REPORT = "generate_report"
    PLAN_STRATEGY = "plan_strategy"
    LEARN_PATTERN = "learn_pattern"
    ANALYZE_FEEDBACK = "analyze_feedback"
    # PM-009: Project management workflow types
    CONFIRM_PROJECT = "confirm_project"
    SELECT_PROJECT = "select_project"
    ANALYZE_FILE = "analyze_file"  # Add this line for file analysis workflows
    # PM-021: Project listing workflow type
    LIST_PROJECTS = "list_projects"
    # Multi-Agent coordination workflow type
    MULTI_AGENT = "multi_agent"


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(Enum):
    # Analysis tasks
    ANALYZE_REQUEST = "analyze_request"
    EXTRACT_REQUIREMENTS = "extract_requirements"
    IDENTIFY_DEPENDENCIES = "identify_dependencies"

    # Execution tasks
    CREATE_WORK_ITEM = "create_work_item"
    UPDATE_WORK_ITEM = "update_work_item"
    NOTIFY_STAKEHOLDERS = "notify_stakeholders"

    # Synthesis tasks
    GENERATE_DOCUMENT = "generate_document"
    CREATE_SUMMARY = "create_summary"

    # Integration tasks
    GITHUB_CREATE_ISSUE = "github_create_issue"
    GENERATE_GITHUB_ISSUE_CONTENT = "generate_github_issue_content"
    ANALYZE_GITHUB_ISSUE = "analyze_github_issue"
    ANALYZE_FILE = "analyze_file"
    SUMMARIZE = "summarize"

    # PM-021: Project listing task type
    LIST_PROJECTS = "list_projects"
    EXTRACT_WORK_ITEM = "extract_work_item"
    JIRA_CREATE_TICKET = "jira_create_ticket"
    SLACK_SEND_MESSAGE = "slack_send_message"

    # Feedback tasks
    PROCESS_USER_FEEDBACK = "process_user_feedback"

    # Document processing tasks (Issue #290)
    ANALYZE_DOCUMENT = "analyze_document"
    QUESTION_ANSWER_DOCUMENT = "qa_document"
    COMPARE_DOCUMENTS = "compare_documents"
    SUMMARIZE_DOCUMENT = "summarize_document"
    SEARCH_DOCUMENTS = "search_documents"


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


# PM-009: Integration type enum for project integrations
class IntegrationType(Enum):
    GITHUB = "github"
    JIRA = "jira"
    LINEAR = "linear"
    SLACK = "slack"


# PM-081: Todo management system enums
class TodoStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class TodoPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class ListType(Enum):
    PERSONAL = "personal"
    PROJECT = "project"
    TEAM = "team"
    TEMPLATE = "template"
    ARCHIVE = "archive"


class OrderingStrategy(Enum):
    MANUAL = "manual"  # User-defined order
    PRIORITY = "priority"  # Sort by priority
    DUE_DATE = "due_date"  # Sort by due date
    CREATED_DATE = "created_date"  # Sort by creation date
    ALPHABETICAL = "alphabetical"  # Sort alphabetically
    STATUS = "status"  # Group by status


# PM-040: Knowledge graph node types
class NodeType(Enum):
    CONCEPT = "concept"
    DOCUMENT = "document"
    PERSON = "person"
    ORGANIZATION = "organization"
    TECHNOLOGY = "technology"
    PROCESS = "process"
    METRIC = "metric"
    EVENT = "event"
    RELATIONSHIP = "relationship"
    CUSTOM = "custom"


# PM-040: Knowledge graph edge types (Issue #278: CORE-KNOW-ENHANCE)
class EdgeType(Enum):
    """Basic relationship types"""

    REFERENCES = "references"
    DEPENDS_ON = "depends_on"
    IMPLEMENTS = "implements"
    MEASURES = "measures"
    INVOLVES = "involves"
    TRIGGERS = "triggers"
    ENHANCES = "enhances"
    REPLACES = "replaces"
    SUPPORTS = "supports"

    """Causal relationship types (Issue #278)"""
    BECAUSE = "because"  # X happens BECAUSE of Y
    ENABLES = "enables"  # X ENABLES Y capability
    REQUIRES = "requires"  # X REQUIRES Y to function
    PREVENTS = "prevents"  # X PREVENTS Y from happening
    LEADS_TO = "leads_to"  # X LEADS_TO Y outcome

    """Temporal relationship types (Issue #278)"""
    BEFORE = "before"  # X occurs BEFORE Y
    DURING = "during"  # X occurs DURING Y
    AFTER = "after"  # X occurs AFTER Y

    """Other relationship types"""
    CUSTOM = "custom"


class PatternType(Enum):
    """
    Types of patterns that can be learned by the auto-learning system.

    Issue #300: CORE-ALPHA-LEARNING-BASIC - Basic Auto-Learning
    """

    USER_WORKFLOW = "user_workflow"  # Recurring user action sequences
    COMMAND_SEQUENCE = "command_sequence"  # Frequently used command patterns
    TIME_BASED = "time_based"  # Temporal patterns (e.g., daily standup)
    CONTEXT_BASED = "context_based"  # Context-triggered patterns
    PREFERENCE = "preference"  # User preference patterns
    INTEGRATION = "integration"  # Integration usage patterns


class StandupConversationState(Enum):
    """
    State machine for interactive standup conversations.

    Issue #552: STANDUP-CONV-STATE - Conversation State Management
    Epic #242: CONV-MCP-STANDUP-INTERACTIVE
    """

    INITIATED = "initiated"  # User requested standup
    GATHERING_PREFERENCES = "gathering_preferences"  # Asking refinement questions
    GENERATING = "generating"  # Generating standup content
    REFINING = "refining"  # User providing feedback/edits
    FINALIZING = "finalizing"  # Confirming final version
    COMPLETE = "complete"  # Standup delivered
    ABANDONED = "abandoned"  # User cancelled or timed out
