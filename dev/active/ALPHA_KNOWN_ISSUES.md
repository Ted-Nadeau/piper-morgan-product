# Known Issues & Feature Status (v0.8.0)

**Version**: 0.8.0 (First Alpha Release)
**Last Updated**: October 24, 2025
**Status**: DRAFT - Pending PM Review

---

## ✅ What Works (Production Ready)

These features have been tested, completed, and are ready for alpha testing:

### Core Infrastructure
- ✅ **Interactive setup wizard** (`python main.py setup`)
  - System verification (Docker, Python, ports)
  - User account creation
  - API key validation and storage
  - Database initialization
  - Docker installation guidance (platform-specific)

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
  - JWT token generation and validation
  - Token blacklist (revocation support)
  - Secure keychain storage for API keys
  - Session management

### Security & Audit
- ✅ **Comprehensive audit logging**
  - All authentication events logged
  - API key operations logged
  - User actions tracked
  - JWT operations audited

- ✅ **API key management**
  - Multi-provider support (OpenAI, Anthropic)
  - Key validation before storage
  - Zero-downtime rotation
  - Strength validation
  - Cost tracking and usage analytics
  - Rotation reminders

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

- ✅ **Knowledge graph**
  - Node creation and updates
  - Edge management
  - Boundary-filtered queries
  - Bulk operations
  - Subgraph extraction

### Development Quality
- ✅ **Test coverage**: 100% pass rate (250+ tests)
  - Auth tests: 17/17 passing
  - Boundary tests: Working (1 pre-existing bug documented as #263)
  - Migration tests: Verified
  - Integration tests: Passing

- ✅ **CI/CD pipeline**: 13/13 workflows operational

### UX Polish (Sprint A7)
- ✅ **Quiet startup mode** (default)
  - Minimal console output
  - Use `--verbose` flag for details

- ✅ **Auto-launch browser** (#256)
  - Opens http://localhost:8001 after startup
  - Skips in CI/SSH environments
  - Disable with `--no-browser` flag

---

## ⚠️ Known Issues

### Minor Issues (Non-Blocking)

**Issue #263: Adaptive Boundaries Type Mismatch**
- **Status**: Tech debt, documented for Sprint A8+
- **Impact**: Low - affects unused adaptive_boundaries.get_adaptive_patterns() method
- **Workaround**: Content-based boundary methods work fine
- **Error**: `AttributeError: 'list' object has no attribute 'get'`
- **Location**: `services/ethics/boundary_enforcer.py:282`
- **Fix**: Change return type from List[str] to Dict[str, Any]

**[PM: Add any other known issues from testing]**

---

## 🚧 Experimental / Needs Testing

These features exist but need more alpha testing validation:

### Learning System
- **Pattern recognition**: Implemented but needs real-world usage data
- **Preference learning**: Working but needs validation with varied user styles
- **Workflow optimization**: Chain-of-Draft implemented, needs testing
- **Intelligent automation**: Safety-first system complete, needs alpha validation

### Integrations (Status TBD)
**[PM: Please review these with Chief Architect]**
- **GitHub**: Issue creation, updates, search
- **Slack**: Message sending, channel reading
- **Notion**: Page creation, search
- **Calendar**: Schedule checking, event creation

### Morning Standup
- **Status**: Handler exists, needs end-to-end testing
- **Features**: Multi-modal generation (text, Slack), reminder integration
- **Validation needed**: Real daily usage

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

| Feature Category | Status | Alpha Ready? | Notes |
|------------------|--------|--------------|-------|
| Setup Wizard | ✅ Complete | Yes | Tested in A6 |
| User Management | ✅ Complete | Yes | A7 complete |
| Authentication | ✅ Complete | Yes | JWT + blacklist |
| API Keys | ✅ Complete | Yes | Multi-provider |
| Audit Logging | ✅ Complete | Yes | Comprehensive |
| Boundary Enforcement | ✅ Complete | Yes | Ethics layer |
| Knowledge Graph | ✅ Complete | Yes | With boundaries |
| Learning System | 🚧 Experimental | Partial | Needs validation |
| Integrations | 🚧 Experimental | TBD | PM to review |
| Standup Automation | 🚧 Experimental | Partial | Needs E2E test |

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
- `ALPHA_AGREEMENT.md` - Legal terms and conditions
- `VERSION_NUMBERING.md` - Understanding version 0.8.0
- GitHub Issues: https://github.com/Codewarrior1988/piper-morgan/issues

---

**⚠️ DRAFT STATUS ⚠️**

**PM Review Needed:**
1. ☐ Verify feature completeness matrix
2. ☐ Confirm integration status (GitHub, Slack, Notion, Calendar)
3. ☐ Add any known issues from recent testing
4. ☐ Populate "Planned for Beta" section
5. ☐ Review alpha testing goals
6. ☐ Confirm GitHub URL and contact email

**Remove this section when approved.**

---

_Last Updated: October 24, 2025_
_Status: DRAFT (awaiting PM review)_
_Software Version: 0.8.0_
