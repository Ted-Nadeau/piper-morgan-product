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
    LEARNING = "learning"
    QUERY = "query"  # CQRS-lite: For read-only data retrieval operations
    CONVERSATION = "conversation"  # For greetings, chitchat, social interaction
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


# PM-040: Knowledge graph edge types
class EdgeType(Enum):
    REFERENCES = "references"
    DEPENDS_ON = "depends_on"
    IMPLEMENTS = "implements"
    MEASURES = "measures"
    INVOLVES = "involves"
    TRIGGERS = "triggers"
    ENHANCES = "enhances"
    REPLACES = "replaces"
    SUPPORTS = "supports"
    CUSTOM = "custom"
