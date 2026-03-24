# Architecture Decision Records (ADRs)

## Overview

This directory contains Architecture Decision Records (ADRs) that document significant architectural decisions, their context, rationale, and consequences.

**Total ADRs**: 61 records (000-060)

## Recent ADRs

- **[ADR-060: Floor-First Routing](adr-060-floor-first-routing.md)** (Mar 2026) - Invert routing: floor handles everything, handlers prove specificity
- **[ADR-059: Workflow Dispatcher & Offer Consolidation](adr-059-workflow-dispatcher-offer-consolidation.md)** (Mar 2026) - Unified dispatch replacing per-handler workflow management
- **[ADR-058: Multi-Tenancy Isolation](adr-058-multi-tenancy-isolation.md)** (Mar 2026) - User data isolation patterns

- **[ADR-057: CommandRegistry - Unified Command Discovery](adr-057-command-registry.md)** (Jan 2026) - Central registry for command parity across interfaces (#551)
- **[ADR-056: Consciousness Expression Patterns](adr-056-consciousness-expression-patterns.md)** (Jan 2026) - Template-based personality consistency
- **[ADR-055: Object Model Implementation](adr-055-object-model-implementation.md)** (Jan 2026) - Domain model dataclass patterns
- **[ADR-054: Cross-Session Memory Architecture](adr-054-cross-session-memory-architecture.md)** (Jan 2026) - Three-layer context persistence from PDR-002
- **[ADR-053: Trust Computation Architecture](adr-053-trust-computation-architecture.md)** (Jan 2026) - Trust gradient model from PDR-002
- **[ADR-052: Tool-Based MCP Standardization](adr-052-tool-based-mcp-standardization.md)** (Oct 2025, updated Jan 2026) - MCP implementation pattern standardization
- **[ADR-051: Unified User Session Context](adr-051-unified-user-session-context.md)** (Jan 2026) - User context unification
- **[ADR-050: Conversation-as-Graph Model](adr-050-conversation-as-graph-model.md)** (Jan 2026) - Multi-party conversation modeling
- **[ADR-049: Conversational State and Hierarchical Intent](adr-049-conversational-state-hierarchical-intent.md)** (Jan 2026) - Multi-turn conversation architecture
- **[ADR-048: ServiceContainer Lifecycle Management](adr-048-service-container-lifecycle.md)** (Jan 2026) - Service container singleton pattern
- **[ADR-047: Async Event Loop Awareness](adr-047-async-event-loop-awareness.md)** (Dec 2025) - Database connection event loop handling
- **[ADR-046: Moment.type Agent Architecture](adr-046-moment-type-agent-architecture.md)** (Nov 2025) - Typed input decomposition and specialized agent routing

## ADR Categories

ADRs are organized by decision domain:
- **Platform & Integration** (MCP, Claude Code, spatial intelligence)
- **Infrastructure** (staging, monitoring, configuration)
- **Security & Auth** (JWT, authentication patterns)
- **Development Process** (testing, session management)
- **Product Strategy** (mobile, features, prioritization)

## Creating New ADRs

See [adr-000-meta-platform.md](adr-000-meta-platform.md) for the standard ADR template and decision-making framework.

## Navigation

- **[← Back to Current](../README.md)**
- **[📚 Documentation Home](../../README.md)**
- **[Pattern Index](../patterns/README.md)** - Related architectural patterns

---

**Last Updated**: March 23, 2026
**Maintained By**: Documentation Team
**Purpose**: Directory navigation and content overview
