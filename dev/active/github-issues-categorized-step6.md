# GitHub Issue Categorization - First Pass
**Total Issues**: 120
**Date**: December 27, 2025
**Framework**: 6-tier priority system

---

## 🔴 Alpha Critical (4 issues)
Must have for alpha testing to function

1. **#440** ALPHA-SETUP-TEST: Setup wizard integration test (A11 - Status: Review)
2. **#358** SEC-ENCRYPT-ATREST: Implement Encryption at Rest (S2 - In Progress)
3. **#322** ARCH-FIX-SINGLETON: Replace ServiceContainer singleton (S2 - Sprint Backlog)
4. **#484** ARCH-SCHEMA-VALID: Add Schema Validation Check on Startup (S2 - Sprint Backlog)

---

## 🟠 Beta Enablers (9 issues)
Needed for beta - discovery and conversation

1. **#519** Canonical Queries Phase B-1: GitHub Issue Operations
2. **#520** Canonical Queries Phase B-2: Slack Slash Commands
3. **#522** Canonical Queries Phase B-4: Document Update
4. **#517** Update multi-agent coordination protocols
5. **#488** MUX-INTERACT-DISCOVERY: Discovery-Oriented Intent Architecture (I1)
6. **#310** CONV-UX-QUICK: Settings & Startup Quick Wins (M2)
7. **#102** CONV-UX-GREET: Calendar Scanning on Greeting (M2)
8. **#304** CONV-INFR-NOTN: Activate Existing Notion Integration (M2)
9. **#524** Pattern Sweep 2.0: Multi-Lens Analysis (our new framework!)

---

## 🟡 MUX Foundation (45 issues)

### MUX Meta (1)
- **#398** MUX: Modeled User Experience (MVP)

### V1 - Vision Formalization (6)
- **#401** MUX-VISION: Conceptual architecture (Sprint Backlog)
- **#399** MUX-VISION-OBJECT-MODEL: Formalize the Object Model
- **#404** MUX-VISION-GRAMMAR-CORE: "Entities experience Moments in Places"
- **#400** MUX-VISION-CONSCIOUSNESS: Extract Embodied AI Patterns
- **#405** MUX-VISION-METAPHORS: Formalize ownership metaphors
- **#477** Refine todo list UX and paradigm

### V2 - Integration Mapping (4)
- **#406** MUX-VISION-FEATURE-MAP: Map existing features to object model
- **#407** MUX-VISION-STANDUP-EXTRACT: Extract consciousness patterns
- **#408** MUX-VISION-LIFECYCLE-SPEC: Formalize 8-stage lifecycle
- **#431** MUX-VISION-LEARN: Learning System Experience Design
- **#474** Enable full list management (add/edit/delete items)

### X1 - Tech Implementation (5)
- **#432** MUX-TECH (meta issue)
- **#433** MUX-TECH-PHASE1-GRAMMAR: Core Object Model Grammar
- **#434** MUX-TECH-PHASE2-ENTITY: Piper as Entity with Consciousness
- **#435** MUX-TECH-PHASE3-OWNERSHIP: Implement Ownership Model
- **#436** MUX-TECH-PHASE4-COMPOSTING: Learning Pipeline

### I1-I3 - Interact (13)
- **#402** MUX-INTERACT: Interaction Design (meta)
- **#410** MUX-INTERACT-CANONICAL-ENHANCE: Evolve queries to orientation
- **#411** MUX-INTERACT-RECOGNITION: "did you mean..." patterns
- **#412** MUX-INTERACT-INTENT-BRIDGE: Bridge intent to recognition
- **#413** MUX-INTERACT-TRUST-LEVELS: Trust gradient mechanics
- **#414** MUX-INTERACT-DELEGATION: System vs user-initiated
- **#415** MUX-INTERACT-PREMONITION: When/how Piper surfaces insights
- **#416** MUX-INTERACT-WORKSPACE: Context navigation
- **#417** MUX-INTERACT-ATTENTION: Attention algorithms
- **#418** MUX-INTERACT-MOMENT-UI: How Moments appear

