import re
from typing import Optional


class ActionHumanizer:
    """Service to convert technical action strings to natural language (rule-based only)"""

    def __init__(self):
        pass

    async def humanize(self, action: str, category: Optional[str] = None) -> str:
        """Convert technical action to human-readable format (rule-based only)"""
        # Handle common verb patterns
        if "_" not in action:
            return action
        parts = action.split("_")
        # Common patterns: verb_noun → verb a noun
        if len(parts) == 2:
            verb, noun = parts
            if verb in [
                "create",
                "investigate",
                "analyze",
                "review",
                "update",
                "delete",
                "close",
                "triage",
                "plan",
                "prioritize",
                "estimate",
                "notify",
                "schedule",
                "send",
                "extract",
                "assign",
                "summarize",
                "generate",
                "add",
                "list",
                "count",
            ]:
                article = "an" if noun[0] in "aeiou" else "a"
                if verb in [
                    "list",
                    "count",
                    "review",
                    "analyze",
                    "extract",
                    "prioritize",
                    "plan",
                    "estimate",
                    "notify",
                    "schedule",
                    "send",
                ]:
                    return f"{verb} {noun.replace('backlog', 'the backlog').replace('team', 'the team').replace('metrics', 'metrics').replace('data', 'data').replace('insights', 'insights').replace('requirements', 'requirements').replace('performance', 'performance').replace('meeting', 'a meeting').replace('update', 'an update').replace('feature', 'a feature').replace('task', 'a task').replace('issue', 'an issue').replace('bug', 'a bug').replace('crash', 'a crash').replace('sprint', 'a sprint').replace('report', 'a report').replace('document', 'a document').replace('file', 'a file').replace('code', 'code').replace('user_story', 'a user story').replace('pull_request', 'a pull request')}"
                else:
                    return f"{verb} {article} {noun.replace('_', ' ')}"
        # Default: just replace underscores
        return action.replace("_", " ")
