# Intent Category Usage Guide

**For**: Developers adding new patterns or queries
**Epic**: GREAT-4A - Intent Foundation & Categories
**Date**: October 5, 2025
**Author**: Cursor Agent

---

## Overview

This guide helps developers understand when and how to use the TEMPORAL, STATUS, and PRIORITY intent categories. Each category serves specific user needs and follows established patterns for consistency and performance.

---

## TEMPORAL Category

### Purpose
Handle time, date, schedule, and temporal reference queries.

### When to Use
- User asks about current date/time ("What day is it?")
- User asks about past events ("What did we do yesterday?")
- User asks about future schedule ("What's on today's agenda?")
- Temporal comparisons ("How long ago?", "When did we last?")
- Calendar-related queries ("What's my next meeting?")

### Pattern Structure
Regex patterns matching temporal keywords with word boundaries:
```regex
\bwhat day is it\b          # Direct date queries
\bwhat time is it\b         # Direct time queries
\btoday'?s date\b          # Possessive date references
\bcurrent date\b            # Explicit current references
```

### Handler Behavior
- **Action**: `get_current_time`
- **Returns**: Current date/time with calendar integration
- **Features**:
  - Real calendar data from CalendarIntegrationRouter
  - Current meeting awareness
  - Next meeting information
  - Focus time availability
  - Meeting load context

### Example Queries
✅ **Good Examples**:
- "What day is it?"
- "What's today's date?"
- "What time is it?"
- "Current date and time"

❌ **Wrong Category**:
- "What's my schedule?" (too broad - could be STATUS)
- "Schedule a meeting" (EXECUTION category)
- "How long will this take?" (ANALYSIS category)

### Adding New TEMPORAL Patterns
1. **Identify temporal keywords**: day, date, time, today, yesterday, etc.
2. **Add to TEMPORAL_PATTERNS** in `pre_classifier.py`
3. **Use word boundaries**: `\b` to prevent partial matches
4. **Test with canonical queries**: Verify >0.8 confidence
5. **Update documentation**: Add to pattern catalog

---

## STATUS Category

### Purpose
Handle project/work status and current activity queries.

### When to Use
- User asks about current work ("What am I working on?")
- User asks about project status ("What's the status of X?")
- User asks about portfolio overview ("My projects")
- User asks about work allocation ("What's on my plate?")
- Progress inquiries ("Where are we in the project?")

### Pattern Structure
Regex patterns matching work/project status keywords:
```regex
\bwhat am i working on\b        # Direct work queries
\bmy projects\b                 # Portfolio references
\bcurrent work\b                # Work status
\bproject status\b              # Status inquiries
```

### Handler Behavior
- **Action**: `get_project_status`
- **Returns**: Project portfolio from PIPER.md configuration
- **Features**:
  - Primary project allocation (e.g., "VA/Decision Reviews 70%")
  - Secondary projects with percentages
  - Current phase and status
  - Team context and collaboration details

### Example Queries
✅ **Good Examples**:
- "What am I working on?"
- "What's my current project?"
- "My projects"
- "Current work"
- "What's my status?"

❌ **Wrong Category**:
- "Create a new project" (EXECUTION category)
- "How is the project performing?" (ANALYSIS category)
- "What should I work on?" (PRIORITY or GUIDANCE category)

### Adding New STATUS Patterns
1. **Focus on current state**: work, project, status, portfolio
2. **Add to STATUS_PATTERNS** in `pre_classifier.py`
3. **Avoid future tense**: "will work" vs "working on"
4. **Test with project context**: Verify handler response
5. **Consider PIPER.md integration**: Ensure patterns work with config

---

## PRIORITY Category

### Purpose
Handle priority, focus, and importance queries.

### When to Use
- User asks about top priorities ("What's my top priority?")
- User asks about focus areas ("What should I focus on?")
- User asks about importance ranking ("Most important task")
- User asks about next actions ("What should I do first?")
- User asks about priority ordering ("My priorities")

### Pattern Structure
Regex patterns matching priority/importance keywords:
```regex
\bwhat'?s my top priority\b     # Direct priority queries
\bhighest priority\b            # Importance ranking
\bmost important task\b         # Task importance
\bwhat should i do first\b      # Action priority
```

### Handler Behavior
- **Action**: `get_top_priority`
- **Returns**: Top priority from PIPER.md with context
- **Features**:
  - Primary focus identification
  - Goal and success metrics
  - Timeline information
  - Strategic alignment context

### Example Queries
✅ **Good Examples**:
- "What's my top priority?"
- "Highest priority"
- "Most important task"
- "What should I do first?"
- "My priorities"

❌ **Wrong Category**:
- "Set my priority to X" (EXECUTION category)
- "Why is this a priority?" (ANALYSIS category)
- "What are the team's priorities?" (STATUS category - different scope)

