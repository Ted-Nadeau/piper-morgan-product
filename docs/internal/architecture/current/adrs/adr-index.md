# Architectural Decision Records (ADR) Index

**Last Updated**: November 4, 2025
**Total ADRs**: 43
**Status**: Active

## Overview

This index provides a complete catalog of all Architectural Decision Records (ADRs) in the Piper Morgan system. ADRs document important architectural decisions, their context, rationale, and consequences.

## ADR Catalog

### Foundation & Core Platform

- [ADR-000: Meta-Platform](adr-000-meta-platform.md) - Core platform architecture foundation

### Integration & Communication

- [ADR-001: MCP Integration](adr-001-mcp-integration.md) - Model Control Protocol integration
- [ADR-002: Claude Code Integration](adr-002-claude-code-integration.md) - Claude Code agent integration
- [ADR-013: MCP + Spatial Intelligence Integration Pattern](adr-013-mcp-spatial-integration-pattern.md) - Spatial intelligence integration

### Service Enhancement & Features

- [ADR-003: Intent Classifier Enhancement](adr-003-intent-classifier-enhancement.md) - Intent classification improvements
- [ADR-004: Action Humanizer Integration](adr-004-action-humanizer-integration.md) - Human-readable action formatting
- [ADR-014: Attribution First](adr-014-attribution-first.md) - Attribution-based architecture
- [ADR-015: Wild Claim](adr-015-wild-claim.md) - Wild claim handling approach
- [ADR-016: Ambiguity Driven](adr-016-ambiguity-driven.md) - Ambiguity-driven design decisions

### Data & Repository Management

- [ADR-005: Eliminate Dual Repository Implementations](adr-005-eliminate-dual-repository-implementations.md) - Repository pattern standardization
- [ADR-006: Standardize Async Session Management](adr-006-standardize-async-session-management.md) - Session management patterns
- [ADR-025: Unified Session Management Architecture](adr-025-unified-session-management.md) - Comprehensive session management

### Infrastructure & Operations

- [ADR-007: Staging Environment Architecture](adr-007-staging-environment-architecture.md) - Staging environment design
- [ADR-008: MCP Connection Pooling Production](adr-008-mcp-connection-pooling-production.md) - Connection pooling strategy
- [ADR-009: Health Monitoring System](adr-009-health-monitoring-system.md) - System health monitoring
- [ADR-010: Configuration Patterns](adr-010-configuration-patterns.md) - Configuration management
- [ADR-012: Protocol Ready JWT Authentication](adr-012-protocol-ready-jwt-authentication.md) - Authentication architecture
- [ADR-027: Configuration Architecture: User vs. System Separation](adr-027-configuration-architecture-user-vs-system-separation.md) - Configuration architecture (may partly supersede ADR-010?)
- [ADR-040: Local Database Per Environment](adr-040-local-database-per-environment.md) - CODE ≠ DATA architecture (git-managed code, PostgreSQL per environment data)

### Testing & Quality Assurance

- [ADR-011: Test Infrastructure Hanging Fixes](adr-011-test-infrastructure-hanging-fixes.md) - Test infrastructure reliability
- [ADR-023: Test Infrastructure Activation](adr-023-test-infrastructure-activation.md) - Test activation patterns

### Spatial Intelligence & Advanced Features

- [ADR-013: MCP + Spatial Intelligence Integration Pattern](adr-013-mcp-spatial-integration-pattern.md) - Spatial intelligence integration
- [ADR-017: Spatial MCP](adr-017-spatial-mcp.md) - Spatial MCP implementation
- [ADR-018: Server Functionality](adr-018-server-functionality.md) - Server capability architecture
- [ADR-019: Orchestration Commitment](adr-019-orchestration-commitment.md) - Orchestration strategy
- [ADR-020: Protocol Investment](adr-020-protocol-investment.md) - Protocol investment decisions
- [ADR-021: Multi Federation](adr-021-multi-federation.md) - Multi-federation architecture
- [ADR-038: Spatial Intelligence Architecture Patterns](adr-038-spatial-intelligence-patterns.md) - Two validated spatial patterns (Granular Adapter, Embedded Intelligence)

