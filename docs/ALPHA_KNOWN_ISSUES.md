# Known Issues & Feature Status (v0.8.4.1)

**Version**: 0.8.4.1
**Last Updated**: January 13, 2026
**Status**: Stable Core (Sprint B1 Complete + Bug Fixes)

---

## ✅ What Works (Production Ready)

These features have been tested, completed, and are ready for alpha testing:

### Core Infrastructure

- ✅ **Integration Health Dashboard** (New in 0.8.3)

  - Real-time health status at Settings → Integrations
  - One-click "Test" button for each integration
  - "Test All" button for comprehensive health check
  - Visual status indicators (healthy, degraded, failed, not configured)
  - Error messages with fix suggestions

- ✅ **OAuth Connection Management** (New in 0.8.3)

  - Connect/disconnect Slack directly from Settings UI
  - Connect/disconnect Google Calendar from Settings UI
  - OAuth 2.0 with PKCE and state tokens (CSRF protection)
  - Refresh tokens stored in secure keychain
  - No more editing environment variables for integrations

- ✅ **GUI Setup Wizard** (Enhanced in 0.8.3)

  - Visual web interface at http://localhost:8001/setup
  - System health checks with visual indicators (Docker, Python, ports, database)
  - API key configuration via web form (much easier than CLI)
  - User account creation with real-time validation
  - Support for OpenAI, Anthropic, Google Gemini, and **Notion** (new)
  - Alternative CLI wizard still available: `python main.py setup`

- ✅ **Interactive Standup Assistant** (New in 0.8.3.2)

  - Conversational standup creation via chat ("let's write a standup")
  - 7-state conversation flow (INITIATED → COMPLETE/ABANDONED)
  - Preference gathering and learning within conversation
  - Iterative refinement until satisfied
  - Version history for standup drafts
  - Performance monitoring: P95 < 500ms response times
  - Memory optimization: Turn history limited to prevent unbounded growth
  - Epic #242: CONV-MCP-STANDUP-INTERACTIVE complete (Issues #552-#556)

- ✅ **Integration Settings** (New in 0.8.4)

  - Configure all integration credentials from Settings → Integrations
  - OAuth Connect for Slack and Google Calendar
  - Personal Access Token configuration for GitHub (with keychain fallback)
  - API Key configuration for Notion (with keychain fallback)
  - Preferences panels for Calendar sync, Notion workspace, GitHub repos
  - "Disconnect All" button for bulk management
  - Epic #543 complete (Issues #544, #571-#579)

- ✅ **Portfolio Onboarding** (New in 0.8.4)

  - Conversational project setup for new users
  - Triggered on first greeting ("Hello!")
  - Multi-turn flow: INITIATED → GATHERING_PROJECTS → CONFIRMING → COMPLETE
  - Natural language project extraction
  - Creates Project entities in database for future context
  - Issue #490: FTUX-PORTFOLIO complete

- ✅ **Quality Validation** (Enhanced in 0.8.4)

  - 2100+ automated tests (major expansion in v0.8.4)
  - CI/CD quality gates with GitHub Actions
  - 100% pass rate on critical path tests
  - UI stability improvements across navigation and forms

