# Memo: Distribution Model — Architecture Perspective

**From**: Chief Architect
**To**: Chief of Staff, PPM
**Date**: February 16, 2026
**Re**: Infrastructure requirements for distribution options

---

## Summary

The MCP-native architecture gives us unusual flexibility. My recommendation: **start with desktop download, but architect for eventual hosted option**. Here's the infrastructure analysis.

---

## Infrastructure Requirements by Model

### Option A: Desktop Download

**What we need**:
- Packaged installer (Electron wrapper or native packaging)
- Auto-update mechanism
- Local database (SQLite instead of PostgreSQL)
- Self-contained MCP server
- Local API key management

**What we have**:
- ✅ FastAPI backend (portable)
- ✅ MCP server implementation
- ⚠️ PostgreSQL dependencies (needs SQLite adapter)
- ❌ Packaging/installer infrastructure
- ❌ Auto-update system

**New work required**: 3-5 weeks
- SQLite adapter for repositories (1-2 weeks)
- Electron/Tauri wrapper (1-2 weeks)
- Auto-update mechanism (1 week)
- Installation experience (overlaps with alpha docs work)

**Support burden**: Low. Users self-serve. Bugs are "their problem" until they report them. No infrastructure to maintain.

**Scaling**: Linear with downloads. No operational ceiling.

### Option B: Hosted Service

**What we need**:
- Multi-tenant PostgreSQL
- User authentication at scale
- API rate limiting
- Infrastructure monitoring
- Payment/subscription management
- GDPR/privacy compliance
- Support ticketing system

**What we have**:
- ✅ Multi-tenant architecture (ADR-058, just fixed)
- ✅ JWT authentication
- ⚠️ Rate limiting (basic)
- ⚠️ Monitoring (basic health checks)
- ❌ Payment integration
- ⚠️ Privacy compliance (unclear on hosted data)
- ❌ Support infrastructure

**New work required**: 8-12 weeks minimum
- Infrastructure hardening (2-3 weeks)
- Payment integration (2-3 weeks)
- Privacy/compliance review (2-4 weeks)
- Support systems (2-3 weeks)
- Scale testing (1-2 weeks)

**Support burden**: High. Every user issue is our issue. 24/7 availability expectations. Ted Nadeau's 14 issues × N users = unsustainable without support team.

**Scaling**: Requires ops investment. Server costs grow with users. Support costs grow faster.

### Option C: MCP-Native Protocol

**What this means**: Piper as an MCP server that users connect to from their preferred client (Claude Desktop, VS Code, etc.)

**What we need**:
- Published MCP server package (npm/pip)
- Documentation for integration
- Protocol compliance testing
- Registry listing

**What we have**:
- ✅ MCP server already works
- ✅ Tools registered properly
- ⚠️ Documentation (alpha-focused, not general)
- ❌ Published package
- ❌ Registry presence

**New work required**: 2-3 weeks
- Package publishing (1 week)
- Integration documentation (1 week)
- Protocol compliance verification (few days)

**Support burden**: Medium. Integration issues, not operational issues. Users bring their own LLM, their own client.

**Scaling**: Excellent. We publish code, not run servers.

### Option D: Hybrid

**What this means**: Desktop download with optional cloud sync for cross-device continuity.

**Infrastructure**: Desktop base + selective cloud features (memory sync, backup).

**New work required**: Desktop work + 3-4 weeks for sync infrastructure

**Complexity**: Highest. Two deployment targets. Sync conflicts. Partial offline mode.

---

## The Lightest Path to More Hands

**Shortest path**: Option C (MCP-native)

If users already have Claude Desktop or another MCP client, we're essentially a plugin. No installer complexity. No hosting burden. Ship a package, publish docs.

**Caveat**: This limits us to users who already have MCP clients. Current audience is developers, not general PMs.

**Second lightest**: Option A (Desktop download) with SQLite

Self-contained app. No operational overhead. Users handle their own environment. We handle quality.

---

## Architecture Recommendation

**Sequence**:

1. **Now (M0)**: Keep current architecture. Alpha testers run from source.

2. **Post-M0 (Q1)**: Package as desktop download with SQLite option. This is the minimum viable distribution.

3. **If demand warrants (Q2+)**: Add hosted option. Only after we understand support burden from desktop users.

**Why this order**:

- Desktop-first lets us validate product-market fit without infrastructure investment
- Desktop users generate bug reports, not support tickets
- We can always add hosted later; hard to remove it once users depend on it
- "Methodology IS the product" works for desktop too—we're distributing a way of working, packaged as software

---

## Should This Decision Wait for M0?

**My view**: No, the sprint work doesn't inform the answer.

M0 is about conversational quality, not deployment model. The same code runs in all deployment modes. What M0 *does* inform:

- **User expectations**: If M0 succeeds, users expect "colleague" quality. That's harder to support at scale.
- **Integration complexity**: M0 features (context persistence, memory) are simpler in single-user desktop than multi-tenant hosted.

If anything, M0's success makes desktop-first more attractive—fewer edge cases, simpler architecture, same experience.

---

## Questions for PPM

1. **Who is the near-term user?** If developers/technical PMs, MCP-native is viable. If general PMs, desktop download is more accessible.

2. **Is "methodology IS the product" better served by software or by SaaS?** Software can be studied, forked, adapted. SaaS is consumed.

3. **What's the revenue model?** One-time purchase, subscription, freemium? This might drive distribution choice more than infrastructure does.

---

*Ready to discuss further. This can be a slow-burn conversation—no urgency from architecture perspective.*
