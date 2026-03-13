# Security Operations Session Log

**Date**: January 17, 2026
**Start Time**: 5:38 AM PT
**Agent**: Security Operations (Opus)
**PM**: Xian
**Session Type**: Incident Response

---

## Incident Summary

**Alert Type**: Google Cloud Platform Project Suspension
**Project Name**: Piper Morgan
**Project ID**: `gen-lang-client-0285520798`
**Violation Category**: "Abusive activity consistent with hijacked resources"
**Required Action**: Appeal submission with investigation findings

---

## Investigation Timeline

### 5:38 AM - Alert Received
- GCP Trust & Safety notification received
- Project suspended for suspected hijacked resources
- No prior warning mentioned in alert (indicating "seriously impacting service of other users")

### 5:40 AM - Initial Assessment
- [x] Identify what services this GCP project provides → Gemini API (backup LLM provider)
- [ ] Check for unauthorized access indicators → BLOCKED (console redirects to appeal only)
- [ ] Review recent API usage patterns → BLOCKED
- [ ] Check for exposed credentials

### 5:41 AM - GCP Console Details
**Google's Assessment**: "We believe that your organization may have inadvertently published the affected Service Account credentials or API keys in public sources or websites, where a third party harvested them to initiate resources in your project."

**Console Access**: Fully locked - all navigation redirects to appeal page

### 5:48 AM - PM Responses to Investigation Questions
1. **Gemini usage**: Backup/POC only, not actively used
2. **Console access**: Locked out, cannot check API usage or IAM
3. **Other applications**: None use this project
4. **Key storage**: Apple Notes (local file, not in repo)

### 5:48 AM - Git History Audit
```bash
git log --all -p | grep -i "gemini\|AIza" | head -20
```
**Result**: ✅ NO API KEYS IN GIT HISTORY
- Only feature references to "Gemini" as a provider name
- No `AIza...` pattern (Google API key prefix) found
- Clean commit history

---

## Investigation Findings

### Project Purpose
**Confirmed**: `gen-lang-client-0285520798` is the Google Generative Language API project used for **Google Gemini** LLM integration.

