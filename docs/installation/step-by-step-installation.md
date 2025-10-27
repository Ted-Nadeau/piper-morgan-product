# 🚀 Piper Morgan: Complete Installation Guide

**For**: First-time users, fresh laptops, zero assumptions
**Time**: ~20-30 minutes from complete nothing to running Piper Morgan
**Difficulty**: Beginner-friendly (we explain everything)

---

## ⚠️ Prerequisites Check: Do You Have What You Need?

Before we start, let's make sure your computer is ready. If anything is missing, don't worry—we'll install it!

### Check 1: Do You Have Python 3.11 or Later?

Open your terminal and check your Python version:

**Mac**: Press `Cmd + Space`, type "Terminal", press Enter
**Windows**: Press `Windows + R`, type "cmd", press Enter

Once the terminal is open, type this exact command:

```bash
python3 --version
```

Press Enter.

**What you should see**:

```
Python 3.11.x
```

or

```
Python 3.12.x
```

✅ **If you see Python 3.11 or 3.12**: Great! Move to Check 2.

❌ **If you see an error** like `command not found` or an older version like `Python 3.9`:

**Mac** - Install Python 3.12:

1. Open a browser and go to [python.org/downloads](https://www.python.org/downloads/)
2. Click "Download Python 3.12.x" (the latest)
3. Run the installer
4. **Important**: Check the box that says "Add Python to PATH" during installation
5. Complete the installation
6. Close your terminal completely
7. Open a NEW terminal and run `python3 --version` again

**Windows** - Install Python 3.12:

1. Open a browser and go to [python.org/downloads](https://www.python.org/downloads/)
2. Click "Download Python 3.12.x" (the latest)
3. Run the installer
4. **CRITICAL**: Check "Add Python to PATH" (bottom of first screen!)
5. Click "Install Now"
6. Wait for it to complete
7. Close your Command Prompt completely
8. Open a NEW Command Prompt and run `python3 --version` again

---

### Check 2: Do You Have Git?

Git is software that downloads code from the internet. Let's check if you have it.

In your terminal, type:

```bash
git --version
```

Press Enter.

**What you should see**:

```
git version 2.x.x
```

✅ **If you see a version**: Great! Move to Check 3.

❌ **If you see an error** like `command not found`:

**Mac** - Install Git:

1. In Terminal, type: `xcode-select --install`
2. Press Enter
3. A window will appear asking if you want to install Command Line Tools
4. Click "Install"
5. Wait ~10 minutes for installation to complete
6. Close Terminal
7. Open a NEW Terminal and run `git --version` again

**Windows** - Install Git:

1. Open a browser and go to [git-scm.com](https://git-scm.com)
2. Click "Download for Windows"
3. Run the installer
4. Keep clicking "Next" through all screens (defaults are fine)
5. At the end, make sure "Launch Git Bash" is checked
6. Click "Finish"
7. Open Command Prompt and run `git --version` again

---

### Check 3: Do You Have Enough Disk Space?

Piper Morgan needs about 500MB of free space.

**Mac**:

1. Click the Apple menu (top-left)
2. Click "About This Mac"
3. Click "Storage"
4. Look at the bar - you need mostly empty space (gray/white, not full)

**Windows**:

1. Open File Explorer
2. Click "This PC"
3. Look at "Local Disk (C:)"
4. You should see plenty of free space (not full/red)

✅ **If you have space**: Perfect! You're ready to install Piper Morgan.

---

## 🎯 Installation: Let's Get Piper Morgan Running

### Step 1: Open Terminal/Command Prompt

**Mac**:

1. Press `Cmd + Space`
2. Type "Terminal"
3. Press Enter
4. You'll see a window with a command prompt

**Windows**:

1. Press `Windows + R`
2. Type "cmd"
3. Press Enter
4. You'll see a black window with a command prompt

**Keep this window open** for all remaining steps. Don't close it!

---

### Step 2: Create a Folder for Piper Morgan

We'll create a dedicated folder to keep everything organized.

**Type this command** (press Enter after each line):

```bash
cd ~
mkdir piper-morgan-workspace
cd piper-morgan-workspace
```

**What these do**:

- `cd ~` takes you to your home folder (fastest way)
- `mkdir piper-morgan-workspace` creates a new folder
- `cd piper-morgan-workspace` moves you into that folder

**Verify it worked**: Type `pwd` and press Enter. You should see a path ending in `piper-morgan-workspace`.

---

### Step 3: Download Piper Morgan from GitHub

Now we'll download all of Piper Morgan's code.

**Type this command**:

```bash
git clone https://github.com/Codewarrior1988/piper-morgan.git
```

Press Enter.

**What this does**: Downloads Piper Morgan's entire codebase to your computer. This will take **1-2 minutes**.

**What you'll see**: Text scrolling by with filenames. This is normal! Wait until you see the command prompt return.

**Verify it worked**: Type `ls` and press Enter. You should see a folder named `piper-morgan`.

---

### Step 4: Enter the Piper Morgan Folder

**Type this command**:

```bash
cd piper-morgan
```

Press Enter.

**Verify it worked**: Type `pwd` and press Enter. You should see a path ending in `piper-morgan`.

---

### Step 5: Create a Python Virtual Environment

This is **critical**. A virtual environment isolates Piper Morgan's Python packages from the rest of your system.

**Type this command**:

```bash
python3 -m venv venv
```

Press Enter.

**What this does**: Creates a special folder called `venv` that contains everything Piper Morgan needs.

**What you'll see**: Nothing much. The command runs silently. Wait for the command prompt to return.

**This takes ~30-60 seconds.** Don't interrupt!

**Verify it worked**: Type `ls -la` and press Enter. You should see a folder named `venv` in the list.

---

### Step 6: Activate the Virtual Environment (CRITICAL STEP)

This step changes your terminal to use the Piper Morgan Python environment. **You must do this step or nothing will work.**

**Mac/Linux - Type this command**:

```bash
source venv/bin/activate
```

**Windows - Type this command**:

```bash
venv\Scripts\activate
```

Press Enter.

**What you'll see**: Your command prompt changes. Look at the beginning of the line—it should now say `(venv)` before your username.

**Before**: `username@computer piper-morgan $`
**After**: `(venv) username@computer piper-morgan $`

❌ **If you don't see `(venv)`**: The activation didn't work. Try the command again.

✅ **If you see `(venv)`**: Perfect! You're now using the virtual environment.

⚠️ **Important**: Every time you close your terminal and open a new one, you'll need to repeat this step (Step 6) to use Piper Morgan again!

---

### Step 7: Update pip (Python's Package Installer)

pip is the software that installs Python packages. Let's make sure it's up to date.

**Type this command**:

```bash
pip install --upgrade pip
```

Press Enter.

**What you'll see**: Text showing pip being downloaded. This takes ~30 seconds. Wait for the prompt to return.

**Verify it worked**: Type `pip --version` and press Enter. You should see a version number.

---

### Step 8: Install All Python Dependencies (THE KEY STEP)

**This is the step that fixes the structlog error!** This command installs all the Python packages Piper Morgan needs.

**Type this command**:

```bash
pip install -r requirements.txt
```

Press Enter.

**What this does**: Reads `requirements.txt` and installs 50+ Python packages that Piper Morgan needs.

**What you'll see**: **A LOT of text** scrolling by. This is totally normal! You'll see package names downloading and installing. This takes **3-5 minutes** depending on your internet speed.

🕐 **Wait patiently**. Don't interrupt this process!

**What if you see red text?** Red text is often just warnings—it's usually fine. Let it continue.

**Verify it worked**: After the command finishes, type this:

```bash
pip list | grep structlog
```

Press Enter.

You should see output like:

```
structlog                                23.2.0
```

✅ **If you see `structlog` with a version**: All dependencies installed successfully!
❌ **If you don't see it**: Try running Step 8 again.

---

### Step 9: Create Your Personal Configuration File

Piper Morgan needs a configuration file with your preferences.

**Type this command**:

```bash
cp config/PIPER.example.md config/PIPER.user.md
```

Press Enter.

**What this does**: Creates your personal config file from the example.

**Verify it worked**: Type `ls config/PIPER.user.md` and press Enter. You should see the file listed.

---

### Step 10: Set Up Your API Key

Piper Morgan uses Claude's API to talk to you. You need an API key.

**First, get an API key**:

1. Open a browser
2. Go to [console.anthropic.com](https://console.anthropic.com)
3. Sign up or log in with your Google account
4. Click your profile (top-right) → "API Keys"
5. Click "Create Key"
6. Copy the key (it starts with `sk-ant-...`)
7. Save it somewhere safe (you'll need it)

**Now add it to Piper Morgan**:

**Mac** - Open the config file:

```bash
open config/PIPER.user.md
```

**Windows** - Open the config file:

```bash
notepad config/PIPER.user.md
```

The file will open in your default editor.

**Find the line that says**:

```
anthropic_api_key: "your-key-here"
```

**Replace `"your-key-here"`** with your actual API key. Your line should look like:

```
anthropic_api_key: "sk-ant-abc123xyz..."
```

⚠️ **Keep the quotes!** The key should be inside the quotes.

**Save the file** and close the editor.

---

### Step 11: Verify Everything is Installed

Let's test that everything is working before we run Piper Morgan.

**Type this command**:

```bash
python -c "from services.container.service_container import ServiceContainer; print('✅ All dependencies installed correctly!')"
```

Press Enter.

**What you should see**:

```
✅ All dependencies installed correctly!
```

✅ **If you see that message**: Perfect! Everything is ready.

❌ **If you see an error**:

- Make sure you're in the virtual environment (look for `(venv)` at the start of your prompt)
- Make sure you ran `pip install -r requirements.txt` in Step 8
- Copy the error and report it

---

### Step 12: Start Piper Morgan! 🎉

You're ready! Let's run Piper Morgan for the first time.

**Type this command**:

```bash
python main.py
```

Press Enter.

**What you should see** (after a few seconds):

```
🚀 Starting Piper Morgan...
   ⏳ Initializing services...
   ✅ Services initialized successfully

Hello! I'm Piper Morgan, your AI PM Assistant.
How can I help you today?
```

✅ **If you see this**: Congratulations! Piper Morgan is running! 🎉

❌ **If you see an error**:

**Error: "No module named 'structlog'"**
→ Go back to Step 8 and run `pip install -r requirements.txt` again

**Error: "Invalid API key"**
→ Go back to Step 10 and check your API key is correct

**Error: "Address already in use"**
→ Piper Morgan is already running in another terminal. Close that terminal and try again.

**Other error**:
→ Copy the error message exactly and report it

---

### Step 13: Try Your First Command

Let's test that Piper Morgan is working.

**At the Piper Morgan prompt, type**:

```
Hello! What can you help me with?
```

Press Enter.

**What you should see**: A friendly response from Piper Morgan describing what it can help with.

✅ **If you got a response**: You're all set! Piper Morgan is fully working!

---

## 📚 Next Time: Starting Piper Morgan Again

After installation, when you want to use Piper Morgan again:

**Step 1: Open Terminal/Command Prompt** (as in Step 1 above)

**Step 2: Navigate to Piper Morgan folder**:

```bash
cd ~/piper-morgan-workspace/piper-morgan
```

**Step 3: Activate the virtual environment**:

**Mac/Linux**:

```bash
source venv/bin/activate
```

**Windows**:

```bash
venv\Scripts\activate
```

(You should see `(venv)` appear in your prompt)

**Step 4: Start Piper Morgan**:

```bash
python main.py
```

That's it! Piper Morgan will start.

---

## 💡 Quick Reference Card

Save this for next time:

### Prerequisites

- [ ] Python 3.11 or later installed
- [ ] Git installed
- [ ] ~500MB disk space free

### Installation Commands (One-Time)

```bash
cd ~
mkdir piper-morgan-workspace
cd piper-morgan-workspace
git clone https://github.com/Codewarrior1988/piper-morgan.git
cd piper-morgan
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows
pip install --upgrade pip
pip install -r requirements.txt
cp config/PIPER.example.md config/PIPER.user.md
# [Add your API key to config/PIPER.user.md]
python main.py
```

### Starting Piper Morgan (Every Time After Installation)

```bash
cd ~/piper-morgan-workspace/piper-morgan
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows
python main.py
```

### Troubleshooting Quick Links

- Python not found? → Install from [python.org](https://python.org)
- Git not found? → See Check 2 in Prerequisites
- structlog error? → Run `pip install -r requirements.txt` again
- API key error? → Check Step 10 configuration

---

## 🆘 Need Help?

If you run into issues:

1. **Read the error carefully** - it often tells you exactly what's wrong
2. **Check troubleshooting.md** in this folder for common issues
3. **Copy the entire error message** and report it (including all red text)
4. **Note what step you were on** when it failed

---

**Last updated**: October 27, 2025
**Version**: 1.0 - Initial extreme-from-nothing guide
**Status**: ✅ Ready for Beatrice on Thursday!
