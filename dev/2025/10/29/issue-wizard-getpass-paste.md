# Issue: Setup Wizard getpass() Doesn't Support Paste

**Date**: October 29, 2025, 5:29 PM
**Discovered By**: User during alpha onboarding testing
**Severity**: Medium - UX friction during setup
**Status**: Temporary workaround implemented

---

## Problem

The setup wizard uses Python's `getpass()` function to securely collect API keys. However, `getpass()` reads input character-by-character and **does not support paste** in most terminal environments.

**User Impact**:
- Cannot paste 51-character OpenAI API keys (sk-proj-...)
- Must manually type long random strings
- Significantly increases setup time and error rate
- Poor first impression for alpha testers

**Error Message**:
```
   ✗ OpenAI key is required
```
(When user tries to paste but nothing appears)

---

## Root Cause

```python
# scripts/setup_wizard.py, line 586
openai_key = getpass("   Enter key (sk-...): ")
```

`getpass()` behavior:
- **Purpose**: Security - hides input from screen
- **Side Effect**: Disables terminal paste in most environments
- **Workaround**: Some terminals support Shift+Insert, but not Cmd+V

---

## Temporary Solution (Implemented 5:30 PM)

Added environment variable support:

```python
# Check for environment variable first
openai_key = os.environ.get("OPENAI_API_KEY")
if openai_key:
    print("   ℹ️  Using OPENAI_API_KEY from environment")
else:
    openai_key = getpass("   Enter key (sk-...): ")
```

**Usage**:
```bash
export OPENAI_API_KEY="sk-proj-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GITHUB_TOKEN="ghp_..."
python main.py setup
```

---

## Better Long-Term Solutions

### Option 1: Rich Terminal UI (Recommended)
Use `rich` library's `Prompt.ask()` with password mode:
```python
from rich.prompt import Prompt

openai_key = Prompt.ask(
    "   Enter key (sk-...)",
    password=True,
    show_default=False
)
```

**Pros**:
- ✅ Supports paste
- ✅ Still hides input
- ✅ Better UX (colors, formatting)
- ✅ Already a project dependency

**Cons**:
- Requires import (minor)

### Option 2: Custom Input with Echo Control
```python
import termios
import tty
import sys

def secure_input_with_paste(prompt: str) -> str:
    """Read password with paste support using termios"""
    print(prompt, end='', flush=True)

    # Disable echo but keep canonical mode (allows paste)
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ECHO  # Disable echo only

    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        password = input()
        print()  # New line after hidden input
        return password
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
```

**Pros**:
- ✅ Supports paste
- ✅ Still hides input
- ✅ No external dependencies

**Cons**:
- Unix-only (doesn't work on Windows)
- More complex code

### Option 3: Web-Based Setup Wizard
Create a local web UI for setup at http://localhost:8001/setup

**Pros**:
- ✅ Best UX (form fields, copy/paste, validation)
- ✅ Cross-platform
- ✅ Can show real-time validation
- ✅ Professional appearance

**Cons**:
- Most complex to implement
- Requires web server running before setup

### Option 4: Interactive TUI (Terminal UI)
Use `textual` or `prompt_toolkit` for full TUI:

**Pros**:
- ✅ Professional appearance
- ✅ Supports paste
- ✅ Arrow key navigation

**Cons**:
- Additional dependency
- Steeper learning curve

---

## Recommendation

**Immediate (Alpha)**: Keep environment variable workaround ✅ (Done)

**Post-Alpha (MVP)**: Implement Option 1 (Rich library)
- Already a dependency
- 5 lines of code
- Perfect balance of UX and simplicity

**Future (Beta)**: Consider Option 3 (Web UI) for best onboarding experience

---

## Testing Needed

1. ✅ Verify env var approach works (user testing now)
2. ⏳ Test on Windows (Cmd+V vs Ctrl+V)
3. ⏳ Test different terminals (iTerm2, Terminal.app, WSL, etc.)
4. ⏳ Measure setup time with/without paste support

---

## References

- Python `getpass` docs: https://docs.python.org/3/library/getpass.html
- Rich Prompt: https://rich.readthedocs.io/en/stable/prompt.html
- Terminal paste issues: https://github.com/python/cpython/issues/87390

---

## Next Steps

1. User tests env var workaround (now)
2. Create GitHub issue for post-alpha improvement
3. Implement Rich library solution for MVP
4. Update installation guide with env var tip

---

**Logged**: 5:30 PM, Oct 29, 2025
