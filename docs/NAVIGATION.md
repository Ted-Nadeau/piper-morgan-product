# Internal Documentation Navigation Hub

**Purpose**: Internal development team navigation for restructured documentation
**Audience**: Agents, developers, architects, and internal contributors
**Public Documentation**: See [README.md](README.md) for pmorgan.tech public site

**Last Updated**: September 20, 2025
**Status**: ✅ **Complete Internal Navigation System** - Role-based access for development teams

---

> **Note**: This navigation serves **internal development workflows**. For public project information, getting started guides, and user documentation, visit the main [README.md](README.md) which powers the pmorgan.tech website.

---

## 🧭 Quick Navigation by Role

### 👨‍💼 Product Managers

- **[Current Planning](internal/planning/current/)** - Active planning cycles and roadmaps
- **[Issue Tracking](internal/planning/current/issues.csv)** - Current PM issue status
- **[Roadmap](internal/planning/roadmap/)** - Strategic planning and milestones
- **[Backlog Management](internal/planning/current/)** - Priority management and organization

### 🏗️ Architects

- **[Architecture Hub](internal/architecture/current/)** - Current architectural decisions
- **[Initialization Sequence](architecture/initialization-sequence.md)** - **NEW: Complete orchestration system startup flow**
- **[Domain Models](internal/architecture/current/models/)** - Hub-and-spoke model documentation
- **[ADRs](internal/architecture/current/adrs/)** - Architectural Decision Records **Note: ADR-036 pending implementation status update**
- **[Patterns](internal/architecture/current/patterns/)** - Established architectural patterns
- **[Technical Evolution](internal/architecture/evolution/)** - Architecture development history

### 👨‍💻 Developers

- **[Orchestration Setup Guide](guides/orchestration-setup-guide.md)** - **NEW: Developer-friendly setup instructions**
- **[Development Tools](internal/development/tools/)** - Setup guides and development workflows
- **[Active Work](internal/development/active/)** - Current development status
- **[Methodology](internal/development/methodology-core/)** - Development methodologies (20 core patterns)
- **[Handoffs](internal/development/handoffs/)** - Agent coordination protocols
- **[Session Templates](internal/development/tools/session-log-templates/)** - Session documentation

### 📚 Researchers & Historians

- **[Session Logs Archive](archives/session-logs/)** - Chronological development history
- **[Archaeological Index](archives/session-logs/yearly-index.md)** - Research navigation
- **[Monthly Summaries](archives/session-logs/2025/09/index.md)** - Detailed monthly insights
- **[Historical Artifacts](archives/artifacts/)** - Generated content and reports
- **[Decision Archive](archives/decisions/)** - Historical decisions and rationale
- **[Omnibus Logs](archives/session-logs/omnibus-logs/)** - Weekly/monthly consolidations

### 👥 External Users

- **[Getting Started](public/getting-started/)** - Public onboarding materials
- **[API Reference](public/api-reference/)** - Public API documentation
- **[User Guides](public/user-guides/)** - End-user documentation

---

## 📁 Documentation Architecture

### 🔓 Public Documentation (`public/`)

**External-facing content for users and developers**

- Getting started guides and tutorials
- API documentation and references
- User manuals and help content

### 🔒 Internal Documentation (`internal/`)

**Working documents for active development**

#### Development (`internal/development/`)

```
├── active/                    # Current work by status
│   ├── in-progress/          # Active development
│   ├── pending-review/       # Files needing review
│   └── ready-for-integration/ # Completed work
├── methodology-core/         # 20 development methodologies
├── tools/                    # Development tools and guides
├── handoffs/                 # Agent coordination prompts
└── planning/                 # Current planning cycles
```

#### Architecture (`internal/architecture/`)

```
├── current/                   # Active architectural decisions
│   ├── models/               # Hub-and-spoke model docs (39 models)
│   ├── adrs/                 # Current ADRs
│   ├── patterns/             # Established patterns
│   └── [core-specs]          # API, technical specifications
├── evolution/                # Architectural evolution tracking
└── decisions/                # Decision logs and rationale
```

#### Planning (`internal/planning/`)

```
├── current/                  # Active planning cycle
│   ├── data/                 # Planning data and analysis
│   ├── draft-issues/         # Issue development
│   ├── editorial/            # Content planning
│   └── integration/          # Integration planning
├── roadmap/                  # Long-term strategic planning
└── historical/               # Previous planning cycles
```

### 📦 Archives (`archives/`)

**Historical preservation and archaeological research**

#### Session Logs (`archives/session-logs/`)

```
├── 2025/                     # Chronological by year
│   ├── 05/ (May logs)
│   ├── 06/ (June logs)
│   ├── 07/ (July logs)
│   ├── 08/ (August logs)
│   └── 09/ (September logs + index.md)
├── omnibus-logs/             # 102+ weekly/monthly consolidations
└── yearly-index.md           # High-level research navigation
```

#### Artifacts & Decisions (`archives/`)

- **Artifacts**: Generated reports, PM files, historical deliverables
- **Decisions**: Completed ADRs and historical planning decisions

### 🎨 Assets (`assets/`)

**Binary files and multimedia content with size management**

