# Alpha Setup Fixes & Improvements (v0.8.2)

**Date**: December 11, 2025
**For**: Alpha testers with v0.8.2

## Issues Fixed

### 1. Smart Setup vs Login Routing

**Problem**: When starting `python main.py` on a fresh system with no users, users were directed to the login page instead of the setup wizard, leading to confusion.

**Root Cause**: The app had no logic to detect whether setup was complete. The root route (`/`) would redirect to login regardless of whether any users existed.

**Solution**: Updated `web/api/routes/ui.py` home route to:
- Check if users are already authenticated → show home page
- Check if ANY users exist in database → redirect to login
- If NO users exist → redirect to setup wizard

**Impact**: First-time users on a clean system will now automatically see the setup wizard instead of a confusing login screen.

### 2. "Sign Up" Link Points to Setup Wizard

**Problem**: The login page had a "Sign up" link that showed an alert saying "Registration coming soon!" instead of directing users to the setup wizard.

**Root Cause**: Hardcoded alert in `templates/login.html` line 65.

**Solution**: Changed the link to point directly to `/setup` with label "Start Setup Wizard".

**Impact**: Users without accounts can now easily access the setup wizard from the login page.

## New: Alpha Setup Script

### Quick Start (One Command)

For testers who prefer automated setup:

**macOS/Linux/WSL2:**
```bash
./scripts/alpha-setup.sh
```

Or from anywhere (if you trust curl):
```bash
bash <(curl -s https://raw.githubusercontent.com/mediajunkie/piper-morgan-product/production/scripts/alpha-setup.sh)
```

**Windows (Command Prompt or PowerShell):**
```cmd
.\scripts\alpha-setup.bat
```

Or if cloning for the first time:
```cmd
git clone -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
.\scripts\alpha-setup.bat
```

### What the Script Does

1. **Checks Requirements**: Verifies Git, Python 3.11/3.12, Docker
2. **Clones Repository**: If not already cloned (uses production branch)
3. **Creates Virtual Environment**: Python venv in project directory
4. **Installs Dependencies**: Runs `pip install -r requirements.txt`
5. **Generates JWT Secret**: Creates secure random key, adds to `.env`
6. **Creates .env File**: From `.env.example` template
7. **Starts Docker**: Runs `docker-compose up -d` for infrastructure
8. **Launches App**: Runs `python main.py` and opens setup wizard

### Features

