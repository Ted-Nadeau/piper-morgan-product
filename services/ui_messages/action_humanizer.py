import re
from typing import Optional


class ActionHumanizer:
    """Service to convert technical action strings to natural language (rule-based only)"""

    def __init__(self):
        # Conversational verb mappings for more natural language
        self.conversational_verbs = {
            "fetch": "grab",
            "retrieve": "get",
            "obtain": "get",
            "acquire": "get",
            "list": "show you",
            "count": "count up",
            "analyze": "take a look at",
            "investigate": "look into",
            "review": "check out",
            "examine": "have a look at",
            "create": "create",
            "generate": "put together",
            "build": "build",
            "update": "update",
            "modify": "change",
            "delete": "remove",
            "remove": "get rid of",
            "send": "send",
            "notify": "let you know about",
            "schedule": "set up",
            "plan": "plan out",
            "organize": "organize",
            "summarize": "sum up",
            "extract": "pull out",
            "process": "work on",
            "handle": "take care of",
            "manage": "handle",
        }

        # Noun context mappings for more natural articles/phrasing
        self.noun_contexts = {
            "issues": "those issues",
            "github_issues": "those GitHub issues",
            "tickets": "those tickets",
            "tasks": "those tasks",
            "files": "those files",
            "documents": "those documents",
            "reports": "those reports",
            "data": "that data",
            "metrics": "those metrics",
            "insights": "those insights",
            "performance": "the performance",
            "backlog": "the backlog",
            "team": "the team",
            "code": "the code",
            "crash": "that crash",
            "bug": "that bug",
            "error": "that error",
            "project": "the project",
            "projects": "the projects",
            "sprint": "the sprint",
            "meeting": "the meeting",
            "user_story": "that user story",
            "pull_request": "that pull request",
            "repository": "the repository",
            "branch": "the branch",
            "commit": "the commit",
        }

        # Special compound noun mappings (full action -> noun phrase)
        self.compound_nouns = {
            "github_issues": "GitHub issues",
            "user_data": "user data",
            "pull_request": "pull request",
            "user_story": "user story",
        }

        # Special handling for specific action patterns
        self.special_patterns = {
            "fetch_github_issues": "grab those GitHub issues",
            "fetch_user_data": "grab that user data",
            "list_github_issues": "show you those GitHub issues",
        }

    async def humanize(self, action: str, category: Optional[str] = None) -> str:
        """Convert technical action to human-readable format with conversational patterns"""
        # Check for special patterns first
        if action in self.special_patterns:
            return self.special_patterns[action]

        # Handle actions without underscores
        if "_" not in action:
            return self.conversational_verbs.get(action, action)

        parts = action.split("_")

        # Handle verb_noun patterns (most common)
        if len(parts) == 2:
            verb, noun = parts

            # Use conversational verb if available
            human_verb = self.conversational_verbs.get(verb, verb)

            # Check for compound nouns first
            compound_key = f"{verb}_{noun}"
            if compound_key in self.compound_nouns or noun in self.compound_nouns:
                if compound_key in self.compound_nouns:
                    human_noun = self.compound_nouns[compound_key]
                else:
                    human_noun = self.compound_nouns[noun]
                return f"{human_verb} {human_noun}"

            # Use contextual noun phrasing if available
            elif noun in self.noun_contexts:
                human_noun = self.noun_contexts[noun]
                return f"{human_verb} {human_noun}"
            else:
                # Fall back to article + noun, but only if verb was actually converted
                clean_noun = noun.replace("_", " ")
                if verb in self.conversational_verbs:
                    # Verb was converted, use article
                    article = "an" if clean_noun[0] in "aeiou" else "a"
                    human_noun = f"{article} {clean_noun}"
                else:
                    # Verb wasn't converted, just use noun without article for better flow
                    human_noun = clean_noun
                return f"{human_verb} {human_noun}"

        # Handle verb_adjective_noun patterns (e.g., "create_new_issue")
        elif len(parts) == 3:
            verb, adjective, noun = parts
            human_verb = self.conversational_verbs.get(verb, verb)

            if noun in self.noun_contexts:
                # For contextual nouns, incorporate adjective naturally
                base_noun = self.noun_contexts[noun]
                if adjective in ["new", "fresh"]:
                    human_noun = f"a new {noun.replace('_', ' ')}"
                else:
                    human_noun = f"{adjective} {base_noun}"
            else:
                article = "an" if adjective[0] in "aeiou" else "a"
                human_noun = f"{article} {adjective} {noun.replace('_', ' ')}"

            return f"{human_verb} {human_noun}"

        # Handle longer patterns by grouping intelligently
        elif len(parts) > 3:
            verb = parts[0]
            noun_phrase = " ".join(parts[1:]).replace("_", " ")
            human_verb = self.conversational_verbs.get(verb, verb)
            return f"{human_verb} {noun_phrase}"

        # Default: just replace underscores and apply conversational mapping
        clean_action = action.replace("_", " ")
        first_word = clean_action.split()[0]
        if first_word in self.conversational_verbs:
            remaining = " ".join(clean_action.split()[1:])
            return f"{self.conversational_verbs[first_word]} {remaining}".strip()

        return clean_action
