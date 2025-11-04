# Agent Prompt: Ultra-Detailed Installation Guide

**Date**: October 27, 2025, 4:20 PM
**Context**: Phase 2 testing revealed documentation gap - installation instructions incomplete
**Root Cause**: Instructions assumed `pip install -r requirements.txt` would happen magically
**Agent**: Cursor

---

## 🎯 **YOUR MISSION**

Write a **super literal, step-by-step installation guide** that assumes the user's Mac (or PC) has **nothing ready yet**. Leave **absolutely nothing to chance**.

---

## 🐛 **THE PROBLEM WE'RE SOLVING**

**What Happened**:
- PM followed existing installation instructions exactly
- Got "ModuleNotFoundError: No module named 'structlog'"
- Root cause: Instructions never said to run `pip install -r requirements.txt`
- structlog IS in requirements.txt - just wasn't installed

**Why It Happened**:
- Documentation made assumptions
- Skipped "obvious" steps
- Assumed user would "just know" to install dependencies
- Classic expert blind spot

**Impact**:
- Alpha tester would hit this immediately
- Bad first impression
- Lost confidence in product
- Support burden

---

## 📝 **WHAT TO CREATE**

### **Document Name**: `docs/installation/step-by-step-installation.md`

### **Audience**:
- Alpha testers (Beatrice on Thursday!)
- Future users
- Someone who may be technical BUT doesn't know Python ecosystem
- Assume ZERO prior knowledge

### **Tone**:
- Ultra-clear, no jargon
- Every step explicit
- No assumptions
- Encouraging, not condescending
- "You've got this!" vibe

---

## 📋 **REQUIRED CONTENT**

### **Section 1: Prerequisites Check**

Check if they have what they need BEFORE starting:

```markdown
## Prerequisites

Before installing Piper Morgan, let's make sure your system is ready.

### Check 1: Do you have Python 3.11 or 3.12?

Open Terminal (on Mac) or Command Prompt (on Windows) and type:

```bash
python3 --version
```

**What you should see**: Something like `Python 3.11.x` or `Python 3.12.x`

**If you see an error** or a version like `Python 3.9.x`:
- Mac: Install Python 3.12 from [python.org/downloads](https://python.org/downloads)
- Windows: Install Python 3.12 from [python.org/downloads](https://python.org/downloads)
- **Important**: Check "Add Python to PATH" during installation (Windows)

### Check 2: Do you have Git?

In Terminal/Command Prompt, type:

```bash
git --version
```

**What you should see**: Something like `git version 2.x.x`

**If you see an error**:
- Mac: Run `xcode-select --install`
- Windows: Install Git from [git-scm.com](https://git-scm.com)

### Check 3: Do you have enough disk space?

Piper Morgan needs about 500MB of disk space.

Check your available space:
- Mac: Click Apple menu → About This Mac → Storage
- Windows: Open File Explorer → This PC

**Ready?** All checks passed? Let's install Piper Morgan! 🚀
```

---

### **Section 2: Installation Steps**

**Every. Single. Step.** No shortcuts.

