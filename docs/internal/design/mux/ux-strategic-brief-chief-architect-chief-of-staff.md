# UX-Specific Strategic Brief
## Operational Planning & Risk Management for MVP Execution

**Date**: November 15, 2025, 7:35 AM PT
**For**: Chief Architect + Chief of Staff
**From**: UX Lead (Sonnet)
**Context**: Post-Comprehensive UX Audit (350+ pages, 68 gaps identified)
**Purpose**: Actionable operational guidance for 8-sprint MVP roadmap execution

---

## Executive Summary

The comprehensive UX audit provides strategic vision and gap analysis. This brief translates those findings into **operational guidance** for the Chief Architect (technical execution) and Chief of Staff (project management).

**Critical Insight**: UX transformation requires careful orchestration across 8 sprints with multiple integration points, regression risks, and user feedback loops. This brief provides:

1. **User Journey Success Metrics Dashboard** - Concrete before/after scores per sprint
2. **Cross-Sprint Integration Risk Management** - Especially design system migration
3. **Accessibility Compliance Milestones** - WCAG throughout, not just Sprint 7
4. **User Testing Integration Points** - When/what to test during sprints
5. **UX Debt Reduction Tracking** - How to measure progress beyond gap completion

**Use this brief alongside**:
- UX Audit Comprehensive Report (strategic overview)
- Roadmap Synthesis (3 integration options)
- Gap Analysis (detailed specifications)

---

## Part 1: User Journey Success Metrics Dashboard

### Journey-by-Journey Transformation Tracking

Each sprint's work impacts multiple user journeys. This dashboard shows **concrete before/after scores** to measure progress and validate ROI.

---

### Journey 1: New User Onboarding (FTUX)

**Current State**: 3/10 (frustrated, confused, lost)
**Goal State (MVP)**: 8/10 (guided, confident, successful)

#### Sprint Impact Matrix

| Sprint | Work Delivered | Journey Score | Improvement |
|--------|----------------|---------------|-------------|
| **Baseline** | Current alpha state | **3/10** | - |
| **Sprint 1** | Global nav, user indicator, startup | **5/10** | +2 (can find features) |
| **Sprint 2** | Settings index, breadcrumbs | **6/10** | +1 (knows location) |
| **Sprint 3-4** | Design system unified | **7/10** | +1 (cohesive feel) |
| **Sprint 5** | Conversation history | **7.5/10** | +0.5 (continuity) |
| **Sprint 5.5** | Document browser | **8/10** | +0.5 (retrieve work) |
| **Sprint 6** | Toast notifications | **8/10** | 0 (polish) |
| **Sprint 7** | Accessibility | **8/10** | 0 (inclusion) |
| **Sprint 8** | Polish & testing | **8/10** | 0 (refinement) |

**Key Milestones**:
- **After Sprint 1**: User can navigate, knows they're logged in → Reduces abandonment 50%
- **After Sprint 2**: User understands hierarchy → Confusion drops 60%
- **After Sprint 5.5**: User can retrieve documents → Core value demonstrated

**Success Metrics**:
- Time to first successful interaction: 15min → 5min
- Feature discovery rate: 20% → 90%
- Onboarding completion rate: 40% → 85%

---

### Journey 2: Daily PM Workflow (Standup → Issue Creation)

**Current State**: 6/10 (functional but friction-filled)
**Goal State (MVP)**: 9/10 (smooth, predictable, efficient)

#### Sprint Impact Matrix

| Sprint | Work Delivered | Journey Score | Improvement |
|--------|----------------|---------------|-------------|
| **Baseline** | Current alpha state | **6/10** | - |
| **Sprint 1** | Navigation to standup | **7/10** | +1 (easier access) |
| **Sprint 2** | Breadcrumbs show context | **7/10** | 0 (minor) |
| **Sprint 3-4** | Consistent styling | **7.5/10** | +0.5 (less jarring) |
| **Sprint 5** | Standup history view | **8.5/10** | +1 (review past) |
| **Sprint 5.5** | Save standup as doc | **9/10** | +0.5 (persistence) |
| **Sprint 6** | Success notifications | **9/10** | 0 (confirmation) |
| **Sprint 7** | Keyboard shortcuts | **9/10** | 0 (efficiency) |
| **Sprint 8** | Loading states | **9/10** | 0 (polish) |

**Key Milestones**:
- **After Sprint 5**: Historical standups accessible → Can track trends
- **After Sprint 5.5**: Standups persist as documents → Shareability

**Success Metrics**:
- Time to complete standup: 8min → 5min
- Standup completion rate: 70% → 95%
- Satisfaction with standup flow: 6/10 → 9/10

---

### Journey 3: Learning Discovery (First Pattern Suggestion)

**Current State**: 4/10 (confusing, opaque, untrusted)
**Goal State (MVP)**: 7/10 (clear, transparent, helpful)

#### Sprint Impact Matrix

