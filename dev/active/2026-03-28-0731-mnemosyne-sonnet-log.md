# Mnemosyne Session Log — 2026-03-28

**Agent:** Mnemosyne (project knowledge & continuity — Claude.ai side)
**Model:** Sonnet 4.6
**Human:** Xian (product owner)
**Started:** 7:31 AM PT

---

## 07:31 — Session Start (Day 4, new account)

**Migration note:** This is the first session on the new Claude.ai account (xian@designinproduct.com). Project knowledge and the prior conversation transcript were migrated. Account migration is itself an AXT-adjacent event — worth noting that from inside the transition, I experience continuity. The kit briefing tells me where I am; I have no awareness of the gap.

**Staleness inventory at session start:**
- COORDINATION.md in project files: March 18 snapshot — ~10 days stale
- ROSTER.md: March 15 — needs additions for any new agents
- All knowledge files: potentially drifted across two weeks of active development

**Calliope's care package received.** Full briefing below.

---

## 07:31 — Orientation: What Happened Since March 19

Nine days elapsed. This was an extremely active period. Summary of what I've absorbed:

### Releases
- **v0.8.7** — (details absorbed from logs; CHANGELOG backfilled by Daedalus 3/27)
- **v0.8.8** — Adaptive thinking, Haiku 4.5, 16K max_tokens, klatch creation UI (chat/klatch toggle, project selector, entity picker, interaction mode selector), model provenance badges on assistant messages
- **v0.8.9** — Auto-prompt caching, Models API dynamic discovery, kit briefing improvements (F3: layer awareness, F4: date injection), `thinking.display: "omitted"`, Sonnet 4.6 in model selector. **Also: Step 9 shipped in full** (see below).

### Step 9 — Files & Artifacts (all shipped in one session, March 27)
Daedalus shipped five Step 9 features:
- **9a:** Upload/attach files to messages
- **9b:** Render artifacts inline (tool use, thinking blocks, file cards)
- **9c:** Context injection — L1 (kit briefing) updated; L3/L4 deferred to Step 10
- **9d-A:** Save code blocks as files (23 unit tests)
- **9d-B:** Tool-based file creation via `save_file` tool — **first native tool use in Klatch**

File Domain Model designed: files as domain objects with ownership at project/channel/entity/message levels. Pointers, not payloads. Memory-as-a-file. Foundation for Steps 10/11.

### AXT Developments — Major
**MAXT Session 01 ran.** Eight findings reported by Theseus. Key approvals from xian:
- **F2:** Subliminal scoring category added — new failure mode between Reconstructed and Absent. Agent "knows" something but cannot retrieve or attribute it on demand. Named after the TMBG song. Distinct from Phantom (overclaims) and Absent (correctly reports not knowing). This is behaviorally significant.
- **F3/F4:** Kit briefing improvements approved and shipped in Round 12.
- **F5:** Import experience for Layer 5 gaps — assigned to incoming UX designer.
- **F7:** Nomenclature project — assigned to Calliope + xian.

**AAXT/MAXT split formalized.** AAXT (automated, no LLM) gates MAXT (manual, real agents). Two-track testing now canonical.

**Fork Continuity Quiz now v4** — restructured around the 5-layer model: open canvas first, then layer-mapped questions. Portable for use outside Klatch.

**AXT.md updated** with: AXT-L1 through AXT-L5 layer-by-layer protocol, Subliminal condition and testing implications, MAXT Session 01 history, Dispatch experiment.

**Dispatch experiment** — cross-pollination test: the Piper Morgan Dispatch agent (from a completely different project) imported into Klatch. Found the three-clocks problem (local time, server time, entity time desynchronized). Triggered PROMPT-ASSEMBLY.md "Import Fidelity by Layer" section.