### P1-P4 - Implement (13)
- **#403** MUX-IMPLEMENT: UI Polish (meta)
- **#419** MUX-IMPLEMENT-NAV-GAP: Address top 10 of 68 gaps
- **#420** MUX-IMPLEMENT-NAV-GLOBAL: Global nav implementation
- **#421** MUX-IMPLEMENT-NAV-DISCOVER: Feature discovery improvements
- **#422** MUX-IMPLEMENT-DOCS-ACCESS: Document retrieval UI
- **#423** MUX-IMPLEMENT-LIFECYCLE: Object lifecycle visualization
- **#424** MUX-IMPLEMENT-COMPOST: Composting interface
- **#425** MUX-IMPLEMENT-MEMORY-SYNC: Memory sync between touchpoints
- **#426** MUX-IMPLEMENT-CONSISTENT: Consistent personality
- **#427** MUX-IMPLEMENT-CONVERSE-MODEL: Unified conversation model
- **#428** MUX-IMPLEMENT-ARIA: ARIA labels
- **#429** MUX-IMPLEMENT-CONTRAST-TESTS: Contrast testing
- **#430** MUX-IMPLEMENT-THEME-CONSISTENCY: Theme consistency

---

## 🟢 Infrastructure/Quality (18 issues)

### Testing (7)
- **#247** BUG-TEST-ASYNC: AsyncSessionFactory event loop conflicts (M1)
- **#190** TEST-QUALITY: Test Reliability for Production (M1)
- **#352** TEST-SMOKE-E2E: Core user journey smoke tests (M1)
- **#276** TEST-SMOKE-CI: Integrate smoke tests into CI (M2)
- **#273** TEST-SMOKE: Smoke test epic (M2)
- **#191** POST-TEST-E2E: Web UI End-to-End Testing (M2)
- **#167** INFR-TEST: Review regression testing gaps (M2)

### Security & Infrastructure (5)
- **#482** SEC-KMS-INTEGRATION: Migrate to AWS KMS (M1)
- **#470** EPIC: SEC-RBAC Phases 4-5 - Projects and Files (M1)
- **#371** INFRA-TIMESERIES: Time-Series Database (M2)
- **#471** EPIC: Infrastructure - OAuth, Learning, TimeSeries (M2)
- **#338** INFRA-MIGRATION-ROLLBACK: Database Migration Testing (M5)

### Process & Documentation (6)
- **#480** FLY-AUDIT: Weekly Docs Audit - Dec 8
- **#463** FLY-COORD-TREES: Git Worktrees for Multi-Agent
- **#503** FLY-AUDIT: Weekly Docs Audit - Dec 22
- **#486** BUG: test_intent_enricher_high_confidence fails
- **#146** FLY-VERIFY: Three-Tier Verification Pyramid (M5)
- **#147** FLY-VERIFY-HAND: Mandatory Handoff Protocol (M5)

---

## 🔵 M1-M6 MVP Work (28 issues)

### M1 - Foundation (2)
- **#372** CORE-LEARN-PHASE-3: Learning Infrastructure
- **#375** QA: Manual testing for preference detection

### M2 - Activation (5)
- **#242** CONV-MCP-STANDUP-INTERACTIVE: Interactive Standup
- **#309** CONV-MCP-PROTO: DocumentAnalysisSkill Prototype
- **#365** SLACK-ATTENTION-DECAY: Pattern learning for attention
- **#366** SLACK-MEMORY: Persist spatial patterns
- **#472** EPIC: Slack Integration TDD Gaps

### M3 - Skills (3)
- **#118** INFR-AGENT: Multi-Agent Coordinator Deployment
- **#312** CONV-UX-DESIGN: Unified Design System
- **#315** CONV-MCP-LIBRARY: Core Skills Library