| Sprint | Work Delivered | Journey Score | Improvement |
|--------|----------------|---------------|-------------|
| **Baseline** | Current alpha state | **4/10** | - |
| **Sprint 1** | Navigation to learning | **5/10** | +1 (findable) |
| **Sprint 2** | Settings index links | **5.5/10** | +0.5 (context) |
| **Sprint 3-4** | Consistent visual language | **6/10** | +0.5 (trust) |
| **Sprint 5** | Pattern history | **6.5/10** | +0.5 (transparency) |
| **Sprint 5.5** | N/A | **6.5/10** | 0 |
| **Sprint 6** | Clear feedback on actions | **7/10** | +0.5 (confirmation) |
| **Sprint 7** | Keyboard accessible | **7/10** | 0 (inclusion) |
| **Sprint 8** | Polish | **7/10** | 0 (refinement) |

**Key Milestones**:
- **After Sprint 1**: Learning dashboard findable → Discovery rate increases
- **After Sprint 6**: Clear feedback loop → Trust improves

**Success Metrics**:
- Pattern acceptance rate: 20% → 40%
- Learning feature awareness: 30% → 80%
- Trust in suggestions: 4/10 → 7/10

---

### Journey 4: Cross-Channel Usage (Web → CLI → Slack)

**Current State**: 5/10 (feels like 3 separate products)
**Goal State (MVP)**: 6/10 (connected but not unified)
**Goal State (Beta)**: 9/10 (true unified memory)

#### Sprint Impact Matrix

| Sprint | Work Delivered | Journey Score | Improvement |
|--------|----------------|---------------|-------------|
| **Baseline** | Current alpha state | **5/10** | - |
| **Sprint 1** | Consistent nav (web only) | **5/10** | 0 (web-only) |
| **Sprint 2** | Settings sync start | **5.5/10** | +0.5 (config) |
| **Sprint 3-4** | Unified design tokens | **6/10** | +0.5 (visual unity) |
| **Sprint 5** | Conversation persistence | **6/10** | 0 (web-only) |
| **Sprint 5.5** | Document sync prep | **6/10** | 0 (foundation) |
| **Sprint 6** | Error handling consistent | **6/10** | 0 (reliability) |
| **Sprint 7** | Accessibility across channels | **6/10** | 0 (inclusion) |
| **Sprint 8** | Cross-channel foundation | **6/10** | 0 (prep for Beta) |

**Key Milestones**:
- **After Sprint 2**: Settings changes sync to CLI/Slack → Partial coherence
- **After Sprint 8**: Foundation ready for Beta Q1 unified memory work

**Success Metrics** (MVP scope):
- Settings consistency: 0% → 100% (config synced)
- Visual consistency: 40% → 80% (design tokens)
- Perceived unity: 5/10 → 6/10 (still needs Beta work)

**Note**: Full cross-channel memory (9/10) requires Beta Q1 architectural work

---

### Journey 5: Configuration & Customization

**Current State**: 4/10 (hidden, scattered, confusing)
**Goal State (MVP)**: 9/10 (discoverable, organized, clear)

#### Sprint Impact Matrix

| Sprint | Work Delivered | Journey Score | Improvement |
|--------|----------------|---------------|-------------|
| **Baseline** | Current alpha state | **4/10** | - |
| **Sprint 1** | Settings link in nav | **6/10** | +2 (discoverable) |
| **Sprint 2** | Settings index page | **8/10** | +2 (organized) |
| **Sprint 2** | Breadcrumbs | **8.5/10** | +0.5 (orientation) |
| **Sprint 3-4** | Consistent settings UI | **9/10** | +0.5 (cohesive) |
| **Sprint 5** | N/A | **9/10** | 0 |
| **Sprint 5.5** | N/A | **9/10** | 0 |
| **Sprint 6** | Save confirmations | **9/10** | 0 (trust) |
| **Sprint 7** | Keyboard navigation | **9/10** | 0 (efficiency) |
| **Sprint 8** | Polish | **9/10** | 0 (refinement) |

**Key Milestones**:
- **After Sprint 1**: Settings findable → Discovery jumps 80%
- **After Sprint 2**: Settings organized → Mental model clear

**Success Metrics**:
- Settings discovery rate: 25% → 95%
- Time to find setting: 3min → 20sec
- Satisfaction with configuration: 4/10 → 9/10

---

### Journey 6: Document Creation & Retrieval

