# The Cathedral in Winter

*February 10-13*

By Monday, the flu had won.

I'd been fighting it since Saturday — shorter sessions, lighter work. But Monday was different. I couldn't focus. Couldn't coordinate. Could barely follow what was happening in the session logs.

So I did something I'd never done before: I let go.

[PM PLACEHOLDER: What was it like to step back? Was it hard to trust the system? Did you check in compulsively or actually rest?]

## The cathedral without the architect

Monday produced exactly one agent session — a brief Documentation run to synthesize the previous day's omnibus. I published a blog post that had been drafted earlier. Corresponded with Ted Nadeau about some GitHub questions. That was it.

Tuesday, I was still sick. But something strange happened.

The Documentation agent started a routine task: auditing ADR links to make sure all the cross-references still worked. Ted Nadeau had mentioned a broken link in passing, and this was the follow-up.

The audit found the broken links. Seven of them, across three files. Easy fixes. But then the agent noticed something else.

The dev/ directory was nearly empty.

## 2,155 files

The numbers didn't make sense at first. We expected around 2,463 files in dev/. The audit found 308.

Eighty-seven percent of the files were gone.

Session logs — the daily record of everything we'd built — had dropped from 650 to 52. Gameplans — the detailed plans that guide every implementation — were completely gone. Not a single one remained.

[PM PLACEHOLDER: What was your reaction when you saw this? Were you still foggy from the flu, or did this cut through?]

The investigation began immediately. Was this a fresh clone that hadn't pulled the files? No — git reflog showed continuous history. Had someone deleted them? The evidence pointed to something more mundane and more preventable: a destructive git command, probably `git checkout .` or `git restore .`, run sometime around February 7th or 8th.

The dev/ directory was gitignored. It held working files, not committed code. When the restore command ran, git happily overwrote everything with... nothing. The files had never been committed, so there was nothing to restore them from.

Except there was.

## Git archaeology

Git remembers everything — even files that were later gitignored. Every file that had ever been committed, even once, still existed somewhere in the repository's history. The recovery command was ugly but effective:

```bash
git log --all --full-history --diff-filter=A --name-only --format='%H' -- 'dev/*' | \
  while read hash; do git checkout $hash -- dev/ 2>/dev/null; done
```

Translation: find every commit that ever added a file to dev/, and restore that file from that commit.

The result: 2,781 files recovered. More than we'd lost, because the archaeology surfaced files from months ago that had been deleted intentionally but were now restored as a side effect.

The afternoon became a cleanup operation. Sort the recovered files. Delete the ones we didn't need. Compress the archives. Move things to their proper homes. By evening, dev/ had gone from 5.1 GB of chaos to 1.2 GB of organized structure.

The institutional memory was intact.

## The December bug

Wednesday brought a different kind of discovery.

Dominique Derosena — a colleague of Justin Maxwell's — was setting up Piper on Windows. Fresh machine, following the alpha tester instructions. She ran the setup script.

It failed immediately.

Not after a few steps. Not with a subtle error. Immediately. The script printed its opening message and then... stopped.

The bug was in the batch file structure. Helper subroutines used `exit /b` to return to the caller. But in Windows batch files, `exit /b` inside a subroutine doesn't return — it exits the entire script. The correct command is `goto :eof`.

This bug had existed since December 2025. Two months. Through Ted Nadeau's extensive Windows testing — fourteen issues filed and fixed. Through multiple releases. Through the entire alpha program.

Why hadn't Ted caught it?

[PM PLACEHOLDER: Any insight into this? Did you talk to Ted about it?]

The answer was in his issue reports. Ted's fourteen issues focused on requirements.txt conflicts, missing migrations, documentation gaps. All real problems. But nothing about the setup script failing on first run.

He must have hit the failure, shrugged, and switched to manual setup. Then filed issues about everything else he encountered. The script failure was so immediate, so total, that it didn't even register as a bug worth reporting — just an obstacle to work around.

Dominique, coming in fresh, didn't have that context. She expected the script to work. When it didn't, she reported it.

## Systematic prevention

The Windows bug led to a broader question: why wasn't this caught automatically?

The answer was uncomfortable. We had no Windows CI. Our continuous integration tested on Linux and macOS. Windows was... assumed. If a batch file was syntactically valid, we figured it would work.

By Thursday afternoon, we had:
- A fixed setup script (restructured, `goto :eof` replacing `exit /b`)
- A Windows CI workflow (runs on every change to batch files, PowerShell scripts, or requirements.txt)
- A Windows smoke test script (for alpha testers to validate their setup manually)

The gap that had hidden for two months was now systematically covered.

## What the flu revealed

I was sick for most of this week. Genuinely, frustratingly, can't-think-straight sick.

And the cathedral kept building itself.

Not autonomously — agents still needed prompts to start, guidance when stuck, decisions when options diverged. But the infrastructure we'd built over months proved itself. The omnibus logs captured what happened even when I couldn't follow along in real time. The audit protocols surfaced the file loss before it became permanent. The methodology — investigate first, fix second — led to systematic prevention rather than one-off patches.

By Friday, I was still recovering. But all eight leadership agents convened for the weekly review — Chief of Staff, Architect, CIO, CXO, PPM, HOSR, Communications Director, and the Lead Developer's notes. They synthesized seven days of work across twenty-two sessions. Their conclusion matched what I'd been feeling all week: the infrastructure held.

[PM PLACEHOLDER: Any reflection on what this week meant for the project? For your relationship with the system you're building?]

The files that nearly vanished taught me something about institutional memory. The December bug taught me something about fresh eyes. And the flu taught me something about cathedrals: the good ones don't need their architects present every day. They're built to stand.

---

*Next on Building Piper Morgan: [PLACEHOLDER - depends on what comes next chronologically]*

*Have you ever had to step back from something you were building and watch it continue without you? What did that reveal about what you'd built?*

---

## Comms Notes

**Title:** "The Cathedral in Winter"
**Dates covered:** Feb 10-13 (flu week + coda)

**Placeholders:** 4 PM input requests

**Verified facts:**
- 2,155 files missing (87% loss) ✓
- 650 → 52 session logs ✓
- 150 → 0 gameplans ✓
- 2,781 files recovered ✓
- December 2025 batch file bug ✓
- Ted's 14 issues ✓
- `exit /b` vs `goto :eof` ✓
- Recovery bash command from logs ✓
- Feb 13: 8 leadership agents, 22 sessions synthesized ✓

**Open questions:**
- Is the git archaeology section too technical? The bash command might lose non-technical readers.
- Length is ~1500 words before placeholders — appropriate for the drama level.