```
├── images/                   # Organized by purpose
│   ├── architecture/         # System diagrams
│   ├── screenshots/          # Development captures
│   └── blog/                 # Blog content (186+ files)
├── diagrams/                 # Source and generated
│   ├── source/               # Editable formats
│   └── generated/            # PNG/SVG outputs
└── documents/                # Templates and exports
    ├── templates/            # Document boilerplates
    └── exports/              # Generated documentation
```

---

## 🔍 Finding What You Need

### By Work Type

- **Current Tasks**: `internal/development/active/`
- **Strategic Planning**: `internal/planning/current/`
- **Technical Decisions**: `internal/architecture/current/`
- **Historical Research**: `archives/session-logs/`
- **Asset Management**: `assets/` with inventory and guidelines

### By Time Period

- **Today's Work**: Check `internal/` directories for current status
- **Recent History**: `archives/session-logs/2025/09/`
- **Project History**: `archives/session-logs/yearly-index.md`
- **Decision Evolution**: `internal/architecture/evolution/`
- **Weekly Insights**: `archives/session-logs/omnibus-logs/`

### By Content Type

- **Documentation**: Start with role-based navigation above
- **Code References**: `internal/architecture/current/models/`
- **Processes**: `internal/development/methodology-core/`
- **Images/Assets**: `assets/` with inventory in README
- **Historical Deliverables**: `archives/artifacts/`

---

## 🔧 Documentation Workflow

### For Daily Work

1. **Check active status** in relevant `internal/` directory
2. **Review methodology** for process guidance
3. **Create session artifacts** in local `dev/YYYY/MM/DD/` structure
4. **Process to archives** for permanent preservation

### For Research & Investigation

1. **Start with yearly index** for time-based research
2. **Use monthly indices** for detailed period investigation
3. **Cross-reference artifacts** with session logs
4. **Follow agent collaboration** patterns and handoffs
5. **Check omnibus logs** for strategic insights

### For New Content Creation

1. **Determine audience** (public, internal, or archive)
2. **Follow asset guidelines** for binary files
3. **Update navigation** as needed for major additions
4. **Maintain cross-references** between related content

---

## 📊 Restructuring Achievement Summary

### Transformation Completed (September 20, 2025)

- **787 files surveyed** across 104 directories
- **6-phase systematic restructuring** with zero data loss
- **Session log consolidation** with archaeological optimization
- **186+ binary files organized** with size management
- **Role-based navigation** for multiple user types

### Key Organizational Improvements

- ✅ **Clear active/historical separation** across all content types
- ✅ **Session-based archaeological research** with chronological navigation
- ✅ **Asset management** with size compliance and inventory tracking
- ✅ **Multi-role navigation** supporting different user needs
- ✅ **Archaeological research enhancement** with cross-referencing

### Performance Metrics

- **Phase 1**: Foundation architecture (15 min vs 30 min planned)
- **Phase 2**: Session log consolidation (20 min vs 45 min planned)
- **Phase 3**: Development restructuring (45 min vs 60 min planned)
- **Phase 4**: Architecture optimization (20 min vs 30 min planned)
- **Phase 5**: Asset organization (25 min vs 30 min planned)
- **Phase 6**: Navigation system (15 min vs 30 min planned)
- **Total**: 2 hours 20 minutes vs 3.5 hours planned

---

## 🚀 Quick Access Links

### Most Frequently Used

- **[September 2025 Session Logs](archives/session-logs/2025/09/index.md)** - Current month activities
- **[Active Development Work](internal/development/active/)** - What's happening now
- **[Domain Models Hub](internal/architecture/current/models/models-architecture.md)** - Complete model reference
- **[Methodology Core](internal/development/methodology-core/)** - Development patterns and processes

### For New Team Members

- **[Public Getting Started](public/getting-started/)** - External onboarding
- **[Development Tools](internal/development/tools/)** - Developer setup and guides
- **[Architecture Overview](internal/architecture/current/)** - System understanding
- **[Historical Context](archives/session-logs/yearly-index.md)** - Project evolution

### For Research & Analysis

- **[Omnibus Logs](archives/session-logs/omnibus-logs/)** - Strategic insights and weekly summaries
- **[Decision Archive](archives/decisions/)** - Historical decision context
- **[Agent Coordination](internal/development/handoffs/)** - Multi-agent collaboration patterns
- **[Archaeological Index](archives/session-logs/yearly-index.md)** - Complete research navigation

---

## 🆘 Help and Support

### Navigation Issues

- **Can't find specific content?** Check role-based quick navigation above
- **Looking for historical material?** Start with `archives/session-logs/yearly-index.md`
- **Need methodology guidance?** Review `internal/development/methodology-core/`
- **Asset questions?** Check `assets/README.md` and `assets/INVENTORY.md`

### Contributing to Documentation

- **Follow organization principles** established in restructuring
- **Maintain archaeological research** capability in changes
- **Use asset guidelines** in `assets/README.md`
- **Update navigation** when adding major new sections

---

_Comprehensive navigation system established: September 20, 2025_
_Supporting role-based access to restructured documentation architecture_

**Recent Updates (September 25, 2025):**

- ✅ **NEW: Initialization Documentation** - Complete orchestration system startup flow
- ✅ **NEW: Developer Setup Guide** - Practical setup instructions with troubleshooting
- ⚠️ **ADR Status**: ADR-036 (QueryRouter) pending implementation status update after GREAT-1C completion
- ✅ **Testing Framework**: Performance and coverage enforcement documentation complete
