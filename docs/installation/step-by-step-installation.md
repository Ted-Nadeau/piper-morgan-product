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

❌ **If you see an error** like `command not found` or a different version:

**Important Note About Python Versions**:
For best compatibility with current packages, **Python 3.12 is recommended** (3.11 also works). Python 3.13 is very new and some packages don't have pre-built wheels for it yet, which can cause build failures. On macOS, **Python 3.12.10 is the last version with a GUI installer**; later patches are source-only downloads.

**Mac** - Install Python 3.12.10 (Recommended):

1. Open a browser and go to [python.org/downloads/release/python-31210/](https://www.python.org/downloads/release/python-31210/)
2. Download "macOS 64-bit universal2 installer" (this is Python 3.12.10, the last macOS installer build)
3. If the link doesn't work, go to [python.org/downloads](https://www.python.org/downloads/) and scroll to "3.12.10" in "Looking for a specific release?"
4. Choose "macOS 64-bit universal2 installer"
5. Download and run the installer
6. If you later see "Install Certificates.command" and it errors with "Permission denied":
   - Don't worry! Just skip it and continue
   - Inside your venv later, run: `python -m pip install --upgrade certifi`
7. Complete the installation
8. Close your terminal completely
9. Open a NEW terminal and run `python3.12 --version` (verify 3.12.10 is installed)

**Windows** - Install Python 3.12:

1. Open a browser and go to [python.org/downloads](https://www.python.org/downloads/)
2. Scroll down to "Looking for a specific release?"
3. Find "Python 3.12.x" in the table (NOT the big banner at top)
4. Click "Download" next to Python 3.12.x
5. Run the installer
6. **CRITICAL**: Check "Add Python to PATH" (bottom of first screen!)
7. Click "Install Now"
8. Wait for it to complete
9. Close your Command Prompt completely
10. Open a NEW Command Prompt and run `python3 --version` again

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

### Check 4: Do You Have Docker?

Docker runs Piper Morgan's database. Let's check if you have it.

In your terminal, type:

```bash
docker --version
```

Press Enter.

**What you should see**:

```
Docker version 20.x.x, build xxxxx
```

✅ **If you see a version**: Great! Move to Installation below.

❌ **If you see an error** like `command not found`:

**Mac** - Install Docker Desktop:

1. Visit: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Download "Docker Desktop for Mac" (choose Apple Silicon if you have M1/M2/M3, Intel otherwise)
3. Open the downloaded file and drag Docker icon to Applications folder
4. Launch Docker Desktop from Applications (look for whale icon in menu bar)
5. Wait for Docker to fully start (whale icon should be solid, not grayed out)
6. Open a NEW terminal and run `docker --version` again

**Windows** - Install Docker Desktop:

1. Visit: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Download "Docker Desktop for Windows"
3. Run the installer and follow the setup wizard
4. **Important**: When asked "Use WSL 2 instead of Hyper-V", choose "Yes" (simpler setup)
5. Restart your computer when prompted
6. After restart, launch Docker Desktop
7. Wait for Docker to fully start (look for whale icon in system tray)
8. Open Command Prompt and run `docker --version` again

✅ **If you see a version**: Perfect! You're ready.

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

## 🚀 Start Docker (Required Before Wizard)

Piper Morgan's database runs in Docker. Start it now in a **separate terminal tab**:

**Mac/Linux**:

```bash
docker-compose up -d db
```

**Windows** (PowerShell):

```bash
docker-compose up -d db
```

Press Enter.

**What you'll see**:

```
Creating network "piper-morgan-product_default" with the default driver
Creating piper-morgan-product_db_1 ...
Creating piper-morgan-product_db_1 ... done
```

✅ **If you see "done"**: Database is starting! Give it 10 seconds to fully initialize.

**Keep this terminal tab open** (Docker will keep running).

Go back to your **original terminal tab** (the one in the piper-morgan-product folder) and proceed below.

---

## 🎯 Recommended: Use the Setup Wizard (Automated)

Instead of doing Steps 5-10 manually, you can use the automated setup wizard:

```bash
python3.12 main.py setup
```

This single command will:

1. ✅ Check for Python 3.12
2. ✅ Create your virtual environment
3. ✅ Install all dependencies
4. ✅ Generate SSH key (if needed)
5. ✅ Guide you through GitHub setup
6. ✅ System checks (Docker, port, database)
7. ✅ Create your user account
8. ✅ Collect and validate API keys

**Time**: ~5-10 minutes total (including waiting for dependencies to install)

If you prefer to do it manually, continue below. Otherwise, you're done! 🎉

---

## Manual Setup (Optional Alternative)

If you prefer to understand each step, follow Steps 5-10 below. Both approaches work!

### Step 5: Create a Python Virtual Environment

This is **critical**. A virtual environment isolates Piper Morgan's Python packages from the rest of your system.

⚠️ **IMPORTANT: First, clean up any old virtual environment**

If you see a `venv` folder from a previous attempt, delete it:

```bash
rm -rf venv
```

Press Enter.

**Now create the virtual environment using Python 3.12 explicitly:**

**Mac**:

```bash
python3.12 -m venv venv
```

**Windows**:

```bash
python -m venv venv
```

Press Enter.

**What this does**: Creates a special folder called `venv` that contains everything Piper Morgan needs, using Python 3.12.

**What you'll see**: Nothing much. The command runs silently. Wait for the command prompt to return.

**This takes ~30-60 seconds.** Don't interrupt!

**Verify it worked**: Type `ls -la` and press Enter. You should see a folder named `venv` in the list.

**Troubleshoot**: If you see an error like `python3.12: command not found`:

- On Mac: You need to install Python 3.12.10. Go back to Check 1 and follow the Python installation steps.
- On Windows: The installer should have added Python to PATH. Close your command prompt completely, open a NEW one, and try again.

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