- **Color-coded output**: Easy to follow progress
- **Error handling**: Exits with clear error messages if requirements missing
- **Idempotent**: Safe to run multiple times (doesn't re-create venv, etc.)
- **Cross-platform**:
  - Bash version: macOS, Linux, WSL2
  - Batch version: Windows (Command Prompt, PowerShell, Windows Terminal)
- **Verbose**: Clear status messages at each step
- **Two versions**: Choose bash (`alpha-setup.sh`) or batch (`alpha-setup.bat`) based on your OS

### Usage Scenarios

**Scenario 1: Fresh clone**
```bash
cd /tmp
bash <(curl -s https://raw.githubusercontent.com/mediajunkie/piper-morgan-product/production/scripts/alpha-setup.sh)
# Script will:
# - Clone piper-morgan-product
# - Set everything up
# - Start the app
# - Open setup wizard
```

**Scenario 2: Already have repo**
```bash
cd ~/piper-morgan-product
./scripts/alpha-setup.sh
# Script will:
# - See repo already exists
# - Create venv if needed
# - Install deps
# - Start app
```

**Scenario 3: Re-run after pulling updates**
```bash
cd ~/piper-morgan-product
git pull origin production
./scripts/alpha-setup.sh
# Script will:
# - Detect venv exists
# - Update dependencies
# - Restart Docker
# - Start app
```

**Scenario 4: Windows - First time setup**
```cmd
cd C:\Users\YourName\Projects
git clone -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
.\scripts\alpha-setup.bat
REM Script will:
REM - Check Python 3.11/3.12
REM - Create venv
REM - Install dependencies
REM - Generate JWT key
REM - Start Docker
REM - Launch setup wizard
```

**Scenario 5: Windows - Existing repo, need to re-run**
```cmd
cd C:\Users\YourName\Projects\piper-morgan-product
git pull origin production
.\scripts\alpha-setup.bat
REM Script will:
REM - Detect venv exists (reuse it)
REM - Update dependencies
REM - Restart Docker
REM - Start app
```

## Migration from Manual Setup

**Old (manual) process - macOS/Linux:**
```bash
git clone -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python3.12 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Manually edit .env and generate JWT_SECRET_KEY
# Manually start docker-compose
python main.py
```

**New (automated) - macOS/Linux:**
```bash
./scripts/alpha-setup.sh
```

**Old (manual) process - Windows:**
```cmd
git clone -b production https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python -m venv venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt
REM Manually edit .env and generate JWT_SECRET_KEY
REM Manually start docker-compose
python main.py
```

**New (automated) - Windows:**
```cmd
.\scripts\alpha-setup.bat
```

## Technical Details

### Root Route Logic

File: `web/api/routes/ui.py`, route `GET /`

```python
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # 1. If authenticated → show home page
    if user_id and user_id != "user":
        return templates.TemplateResponse(...)

    # 2. If no users exist → setup wizard
    user_count = await check_users_in_db()
    if user_count == 0:
        return RedirectResponse(url="/setup")

    # 3. Otherwise → login
    return RedirectResponse(url="/login")
```

### Login Page Fix

File: `templates/login.html`, "Sign up" link

**Before:**
```html
<a href="#" onclick="alert('Registration coming soon!'); return false;">Sign up</a>
```

**After:**
```html
<a href="/setup">Start Setup Wizard</a>
```

### Setup Scripts

**Bash version** - File: `scripts/alpha-setup.sh`

- 300+ lines of well-commented bash
- Handles Python version detection
- Generates cryptographically secure JWT keys (`openssl rand -hex 32`)
- Idempotent (safe to re-run)
- Platforms: macOS, Linux, WSL2

**Batch version** - File: `scripts/alpha-setup.bat`

- 300+ lines of well-commented batch script
- Handles Python version detection (3.11 vs 3.12)
- Generates random JWT keys using PowerShell
- Idempotent (safe to re-run)
- ANSI color support in Windows Terminal / Command Prompt 21H2+
- Platforms: Windows (Command Prompt, PowerShell, Windows Terminal)

## Testing Recommendations

### Test Case 1: Fresh System
1. Delete existing piper-morgan-product directory
2. Run: `./scripts/alpha-setup.sh`
3. Expected: Setup wizard appears at http://localhost:8001/setup

### Test Case 2: Existing System
1. Run: `./scripts/alpha-setup.sh`
2. Expected: Detects venv exists, updates deps, starts app

### Test Case 3: Post-Setup Flow
1. Complete setup wizard
2. Create user account
3. Return to http://localhost:8001
4. Expected: Home page appears (not login)

### Test Case 4: Sign Up Link
1. Complete setup, create account, logout
2. Visit http://localhost:8001/login
3. Click "Start Setup Wizard" link
4. Expected: Redirected to http://localhost:8001/setup

### Test Case 5: Windows Batch Script (Fresh System)
1. Open Command Prompt or PowerShell
2. Clone repo: `git clone -b production https://github.com/mediajunkie/piper-morgan-product.git`
3. Navigate: `cd piper-morgan-product`
4. Run: `.\scripts\alpha-setup.bat`
5. Expected:
   - Python 3.11/3.12 detected ✓
   - venv created ✓
   - Dependencies installed ✓
   - JWT key generated ✓
   - Docker started ✓
   - Setup wizard opens at http://localhost:8001/setup

### Test Case 6: Windows Batch Script (Existing Installation)
1. Open Command Prompt or PowerShell
2. Navigate to existing repo: `cd piper-morgan-product`
3. Pull updates: `git pull origin production`
4. Run: `.\scripts\alpha-setup.bat`
5. Expected:
   - Script detects venv exists (reuses it) ✓
   - Dependencies updated ✓
   - Docker containers restarted ✓
   - App launches successfully

## Known Limitations

**Bash version (`alpha-setup.sh`)**:
- JWT secret generation uses `openssl` (standard on macOS/Linux)
- For Windows users, WSL2 is recommended (script works in WSL2)
- Script assumes `docker-compose` is available (Docker Desktop includes this)

**Batch version (`alpha-setup.bat`)**:
- Requires Python to be added to PATH during installation (checked during setup)
- JWT secret generation uses PowerShell (Windows 7+ PowerShell 2.0+)
- Fallback random key generation if PowerShell random fails
- Colored output requires Windows 10 21H2+ or Windows Terminal
- Script assumes `docker-compose` is available (Docker Desktop includes this)

**Both versions**:
- Script exits if requirements are missing (user must install manually)
- Docker Desktop must be running before setup script is executed

## Feedback

If alpha testers encounter issues with:
- Smart routing (landing on wrong page)
- Sign up link
- Setup script

Please report with:
- Operating system (macOS/Linux/Windows/WSL2)
- Python version (`python --version`)
- Docker version (`docker --version`)
- Steps to reproduce
- Error messages (from console or terminal)

---

**Related Issues:**
- Issue #390: ALPHA-SETUP-UI (GUI setup wizard)
- Issue #393: CORE-UX-AUTH (auth UI improvements)
- Issue #385: INFR-MAINT-REFACTOR (UI route organization)
