# Setup Wizard Completeness Audit

**Date**: October 29, 2025, 8:55 AM
**Issue**: Reactive bug-fixing instead of planned implementation
**User Insight**: "we should have known we'd need database tables"

## The Problem

We've been discovering setup requirements **reactively** through user testing:

- ❌ Port 5432 vs 5433
- ❌ Password mismatch
- ❌ Missing database tables

This is **inefficient** and creates a **poor alpha onboarding experience**.

---

## COMPLETE FIRST-TIME SETUP REQUIREMENTS

### **Phase 0: Pre-Flight** (Current: ✅ COMPLETE)

- [x] Python 3.12 available
- [x] Virtual environment creation
- [x] Dependency installation (`requirements.txt`)
- [x] SSH key setup (optional)

### **Phase 1: System Prerequisites** (Current: ⚠️ INCOMPLETE)

#### Infrastructure Services (docker-compose.yml)

- [x] **Docker Desktop** running
- [x] **PostgreSQL** (5433) - connection tested
- [ ] **Redis** (6379) - **NOT CHECKED** ❌
- [ ] **ChromaDB** (8000) - **NOT CHECKED** ❌
- [ ] **Temporal** (7233) - **NOT CHECKED** ❌
- [ ] **Traefik** (80) - **NOT CHECKED** ❌

#### Port Availability

- [x] Port 8001 (Piper web)
- [ ] Port 5433 (PostgreSQL) - **Checks connection, not port** ⚠️
- [ ] Port 6379 (Redis) - **NOT CHECKED** ❌
- [ ] Port 8000 (ChromaDB) - **NOT CHECKED** ❌
- [ ] Port 7233 (Temporal) - **NOT CHECKED** ❌
- [ ] Port 80 (Traefik) - **NOT CHECKED** ❌

#### System Checks

- [x] Python version
- [x] Docker installed
- [ ] Docker daemon running - **Implicit via postgres check** ⚠️
- [ ] Docker Compose available - **NOT CHECKED** ❌
- [ ] Sufficient disk space - **NOT CHECKED** ❌
- [ ] Sufficient memory - **NOT CHECKED** ❌

### **Phase 1.5: Database Schema** (Current: ✅ JUST ADDED)

- [x] Check if tables exist
- [x] Create tables if needed
- [ ] Run migrations (Alembic?) - **NOT CHECKED** ❌
- [ ] Seed data (if needed) - **NOT CHECKED** ❌

### **Phase 2: User Account** (Current: ✅ COMPLETE)

- [x] Username prompt
- [x] Email prompt (optional)
- [x] Create user record
- [ ] Verify user created successfully - **NOT CHECKED** ❌

### **Phase 3: API Keys** (Current: ⚠️ UNKNOWN - NOT TESTED YET)

- [ ] Prompt for LLM providers
- [ ] Validate key format
- [ ] Test key connectivity
- [ ] Store in OS keychain
- [ ] Verify keychain storage

### **Phase 4: Configuration** (Current: ❌ MISSING)

- [ ] Check for PIPER.user.md - **NOT CREATED** ❌
- [ ] Copy from PIPER.user.md.example - **NOT DONE** ❌
- [ ] Set default preferences - **NOT DONE** ❌
- [ ] Environment variables (.env) - **NOT CREATED** ❌

### **Phase 5: Service Verification** (Current: ❌ COMPLETELY MISSING)

- [ ] Start all docker services (`docker-compose up -d`)
- [ ] Wait for health checks to pass
- [ ] Verify Redis connectivity
- [ ] Verify ChromaDB connectivity
- [ ] Verify Temporal connectivity
- [ ] Verify Piper can start (`python main.py --verbose`)
- [ ] Verify web UI accessible (http://localhost:8001)

### **Phase 6: Post-Setup** (Current: ❌ COMPLETELY MISSING)

- [ ] Display setup summary
- [ ] Show next steps (how to start Piper)
- [ ] Show troubleshooting resources
- [ ] Offer to start Piper now

---

## CRITICAL MISSING PIECES

### 1. **Multi-Service Docker Check** ❌

**Impact**: HIGH - Piper won't work without Redis, ChromaDB, Temporal
**Current**: Only checks PostgreSQL
**Need**: Check all 5 services from docker-compose.yml

### 2. **Service Startup** ❌

**Impact**: HIGH - User has to manually run `docker-compose up -d`
**Current**: Only tells user in troubleshooting
**Need**: Wizard should start services automatically

### 3. **Configuration Files** ❌

**Impact**: MEDIUM - User preferences not initialized
**Current**: No PIPER.user.md created
**Need**: Copy example, prompt for key preferences

### 4. **End-to-End Verification** ❌

**Impact**: CRITICAL - Can't confirm setup actually worked
**Current**: No verification after setup
**Need**: Try to start Piper, verify services, test API key

### 5. **Environment Variables** ❌

**Impact**: LOW - .env.example exists but not copied
**Current**: Relies on docker-compose defaults
**Need**: Create .env from .env.example with user's values

---

## RECOMMENDATION: SYSTEMATIC REWRITE

**Stop reactive bug-fixing. Plan the complete wizard.**

### Proposed Structure:

```python
async def run_setup_wizard():
    """Complete first-time setup with comprehensive checks"""

    # Phase 0: Pre-Flight (DONE)
    check_python_312()
    setup_virtual_environment()
    install_dependencies()
    setup_ssh_key()

    # Phase 1: Infrastructure (NEEDS EXPANSION)
    check_docker_desktop_running()
    check_docker_compose_available()
    start_all_docker_services()  # NEW!
    wait_for_health_checks()     # NEW!
    verify_all_services()         # NEW!
    check_all_ports_available()   # NEW!

    # Phase 1.5: Database (DONE)
    create_database_tables()
    run_migrations()              # NEW!

    # Phase 2: User Account (DONE)
    create_user_account()
    verify_user_created()         # NEW!

    # Phase 3: API Keys (NEEDS TESTING)
    collect_api_keys()
    validate_and_test_keys()      # NEW!
    store_in_keychain()
    verify_keychain_storage()     # NEW!

    # Phase 4: Configuration (NEW!)
    create_piper_user_config()
    create_env_file()
    set_default_preferences()

    # Phase 5: End-to-End Verification (NEW!)
    verify_piper_can_start()
    test_web_ui_accessible()
    test_basic_api_call()

    # Phase 6: Success (NEEDS EXPANSION)
    display_setup_summary()
    show_next_steps()
    offer_to_start_piper()
```

---

## IMMEDIATE ACTION ITEMS

1. **Audit Current State**: What actually works vs. what's assumed
2. **Design Complete Flow**: All prerequisites, not just database
3. **Implement Missing Checks**: Redis, ChromaDB, Temporal, etc.
4. **Add Service Startup**: Automated `docker-compose up -d`
5. **Add E2E Verification**: Confirm setup actually succeeded
6. **Test Alpha Path**: Fresh laptop, zero context, works first time

---

## SUCCESS CRITERIA

**"A non-technical alpha tester with zero Docker/Python knowledge can:**

1. Clone the repo
2. Run `python3.12 main.py setup`
3. Answer prompts
4. **Have a working Piper Morgan instance**
5. Never see a traceback"

**Current Reality**: We're at step 2.5, failing on step 4.