```markdown
## Installation Steps

### Step 1: Open Terminal (Mac) or Command Prompt (Windows)

**Mac**:
1. Press `Cmd + Space` to open Spotlight
2. Type "Terminal"
3. Press Enter

**Windows**:
1. Press `Windows + R`
2. Type "cmd"
3. Press Enter

You should see a window with text - this is your command line. **Keep this window open** for all the steps below.

---

### Step 2: Create a folder for Piper Morgan

We'll create a new folder to keep Piper Morgan organized.

**Type this command** (press Enter after typing):

```bash
cd ~
mkdir piper-morgan-install
cd piper-morgan-install
```

**What this does**:
- `cd ~` takes you to your home folder
- `mkdir piper-morgan-install` creates a new folder called "piper-morgan-install"
- `cd piper-morgan-install` moves you into that folder

**Check it worked**: Type `pwd` and press Enter. You should see a path ending in `piper-morgan-install`.

---

### Step 3: Download Piper Morgan from GitHub

**Type this command** (press Enter after typing):

```bash
git clone https://github.com/your-org/piper-morgan.git
```

**What this does**: Downloads all of Piper Morgan's code to your computer.

**What you'll see**: Text scrolling by showing files being downloaded. Wait until you see a new command prompt (the `$` or `>` symbol).

**Check it worked**:
```bash
ls
```
You should see a folder called `piper-morgan`.

---

### Step 4: Go into the Piper Morgan folder

**Type this command**:

```bash
cd piper-morgan
```

**What this does**: Moves you inside the Piper Morgan folder where all the code lives.

**Check it worked**: Type `pwd`. You should see a path ending in `piper-morgan`.

---

### Step 5: Create a Python virtual environment

A virtual environment keeps Piper Morgan's Python packages separate from other Python projects on your computer. This is **important** - don't skip this step!

**Type this command**:

```bash
python3 -m venv venv
```

**What this does**: Creates a special isolated Python environment called "venv".

**What you'll see**: Nothing much - the command runs quietly. Wait for the command prompt to return.

**Check it worked**:
```bash
ls -la
```
You should see a folder called `venv` in the list.

---

### Step 6: Activate the virtual environment

This step is **critical**. You must activate the virtual environment before installing packages.

**Mac/Linux - Type this command**:
```bash
source venv/bin/activate
```

**Windows - Type this command**:
```bash
venv\Scripts\activate
```

**What you'll see**: Your command prompt will change. You should see `(venv)` at the beginning of your prompt.

**Example**:
- Before: `user@computer piper-morgan $`
- After: `(venv) user@computer piper-morgan $`

**If you don't see (venv)**, the activation didn't work. Try the command again.

**Important**: Every time you open a new Terminal/Command Prompt window to use Piper Morgan, you'll need to:
1. Navigate to the piper-morgan folder: `cd ~/piper-morgan-install/piper-morgan`
2. Activate the environment again: `source venv/bin/activate` (Mac) or `venv\Scripts\activate` (Windows)

---

### Step 7: Upgrade pip (Python's package installer)

Before installing Piper Morgan's dependencies, let's make sure pip is up to date.

**Type this command**:

```bash
pip install --upgrade pip
```

**What this does**: Updates pip to the latest version.

**What you'll see**: Text showing pip being downloaded and installed. Wait for the command prompt to return.

---

### Step 8: Install Piper Morgan's Python dependencies

This is the step that was missing from the original instructions! This step installs all the Python packages that Piper Morgan needs to run.

**Type this command**:

```bash
pip install -r requirements.txt
```

**What this does**: Reads the `requirements.txt` file and installs all 50+ Python packages that Piper Morgan needs.

**What you'll see**: **A LOT of text** scrolling by. This is normal! It's downloading and installing packages. This will take **2-5 minutes**.

**Wait for**: The command prompt to return. Don't interrupt this process!

**What if you see errors?**:
- Red text is normal for some packages (they're just warnings)
- If the process stops with an error, copy the error message and report it

**Check it worked**:
```bash
pip list | grep structlog
```
You should see `structlog` with a version number. If you do, all dependencies were installed successfully!

---

### Step 9: Verify the installation

Let's make sure everything is installed correctly before trying to start Piper Morgan.

**Type this command**:

```bash
python -c "from services.container.service_container import ServiceContainer; print('✅ Installation successful!')"
```

**What this does**: Tries to import Piper Morgan's code. If it works, installation succeeded.

**What you should see**: `✅ Installation successful!`

**What if you see an error?**:
- Check that you activated the virtual environment (see Step 6)
- Check that you ran `pip install -r requirements.txt` (see Step 8)
- If still broken, report the error message

---

### Step 10: Create your configuration file

Piper Morgan needs a configuration file to know your preferences.

**Type this command**:

```bash
cp config/PIPER.example.md config/PIPER.user.md
```

**What this does**: Creates your personal configuration file from the example.

**Check it worked**:
```bash
ls config/PIPER.user.md
```
You should see the file listed.

---

### Step 11: Set up your API keys

Piper Morgan needs an API key to talk to Claude (Anthropic's AI).

**Open the config file**:

```bash
# Mac:
open config/PIPER.user.md

# Windows:
notepad config/PIPER.user.md
```

**Find the API Keys section** and add your Anthropic API key:

```markdown
## API Keys

```yaml
anthropic_api_key: "your-key-here"
```
```

**Where to get an API key**:
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Go to API Keys section
4. Create a new key
5. Copy it and paste it into your config file

**Save the file** and close the editor.

---

### Step 12: Start Piper Morgan! 🚀

You're ready! Let's start Piper Morgan for the first time.

**Type this command**:

```bash
python main.py
```

**What you should see**:

```
🚀 Starting Piper Morgan...
   ⏳ Initializing services...
   ✅ Services initialized successfully