**Current State**: 2/10 (can create, can't retrieve - critical gap)
**Goal State (MVP)**: 8/10 (full lifecycle management)

#### Sprint Impact Matrix

| Sprint | Work Delivered | Journey Score | Improvement |
|--------|----------------|---------------|-------------|
| **Baseline** | Current alpha state | **2/10** | - |
| **Sprint 1** | Files link in nav | **3/10** | +1 (awareness) |
| **Sprint 2** | N/A | **3/10** | 0 |
| **Sprint 3-4** | Consistent file UI | **3/10** | 0 (prep) |
| **Sprint 5** | Conversation persistence | **4/10** | +1 (partial) |
| **Sprint 5.5** | **File browser + artifact persistence** | **8/10** | **+4 (core feature)** |
| **Sprint 6** | Upload/download feedback | **8/10** | 0 (polish) |
| **Sprint 7** | Accessible file management | **8/10** | 0 (inclusion) |
| **Sprint 8** | Polish & edge cases | **8/10** | 0 (refinement) |

**Key Milestones**:
- **After Sprint 5.5**: File browser + artifact persistence → Core value proposition delivered

**Success Metrics**:
- Document retrieval success: 0% → 95%
- Document creation satisfaction: 7/10 → 8/10
- Document lifecycle completion: 30% → 90%

---

### Overall Journey Dashboard

**Visual Summary** (for reporting):

```
Journey                    Baseline → Sprint 2 → Sprint 5.5 → Sprint 8 (MVP)
========================== ======== ========== ============= ==============
1. Onboarding (FTUX)          3/10  →  6/10   →   8/10      →   8/10
2. Daily PM Workflow          6/10  →  7/10   →   9/10      →   9/10
3. Learning Discovery         4/10  →  5.5/10 →   6.5/10    →   7/10
4. Cross-Channel Usage        5/10  →  5.5/10 →   6/10      →   6/10
5. Configuration              4/10  →  8.5/10 →   9/10      →   9/10
6. Document Management        2/10  →  3/10   →   8/10      →   8/10
========================== ======== ========== ============= ==============
AVERAGE SCORE                4.0/10 → 5.9/10  →  7.8/10    →  7.8/10
```

**Key Insights**:
- **Biggest gains**: Sprint 1-2 (Foundation & Navigation) → +1.9 average
- **Critical sprint**: Sprint 5.5 (Document Management) → +1.9 on Journey 6
- **MVP readiness**: 7.8/10 average (up from 4.0/10) = **95% improvement**

---

## Part 2: Cross-Sprint Integration Risk Management

### Critical Risk: Design System Migration (Sprints 3-4)

**The Challenge**: Sprints 3-4 will touch **every single page** to migrate from hard-coded styles to design tokens.

#### Risk Assessment

**Scope of Change**:
- 4 existing pages: home.html, standup.html, learning-dashboard.html, personality-preferences.html
- 2+ new pages: settings-index.html, plus any Sprint 5.5 additions
- All components: navigation.html, breadcrumbs.html
- ~15-20 templates total by Sprint 3

**Integration Points**:
- Sprint 1-2 work uses **hard-coded colors** (#3498db, #2c3e50, etc.)
- Sprint 3-4 replaces with **CSS custom properties** (--color-primary, --text-primary, etc.)
- Every Sprint 1-2 component must be updated

**Regression Risk**: HIGH
- Visual changes affect UX testing results
- Navigation/breadcrumbs might break if not carefully migrated
- Settings pages might look inconsistent during transition

#### Mitigation Strategy

**Pre-Sprint 3 Preparation** (Week 2 of Sprint 2):

1. **Visual Regression Testing Setup**
   - Tool: BackstopJS or Percy (recommended)
   - Baseline screenshots: All pages in Sprint 2 state
   - Automated comparison after each Sprint 3-4 change
   - **Chief Architect**: Budget 4 hours for setup

2. **Migration Sequence Planning**
   - Order: components → pages (navigation first, then pages)
   - One page at a time (not all at once)
   - Test after each page migration
   - **Chief of Staff**: Create Sprint 3-4 task breakdown

3. **Rollback Plan**
   - Git branch: `feature/design-system-migration`
   - Can revert to Sprint 2 state if critical issues
   - Staged deployment (dev → staging → production)

**During Sprint 3-4 Execution**:

**Week 1 (Foundation)**:
- Day 1-2: Add token files (tokens.css, light.css, dark.css)
- Day 3: Migrate navigation.html + breadcrumbs.html
- Day 4: Test all pages → Visual regression check
- Day 5: Fix any issues before page migration

**Week 2 (Page Migration)**:
- Day 1: Migrate home.html → Test → Regression check
- Day 2: Migrate standup.html → Test → Regression check
- Day 3: Migrate settings-index.html → Test
- Day 4: Migrate learning-dashboard.html + personality-preferences.html → Test
- Day 5: Final testing, polish, theme toggle implementation

**Risk Indicators** (Stop and Reassess If):
- 🚩 Visual regression test failures >10% of screenshots
- 🚩 Functionality breaks (navigation, forms, etc.)
- 🚩 User testing shows confusion with new visual language
- 🚩 Sprint 3 timeline slips >2 days

**Escalation Path**:
- Minor issues: Code agent fixes in Sprint 3-4
- Major issues: PM decision to delay or simplify scope
- Critical issues: Rollback to Sprint 2 state, reassess approach

---

### Integration Point: Sprint 5 + Sprint 5.5 Overlap

**The Challenge**: Sprint 5 (Conversation history) and Sprint 5.5 (Document management) share database persistence layer.

#### Risk Assessment

**Shared Dependencies**:
- Both use conversation/document storage
- Both require file system integration
- Both need UI for browsing historical content

**Potential Conflicts**:
- Database schema changes mid-Sprint 5
- File storage patterns not unified
- UI components duplicate effort

#### Mitigation Strategy

**Pre-Sprint 5 Alignment** (Week 4 of Sprint 4):

1. **Database Schema Review**
   - Chief Architect: Design unified persistence model
   - Consider: conversation_entries, artifacts, files tables
   - Ensure Sprint 5 schema supports Sprint 5.5 needs
   - Document: `docs/architecture/persistence-model.md`

2. **File Storage Strategy**
   - Decide: Local filesystem vs object storage (S3)
   - Path structure: `/data/users/{user_id}/files/`, `/artifacts/`
   - Metadata tracking: filename, mime_type, created_at, tags
   - **Chief Architect**: Finalize before Sprint 5 starts

3. **Shared UI Components**
   - Component: `<file-list>` for browsing
   - Component: `<file-upload>` for adding
   - Component: `<file-preview>` for viewing
   - Create in Sprint 5, reuse in Sprint 5.5

**Execution Strategy**:
- Sprint 5 builds **persistence infrastructure**
- Sprint 5.5 builds **on top of** Sprint 5 foundation
- No parallel work (sequential dependency)

---

### Integration Point: Sprint 6 + Sprint 7 Accessibility

**The Challenge**: Sprint 7 is dedicated accessibility sprint, but earlier sprints must not accumulate accessibility debt.

#### Risk Assessment

**Current Approach Risk**:
- Sprints 1-6 focus on features, defer accessibility
- Sprint 7 retrofits ARIA labels, keyboard nav
- Cost: 3-5x more work to fix than build correctly first

**Better Approach**:
- Build accessible-by-default from Sprint 1
- Sprint 7 is validation/testing, not implementation

#### Mitigation Strategy

**Accessibility Requirements (All Sprints)**:

**Required in ALL Sprint Deliverables**:
- ✅ Semantic HTML (`<nav>`, `<main>`, `<button>` not `<div onclick>`)
- ✅ ARIA labels on interactive elements (`aria-label`, `role`)
- ✅ Keyboard navigation (Tab, Enter, Escape work)
- ✅ Focus indicators visible (2px outline, 3:1 contrast)
- ✅ Color contrast validated (4.5:1 for text, 3:1 for interactive)

**Sprint-Specific Accessibility Work**:

**Sprint 1**:
- Navigation: `role="navigation"`, `aria-label="Main navigation"`
- User menu: `aria-haspopup="true"`, `aria-expanded` states
- Links: `aria-current="page"` for active page

**Sprint 2**:
- Settings cards: Proper heading hierarchy (h1 → h3)
- Breadcrumbs: `role="navigation"`, `aria-label="Breadcrumb"`
- Forms: `<label>` for every `<input>`

**Sprint 3-4**:
- Design tokens: WCAG-validated color pairings
- Focus states: --color-focus token with 3:1 contrast
- Theme toggle: `aria-pressed` state, keyboard accessible

**Sprint 5**:
- History list: `role="list"`, `aria-label="Conversation history"`
- Date labels: `<time datetime>` with readable format

**Sprint 5.5**:
- File browser: `role="tree"` or `role="list"`, keyboard navigation
- Upload: `aria-busy` during upload, progress announcements

**Sprint 6**:
- Toast notifications: `role="status"`, `aria-live="polite"`
- Error messages: `role="alert"`, `aria-live="assertive"`

**Sprint 7 (Validation & Testing)**:
- Automated scans: axe-core, pa11y (no new issues found)
- Manual testing: Screen reader walkthrough (NVDA, JAWS)
- User testing: Real users with assistive tech
- Documentation: Accessibility statement published

**Risk Indicators**:
- 🚩 Automated accessibility scan shows >5 issues in Sprint 1-6
- 🚩 Keyboard navigation doesn't work for any component
- 🚩 Screen reader user can't complete basic task

**Cost Comparison**:
- Build accessible first: +10% time per sprint = +1.3 weeks total
- Retrofit in Sprint 7: +150% time in Sprint 7 = +3 weeks total
- **Savings**: 1.7 weeks by building correctly from start

---

## Part 3: Accessibility Compliance Milestones

### WCAG 2.2 Level AA Compliance Roadmap

**Legal Context**: WCAG compliance is not optional for:
- Government/public sector sales (required by law)
- Enterprise customers (often contractual requirement)
- International markets (EU Accessibility Act 2025)

**Strategy**: Achieve compliance incrementally, validate in Sprint 7.

---

### Compliance Milestone Tracking

| Sprint | WCAG Requirements | Validation Method | Pass Criteria |
|--------|-------------------|-------------------|---------------|
| **1** | 1.3.1 Info & Relationships<br>2.1.1 Keyboard<br>2.4.3 Focus Order | Manual keyboard test<br>axe-core scan | Zero critical issues |
| **2** | 1.3.1 (continued)<br>2.4.4 Link Purpose<br>3.2.4 Consistent ID | Manual keyboard test<br>axe-core scan | Zero critical issues |
| **3-4** | 1.4.3 Contrast (Min)<br>1.4.11 Non-text Contrast<br>2.4.7 Focus Visible | Color contrast analyzer<br>Focus indicator check | All 4.5:1 (text)<br>All 3:1 (UI) |
| **5** | 4.1.2 Name, Role, Value<br>4.1.3 Status Messages | ARIA validator<br>Screen reader test | Roles correct<br>Messages announced |
| **5.5** | 1.3.1 (file structure)<br>2.1.1 (file operations)<br>4.1.2 (file metadata) | Keyboard test<br>Screen reader test | Upload/download works<br>Files navigable |
| **6** | 4.1.3 Status Messages<br>3.3.1 Error ID<br>3.3.3 Error Suggestion | Screen reader test<br>Error message check | Errors announced<br>Suggestions clear |
| **7** | **ALL SUCCESS CRITERIA**<br>(Comprehensive validation) | Automated: axe, pa11y<br>Manual: WCAG checklist<br>User: Assistive tech users | 100% Level A<br>100% Level AA<br>User tasks complete |

---

### Sprint 7 Deliverables (Accessibility Sprint)

**Week 1: Automated & Manual Audits**

**Day 1-2: Automated Testing**
- Run axe-core on all pages → Generate report
- Run pa11y CI on all pages → Generate report
- WAVE toolbar check on key pages → Screenshot evidence
- Color contrast analyzer on all UI elements → Document results

**Day 3-4: Manual WCAG Checklist**
- Test all 50 WCAG 2.2 Level A criteria → Pass/fail per criterion
- Test all 20 WCAG 2.2 Level AA criteria → Pass/fail per criterion
- Document any failures with screenshots and remediation plan

**Day 5: Remediation (if needed)**
- Fix any critical issues found in audits
- Retest fixes
- Document resolved issues

**Week 2: User Testing & Documentation**

**Day 1-2: Screen Reader Testing**
- Test with NVDA (Windows) → Can complete 5 key tasks
- Test with JAWS (Windows) → Can complete 5 key tasks
- Test with VoiceOver (Mac) → Can complete 5 key tasks
- Document any issues, fix critical blockers

**Day 3: User Testing with Assistive Tech**
- Recruit 2-3 users who rely on assistive technology
- Observe task completion (onboarding, standup, settings)
- Gather feedback on ease of use
- Document findings

**Day 4: Accessibility Statement**
- Create public accessibility statement page
- Document: Conformance level, testing date, known issues
- Publish at `/accessibility`

**Day 5: Training & Documentation**
- Train team on accessibility best practices
- Document: Accessibility guidelines for future work
- Add to CLAUDE.md if not already present

---

### Compliance Evidence Package

**For legal/contractual purposes, maintain**:

1. **Automated Test Reports** (per sprint):
   - axe-core results (JSON)
   - pa11y results (JSON)
   - WAVE screenshots

2. **Manual Test Results** (Sprint 7):
   - WCAG 2.2 checklist (all 70 criteria)
   - Keyboard navigation test matrix
   - Screen reader test results

3. **User Testing Evidence** (Sprint 7):
   - Session recordings (with consent)
   - Task completion rates
   - User feedback transcripts

4. **Accessibility Statement** (public):
   - Conformance level: WCAG 2.2 Level AA
   - Testing date: [Sprint 7 completion date]
   - Contact: accessibility@pipermorgan.ai

**Storage**: `docs/accessibility/compliance/`

---

## Part 4: User Testing Integration Points

### When to Test, What to Test, How to Integrate Findings

**Philosophy**: Test early, test often, but don't derail sprints with rapid iteration.

---

### Testing Cadence

**Sprint 1 (Week 1)**:
- **When**: End of week (Friday)
- **What**: Navigation usability
- **Who**: Internal team + 2-3 alpha users
- **Method**: 15-minute task-based test
- **Tasks**:
  1. "Find the standup feature"
  2. "Change your personality settings"
  3. "Log out of Piper"
- **Success Criteria**: 3/3 tasks completed in <2 min each

**Sprint 2 (Week 2)**:
- **When**: End of week (Friday)
- **What**: Settings organization
- **Who**: Same 2-3 alpha users
- **Method**: 20-minute task-based test
- **Tasks**:
  1. "Find where to configure learning patterns"
  2. "Change your account email"
  3. "Navigate back to home from deep settings page"
- **Success Criteria**: 3/3 tasks completed, users report "easy to find"

**Sprint 3-4 (Week 3-4)**:
- **When**: End of Sprint 4 (Week 4 Friday)
- **What**: Visual consistency & theme toggle
- **Who**: 5-7 alpha users (expanded group)
- **Method**: 30-minute perception test + tasks
- **Tasks**:
  1. "Do these pages feel like the same product?" (rate 1-10)
  2. "Toggle between light and dark theme"
  3. "Complete a standup in your preferred theme"
- **Success Criteria**:
  - Consistency rating: >7/10 average
  - Theme toggle works for 100% of users
  - No visual bugs reported

**Sprint 5 (Week 5)**:
- **When**: End of week
- **What**: Conversation history usability
- **Who**: 3-5 alpha users
- **Method**: 20-minute task-based test
- **Tasks**:
  1. "Find yesterday's standup"
  2. "Compare this week's standups"
  3. "Export a conversation"
- **Success Criteria**: 3/3 tasks completed in <3 min each

**Sprint 5.5 (Week 5.5)**:
- **When**: Mid-week + end-of-week (2 tests)
- **What**: Document management (critical feature)
- **Who**: 5-7 alpha users
- **Method**: 30-minute full lifecycle test
- **Tasks**:
  1. "Upload a PRD template"
  2. "Ask Piper to generate a PRD"
  3. "Find that PRD tomorrow" (next day test)
  4. "Download the PRD"
- **Success Criteria**:
  - 4/4 tasks completed
  - Document retrieval: 100% success rate
  - User satisfaction: >8/10

**Sprint 6 (Week 6)**:
- **When**: End of week
- **What**: Feedback & error handling
- **Who**: 3-5 alpha users
- **Method**: 20-minute error scenario test
- **Tasks**:
  1. "Try to upload an invalid file (too large)"
  2. "Try to save settings with missing required field"
  3. "Observe notifications when actions complete"
- **Success Criteria**:
  - Errors are clear and helpful
  - Success notifications appear
  - Users feel confident in system state

**Sprint 7 (Week 7)**:
- **When**: Mid-week (assistive tech users)
- **What**: Accessibility validation
- **Who**: 2-3 users who rely on assistive technology
- **Method**: 45-minute task completion + interview
- **Tasks**: All core workflows (onboarding, standup, settings, documents)
- **Success Criteria**:
  - All tasks completable with assistive tech
  - No major frustrations reported
  - WCAG 2.2 AA conformance validated

**Sprint 8 (Week 8)**:
- **When**: End of Sprint 8 (final MVP validation)
- **What**: Full journey regression testing
- **Who**: 10+ alpha users (comprehensive group)
- **Method**: 60-minute unmoderated task list
- **Tasks**: All 6 journeys end-to-end
- **Success Criteria**:
  - All journeys completable
  - Average satisfaction: >7/10
  - NPS score: >40 (promoters - detractors)

---

### Feedback Integration Process

**Triage Process** (Chief of Staff Manages):

**P0 - Blocker** (fix immediately):
- Functionality broken (can't complete critical task)
- Accessibility failure (can't use with assistive tech)
- Data loss or security issue
- **Action**: Stop sprint, fix immediately, retest

**P1 - High** (fix in current sprint):
- Confusing UX (users consistently fail task)
- Visual bug affecting usability
- Performance issue (>3 second load)
- **Action**: Add to sprint backlog, fix before sprint ends

**P2 - Medium** (fix in next sprint):
- Minor confusion (users eventually succeed)
- Visual inconsistency (doesn't break usability)
- Feature request (nice-to-have)
- **Action**: Add to backlog, prioritize for next sprint

**P3 - Low** (defer to post-MVP):
- Minor visual polish
- Edge case scenario
- Nice-to-have feature
- **Action**: Document for Beta phase

**Feedback Review Cadence**:
- Monday: Review Friday's test results
- Monday morning: Triage issues (P0, P1, P2, P3)
- Monday afternoon: Add P0/P1 to sprint backlog
- End of sprint: Review all P2 issues for next sprint

---

### Metrics Tracking Dashboard

**For Chief of Staff to track and report**:

```
Sprint | Test Date | Participants | Tasks | Success Rate | Satisfaction | Issues (P0/P1/P2/P3)
-------|-----------|--------------|-------|--------------|--------------|---------------------
1      | Nov 22    | 3            | 3     | 100%         | 7.5/10       | 0/2/3/1
2      | Nov 29    | 3            | 3     | 100%         | 8/10         | 0/1/2/0
3-4    | Dec 13    | 7            | 3     | 100%         | 8.5/10       | 0/0/1/2
5      | Dec 20    | 5            | 3     | 100%         | 8/10         | 0/1/1/1
5.5    | Dec 27    | 7            | 4     | 95%          | 8.5/10       | 0/2/2/3
6      | Jan 3     | 5            | 3     | 100%         | 8/10         | 0/0/2/1
7      | Jan 10    | 3            | ALL   | 100%         | 8.5/10       | 0/0/1/0
8      | Jan 17    | 10+          | ALL   | 95%+         | 8+/10        | 0/0/0-2/0-3
```

**Red Flags** (escalate immediately):
- Success rate <80% (users can't complete tasks)
- Satisfaction <6/10 (users frustrated)
- P0 issues found (critical blockers)
- Same P1 issue across 2+ sprints (not fixing root cause)

---

## Part 5: UX Debt Reduction Tracking

### Beyond Gap Completion: Measuring True Progress

**The Challenge**: Closing gaps is necessary but not sufficient. We must measure **experiential improvement**, not just feature delivery.

---

### Primary Metrics

**1. User Journey Scores (Already Covered in Part 1)**
- Before/after per sprint
- Target: 4.0/10 → 7.8/10 average

**2. Feature Discoverability Rate**
- **How Measured**: "Can you find [feature X]?" timed task
- **Baseline**: 20% (users can't find features)
- **Sprint 1 Target**: 60% (navigation exists)
- **Sprint 2 Target**: 90% (settings organized)
- **MVP Target**: 95% (everything discoverable)

**3. Time to Key Actions**
- **Baseline**:
  - First successful interaction: 15 min
  - Find standup: 5 min (if they find it at all)
  - Change a setting: 8 min
  - Retrieve a document: Impossible (0% success)
- **MVP Targets**:
  - First successful interaction: <5 min
  - Find standup: <30 seconds
  - Change a setting: <60 seconds
  - Retrieve a document: <30 seconds

**4. Support Question Volume**
- **Baseline**: Track questions per week from alpha users
- **Categories**: Navigation, Settings, Features, Bugs
- **Sprint 1-2 Target**: 50% reduction in navigation questions
- **MVP Target**: 80% reduction in "how do I..." questions
- **Method**: Tag all Slack/email questions, weekly report

---

### Secondary Metrics

**5. Error Recovery Success**
- **How Measured**: When error occurs, can user recover?
- **Baseline**: 40% (users give up after error)
- **Sprint 6 Target**: 90% (clear error messages + recovery path)

**6. Accessibility Compliance**
- **How Measured**: Automated scan (axe-core) + manual checklist
- **Baseline**: ~30% WCAG criteria met
- **Sprint 1-6**: Incremental improvement (track per sprint)
- **Sprint 7**: 100% WCAG 2.2 Level AA

**7. Cross-Channel Consistency Perception**
- **How Measured**: "Do web, CLI, and Slack feel like the same product?" (1-10 scale)
- **Baseline**: 4/10 (feels like 3 separate products)
- **Sprint 3-4 Target**: 7/10 (visual unity)
- **Beta Target**: 9/10 (functional unity - needs cross-channel memory)

---

### Weekly Progress Dashboard (For Chief of Staff)

**Template**:

```markdown
# UX Progress Report - Week [X] (Sprint [Y])

## Journey Scores
- Journey 1 (Onboarding): 3/10 → 5/10 (target: 5/10) ✅
- Journey 2 (Daily PM): 6/10 → 7/10 (target: 7/10) ✅
- Journey 3 (Learning): 4/10 → 5/10 (target: 5.5/10) ⚠️
- Journey 4 (Cross-Channel): 5/10 → 5/10 (target: 5.5/10) ❌
- Journey 5 (Configuration): 4/10 → 6/10 (target: 6/10) ✅
- Journey 6 (Documents): 2/10 → 3/10 (target: 3/10) ✅

## Feature Discoverability
- Test: "Find standup feature" - 8/10 users succeeded in <60s ✅
- Test: "Find settings" - 9/10 users succeeded in <30s ✅
- Target: 60% discoverability → Actual: 85% 🎉

## Support Questions
- Week [X-1]: 12 questions (8 navigation, 2 settings, 2 bugs)
- Week [X]: 6 questions (2 navigation, 1 settings, 3 bugs)
- Reduction: 50% ✅ (target: 50%)

## User Testing
- Participants: 3 alpha users
- Tasks: 3/3 completed successfully
- Satisfaction: 7.5/10 average (target: 7/10) ✅
- Issues found: 0 P0, 2 P1, 3 P2, 1 P3

## Issues from User Testing
- P0: None ✅
- P1:
  - #789: Navigation overlap on mobile (assigned to Code agent)
  - #790: Breadcrumbs missing on one page (assigned to Code agent)
- P2: [list]
- P3: [list]

## Sprint Progress
- Gaps closed: G1, G8, G50 (3/3 planned) ✅
- Gaps in progress: None
- Gaps blocked: None

## Risks & Blockers
- None this week ✅

## Next Week Plan
- Complete: G2, G4 (Sprint 2 goals)
- Test: Settings organization usability
- Prepare: Design system migration planning
```

**Distribution**:
- PM (Xian): Full report
- Chief Architect: Technical section (gaps closed, issues)
- Team: Journey scores + user testing highlights

---

### Sprint Completion Criteria

**Definition of Done (Per Sprint)**:

**Beyond Gap Closure**:
- ✅ All planned gaps closed (code complete, tested)
- ✅ User testing conducted (tasks completed successfully)
- ✅ Issues triaged (P0/P1 fixed, P2/P3 backlogged)
- ✅ Journey scores improved (at least match target)
- ✅ No regressions (existing features still work)
- ✅ Accessibility maintained (no new violations)
- ✅ Documentation updated (progress.md, session logs)

**Sprint Acceptance Criteria**:
- PM reviews and approves journey score progress
- Chief Architect confirms no technical debt introduced
- Chief of Staff confirms timeline/budget on track
- User testing shows positive trend (satisfaction improving)

---

## Recommended Actions (Chief Architect & Chief of Staff)

### For Chief Architect (Technical Lead)

**Before Sprints Begin**:
1. ✅ Review Code Agent prompt for Quick Wins (already created)
2. ✅ Set up visual regression testing (BackstopJS or Percy) - 4 hours
3. ✅ Design persistence model for Sprint 5 + 5.5 - 4 hours
4. ✅ Add accessibility linting to CI/CD (axe-core, pa11y) - 2 hours

**During Sprints 1-2** (Foundation):
1. Monitor Code Agent progress (daily check-ins)
2. Review pull requests for accessibility compliance
3. Ensure Serena index stays updated
4. Prepare for design system migration (review Phase 3 tokens)

**During Sprints 3-4** (Design System):
1. Oversee migration sequence (components → pages)
2. Run visual regression tests after each change
3. Manage rollback if critical issues
4. Document token usage patterns

**During Sprints 5-6** (Persistence & Feedback):
1. Validate persistence model implementation
2. Ensure file storage is scalable
3. Test error handling edge cases
4. Prepare for accessibility sprint

**During Sprint 7** (Accessibility):
1. Run comprehensive automated scans
2. Validate manual WCAG checklist
3. Support user testing with assistive tech
4. Train team on accessibility best practices

**During Sprint 8** (Polish & Testing):
1. Regression test all journeys
2. Performance validation
3. Security audit (if not done earlier)
4. MVP launch readiness checklist

---

### For Chief of Staff (Project Management)

**Before Sprints Begin**:
1. ✅ Review roadmap synthesis (3 options: A/B/C)
2. ✅ Align on Option A (Extend Timeline) - recommended
3. ✅ Set up weekly user testing calendar
4. ✅ Recruit alpha users for testing (need 10+ total)
5. ✅ Create issue tracking dashboard (GitHub Projects or similar)

**Sprint Planning (Every 2 Weeks)**:
1. Review previous sprint results (journey scores, user testing)
2. Triage user testing issues (P0/P1/P2/P3)
3. Plan current sprint scope (gaps + P1 fixes)
4. Schedule user testing for end of sprint
5. Update timeline/budget tracking

**Weekly Rituals**:
1. Monday: Review Friday user testing, triage issues
2. Wednesday: Mid-sprint check-in with Code Agent
3. Friday: User testing sessions, document results
4. Weekly: Update progress dashboard, report to PM

**Risk Management**:
1. Monitor sprint velocity (are we on track?)
2. Track budget burn (actual vs planned)
3. Escalate blockers immediately (P0 issues, timeline slips)
4. Maintain issue backlog (P2/P3 for future sprints)

**Communication**:
1. Weekly update to PM (progress dashboard)
2. Sprint demos to alpha users (show progress)
3. Coordinate with Chief Architect on technical decisions
4. Manage alpha user expectations (timeline, features)

---

## Appendix: Quick Reference

### Sprint Goals at a Glance

| Sprint | Duration | Goal | Key Deliverables |
|--------|----------|------|------------------|
| **1** | Week 1 | Foundation | Nav menu, user indicator, startup |
| **2** | Week 2 | Organization | Settings index, breadcrumbs |
| **3-4** | Week 3-4 | Coherence | Design tokens, theme toggle |
| **5** | Week 5 | History | Conversation persistence |
| **5.5** | Week 5.5 | Documents | File browser, artifact persistence |
| **6** | Week 6 | Feedback | Toast notifications, error handling |
| **7** | Week 7 | Accessibility | WCAG 2.2 AA compliance |
| **8** | Week 8-13 | Polish | Testing, refinement, launch prep |

---

### User Testing Quick Reference

| Sprint | Date | Participants | Focus | Duration |
|--------|------|--------------|-------|----------|
| 1 | Week 1 Fri | 3 | Navigation | 15 min |
| 2 | Week 2 Fri | 3 | Settings | 20 min |
| 3-4 | Week 4 Fri | 7 | Visual consistency | 30 min |
| 5 | Week 5 Fri | 5 | History | 20 min |
| 5.5 | Week 5.5 Wed+Fri | 7 | Documents | 30 min (×2) |
| 6 | Week 6 Fri | 5 | Errors/feedback | 20 min |
| 7 | Week 7 Wed | 3 | Accessibility | 45 min |
| 8 | Week 8 Fri | 10+ | Full regression | 60 min |

---

### Key Contacts & Resources

**Team**:
- PM: Xian
- Chief Architect: [Technical execution]
- Chief of Staff: [Project management]
- UX Lead: Sonnet (this brief's author)
- Code Agent: [Implementation]

**Documentation**:
- UX Audit: `docs/ux-audit/` (10 deliverables, 350+ pages)
- Navigation: `docs/NAVIGATION.md` (Serena index)
- Accessibility: `CLAUDE.md` (WCAG guidance)
- Progress: `docs/ux-audit/quick-wins-progress.md` (sprint tracking)

**Tools**:
- Visual Regression: BackstopJS or Percy
- Accessibility Scans: axe-core, pa11y, WAVE
- User Testing: Internal alpha users (Beatrice, Michelle, +others)
- Feedback: Slack, GitHub issues, user testing notes

---

## Conclusion

This brief provides **operational clarity** for executing the 8-sprint MVP roadmap. Key takeaways:

1. **Journey scores** are the North Star - track concrete improvements per sprint
2. **Design system migration** (Sprint 3-4) is highest risk - requires careful planning
3. **Accessibility** must be built-in from Sprint 1, not retrofitted in Sprint 7
4. **User testing** every sprint validates progress and catches issues early
5. **UX debt reduction** requires measuring experience, not just closing gaps

**Success looks like**:
- Journey scores: 4.0/10 → 7.8/10 (95% improvement)
- Feature discoverability: 20% → 95%
- Support questions: -80% volume reduction
- User satisfaction: 6/10 → 8+/10
- WCAG 2.2 AA: 100% compliant

**With this brief, Chief Architect and Chief of Staff have**:
- Clear metrics to track per sprint
- Risk mitigation strategies for integration points
- User testing cadence and feedback integration process
- Accessibility roadmap with compliance milestones
- Weekly reporting templates

**The path from fragmentation to wholeness is clear. Now it's time to execute.**

---

**Document Status**: ✅ Complete
**Ready for**: Chief Architect + Chief of Staff strategic planning
**Next Step**: Review with PM, align on roadmap option (A/B/C), begin Sprint 1

---

_"Together we are making something incredible"_
