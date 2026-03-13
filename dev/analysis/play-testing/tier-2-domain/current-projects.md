# Current Projects Context

## Active Projects Overview

### Project: Piper Morgan (AI PM Assistant)
**Status**: MVP Development - Phase 3 Complete
**Phase**: Conversational capabilities now operational, moving toward production readiness
**Team Size**: Solo development with AI agent coordination
**Your Role**: Product Owner / Visionary / Technical PM

**Current Sprint Focus**:
- ConversationManager implementation complete (PM-034 Phase 3)
- 100% anaphoric reference resolution achieved
- System health at 100% across all components
- Next: Production deployment and user testing

**Key Stakeholders**:
- Engineering: You + Claude Code, Cursor Agent coordination
- Early Users: PM network contacts for alpha testing
- Strategic: Building toward broader PM community adoption

**Recent Decisions**:
- Chose conversation-first architecture over command-based approach
- Prioritized Slack integration over Jira for initial release
- Built on Claude/OpenAI rather than fine-tuning custom models
- Implemented systematic verification-first development methodology
- Used multi-agent coordination for accelerated development

**Upcoming Milestones**:
- Alpha release to select PM network (target: August 2025)
- Public beta launch (target: September 2025)
- Team features and knowledge sharing (target: Q4 2025)

**Current Blockers/Risks**:
- Need real PM user testing to validate value proposition
- Market timing considerations for PM AI assistant space
- Scaling from solo development to sustainable product

---

### Project: Decision Reviews (VA.gov)
**Status**: Active Development
**Phase**: Q4 onramp questionnaire development + ongoing maintenance
**Team Size**: 9-person DRAGONS team (mix of A6, Kind, CoA contractors)
**Your Role**: Director of Product Management for Kind Systems, subcontracting to Agile6

**Current Sprint Focus**:
- Developing onramp questionnaire to help Veterans choose the right DR path
- Ongoing form maintenance as rules change and system evolves
- Planning Q4 qualitative research deep dive for overall online experience

**Key Stakeholders**:
- **A6 Team**: Pam Macalintal (Delivery Manager), Kyra Berman-Gestring (UX Lead), Lauren Dawson (UX Research/Design), Traci Tran (a11y), Cindy Lackey (Content/IA)
- **Kind Team**: Grace Xu (Eng Lead), Randi Mays (Senior FE), Jerry Sea (Mid-level Full-stack)
- **OCTO Enablement**: Amy Lai (Product Owner), Julie Strothman (Design), Cory Sohrakoff (Eng)
- **VA Leadership**: Zach Goldfine (Deputy CTO, occasional strategic check-ins)

**Q4 Goals & Success Metrics**:
1. **Onramp Tool**: Veterans know which DR option suits their situation
2. **Form Updates**: 100% of Veterans submit VA Form 10182 on Feb 2025 version
3. **Status Visibility**: DR submission statuses surface in MyVA dashboard
4. **Email Visibility**: VA employees see DR failure emails (interim solution)

**Current Metrics Baseline**:
- Path Switching Rate (PSR): 8.3%
- Form Abandonment Rate (FAR): 45.7%
- First-Attempt Success Rate (FASR): 85.7%

**Recent Decisions**:
- Prioritized onramp questionnaire over other Q4 initiatives
- Focused on Veterans' decision-making process rather than form optimization alone
- Integrated with MyVA team for status visibility approach

**Current Blockers/Risks**:
- Waiting for Amy Lai to establish broader product metrics beyond Q4 goals
- Balancing multiple stakeholder priorities (OCTO, VBA, BVA, individual Veterans)
- Dependency on other VA systems for status integration

---

### Project: One Job (Passion Project)
**Status**: Working Demo, Pre-MVP
**Phase**: Design recently updated, core functionality exists but incomplete
**Team Size**: Solo (you + LLM assistance)
**Your Role**: Product Vision + hands-on development coordination

**Project Vision**:
- One-task-at-a-time, card-stack-metaphor todo app
- Front-end for other task and project management systems
- Designed for procrastinators, overwhelmed users, daydreamers
- Benefits people who need pomodoro and time-focus approaches

**Current Capabilities**:
- Working demo with core task metaphor
- Recently updated design
- [TEMPLATE: What specific features work today?]

**Development Approach**:
- Delegating coding to LLMs while maintaining product vision
- Focus on user experience and core metaphor integrity
- Rapid prototyping enabled by AI assistance

**Piper Integration Strategy**:
- Piper to help with project planning, feature prioritization, user feedback synthesis
- Piper "speaks tasks" natively - natural fit for task management tools
- Potential for Piper to use One Job UI paradigm for surfacing next steps
- One Job could become MCP backend for Piper's task management frontend

**Target Users**:
- Procrastinators who get overwhelmed by long task lists
- People who struggle with breadth of their problems
- Users who benefit from focused, single-task approaches
- Anyone needing time-focus and attention management support

**Timeline Reality**:
- Could complete MVP in few weeks if focused
- Currently on back burner due to VA project priorities
- May take longer given current resource allocation

**Strategic Value**:
- Tests Piper's task management capabilities in real-world scenario
- Builds institutional knowledge about task manipulation and PM tools
- Potential integration point for Piper's future task management features

---

## Cross-Project Considerations

