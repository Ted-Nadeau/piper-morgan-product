The Action Humanizer: Teaching AI to Speak Human
christian crumlish
christian crumlish
5 min read
·
Aug 4, 2025
8






Press enter or click to view image in full size
A speech pathologist teaches a robot how to say “gonna”
“Now you try”
July 13, later that day

There’s something deeply unsatisfying about building an AI assistant that talks to users like a developer. When your system responds with “I understand you want to investigate_crash,” it sounds like a robot that’s trying to be helpful but doesn’t quite understand how humans communicate. (Which, well, it kind of is?)

Yesterday we fixed this with the Action Humanizer — a smart caching system that converts technical action strings into natural language. Now the system says “I understand you want to investigate a crash,” which feels like talking to a colleague instead of debugging a program.

Small change, big difference.

The problem that bothered me for weeks
This issue had been nagging at me since we implemented the intent classification system. The AI was correctly understanding user requests and classifying them into structured actions like investigate_crash, create_github_issue, or analyze_performance. Technically perfect, humanly awful.

Every user message would get responses like:

“I’ve started a workflow to handle your investigate_crash request”
“I understand you want to create_github_issue”
“Let me help you with analyze_performance”
Functionally correct, emotionally jarring. Like having a conversation with someone who learned English from technical specifications or getting one of those personalized emails addressed to Dear $FIRSTNAME.

The architecture insight
The solution couldn’t be simple find-and-replace. Different actions need different treatments:

investigate_crash → "investigate a crash"
create_github_issue → "create a GitHub issue"
analyze_performance → "analyze performance"
list_projects → "list projects" (plural, no article)
The patterns are consistent enough for rules but nuanced enough to need intelligence. Perfect candidate for a hybrid approach: rule-based conversion for common patterns, LLM fallback for complex cases, smart caching to avoid repeated processing.

Building the smart caching system
We designed the Action Humanizer as a proper service with three layers:

Layer 1: Database caching
Every technical action gets cached with its human-readable equivalent. Once we’ve figured out that investigate_crash becomes "investigate a crash," we never need to compute it again.

The database schema captures not just the mapping, but metadata:

Usage count (how often this action appears)
Last used timestamp (for cache maintenance)
Category context (analysis vs execution actions might be treated differently)
Layer 2: Rule-based conversion
For common patterns, we built explicit rules:

# verb_noun patterns get articles
if verb in ['create', 'investigate', 'analyze', 'review']:
    return f"{verb} a {noun}"

# list/count patterns get pluralization
elif verb in ['list', 'count']:
    return f"{verb} {noun}s"
This handles 80% of cases instantly and consistently.

Layer 3: LLM fallback
For complex actions that don’t match rules, we fall back to the LLM with a carefully crafted prompt:

Convert this technical action identifier to natural conversational English.

Technical action: update_user_story_acceptance_criteria

Examples:

- investigate_crash → investigate a crash

- create_github_issue → create a GitHub issue

Natural language version:

The LLM is surprisingly good at this task. It understands context (github → GitHub), articles (when to use “a” vs no article), and maintains the action verb structure.

The implementation sprint
This was a perfect test of our multi-AI development approach. We broke the work into clear phases and executed with Test-Driven Development:

Phase 1: Database and domain models (Cursor Assistant)

Alembic migration for the cache table
Domain model for ActionHumanization
SQLAlchemy mapping and repository pattern
Phase 2: Service implementation (Cursor Assistant)

ActionHumanizer service with the three-layer architecture
Rule-based conversion logic
Integration points with the LLM client
Phase 3: Template integration (Collaborative)

TemplateRenderer to handle placeholder replacement
Integration with existing message templates
Testing across different workflow types
Phase 4: Testing and validation (All hands)

Unit tests for rule-based conversion
Integration tests for the full pipeline
Manual testing through the UI
The TDD approach kept us focused. Write a test for “investigate_crash” → “investigate a crash”, implement just enough to pass, refactor if needed. Repeat for the next pattern.

The satisfying results
The system now handles natural language conversion seamlessly:

Technical actions → Human language

investigate_crash → "investigate a crash"
create_github_issue → "create a GitHub issue"
analyze_performance → "analyze performance"
review_pull_request → "review a pull request"
update_user_story → "update a user story"
list_projects → "list projects"
The UI responses now feel natural:

“I understand you want to investigate a crash. I’ve started a workflow to handle this.”
“I’ll help you create a GitHub issue with the details you’ve provided.”
“Let me analyze performance patterns for you.”
Small change, but it fundamentally improves the user experience. The system feels less like a developer tool and more like a collaborative assistant.

The performance characteristics
The caching system delivers the performance we need:

Cache hits: Instant response for known actions
Rule-based misses: Sub-millisecond conversion for common patterns
LLM fallbacks: ~200ms for complex actions (only happens once per action)
In practice, 95% of requests hit the cache or rules. The LLM fallback is rarely needed after the initial seeding period.

The meta-lesson about AI UX
Building the Action Humanizer reinforced something important about AI user experience: technical accuracy isn’t enough. The system needs to communicate in the user’s language, not the developer’s language.

This applies beyond just action humanization:

Error messages should be helpful, not technical
Status updates should be conversational, not robotic
Suggestions should feel collaborative, not algorithmic
The goal isn’t to hide the AI — it’s to make the AI feel like a thoughtful colleague rather than a sophisticated script.

The unexpected discovery
The implementation revealed something interesting about our action vocabulary. We have 47 distinct technical actions across the system, but they follow only 6–7 linguistic patterns. The rule-based conversion handles the vast majority of cases.

This suggests our action naming is more consistent than I thought. When you design actions with clear verb-noun patterns, the natural language conversion becomes straightforward.

The collaborative development pattern
The Action Humanizer implementation demonstrated something valuable about working with AI assistants on feature development:

Design phase: Human architects the solution approach and breaks down the work

Implementation phase: AI assistants execute specific components with TDD discipline

Integration phase: Collaborative testing and refinement

Validation phase: Human confirms the user experience meets the original goal

This pattern scales well for feature work where you know what you want to build but need help executing it systematically.

Looking forward
The Action Humanizer is complete and working, but it opens up possibilities for broader UX improvements:

Context-aware messaging: Different message templates based on user context or workflow history

Conversational continuity: Maintaining natural language patterns across multi-turn interactions

Personalization: Learning individual user language preferences over time

The foundation is in place to make Piper Morgan feel less like a tool and more like a teammate.

Next in Building Piper Morgan: From Broken Tests to Perfect Architecture: The Great Cleanup

You know the old joke about why Captain Picard has to specify his beverage preference the same way every time (“Tea, Earl Grey, hot”) without ever being able to save it as a favorite? Because it’s Enterprise software. (Pretty sure I got that one from an old-school blogger back in the day.)