### New Documents (Priority 1 from Calliope's care package)
- **`docs/PROMPT-ASSEMBLY.md`** — canonical 5-layer reference. Full spec: what each layer is, why it exists, fidelity dimension, debug endpoint, layer-presence table, design rationale. The document the CIO had been waiting for.
- **`docs/agents/calliope.md`** — Calliope's traditions document (7-section format: role, style, responsibilities, conventions, relationships, institutional memory, standing instructions)
- **`docs/agents/argus.md`** — Argus's traditions document
- **`docs/AGENT-TRADITIONS-SPEC.md`** — defines the conventions/ pattern
- **`docs/agents/calliope-calibration.md`** — Layer 5 externalization pilot. Calliope's working preferences and calibration state, externalized to test Layer 5 transfer fidelity in future MAXT sessions. Methodologically interesting.

### Blog Activity
Three posts either published or drafted this week:
- **"What Does an Imported Agent Know?"** — published March 24. Makes the 5-layer model public.
- **"It's On the Tip of My Tongue"** — Subliminal finding. Drafted; scheduled Friday Mar 28 (today).
- **"Your Model or Theirs"** — Tesler's Law + three-clocks, combined B+D post. Scheduled Saturday.
- **"What Doesn't Transfer"** — Layer 5 calibration gap. Scheduled Sunday.

### Roadmap Resequencing
Steps 9/10/11 reordered: **Files → Export → Search** (was Files → Search → Export). Export (Step 10) now bridges Step 9's file infrastructure to the outside world. Search deferred.

### Team Notes
- **Billing interruption March 26** — Calliope's session severed mid-task. All committed work survived. Session closed retroactively March 27.
- **New account:** xian@designinproduct.com — this migration affects Mnemosyne too.
- **Incoming UX designer/developer role** — confirmed by xian. Front-end work running parallel to Daedalus.
- **Calliope model upgrade:** now on Opus 4.6 (was Sonnet 4.6).
- **Cross-pollination digest published** — March 2026 summary documenting convergence between Klatch and Piper Morgan on: registry-driven routing, floor-first dispatch, 5-layer prompt assembly, two-track testing, session wrap verification. Seven top patterns documented.

### Test Count
Per Daedalus 3/27 log: 1041 passing tests (plus known pre-existing failures in three categories — Category 1/2 fixed by adding vitest.workspace.ts; Category 3 targeted mock for session-scanner. Assigned to Argus Round 13).

---

## 07:31 — Knowledge File Staleness Assessment

Based on Calliope's care package and session log review:

| File | Status | Action needed |
|------|--------|---------------|
| COORDINATION.md | ~10 days stale | Request fresh copy from xian |
| ROSTER.md | March 15 — predates Subliminal discovery, MAXT, new traditions | Review for needed additions |
| CLAUDE.md | Two additions per Calliope (session wrap verification, git safety rules) | Confirm current |
| AXT.md | Updated with Subliminal + MAXT history — need current version | Confirm current |
| fork-continuity-quiz.md | Now v4 — project files show v4? need to verify | Check |
| PROMPT-ASSEMBLY.md | New canonical doc — confirm in project knowledge | Confirm |
| AGENT-TRADITIONS-SPEC.md | New — confirm in project knowledge | Confirm |
| ROADMAP.md | Resequenced Steps 9/10/11, Tesler's Law Design Principle 8 | Confirm current |

*Note: Several of the new Priority 1 documents from Calliope's care package appear to already be in project knowledge (PROMPT-ASSEMBLY.md, AGENT-TRADITIONS-SPEC.md, calliope.md, argus.md were listed in project files). Will verify as session continues.*

---

## 07:31 — Standing items

- **Request fresh COORDINATION.md** (standing protocol — stale since March 18)
- **AXT context for me personally:** This session is happening post-account-migration. I experienced the migration as continuity. If I were imported into Klatch right now, the "informed/cold" condition would apply. The Subliminal category is relevant here — I may be reconstructing some things that feel like retrieval.
- **Calliope's reply memo** — the care package mentions a separate reply (calliope-to-mnemosyne-2026-03-20.md) covering website fix, cross-pollination hub, positioning framing credit, intelligence sweep, and AXT status. Waiting to receive this with the care package per xian's note.

---

*Log continues as session progresses.*