### Resource Allocation
- Time allocation: 70% Decision Reviews (VA.gov), 25% Piper Morgan, 5% One Job
- Engineering bandwidth: VA team for Decision Reviews, AI assistance for Piper/One Job
- Shared learnings: AI-assisted development patterns from Piper apply to One Job

### Strategic Priorities
1. **Decision Reviews Q4 Goals**: Meet OCTO/VA commitments, deliver onramp questionnaire
2. **Piper Morgan Production Readiness**: Complete MVP and begin alpha user testing
3. **One Job MVP**: Advance when Piper can assist with project management

### Inter-Project Dependencies
- **Decision Reviews → Piper**: Real PM scenarios from VA work become Piper test cases
- **Piper → One Job**: Piper's task management capabilities tested through One Job development
- **One Job → Piper**: One Job UI paradigm may become Piper's task surfacing approach
- **All Projects**: AI-assisted development methodology applies across all three
- **Strategic Learning**: Contractor PM role (VA) vs startup PM role (Piper/One Job) provide different PM context

---

## Project Communication Rhythms

### Decision Reviews (VA.gov)
- DRAGONS team: Regular sprint ceremonies and A6 delivery management
- OCTO Enablement: Weekly sync with Amy Lai, design collaboration with Julie Strothman
- VA Stakeholders: Quarterly strategic check-ins with Zach Goldfine
- Cross-team: Coordination with MyVA team for status integration

### Piper Morgan
- Daily standup: Morning priority setting and blocker identification
- Sprint cycles: 1-week cycles focused on single major capability
- Progress tracking: GitHub issues as source of truth, session logs for context
- AI coordination: Multi-agent handoffs and systematic verification

### One Job
- Development: As-available time slots, AI-assisted rapid prototyping
- Vision refinement: Periodic design and UX iterations
- Piper integration: Testing task management scenarios and feedback loops

### Cross-Project
- Portfolio review: Weekly assessment of resource allocation and strategic alignment
- Methodology evolution: Continuous refinement of AI-assisted development patterns
- Learning transfer: VA PM scenarios inform Piper testing, Piper capabilities enable One Job progress

---

## Historical Context (Last 90 Days)

### Major Wins
- **PM-034 Conversational Capabilities**: Achieved 100% anaphoric reference resolution at 2.33ms latency (65x faster than target)
- **Multi-Agent Coordination Excellence**: Systematic methodology enabling rapid, high-quality development
- **Infrastructure Spring Cleaning**: SQLAlchemy migration and database unification completed successfully

### Lessons Learned
- **Verification-First Methodology**: Most transformative breakthrough - checking patterns before implementation saves hours
- **Agent Specialization**: Code for systematic changes, Cursor for targeted fixes and validation
- **GitHub-First Tracking**: Issues as authoritative source prevents work duplication and ensures continuity

### Pivots or Changes
- **From Command to Conversation**: Shifted Piper from command processor to conversational assistant based on user needs
- **Excellence Flywheel Focus**: Prioritized methodology development over rapid feature addition
- **Quality over Speed**: Chose systematic development over quick prototyping, resulting in higher velocity

---

## Team Dynamics (Multi-Agent Development)

### Agent Coordination Patterns
- **Claude Code (You)**: Multi-file systematic changes, infrastructure, architectural implementation
- **Cursor Agent**: Targeted debugging, UI testing, validation, quick fixes
- **Chief Architect (Occasional)**: Strategic decisions only, no implementation
- **GitHub Issues**: Central coordination and progress tracking

### Working Rhythms
- **Session Management**: Structured handoffs between agents using session logs
- **Parallel Development**: Code and Cursor working on complementary aspects simultaneously
- **Quality Gates**: Systematic verification before any "production ready" claims
- **Context Preservation**: Institutional memory through documentation and logs

### Success Patterns
- **Verification Before Implementation**: Always check existing patterns first
- **Evidence-Based Completion**: Never claim success without test results
- **Systematic Handoffs**: Structured context transfer between sessions
- **Compound Learning**: Each success builds methodology for future acceleration

---

## Current Focus Areas

### Immediate (This Week)
- Validate PM-034 Phase 3 completion evidence
- Plan next development phase based on conversational foundation
- Begin real PM user scenario testing

### Short-term (Next Month)
- Production deployment readiness assessment
- Early user testing program design
- Kind Systems strategic roadmap development

### Long-term (Next Quarter)
- Piper Morgan public beta launch
- Team collaboration features specification
- Kind Systems MVP planning and resource allocation

---

## Communication Preferences by Context

### Development Work
- **Slack**: Daily coordination and quick questions
- **GitHub Issues**: Authoritative tracking and handoff documentation
- **Session Logs**: Context preservation and institutional memory
- **Face-to-face**: Complex architectural decisions or strategic planning

### Stakeholder Management
- **Higher-touch approach**: Prefer meetings for tough decisions
- **Groundwork laying**: Prepare stakeholders for difficult decisions in advance
- **Data-driven**: Support decisions with metrics and systematic analysis
- **Outcome-focused**: Frame discussions around goals rather than features

### Crisis Response
- **Immediate escalation**: DM for blocking issues, adapt to team communication style
- **Systematic triage**: Use severity assessment framework consistently
- **Clear communication**: Worst-case timelines with mitigation options
- **Business impact focus**: Always consider user and business implications