### Experimentation & Innovation

- [ADR-022: Autonomy Experimentation](adr-022-autonomy-experimentation.md) - Autonomous system experiments
- [ADR-024: Persistent Context Architecture](adr-024-persistent-context-architecture.md) - Context persistence design

### External Integrations

- [ADR-026: Notion Client Migration](adr-026-notion-client-migration.md) - Migration to official Notion client library

### Methodological Architecture

- [ADR-028: Three-Tier Verification Pyramid\(adr-028-verification-pyramid.md)\
- Foundational framework for all agent coordination, requiring systematic evidence at each level before proceeding

## ADR Status Summary

- **Total**: 43 ADRs
- **Accepted**: 43 ADRs (all current ADRs are accepted/implemented)
- **Superseded**: 0 ADRs
- **Deprecated**: 0 ADRs

## ADR Guidelines

### Creating New ADRs

1. Use next sequential number (next: ADR-041)
2. Follow naming convention: `adr-XXX-descriptive-title.md`
3. Include required sections: Status, Date, Context, Decision, Consequences
4. Update this index when adding new ADRs

### ADR Lifecycle

- **Proposed**: Initial draft, under review
- **Accepted**: Decision approved and implemented
- **Superseded**: Replaced by newer ADR
- **Deprecated**: No longer applicable

## Recent Changes

- **November 4, 2025**: Added ADR-040 (Local Database Per Environment) - CODE ≠ DATA architecture for Sprint A8 P0 blockers - Total now 43 ADRs
- **October 13, 2025**: Updated index with ADR-037, ADR-038, ADR-039 (PROOF-8 audit) - Total was 42 ADRs
- **October 7, 2025**: Added ADR-039 (Canonical Handler Fast-Path Pattern) - Dual-path intent architecture from GREAT-4
- **October 2-4, 2025**: Updated ADR-034 (Plugin Architecture) with implementation verification (GREAT-3)
- **September 30, 2025**: Added ADR-038 (Spatial Intelligence Architecture Patterns) - Three validated spatial patterns from GREAT-2
- **September 22, 2025**: Added ADR-037 (Test-Driven Locking Strategy) and ADR-036 (QueryRouter Resurrection) from GREAT-1

## Related Documentation

- [Architecture Overview](../architecture.md)
- [Domain Models Index](../domain-models-index.md)
- [Pattern Catalog](../pattern-catalog.md)
- [Technical Specifications](../technical-spec.md)
- [ADR-029: Domain Service Mediation Architecture](adr-029-domain-service-mediation-architecture.md) - Complete domain service mediation for external system access
- [ADR-030: Configuration Service Centralization](adr-030-configuration-service-centralization.md) - Centralized configuration management through PortConfigurationService
- [ADR-031: MVP Redefinition](adr-031-mvp-redefinition.md) - Core vs Feature MVP distinction for strategic development
- [ADR-032: Intent Classification Universal Entry](adr-032-intent-classification-universal-entry.md) - Intent classification as universal conversation entry point
- [ADR-033: Multi-Agent Deployment](adr-033-multi-agent-deployment.md) - Multi-agent coordination scripts deployment strategy
- [ADR-034: Plugin Architecture](adr-034-plugin-architecture.md) - Extensible plugin architecture for PM tool integration
- [ADR-035: Inchworm Protocol](adr-035-inchworm-protocol.md) - Sequential execution methodology
- [ADR-036: QueryRouter Resurrection Strategy](adr-036-queryrouter-resurrection.md) - Complete and reenable QueryRouter
- [ADR-037: Test-Driven Locking Strategy](adr-037-test-driven-locking.md) - Lock critical infrastructure with tests
- [ADR-038: Spatial Intelligence Architecture Patterns](adr-038-spatial-intelligence-patterns.md) - Three validated spatial patterns (Granular, Embedded, Delegated MCP)
- [ADR-039: Canonical Handler Fast-Path Pattern](adr-039-canonical-handler-pattern.md) - Dual-path architecture for intent classification
- [ADR-040: Local Database Per Environment](adr-040-local-database-per-environment.md) - CODE ≠ DATA architecture (git-managed code, PostgreSQL per environment data)
