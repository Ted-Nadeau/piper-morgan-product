# Morning Standup Deep Restoration Roadmap

## Mission
Restore Morning Standup to daily usability by fixing CLI, connecting integrations, and enabling web GUI access.

---

## Phase 1: CLI Investigation & Repair (3-4 hours)

### 1.1 Current State Audit
```bash
# What exists now?
piper standup run --dry-run
piper standup run --verbose

# What's the output?
# - Is it hitting the right services?
# - What data is returned vs expected?
# - Error messages or silent failures?
```

### 1.2 Test Coverage Analysis
```bash
# Unit tests
pytest tests/unit/cli/test_standup.py -v

# Integration tests
pytest tests/integration/test_morning_standup.py -v

# End-to-end tests
pytest tests/e2e/test_standup_workflow.py -v
```

### 1.3 Configuration Separation
- **Piper Capability**: "Run morning check-in workflow"
- **User Config**:
  - xian's 5 specific questions
  - 6 AM timing preference
  - Project context needed

### 1.4 Gap Identification
- [ ] Missing tests?
- [ ] Hardcoded values?
- [ ] Broken integrations?
- [ ] Silent failures?

**Deliverable**: CLI that successfully completes with meaningful output

---

## Phase 2: Intelligence Trifecta Integration (4-5 hours)

### 2.1 Map Required Data Sources

**Spatial Intelligence** (Where am I?)
- Current projects
- Active contexts
- Environment state

**Temporal Intelligence** (When am I?)
- Calendar integration
- Deadlines and milestones
- Time-based priorities

**Social Intelligence** (Who am I with?)
- Team contexts
- Stakeholder needs
- Communication priorities

### 2.2 Integration Verification

```python
# Each integration should be testable
def test_spatial_intelligence_connected():
    """Verify project context loads"""

def test_temporal_intelligence_connected():
    """Verify calendar data available"""

def test_social_intelligence_connected():
    """Verify team context accessible"""
```

### 2.3 Data Population Checklist

**User-Config Data Needed**:
- [ ] GitHub projects configuration
- [ ] Google Calendar credentials/setup
- [ ] Slack workspace (if applicable)
- [ ] Project priorities/focus areas
- [ ] Team member contexts

**Canonical Questions Data Requirements**:
1. "What's your name and role?" → Profile config
2. "What day is it?" → Temporal intelligence
3. "What should I focus on?" → Spatial + priorities
4. "What am I working on?" → Project context
5. "What's my top priority?" → Integrated intelligence

### 2.4 Wire Up Connections

```python
# services/orchestration/morning_standup.py
class MorningStandupOrchestrator:
    def __init__(self, config: ConfigManager):
        self.spatial = SpatialIntelligence(config)
        self.temporal = TemporalIntelligence(config)
        self.social = SocialIntelligence(config)

    def gather_context(self):
        """Integrate all three intelligences"""
        return {
            'projects': self.spatial.get_active_projects(),
            'calendar': self.temporal.get_todays_events(),
            'team': self.social.get_team_contexts(),
            'priorities': self._synthesize_priorities()
        }
```

**Deliverable**: All data sources connected and returning real data

---

## Phase 3: Web GUI Enablement (2-3 hours)

### 3.1 Route Implementation
```python
# web/routes/canonical.py
@app.route('/standup', methods=['GET', 'POST'])
def morning_standup():
    """Web interface for morning standup"""
    if request.method == 'GET':
        # Show standup interface
        return render_template('standup.html')
    else:
        # Run standup and return results
        orchestrator = MorningStandupOrchestrator(current_user.config)
        results = orchestrator.run_standup()
        return jsonify(results)
```

### 3.2 UI Implementation
- Display canonical questions
- Show integrated responses
- Enable follow-up queries
- Maintain context

### 3.3 Web Testing
```bash
# Start web server
piper web start

# Navigate to http://localhost:8080/standup
# Test morning flow
# Verify responses meaningful
```

**Deliverable**: Working web interface for daily standup

---

## Phase 4: Canonical Query Expansion (2-3 hours)

### 4.1 Core Canonical Queries

**Your 5 Questions** (User-Config):
1. What's your name and role?
2. What day is it?
3. What should I focus on today?
4. What am I working on?
5. What's my top priority?

**Additional Canonical Patterns** (Piper Capabilities):
- "What's changed since yesterday?"
- "What deadlines are approaching?"
- "Who do I need to coordinate with?"
- "What's blocking progress?"
- "What can I complete today?"

### 4.2 Configuration Structure
```python
# config/users/xian.py
XIAN_CONFIG = {
    "standup_questions": [
        "What's your name and role?",
        "What day is it?",
        "What should I focus on today?",
        "What am I working on?",
        "What's my top priority?"
    ],
    "additional_queries": [
        "What's changed since yesterday?",
        # ... user can customize
    ]
}
```

### 4.3 Extensibility Pattern
- Users can add/remove/reorder questions
- Responses adapt to available integrations
- Graceful degradation if integration missing

---

## Phase 5: Daily Usage & Benchmarking (Ongoing)

### 5.1 Personal Daily Testing
- Run every morning at 6 AM
- Document what works/doesn't
- Note missing data or context
- Iterate on responses

### 5.2 "Playing Piper Morgan" Benchmark
- Set up test project on Claude.ai
- Run same canonical queries
- Compare responses
- Identify gaps in capability

### 5.3 Success Metrics
- [ ] Standup completes in <30 seconds
- [ ] All 5 questions answered meaningfully
- [ ] Data is current and accurate
- [ ] Responses are actionable
- [ ] Works reliably every day

---

## Implementation Sequence

### Week 1 Focus
**Monday-Tuesday**: Phase 1 (CLI Investigation)
**Wednesday-Thursday**: Phase 2 (Integration Wiring)
**Friday**: Phase 3 (Web GUI)

### Week 2 Focus
**Monday-Tuesday**: Phase 4 (Canonical Expansion)
**Wednesday-Friday**: Phase 5 (Daily usage & iteration)

---

## Technical Debt to Track

As we discover issues, log them here:
- [ ] Fetch errors in service X
- [ ] Missing integration for Y
- [ ] Hardcoded value in Z
- [ ] Test coverage gap in Q

---

## Success State

**By end of Week 2**:
- Morning Standup works perfectly every day
- All integrations connected and providing value
- Web UI polished and responsive
- Ready to replicate pattern for next workflow
- Benchmark established against Claude.ai version

---

*Roadmap Version: 1.0*
*Created: September 5, 2025*
*Purpose: Deep restoration of Morning Standup as template for all workflows*