- **Added**: December 8, 2025 (Issue #448: ALPHA-SETUP-CLI - Add Gemini API Key)
- **Purpose**: Alternative LLM provider option (alongside OpenAI, Anthropic)
- **Usage Pattern**: User-configured API key stored in local keyring
- **Not** required for core functionality - Claude/OpenAI are primary providers

### Prior Security Audit
- **December 4, 2025**: Shai-Hulud 2.0 comprehensive audit
- **Result**: "GCP credentials: NOT EXPOSED ✅"
- **Gap**: 6+ weeks since last audit

### Key Questions for PM
1. **Is Gemini actively used?** Or just configured as an option?
2. **When was last legitimate Gemini API call?**
3. **Any unusual GCP billing alerts?**
4. **Who else has access to your GCP project?**

### Potential Compromise Indicators to Check
- [ ] GCP Console → API usage graphs (look for spikes)
- [ ] GCP Console → IAM → Recent access events
- [ ] Local machine → Check if API key was exported anywhere
- [ ] GitHub → Verify no commits contain API key (git log --all -p | grep -i gemini)

---

## Remediation Steps

### Completed ✅

| Time | Action | Status |
|------|--------|--------|
| 6:04 | Deleted compromised Gemini API key (AI Studio) | ✅ |
| 6:10 | Appeal submitted | ✅ |
| 6:10 | Moved all API keys from Apple Notes to macOS Keychain | ✅ |
| 6:10 | Deleted notes containing keys from iCloud-synced Notes | ✅ |
| 6:10 | Git history audit - confirmed clean (no secrets) | ✅ |

### Pending (Blocked)

| Action | Blocker |
|--------|---------|
| Review GCP audit logs | Waiting for appeal approval |
| Set up GCP billing alerts | Waiting for appeal approval |

### To Do

| Action | Status |
|--------|--------|
| Install git-secrets for future protection | Next |
| Document incident in project security docs | Pending |

---

## Five Whys Analysis

| # | Why? | Answer | Intervention |
|---|------|--------|--------------|
| 1 | Why was key harvested? | Exposed in public GitHub repo for 3 months | N/A - public repo intentional |
| 2 | Why was key in repo? | Log file in `dev/` was committed | ✅ Added `dev/` to .gitignore |
| 3 | Why was key in log? | httpx logs full URLs; Gemini uses `?key=` param | ✅ URL redaction filter |
| 4 | Why was log committed? | `dev/` wasn't gitignored; git-secrets not installed yet | ✅ Fixed both |
| 5 | Why didn't we catch it? | No pre-commit scanning; no GitHub secret scanning | ✅ Both now active |

**Root cause chain**: Gemini's URL-param auth → httpx logs full URLs → log committed to tracked dir → no scanning to catch it

---

## Remediation Tracking

| Level | Issue | Fix | Status |
|-------|-------|-----|--------|
| 1 | `dev/` not gitignored | Add to `.gitignore` | ✅ Done |
| 2 | httpx logs full URLs with keys | URL redaction filter | ✅ Done (doc agent) |
| 3 | git-secrets not installed until today | Now installed with patterns | ✅ Done |
| 4 | GitHub secret scanning | Already enabled | ✅ Verified |
| 5 | Gemini uses URL param for auth | Use application-restricted keys | 🔲 Blocked (no GCP access) |

### URL Redaction Implementation (8:26 AM)
- **File**: `services/infrastructure/logging/url_redaction.py`
- **Coverage**: httpx, httpcore, urllib3, requests, aiohttp, root logger
- **Patterns**: key=, api_key=, token=, secret=, password=, access_token=, client_secret=
- **Tests**: 20/20 passing

---

## Appeal Submitted

**Time**: 6:10 AM PT (updated 9:23 AM with root cause)
**Status**: Awaiting Google response

**Key Points in Appeal**:
- Identified as backup LLM provider, not actively used
- Deleted compromised key via AI Studio
- **Root cause identified**: API key committed in log file (`dev/2025/10/16/server-startup.log`) on Oct 16, 2025
- httpx library logged full URL including `?key=` parameter
- Added `dev/` to .gitignore, deployed URL redaction filter
- Committed to preventive measures (restricted keys, billing alerts)

---

## Session Progress

| Time | Action | Result |
|------|--------|--------|
| 5:38 | Alert received | Investigation initiated |
| 5:41 | GCP Console reviewed | Locked to appeal page only |
| 5:48 | PM answered questions | Gemini backup only, key in Apple Notes |
| 5:48 | Git history audit (gemini/AIza) | Clean - no secrets (incorrect - shallow scan) |
| 6:04 | Deleted API key via AI Studio | ✅ Bleeding stopped |
| 6:10 | Appeal submitted | Awaiting response |
| 6:10 | Keys moved to Keychain | ✅ Secure storage |
| 6:10 | iCloud notes deleted | ✅ Secondary vector closed |
| 6:10 | Git audit (broader patterns) | Clean - only env var checks |
| 6:15 | Verified git-secrets installed | Already configured |
| 6:28 | `git secrets --scan-history` | **ROOT CAUSE FOUND** |
| 6:28 | Identified leak: dev/server-startup.log | Key in commit from Oct 16, 2025 |
| 8:00 | Added dev/ to .gitignore | ✅ Prevention in place |
| 8:07 | Five Whys analysis | Identified 5 intervention points |
| 8:26 | URL redaction filter deployed | ✅ Doc agent implemented |
| 8:28 | Verified GitHub secret scanning | ✅ Already enabled |
| 9:23 | Confirmed appeal updated with root cause | ✅ |
| 9:23 | Session paused | Awaiting Google response |

---

## End of Session Notes

**Incident**: GCP project suspended due to API key exposure
**Root Cause**: Gemini API key logged by httpx, committed in `dev/` directory Oct 16, 2025
**Exposure Window**: ~3 months (Oct 16, 2025 → Jan 17, 2026)

### Completed This Session
- ✅ Deleted compromised API key
- ✅ Submitted appeal (with root cause update)
- ✅ Moved all API keys from Apple Notes to macOS Keychain
- ✅ Deleted sensitive iCloud-synced notes
- ✅ Added `dev/` to .gitignore
- ✅ Deployed URL redaction filter for all HTTP client loggers
- ✅ Verified git-secrets and GitHub secret scanning are active

### Blocked Until GCP Access Restored
- 🔲 Set up GCP billing alerts ($1, $10, $50 thresholds)
- 🔲 Review audit logs for scope of unauthorized activity
- 🔲 Create new Gemini API key with application restrictions
- 🔲 Investigate header-based auth as alternative to URL params

### Lessons Learned
1. **Never commit log files** - Add log directories to .gitignore
2. **URL params are dangerous** - Use header-based auth when possible; use application-restricted keys when not
3. **Deep scans catch what grep misses** - `git secrets --scan-history` > manual grep
4. **Defense in depth works** - git-secrets + GitHub scanning + log redaction = multiple layers

**End Time**: 9:23 AM PT
**Status**: Paused - awaiting Google appeal response
**Next Actions**: Return when GCP access restored to complete blocked items

---

*Session log maintained per methodology-20-OMNIBUS-SESSION-LOGS.md*
