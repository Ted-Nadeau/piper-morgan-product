# PM Ticket Numbering Guide

## Purpose
Prevent numbering conflicts between roadmap.md, backlog.md, and GitHub issues.

## Number Ranges

### PM-001 to PM-050: Core Features
- User-facing functionality
- Primary value propositions
- Feature enhancements

### PM-051 to PM-099: Infrastructure & Technical
- Technical debt
- Infrastructure improvements
- Developer tools
- Testing enhancements

### PM-100 to PM-149: Integrations
- External system integrations
- API connections
- Third-party tools

### PM-150+: Research & Experimental
- Research spikes
- Experimental features
- Future explorations

## Best Practices
1. ALWAYS check both backlog.md AND roadmap.md before assigning numbers
2. ALWAYS check GitHub issues for existing PMs
3. Use next available number in appropriate range
4. Update both docs when creating new tickets
5. Keep completed tickets' numbers permanent

## Current Allocations

### Completed (DO NOT REUSE)
- PM-001: Database Schema Initialization ✅
- PM-002: Workflow Factory Implementation ✅
- PM-003: GitHub Issue Creation Workflow ✅
- PM-004: Basic Workflow State Persistence ✅
- PM-006: Clarifying Questions System ✅
- PM-007: Knowledge Hierarchy Enhancement ✅
- PM-008: GitHub Issue Review & Improvement ✅
- PM-009: Multi-Project Context Resolution ✅
- PM-010: Comprehensive Error Handling ✅
- PM-011: Web Chat Interface ✅
- PM-014: Documentation and Test Suite Health ✅
- PM-032: Unified Response Rendering & DDD/TDD Web UI Refactor ✅

### Active/In Progress
- PM-012: GitHub Repository Integration within Projects 🔄
- PM-015: Test Infrastructure Isolation Fix 🔄
- PM-038: MCP Real Content Search Implementation 🔄

### Planned Core Features (PM-001 to PM-050)
- PM-005: Knowledge search improvements
- PM-039: Learning & Feedback Implementation
- PM-040: Advanced Knowledge Graph Implementation
- PM-041-050: Available for new core features

### Planned Infrastructure (PM-051 to PM-099)
- PM-051: Workflow optimization
- PM-052: Proactive assistance
- PM-053: Visual Content Analysis Pipeline
- PM-054: Predictive Project Analytics
- PM-055-099: Available for infrastructure

### Special Ranges
- PM-R001-R999: Research tickets (experimental)
- PM-T001-T999: Technical debt tickets

## Recent Cleanup (July 18, 2025)

### Resolved Conflicts
| Old Number | New Number | Title | Reason |
|------------|------------|-------|---------|
| PM-013 (roadmap) | PM-005 | Knowledge search improvements | Conflict with backlog PM-013 |
| PM-013 (backlog) | PM-039 | Learning & Feedback Implementation | Conflict with roadmap PM-013 |
| PM-016 (bulk ops) | PM-020 | Bulk Operations Support | Duplicate PM-016 |
| PM-018 (slack) | PM-021 | Slack/Teams Integration | Duplicate PM-018 |
| PM-018 (predictive) | PM-022 | Predictive Analytics & Insights | Duplicate PM-018 |
| PM-031 (knowledge graph) | PM-040 | Advanced Knowledge Graph Implementation | Duplicate PM-031 |
| PM-035 (test isolation) | PM-026 | Test Infrastructure Isolation Fix | Duplicate PM-035 |

## Next Available Numbers
- **Core Features**: PM-013, PM-016-037, PM-041-050
- **Infrastructure**: PM-055-099
- **Integrations**: PM-100-149
- **Research**: PM-R008+, PM-T005+

## Maintenance
This guide should be updated whenever:
- New PM numbers are assigned
- Tickets are completed
- Number ranges are adjusted
- Conflicts are discovered

_Last Updated: July 18, 2025_
