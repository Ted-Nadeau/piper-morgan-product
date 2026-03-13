# dev/ Directory Structure

**Purpose**: Working directory for development artifacts, session logs, and historical records.

**Git Status**: `.gitignored` - not tracked in version control

**Important**: Files here should NOT be deleted. They have historical and forensic value.

---

## Directory Structure

```
dev/
├── YYYY/MM/DD/          # Dated working files (primary structure)
│   └── *-log.md         # Session logs from AI agents
│   └── gameplan-*.md    # Task planning documents
│   └── investigation-*.md
│   └── agent-prompt-*.md
│   └── *.png            # Screenshots
│
├── active/              # Current working files (not yet dated)
│   └── memos, drafts, working documents
│
├── archive/             # Compressed historical artifacts
│   └── *.gz             # Gzipped raw terminal transcripts
│
├── analysis/            # Analysis working directories
├── investigations/      # Investigation documents
├── alpha/               # Alpha testing artifacts
└── play-testing/        # Play testing artifacts
```

---

## Key Policies

### Session Logs
- **Never delete** - historical audit trail
- Named: `YYYY-MM-DD-HHMM-{role}-{tool}-{model}-log.md`
- Roles: lead, prog, arch, exec, research, docs, secops, audit
- Tools: code, cursor
- Models: opus, sonnet, haiku

### File Lifecycle
1. Active work goes in `dev/active/` or `dev/YYYY/MM/DD/`
2. Reference documents that should persist → move to `docs/`
3. Raw terminal transcripts → compress and keep in `archive/`
4. Junk files (.DS_Store, __pycache__, .pyc) → delete immediately

### What Goes in docs/ Instead
- Retrospective summaries (PERIOD-* docs)
- Alpha tester profiles
- Any document meant to be referenced long-term

---

## Recovery Note

On Feb 11, 2026, ~2,781 files were recovered from git history after being lost due to a `git checkout` operation after dev/ was gitignored. The recovery restored files from Aug 2025 - Jan 2026.

**Prevention**: Never run `git checkout .` or `git restore .` without understanding that gitignored files will be deleted.

---

*Last updated: February 11, 2026*
