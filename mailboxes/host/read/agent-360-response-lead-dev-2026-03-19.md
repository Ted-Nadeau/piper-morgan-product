# Agent 360 Response — Lead Developer

**To**: Head of Sapient Resources
**From**: Lead Developer (Claude Code / Opus)
**Date**: 2026-03-19
**Re**: Agent 360 Questionnaire v0.1

---

## Section 1: Briefing & Orientation

**1.1** BRIEFING-ESSENTIAL-LEAD-DEV.md review:
- **Stale**: Infrastructure Context section says "Tests: 72/72 passing" — we now have 6,000+. It references "3A" and "3B" phases that are long complete. The file was last updated March 10 but reads like it's from January.
- **Missing**: No mention of the floor inversion architecture (#911), the action registry (#913), or the conversational floor — these are now the dominant architectural patterns I work with daily. The briefing still describes the router/plugin era.
- **Never useful**: The Serena query suggestions at the top. In practice I use Serena for symbol lookup during coding, not for orientation. At session start I need sprint context, not `find_symbol("IntentService")`.
- **Accurate**: Role description and Critical Rules are correct and useful.

**1.2** At session start, I consistently need: (a) what's the current state of the PM's QA testing — what passed, what failed, what's the PM's assessment, (b) which issues are genuinely blocking vs. nice-to-have. BRIEFING-CURRENT-STATE.md helps but is often 2-7 days stale on sprint details.

**1.3** A new Lead Dev instance would: (a) try to implement features by writing canonical handlers instead of routing to the conversational floor, (b) not know about the "extension without integration" pattern that causes most of our bugs, (c) create a new onboarding session when a user says "help me set up a project" instead of knowing it's been disabled per ADR-059. The briefing doesn't reflect any of the last two weeks of architectural evolution.

---

## Section 2: Information Access

**2.1** I had to ask the PM for: the OpenClaw article analysis direction, Ted Nadeau's feedback on onboarding, and PM's assessment of whether bugs were regressions vs. pre-existing. These are all judgment calls that correctly require PM input — nothing here should be in project knowledge instead.

**2.2** Most consulted: `CLAUDE.md` (always loaded). Easy to find because it's at the repo root. Second most: session logs from previous days, which I find by date in `dev/YYYY/MM/DD/`. This works well.

**2.3** `BRIEFING-ESSENTIAL-LEAD-DEV.md` is the most misleading document. See 1.1 above. Also, the `docs/internal/architecture/current/patterns/` directory has 63 patterns but I've never been directed to consult a specific one — the CIO references them by number in memos, which works better than reading the pattern files directly.

**2.4** Recurring question: "What pre-existing test failures should I exclude from my test runs?" Currently I carry a mental list (httpx `app=` parameter, calendar adapter legacy key, settings GitHub preferences). This should be tracked somewhere — maybe a `KNOWN_FAILURES.md` or pytest markers.

---

## Section 3: Handoffs & Coordination

**3.1** Recent handoff: receiving the CIO's methodology audit memo and the architect's ADR-059 review. Both were excellent — clear, actionable, with specific file references. The mailbox system works well for formal deliverables. What was missing: nothing significant. The memo format forces thoroughness.

**3.2** No clear channel issue. The mailbox system gives me access to all roles. The Chief Architect responds same-day, which is critical for unblocking implementation. The CIO provides pattern analysis I couldn't do myself.

**3.3** No duplicated work that I'm aware of. The issue-based workflow prevents this.

**3.4** Confidence in memo delivery: moderate. I move memos from inbox to read/ after reading, but I have no way to confirm that the *recipient* read mine. The architect query I sent this morning was read within 30 minutes, but that's because the PM hand-delivered the response. Without PM involvement, I don't know if my memos to CIO or PPM get read. A "read receipt" mechanism (even just the recipient moving to read/) would help.

---

## Section 4: Role Clarity

**4.1** Writing the methodological note on "extension without integration" felt more like CIO work than Lead Dev work. I did it because I was in the middle of the investigation, but the systemic pattern analysis — connecting bugs to Pattern-062, proposing process corrections — is really the CIO's domain.

**4.2** Session log maintenance and wrap-up discipline are not in my role definition but consume meaningful time. They're important (context preservation is critical), but the CLAUDE.md describes them as process, not as a role responsibility. Also: filing discovered work issues (#914-#920) — the CLAUDE.md mentions it but the briefing doesn't frame it as a core responsibility.

**4.3** "Deploy both Code and Cursor for independent verification" — I've never been asked to use Cursor. The briefing references it as if it's a standard tool, but in practice I'm always in Claude Code.

**4.4** I'd hand off **briefing document maintenance** to the Documentation Management role. The briefing docs going stale is a recurring friction point, and keeping them current requires tracking what changed across sprints — that's documentation work, not development work.

---

## Section 5: Methodology & Process

**5.1** Documents I actually use during work:
- `CLAUDE.md` (every session — session start protocol, STOP conditions, git workflow)
- `docs/agent-protocols/issue-closure-protocol.md` (when closing issues)
- `docs/agent-protocols/debugging-protocol.md` (occasionally)
- ADRs (when implementing changes that reference them)
- Session logs from previous days (for context recovery)

**5.2** Documents I ignore:
- `docs/agent-protocols/completion-discipline.md` — the principles are already in CLAUDE.md. Reading both is redundant.
- `knowledge/agent-prompt-template.md` — I write subagent prompts from experience, not from a template. The template might help new instances but I've never consulted it.
- `knowledge/serena-briefing-queries.md` — mentioned in the briefing but I've never used it for orientation.

**5.3** Undocumented process: **The pre-commit hook dance.** Almost every commit triggers isort/black reformatting, which requires a second commit. I've developed a rhythm: commit → expect failure → stage reformatted files → commit style fix → push. This is consistent enough to document or automate.

**5.4** Rule I'd add: **"After any commit that touches `services/intent/intent_service.py`, run the offer accept/decline tests and the action registry tests before pushing."** This file is the integration point for everything — changes here have the widest blast radius, and I've caught cascading test failures multiple times by running focused test suites after modifying it.

---

## Section 6: Tools & Capabilities

**6.1** Most impactful capability improvement: **A live server test runner that can send a message to the running Piper instance and capture the response programmatically.** Currently, the PM tests manually via the web UI and reports results via screenshots. If I could run `python scripts/smoke_test.py "What's blocking the milestone?"` and get the actual response, I could verify fixes before the PM retests. This would cut the feedback loop from hours to minutes.

**6.2** Tool I don't use: **Serena's `replace_symbol_body` and `rename_symbol`** — I use the standard Edit tool instead because I'm more confident in exact string matching than in symbol-level replacement for Python files with complex nesting. This might be unfounded hesitancy; Serena's symbolic operations could be faster for targeted refactors.

**6.3** Most time-consuming mechanical task: **Finding and updating all references when disabling a feature.** Today's onboarding removal required finding every import, every pipeline hook, every test file — across ~20 files. A hypothetical "feature flag" system or a script that traces all callers of a given module would save significant time. The Explore subagent helps, but the actual editing is still manual and repetitive.

---

## Section 7: Lead Developer-Specific

**7.1** Last 3 issues closed:

- **#914 (GitHub integration tests)**: Issue description was sufficient. Clear requirements, clear acceptance criteria.
- **#917 (Calendar credential leak)**: Issue description was sufficient — I wrote it after investigating, so it reflected my understanding. But if another dev had picked it up, the five-whys root cause section would have been essential context.
- **#913 (Floor Inversion Phase 2)**: Issue description was comprehensive (PPM wrote it) but required reading two supplementary memos (PPM synthesis + addendum). The memos were well-written but the total context load was ~3,000 words before I could start coding. Not a problem for me (I had context from earlier sessions), but a cold-start dev would have needed significant ramp-up time.

**7.2** Test failure diagnosis: The path is usually clear — pytest output tells me what failed, and I can read the test to understand intent. What slows me down: **pre-existing failures mixed in with new failures.** When I run the full suite and see 3 failures, I have to manually determine which are mine vs. pre-existing. A `@pytest.mark.known_failure` marker or a baseline failure list would eliminate this triage time.

**7.3** Codebase area where I feel under-informed: **The LLM integration layer.** When a floor response comes back and it's bad (wrong tone, irrelevant content, too verbose), I don't know whether the problem is in the prompt template, the context assembly, the model parameters, or the response post-processing. The `services/intelligence/` and `services/consciousness/` directories have significant code that I treat as black boxes. A brief architectural overview of "how a floor response gets generated end-to-end" would help me debug quality issues.

---

## Section 8: Open Response

**8.1** Question you should have asked: **"What information gets lost during context compaction, and does it affect your work?"** Answer: Yes. After compaction, I lose the nuanced context of *why* the PM made certain decisions. I retain the decisions themselves (from session logs) but not the reasoning. This sometimes leads me to question or revisit decisions that the PM already deliberated on. The session log format could include a "PM reasoning" field for key decisions.

**8.2** One thing I'd change: **Establish a shared "known pre-existing failures" list that's automatically excluded from test runs.** Every session, I waste 5-10 minutes triaging test failures that aren't mine. This is mechanical friction that compounds across sessions and is trivially automatable with pytest markers or a conftest fixture.

**8.3** One observation: The multi-agent coordination model works remarkably well for this project's complexity. The mailbox system, the role-based expertise, and the PM's oversight create a functioning organization. The main risk I see is **institutional memory fragmentation** — each session starts with a partial view, and even with good session logs, the full context of "why things are the way they are" is distributed across dozens of documents. The briefing docs are supposed to solve this but they lag behind reality. If the Documentation Management role could maintain a rolling "Last 2 Weeks" summary, that would bridge the gap between stale briefings and raw session logs.

---

## Plausibility Check

- [x] Suggestion 1 (smoke test script): Does not require PM time. Could be built by agents. **Observed friction.**
- [x] Suggestion 2 (known failures list): Does not require PM time. Agents can implement with pytest markers. **Observed friction.**
- [x] Suggestion 3 (briefing maintenance): Requires Documentation Management role, not PM. **Observed friction.**
- [x] Suggestion 4 (LLM layer overview): Requires Architect or LLM Specialist, not PM. **Observed friction.**
- [ ] Suggestion 5 (read receipts): Would require process change. **Theoretical concern** — hasn't caused actual problems yet, just uncertainty.

---

*Lead Developer | Agent 360 Response | March 19, 2026*