- ✅ **System health checker** (`python main.py status`)

  - Database connection status
  - API key validation
  - Performance metrics
  - User detection (#255)
  - Recommendations

- ✅ **Preference system** (`python main.py preferences`)
  - 5-dimension questionnaire (communication, work, decision, learning, feedback)
  - Stores in alpha_users.preferences (JSONB)
  - Personalizes Piper's behavior

### User Management

- ✅ **Multi-user support**

  - Separate alpha_users table (21 columns, 9 indexes)
  - User migration tool (`python main.py migrate-user`)
  - Role-based access control (superuser, user)
  - Clean alpha/production separation

- ✅ **Authentication**
  - Password setup via interactive wizard (bcrypt, 12 rounds)
  - JWT token generation and validation
  - Token blacklist with CASCADE delete (Issue #291)
  - Secure keychain storage for API keys
  - Session management
  - Login/logout flow

### Security & Audit

- ✅ **Comprehensive audit logging**

  - All authentication events logged
  - API key operations logged
  - User actions tracked
  - JWT operations audited

- ✅ **API key management**

  - Multi-provider support (OpenAI, Anthropic, Google Gemini)
  - Key validation before storage
  - Zero-downtime rotation
  - Strength validation
  - Cost tracking and usage analytics
  - Rotation reminders
  - Secure keychain storage (API keys never stored in plain text)

- ⚠️ **Data Encryption Status** (Important Security Note)
  - **API keys**: Encrypted in system keychain ✅
  - **Passwords**: Bcrypt-hashed (12 rounds) ✅
  - **Data at rest**: NOT yet fully encrypted ❌
  - **Recommendation**: Use test data only, no sensitive information
  - **Planned**: Full encryption at rest for beta (0.9.0)

- ✅ **Boundary enforcement (ethics layer)**
  - Content-based harassment checking
  - Inappropriate content filtering
  - Boundary violation prevention
  - Knowledge graph protection

### Database & Persistence

- ✅ **PostgreSQL database** (via Docker)

  - Alembic migrations working
  - SSL/TLS support
  - Connection pooling
  - Health checks
  - Performance tests passing

- ✅ **UUID-based user IDs** (Issue #262)

  - Native PostgreSQL UUID type
  - Optimized indexing and foreign keys
  - 1.70ms lookup performance
  - Migration complete (Nov 10, 2025)

- ✅ **Referential integrity** (Issue #291)

  - Token blacklist CASCADE delete
  - Foreign key constraints enforced
  - Orphaned token prevention
  - Migration complete (Nov 10, 2025)

- ✅ **Knowledge graph**
  - Node creation and updates
  - Edge management
  - Boundary-filtered queries
  - Bulk operations
  - Subgraph extraction

### File Operations

- ✅ **File upload** (via web interface)

  - Supported formats: PDF, DOCX, TXT, MD, JSON
  - Max size: 10MB
  - Security: MIME type validation, size limits
  - User-isolated storage
  - Authentication required

- ✅ **Document processing**
  - AI-powered analysis and summarization
  - Content extraction
  - Integration with LLM providers
  - Database metadata tracking

### Development Quality

- ✅ **Test coverage**: 100% pass rate (2100+ tests)

  - Auth tests: 17/17 passing
  - UUID migration tests: Verified
  - Token blacklist FK tests: Verified
  - Integration tests: Passing
  - Standup tests: 260 tests (conversation, learning, performance)

- ✅ **CI/CD pipeline**: 13/13 workflows operational

### UX Polish (Sprint A7)

- ✅ **Quiet startup mode** (default)

  - Minimal console output
  - Use `--verbose` flag for details

- ✅ **Auto-launch browser** (#256)
  - Opens http://localhost:8001 after startup
  - Skips in CI/SSH environments
  - Disable with `--no-browser` flag

### User Interface (Nov 22-23, 2025)

- ✅ **Lists Management** (/lists)
  - Create, view, edit, delete lists
  - Share with other users (Viewer/Editor/Admin roles)
  - Permission-aware UI with role badges
  - Breadcrumb navigation
  - Issue #379-6: Create button fixed (was commented out, now working)

- ✅ **Todos Management** (/todos)
  - Same functionality as Lists
  - Separate organization for tasks
  - Issue #379-7: Create button fixed (pattern reused from Lists)

- ✅ **Projects Management** (/projects)
  - Same functionality as Lists/Todos
  - For larger work items

- ✅ **Files Management** (/files)
  - Upload files (PDF, DOCX, TXT, MD, JSON - max 10MB)
  - Download files
  - Delete files
  - Owner-based access control
  - Issue #379-8: UI built Nov 23 (backend was ready)

- ✅ **Permission System**
  - Share resources with specific users
  - Role-based access (Viewer, Editor, Admin, Owner)
  - Conversational permission commands ("share my list with alex@example.com as editor")
  - Visual permission badges in UI
  - Permission helper functions (canEdit, canDelete, canShare, isOwner)

- ✅ **Authentication UI**
  - User menu in navigation header
  - Logout functionality (Issue #379-14: endpoint path corrected)
  - Token revocation on logout
  - Multi-user testing enabled

- ✅ **Interactive Standup Assistant** (Enhanced in 0.8.3.2)
  - Conversational standup creation ("let's write a standup" or "/standup")
  - 7-state conversation flow with preference gathering
  - Iterative refinement and version history
  - P95 response time: 0.03ms (target: <500ms)
  - Epic #242: CONV-MCP-STANDUP-INTERACTIVE complete

- ✅ **Quick Standup Generation** (Legacy)
  - Generate daily standup reports via button
  - 2-3 second completion time
  - AI-powered summaries
  - Issue #379-4: Proxy endpoint fixed

- ✅ **Navigation Polish** (Issue #379 - 14 fixes total)
  - Breadcrumb navigation on all pages (Home › Lists, etc.)
  - Normalized titles (removed "My" prefix from Lists/Todos)
  - Settings pages on unified grid
  - Integrations placeholder page (no more 404 errors)
  - Privacy & Data settings with clear messaging
  - Learning dashboard cosmetic polish
  - Home page help shortcut

### Security & Access Control (Nov 21-23, 2025)

- ✅ **SEC-RBAC Phase 1 Complete** (Issue #357)
  - owner_id validation on 9 resource tables (Files, Lists, Todos, Projects, KnowledgeGraph, etc.)
  - shared_with JSONB arrays for permission grants
  - Admin bypass pattern (owner_id checks skip for is_admin users)
  - All CRUD repositories RBAC-aware
  - Migration: 5 Alembic migrations (add columns, backfill owner_id, add shared_with)
  - 22/22 integration tests passing
  - ADR-044: Lightweight RBAC architecture approved

---

## 🗣️ Chat Capabilities (Canonical Query Status)

**Reference**: [Canonical Query Test Matrix](internal/testing/canonical-query-test-matrix.md)
**Last Verified**: December 24, 2025 (240 unit tests passing)

Piper understands 25 canonical queries across 5 categories. Here's what actually works:

### Summary: 19/25 PASS (76%), 1 PARTIAL, 5 NOT IMPL

| Category | Status | Coverage |
|----------|--------|----------|
| Identity (1-5) | ✅ **100%** | 5/5 PASS |
| Temporal (6-10) | ✅ **100%** | 5/5 PASS |
| Spatial (11-15) | ✅ 80% | 4/5 PASS, 1 NOT IMPL |
| Capability (16-20) | ✅ **100%** | 5/5 PASS |
| Predictive (21-25) | ⚠️ 20% | 1 PARTIAL, 4 NOT IMPL |

### What Works in Chat (19 queries)

**Identity Queries** (all 5 work):
| Query | Example | Status |
|-------|---------|--------|
| Name/role | "What's your name?" | ✅ Works |
| Capabilities | "What can you do?" | ✅ Dynamic list from PluginRegistry |
| Health check | "Are you working properly?" | ✅ Checks database + integrations |
| Help/onboarding | "How do I get help?" | ✅ Returns resources + examples |
| Differentiation | "What makes you different?" | ✅ Unique features + positioning |

**Temporal Queries** (all 5 work):
| Query | Example | Status |
|-------|---------|--------|
| Date/time | "What day is it?" | ✅ With calendar context |
| Retrospective | "What did we accomplish yesterday?" | ✅ Completed todos from yesterday |
| Agenda | "What's on the agenda today?" | ✅ Calendar + todos + priorities |
| Last activity | "When did we last work on this?" | ✅ GitHub activity lookup |
| Duration | "How long have we been working on this?" | ✅ Project duration calculation |

**Spatial Queries** (4 of 5 work):
| Query | Example | Status |
|-------|---------|--------|
| Project list | "What projects are we working on?" | ✅ With GitHub metadata |
| Landscape | "Show me the project landscape" | ✅ Health status grouping |
| Priority | "Which project should I focus on?" | ✅ Smart recommendations |
| Project status | "What's the status of [project]?" | ✅ Detailed with issues |
| Lifecycle | "Where are we in the project lifecycle?" | ❌ Not implemented |

**Capability Queries** (all 5 work):
| Query | Example | Status |
|-------|---------|--------|
| GitHub issues | "Create a GitHub issue about X" | ✅ Uses defaults from PIPER.md |
| Project list | "List all my projects" | ✅ Routes to spatial handler |
| Status report | "Give me a status report" | ✅ Aggregated health + todos |
| Document analysis | "Analyze this document" | ✅ Via Notion (Issue #515) |
| Document search | "Search for X in our documents" | ✅ Via Notion (Issue #516) |

### What's Partially Implemented (1 query)

| Query | Example | Current Behavior |
|-------|---------|------------------|
| Focus guidance | "What should I focus on today?" | Returns time-based advice (no calendar integration yet) |

### What's Not Yet Implemented (5 queries)

These return a graceful fallback message (no errors):

| Query | Example | Reason |
|-------|---------|--------|
| Lifecycle detection | "Where are we in the project lifecycle?" | Needs workflow state tracking (may remove from canonical list) |
| Pattern recognition | "What patterns do you see?" | Future v1.1 feature |
| Risk analysis | "What risks should I be aware of?" | Future v1.1 feature |
| Opportunity detection | "What opportunities should I pursue?" | Future v1.1 feature |
| Milestone tracking | "What's the next milestone?" | Future v1.1 feature |

**For detailed testing**: See [Canonical Query Test Matrix](internal/testing/canonical-query-test-matrix.md)

**Related Issues** (all resolved Dec 21-24, 2025):
- #499 - Agenda aggregation ✅
- #500 - Project-specific status ✅
- #501 - Historical retrospective ✅
- #504-#511 - Various temporal/spatial queries ✅
- #513 - Status report generator ✅
- #515 - Document analysis via Notion ✅ (Dec 24)
- #516 - Document search via Notion ✅ (Dec 24)

---

## ⚠️ Known Issues

### Minor Issues (Non-Blocking)

**Cosmetic Issues** (Low Priority):
- Settings/Personality page: Minor layout inconsistencies (Issue #379-11 fixed)
- Some pages had missing breadcrumbs (Issue #379 - all fixed)

**Features with Placeholder Pages**:
- ⏸️ **Advanced Privacy Controls**: Basic privacy working (owner_id, shared_with), granular controls planned for beta
- ⏸️ **GitHub OAuth**: GitHub integration uses PAT tokens; OAuth connect flow planned for 0.8.4

**All P0/P1 issues resolved** as of November 23, 2025:
- ✅ Issue #262: UUID Migration - Complete
- ✅ Issue #291: Token Blacklist FK - Complete
- ✅ Issue #263: Response Humanization - Complete
- ✅ Issue #297: Password Setup in Wizard - Complete
- ✅ Issue #376: Frontend RBAC Awareness - Complete (Nov 22)
- ✅ Issue #379: UI Quick Fixes - Complete (14 issues fixed, Nov 23)
- ✅ Issue #357: SEC-RBAC Phase 1 - Complete (Nov 21)

**Note**: This is alpha software. New issues may be discovered during testing.

---

## 🚧 Experimental / Needs Testing

These features exist but need more alpha testing validation:

### Learning System

- **Pattern recognition**: Implemented but needs real-world usage data
- **Preference learning**: Working but needs validation with varied user styles
- **Workflow optimization**: Chain-of-Draft implemented, needs testing
- **Intelligent automation**: Safety-first system complete, needs alpha validation

### Integrations (Updated in 0.8.3)

**Now with OAuth and Health Dashboard!**

- ✅ **Slack**: OAuth connect from Settings UI, message sending, channel reading
- ✅ **Google Calendar**: OAuth connect from Settings UI, schedule checking, event creation
- ✅ **Notion**: API key in setup wizard, page creation, search
- ✅ **GitHub**: PAT token configuration, issue creation, updates, search
- ✅ **Health Dashboard**: Real-time status monitoring for all integrations

### Interactive Standup Assistant (New in 0.8.3.2)

- **Status**: ✅ Complete (Epic #242 closed Jan 8, 2026)
- **Features**:
  - Conversational standup creation via chat
  - 7-state conversation flow with state machine validation
  - Preference gathering and learning integration
  - Iterative refinement with version history
  - Performance monitoring with structured logging
- **Performance**: P95 0.03ms response time (target: <500ms)
- **Test Coverage**: 260 standup tests passing
- **Validation needed**: Real daily usage with alpha testers

---

## 📋 Planned for Beta (0.9.0)

Features not yet implemented or incomplete:

**[PM: Please populate based on roadmap]**

### High Priority

- [ ] **[TBD]**: Specify beta priorities

### Medium Priority

- [ ] **[TBD]**: Additional planned features

### Nice to Have

- [ ] **[TBD]**: Future enhancements

---

## 🐛 How to Report Issues

### If You Find a Bug

1. **Check this list first** - Is it already known?
2. **Gather context**:
   ```bash
   python main.py status > status.txt
   ```
3. **Create detailed report**:
   ```
   WHAT I TRIED: [specific action]
   WHAT EXPECTED: [expected result]
   WHAT HAPPENED: [actual result]
   ERROR MESSAGE: [if any]
   SYSTEM STATUS: [attach status.txt]
   ```

### Reporting Channels

- **GitHub Issues**: For bugs and feature requests
- **Email**: christian@[domain] for private issues
- **Weekly Check-in**: Discuss during scheduled calls

---

## 📊 Feature Completeness Matrix

| Feature Category     | Status          | Alpha Ready? | Notes                    |
| -------------------- | --------------- | ------------ | ------------------------ |
| Setup Wizard         | ✅ Complete     | Yes          | With Notion support (0.8.3) |
| Integration Dashboard| ✅ Complete     | Yes          | Health status + testing (0.8.3) |
| OAuth Connections    | ✅ Complete     | Yes          | Slack + Calendar (0.8.3) |
| User Management      | ✅ Complete     | Yes          | UUID-based IDs (#262)    |
| Authentication       | ✅ Complete     | Yes          | JWT + bcrypt + blacklist |
| Password Security    | ✅ Complete     | Yes          | Bcrypt 12 rounds (#297)  |
| API Keys             | ✅ Complete     | Yes          | Multi-provider           |
| File Upload          | ✅ Complete     | Yes          | 10MB, 5 formats          |
| Document Processing  | ✅ Complete     | Yes          | LLM-powered analysis     |
| Audit Logging        | ✅ Complete     | Yes          | Comprehensive            |
| Boundary Enforcement | ✅ Complete     | Yes          | Ethics layer             |
| Knowledge Graph      | ✅ Complete     | Yes          | With boundaries          |
| Learning System      | 🚧 Experimental | Partial      | Needs validation         |
| Integrations         | ✅ Complete     | Yes          | OAuth + health dashboard (0.8.3) |
| Interactive Standup  | ✅ Complete     | Yes          | Epic #242 complete (0.8.3.2) |
| Lists Management     | ✅ Complete     | Yes          | CRUD + sharing (Issue #376) |
| Todos Management     | ✅ Complete     | Yes          | CRUD + sharing (Issue #376) |
| Projects Management  | ✅ Complete     | Yes          | CRUD + sharing (Issue #376) |
| Files Management     | ✅ Complete     | Yes          | Upload/download/delete (Issue #379) |
| Permission System    | ✅ Complete     | Yes          | RBAC + sharing + conversational |
| SEC-RBAC             | ✅ Complete     | Yes          | Phase 1 owner_id validation |
| Logout Functionality | ✅ Complete     | Yes          | Issue #379-14 fixed      |
| Navigation Polish    | ✅ Complete     | Yes          | 14 QA issues fixed       |

---

## 🎯 Alpha Testing Goals

What we're specifically trying to validate:

1. **Setup Experience**: Is the wizard intuitive? Any confusing steps?
2. **Preference System**: Do the 5 dimensions make sense? Any missing?
3. **Daily Usage**: What workflows feel natural? What's clunky?
4. **Performance**: Is it fast enough? Any lag or delays?
5. **Reliability**: Does it crash? Lose data? Behave unpredictably?
6. **Value**: Does it actually help with PM work? Or just overhead?

---

## 📝 Notes for Alpha Testers

**What to Focus On:**

- Setup experience (did wizard work smoothly?)
- Preference configuration (did it personalize effectively?)
- Core workflows (task management, document handling)
- Integration points (if you use GitHub/Slack/Notion)
- Overall "feel" (is it delightful or frustrating?)

**What to Ignore:**

- UI polish (we know it's rough)
- Missing features (see "Planned for Beta")
- One-off quirks (unless they're blocking)

**What to Report:**

- Blockers (can't use at all)
- Frequent annoyances (happens repeatedly)
- Delightful surprises (what worked great!)
- Missing expectations (thought it would do X, doesn't)

---

## 🔄 Update Frequency

This document will be updated:

- **Weekly** during active alpha testing
- **After each alpha release** (0.8.1, 0.8.2, etc.)
- **As issues are discovered** and fixed

---

## See Also

- `ALPHA_TESTING_GUIDE.md` - Setup and usage instructions
- `ALPHA_AGREEMENT_v2.md` - Legal terms and conditions
- `ALPHA_QUICKSTART.md` - Quick 2-5 minute setup guide
- `VERSION_NUMBERING.md` - Understanding version 0.8.4
- `RELEASE-NOTES-v0.8.4.md` - What changed in this release
- GitHub Issues: https://github.com/mediajunkie/piper-morgan-product/issues

---

_Last Updated: January 8, 2026_
_Status: Stable core (setup, login, chat, interactive standup ready - 76% canonical query coverage)_
_Software Version: 0.8.4_
