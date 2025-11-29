# Create Advisor Mailbox Implementation for Ted Nadeau

## Context
Ted Nadeau wants to participate in architectural discussions without requiring real-time presence. We need an async communication channel where advisors can receive questions, provide input, and have that input integrated into future sessions.

Bootstrap opportunity: Ted can build this feature himself, using it to coordinate on building it - a recursive learning loop that gets him deeply embedded in the codebase while solving his own problem.

## Scope
**In Scope:**
- Create file structure under `/advisors/ted-nadeau/`
- Implement manifest.json for tracking message status
- Create workflow documentation
- Write example messages (inbox/outbox)
- Simple Python script for status management

**Out of Scope:**
- Database storage (keep file-based for now)
- Automated notifications
- Web UI (pure file-based initially)
- Multi-advisor support (Ted only for pilot)

## Acceptance Criteria
- [ ] Directory structure created and documented
- [ ] Manifest schema defined with read/unread status
- [ ] At least one example message in inbox (architectural question)
- [ ] Clear workflow documentation for Ted
- [ ] Python utility for marking messages read/answered
- [ ] Integration point identified for agent sessions

## Deliverables
1. `/advisors/ted-nadeau/` directory structure
2. `/advisors/ted-nadeau/README.md` with workflow
3. `/advisors/ted-nadeau/manifest.json` with schema
4. `/advisors/ted-nadeau/inbox/001-example-question.md`
5. `/advisors/ted-nadeau/utils/mailbox.py` (simple utilities)

## Resources
- Memo to Ted: `/mnt/user-data/uploads/memo-ted-nadeau-2025-11-29.md`
- Agent coordination patterns (for design inspiration)
- Git workflow documentation (for async patterns)

## Special Instructions
This should be simple enough that Ted can understand and extend it immediately. Think "minimum viable mailbox" that proves the concept. The elegance is in the simplicity, not the features.

Include a "bootstrapping message" as the first item in Ted's inbox, asking him for feedback on the mailbox design itself.

## Verification
- Ted can understand the workflow from documentation alone
- The first message in inbox demonstrates the pattern
- Manifest provides clear status tracking
- Integration points with agent workflow are documented
- Code is simple enough for Ted to extend

## Notes
Remember: Ted is both the builder and the first user. This creates a virtuous cycle where he improves the tool based on his own experience using it.