Hello! I'm Piper Morgan, your AI-powered PM assistant. How can I help you today?
```

**If you see that**, congratulations! Piper Morgan is running! 🎉

**What if you see an error?**:
- "No module named 'structlog'": Go back to Step 8 and run `pip install -r requirements.txt`
- "Invalid API key": Go back to Step 11 and check your API key
- Something else: Copy the error message and report it

---

### Step 13: Try your first command

Let's make sure Piper Morgan is working.

**Type this** at the Piper Morgan prompt:

```
Hello, what can you help me with?
```

**What you should see**: A friendly response from Piper Morgan listing its capabilities.

**If that works**, you're all set! Welcome to Piper Morgan! 🎉

---

## Quick Reference: Starting Piper Morgan Again

After installation, when you want to use Piper Morgan again:

1. Open Terminal/Command Prompt
2. Navigate to Piper Morgan:
   ```bash
   cd ~/piper-morgan-install/piper-morgan
   ```
3. Activate the virtual environment:
   ```bash
   # Mac/Linux:
   source venv/bin/activate

   # Windows:
   venv\Scripts\activate
   ```
4. Start Piper Morgan:
   ```bash
   python main.py
   ```

**Tip**: Save these commands in a text file so you don't have to remember them!
```

---

## 🎯 **REQUIREMENTS**

### **Must Have**:
- [ ] Every single step numbered
- [ ] Command to type for each step
- [ ] What user will see for each step
- [ ] How to verify each step worked
- [ ] What to do if something goes wrong
- [ ] Mac AND Windows instructions where different
- [ ] Prerequisites check at beginning
- [ ] Verification at end
- [ ] "Quick reference" for next time

### **Tone Requirements**:
- [ ] Clear and simple language
- [ ] No jargon without explanation
- [ ] Encouraging (not condescending)
- [ ] Assumes user is smart but unfamiliar with Python
- [ ] Celebrates small wins ("Check it worked!")

### **Testing Requirements**:
- [ ] You must actually test these instructions
- [ ] On a fresh machine or clean virtual environment
- [ ] Every single step exactly as written
- [ ] No shortcuts or assumptions
- [ ] If ANY step fails, fix it

---

## 📂 **FILE STRUCTURE**

```
docs/
  installation/
    step-by-step-installation.md          ← Create this
    troubleshooting.md                     ← Also create this
    quick-reference.md                     ← One-page cheat sheet
```

---

## 🔍 **ALSO CREATE: Troubleshooting Guide**

**File**: `docs/installation/troubleshooting.md`

Common issues:
1. "No module named 'structlog'" → Solution
2. "Invalid API key" → Solution
3. "Command not found: python3" → Solution
4. "Permission denied" → Solution
5. Virtual environment not activating → Solution
6. Import errors → Solution

Each issue needs:
- The exact error message user will see
- Why it happens
- Step-by-step fix
- How to verify fix worked

---

## 🔍 **ALSO CREATE: Quick Reference**

**File**: `docs/installation/quick-reference.md`

One-page cheat sheet:
- Prerequisites (bullet points)
- Installation commands (copy-paste ready)
- Starting Piper Morgan (commands only)
- Common commands
- Where to get help

---

## ✅ **SUCCESS CRITERIA**

1. **Someone with zero Python knowledge** can follow these instructions and get Piper Morgan running
2. **Every step** has verification
3. **Every step** has troubleshooting
4. **Nothing is assumed** or implied
5. **You tested it** on a clean environment
6. **Beatrice can follow this Thursday** without asking questions

---

## 📊 **DELIVERABLES**

1. **step-by-step-installation.md** (comprehensive guide)
2. **troubleshooting.md** (common issues + fixes)
3. **quick-reference.md** (one-page cheat sheet)
4. **Test report**: "I tested these instructions on [clean Mac/Windows] and they worked perfectly"

---

## 💡 **INSPIRATION**

Think about:
- Times you've followed installation instructions that assumed too much
- Times you've been frustrated by "just install X" with no details
- Times you've wanted to help someone but documentation was incomplete

**Write the guide you wish existed when you first started coding.**

---

## 🎯 **PRIORITY**

**HIGH** - Beatrice is coming Thursday. These instructions must be bulletproof.

**Timeline**: Complete by end of day (Oct 27)

---

## 📝 **REPORTING TEMPLATE**

When done:

```
## Installation Guide - Complete

**Files Created**:
- [x] docs/installation/step-by-step-installation.md
- [x] docs/installation/troubleshooting.md
- [x] docs/installation/quick-reference.md

**Tested On**:
- [x] Fresh Mac (macOS version X)
- [x] Fresh Windows (Windows version X)
- [x] Clean Python virtual environment

**Test Results**:
- Installation time: X minutes
- Steps that needed clarification: [list]
- Issues found: [list]
- All steps verified: ✅

**Verification**:
- [x] Piper Morgan starts successfully
- [x] First conversation works
- [x] No errors in any step
- [x] Instructions are clear and complete

**Ready for Alpha**: ✅ YES / ❌ NO
```

---

**CRITICAL**: These instructions are what Beatrice will use Thursday. They must be perfect!

---

**Created**: October 27, 2025, 4:20 PM
**For**: Cursor Agent
**Status**: Ready to execute