### M4 - Document Revolution (4)
- **#302** CONV-MCP-DOCS: Unified Document Processing
- **#313** CONV-UX-DOCS: File Browser & Document Management UI
- **#314** CONV-UX-PERSIST: Conversation History & Persistence
- **#355** DOCS-STOPGAP: Basic Artifact Persistence

### M5 - Polish (10)
- **#148** FLY-VERIFY-CONFIG: Extract Configuration Layer
- **#100** CONV-FEAT-PROJ: Project Portfolio Awareness
- **#101** CONV-FEAT-TIME: Temporal Context System
- **#103** CONV-FEAT-PRIOR: Priority Calculation Engine
- **#244** CONV-UX-SLACK: Interactive Slack Standup
- **#272** RESEARCH-TOKENS-THINKING: Thinking Token Optimization
- **#441** CORE-UX-AUTH-PHASE2: Registration, Password Reset
- **#449** FLY-MAINT-CLEANUP: Archive deprecated folders
- **#465** FLY-COORD-TREES-2: Phase 3-5 Python Integration

### M6 - Future (3)
- **#106** CONV-FEAT-STRAT: Strategic Recommendations
- **#104** CONV-FEAT-ALLOC: Time Allocation Analysis
- **#241** CORE-ETHICS-TUNE: Post-Alpha Ethics Optimization

---

## ⚫ Future/Enterprise (15 issues)

### Enterprise Features (11)
- **#299** AUTH-CONCURRENT-SESSIONS: Concurrent Session Handling
- **#159** FEAT-STAND-MODEL: Sprint Model & Team Coordination
- **#87** FEAT-GRAPH: Visual knowledge graph interface
- **#65** FEAT-VISION: Visual Content Analysis Pipeline
- **#58** FEAT-DASH: Analytics Dashboard Integration
- **#57** FEAT-MEET: Transcript Analysis & Visualization
- **#66** FEAT-PREDICT: Predictive Project Analytics
- **#213** MVP-QUALITY-ENHANCE: Enterprise Infrastructure
- **#243** MVP-STAND-MODES-UI: Advanced Multi-Modal UI
- **#251** ENT-KEYS-TEAM-SHARING: Team API Key Sharing
- **#374** Enhancement: Semantic classification (post-MVP)

### Fast Follow (4)
- **#364** SLACK-MULTI-WORKSPACE: Multiple workspace support
- **#373** INFRA-OAUTH-MULTI: Multi-OAuth Installation
- **#326** ARCH-MULT-ORG: Multi-organization support
- **#327** PROCESS-AI-ACCOUNTS: Separate GitHub accounts for agents

---

## Summary by Priority

| Category | Count | Percentage |
|----------|-------|------------|
| 🔴 Alpha Critical | 4 | 3.3% |
| 🟠 Beta Enablers | 9 | 7.5% |
| 🟡 MUX Foundation | 45 | 37.5% |
| 🟢 Infrastructure | 18 | 15% |
| 🔵 MVP Work | 28 | 23.3% |
| ⚫ Future | 15 | 12.5% |
| **Total** | **119** | 99.1% |

*Note: One issue appears twice in TSV (#503) but counted once*

---

## Recommended Sequencing

### Phase 1: Alpha Polish (January Week 1-2)
- Complete 4 Alpha Critical issues
- Start Setup/Config work from Beta Enablers

### Phase 2: Conversational Foundation (January Week 3-4)
- Conversational glue implementation
- Canonical queries B1, B2, B4
- Discovery patterns

### Phase 3: MUX Sprint V1 (February Week 1-2)
- Vision formalization (6 issues)
- Pattern discovery ceremony at end

### Phase 4: MUX Sprint X1 (February Week 3-4)
- Tech implementation (5 issues)
- Beads discipline enforcement

### Parallel Tracks (Ongoing)
- Infrastructure/Testing improvements
- Pattern Sweep every 6 weeks
- Weekly doc audits