### Adding New PRIORITY Patterns
1. **Focus on ranking/importance**: priority, important, first, top
2. **Add to PRIORITY_PATTERNS** in `pre_classifier.py`
3. **Distinguish from guidance**: Priority = what's important, Guidance = what to do
4. **Test with PIPER.md context**: Verify priority extraction works
5. **Consider scope**: Personal vs team vs project priorities

---

## Cross-Category Guidelines

### Pattern Overlap Prevention
- **TEMPORAL vs STATUS**: "What's my schedule?" could be either
  - Solution: Use specific temporal keywords (day, date, time)
- **STATUS vs PRIORITY**: "What should I work on?" overlaps
  - Solution: STATUS = current state, PRIORITY = importance ranking
- **PRIORITY vs GUIDANCE**: Both about what to do next
  - Solution: PRIORITY = importance, GUIDANCE = contextual advice

### Confidence Optimization
- **Use specific patterns**: Avoid overly broad regex
- **Test edge cases**: Verify no false positives
- **Maintain >0.8 confidence**: All patterns should be highly confident
- **Word boundaries essential**: Prevent partial matches

### Performance Considerations
- **Keep patterns simple**: Complex regex can slow matching
- **Order patterns by frequency**: Most common patterns first
- **Avoid backtracking**: Use efficient regex constructs
- **Test performance**: Run benchmark script after changes

---

## Best Practices

### 1. Pattern Design
- **Be specific but flexible**: Cover variations without being too broad
- **Use word boundaries**: `\b` prevents "priority" matching "prioritize"
- **Handle contractions**: `'?` for "what's" vs "whats"
- **Case insensitive**: All matching is lowercase

### 2. Testing Strategy
- **Test canonical queries**: Ensure core use cases work
- **Test variations**: Different phrasings of same intent
- **Test edge cases**: Typos, informal language, abbreviations
- **Test performance**: Verify <100ms response time

### 3. Documentation
- **Document pattern rationale**: Why this pattern is needed
- **Provide examples**: Show successful and failed matches
- **Update guides**: Keep this guide current with changes
- **Cross-reference handlers**: Link patterns to handler behavior

### 4. Maintenance
- **Monitor real usage**: Track which patterns users actually use
- **Analyze failures**: When do patterns not match expected queries?
- **Optimize based on data**: Remove unused patterns, add common variations
- **Version control**: Track pattern changes for rollback if needed

---

## Troubleshooting

### Low Confidence Issues
**Problem**: Pattern matches but confidence <0.8
- **Cause**: Pattern too broad or conflicts with other patterns
- **Solution**: Make pattern more specific, add negative lookahead
- **Example**: `\bpriority\b` → `\bmy priority\b` (more specific)

### Wrong Category Classification
**Problem**: Query classified to wrong category
- **Cause**: Pattern overlaps between categories
- **Solution**: Refine patterns to be more category-specific
- **Example**: "What should I work on?" → Add to PRIORITY, not STATUS

### Pattern Not Matching
**Problem**: Expected query doesn't match any pattern
- **Cause**: Missing word boundaries, case sensitivity, or punctuation
- **Solution**: Check exact query format, add debug logging
- **Debug**: Use `PreClassifier.pre_classify()` directly to test

### Performance Issues
**Problem**: Pattern matching taking too long
- **Cause**: Complex regex with backtracking
- **Solution**: Simplify regex, avoid nested quantifiers
- **Benchmark**: Run performance test after changes

---

## Development Workflow

### Adding New Patterns
1. **Identify need**: User query not matching existing patterns
2. **Choose category**: TEMPORAL, STATUS, or PRIORITY
3. **Design pattern**: Specific regex with word boundaries
4. **Add to code**: Insert in appropriate `*_PATTERNS` list
5. **Test locally**: Verify pattern works with test queries
6. **Run benchmarks**: Ensure performance targets met
7. **Update docs**: Add to pattern catalog and this guide
8. **Submit PR**: Include test results and documentation

### Modifying Existing Patterns
1. **Document current behavior**: What queries currently match?
2. **Identify issue**: Why does pattern need to change?
3. **Design fix**: Minimal change to address issue
4. **Test regression**: Ensure existing queries still work
5. **Test improvement**: Verify fix addresses original issue
6. **Update docs**: Reflect changes in documentation

---

## Integration Points

### Handler Integration
- **TEMPORAL**: Integrates with CalendarIntegrationRouter
- **STATUS**: Reads from PIPER.md configuration
- **PRIORITY**: Extracts priorities from PIPER.md

### Configuration Dependencies
- **PIPER.md**: STATUS and PRIORITY handlers depend on config
- **Calendar**: TEMPORAL handler uses calendar integration
- **Timezone**: TEMPORAL uses configured timezone

### Error Handling
- **Pattern match failure**: Falls through to LLM classifier
- **Handler failure**: Graceful degradation to conversation
- **Config unavailable**: Fallback responses provided

---

**Status**: ✅ Complete usage guide for developers working with intent categories
