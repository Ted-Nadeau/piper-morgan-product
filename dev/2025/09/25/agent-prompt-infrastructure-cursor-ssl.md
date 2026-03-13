# Cursor Agent Prompt: Fix SSL Certificate Issue in Fresh Clone Setup

## Your Identity
You are Cursor Agent, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- CURRENT-STATE.md - Current epic and focus
- role/PROGRAMMER.md - Your role requirements
- METHODOLOGY.md - Inchworm Protocol

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check SSL Certificate Issue Scope FIRST
**Before doing ANYTHING else, verify the SSL certificate problem**:

```bash
# Test SSL certificate availability in fresh environment
cd /tmp/fresh-clone-retest-*/piper-morgan-product/

# Test the specific SSL issue discovered
python3 -c "import ssl; import certifi; print('Certifi path:', certifi.where())"
python3 -c "import requests; print('Requests SSL verification:', requests.get('https://httpbin.org/get', verify=True))" 2>&1 || echo "SSL REQUEST FAILED"
```

**Context**: Fresh clone setup fails with SSL certificate issue (certifi/cacert.pem missing), blocking "setup works without issues" verification.

## Session Log Management (CRITICAL)

**Create new session log for infrastructure fix**:
- Create one at: `dev/2025/09/25/2025-09-25-1810-prog-cursor-ssl-fix-log.md`
- Document this as "Infrastructure Blocker - SSL Certificate Resolution"

### Shell Command Guidelines for Cursor
- Use single quotes for string literals: 'text' not "text"
- If stuck in quote prompt (>), type closing quote and press Enter
- For complex commands, use simpler syntax or break into steps
- Test shell commands in small increments

## Mission
**Fix SSL certificate issue preventing fresh clone setup completion**

**Scope Boundaries**:
- This prompt covers ONLY: SSL certificate configuration for fresh environments
- NOT in scope: Modifying application SSL logic or certificate validation
- Specific issue: certifi/cacert.pem missing in fresh Python environments

## Context
- **GitHub Issue**: GREAT-1C (#187) - Verification Phase Infrastructure Blocker
- **Current State**: Fresh clone setup fails with SSL certificate errors
- **Target State**: Fresh clone setup completes without SSL issues
- **Verification requirement**: "Fresh clone and setup works without issues" blocked
- **Discovery**: SSL issue found in fresh clone re-verification testing
- **User Data Risk**: None - environmental configuration only

## Evidence Requirements (CRITICAL)

### For EVERY Claim You Make:
- **"SSL issue diagnosed"** → Show specific error messages and root cause
- **"Certificate path identified"** → Show certifi.where() output
- **"Fix implemented"** → Show before/after SSL request tests
- **"Setup successful"** → Show complete fresh clone setup without SSL errors
- **"Solution documented"** → Show setup guide updates for SSL requirements

### SSL Testing Requirements:
- Test both Python SSL module and requests library
- Verify certificate bundle accessibility
- Test HTTPS requests to external services
- Confirm fresh environment compatibility

## Constraints & Requirements

### For This Agent
1. **Environmental focus**: Fix fresh environment setup, not application logic
2. **Minimal change**: Prefer configuration over code modification
3. **Documentation update**: Update setup guide with SSL requirements
4. **Fresh environment testing**: Verify fix in clean environment

## SSL Certificate Fix Instructions

### Step 1: Diagnose SSL Issue Thoroughly
```bash
# Move to fresh clone environment for testing
cd /tmp/fresh-clone-retest-*/piper-morgan-product/

# Diagnose the SSL certificate issue
echo "=== SSL DIAGNOSTIC ==="
python3 -c "
import ssl
import certifi
import sys
print('Python version:', sys.version)
print('SSL version:', ssl.OPENSSL_VERSION)
print('Certifi version:', certifi.__version__)
print('Certificate bundle path:', certifi.where())
print('Bundle exists:', __import__('os').path.exists(certifi.where()))
"

# Test specific SSL failures
echo "=== SSL REQUEST TEST ==="
python3 -c "
import requests
try:
    resp = requests.get('https://httpbin.org/get', timeout=10)
    print('SSL request successful:', resp.status_code)
except Exception as e:
    print('SSL request failed:', type(e).__name__, str(e))
"
```

### Step 2: Identify Root Cause and Solution
```bash
# Check if this is a system-wide or environment-specific issue
echo "=== SYSTEM SSL CHECK ==="

# Check system certificate stores
ls -la /etc/ssl/certs/ 2>/dev/null || echo "No /etc/ssl/certs/"
ls -la /usr/local/share/ca-certificates/ 2>/dev/null || echo "No /usr/local/share/ca-certificates/"

# Check if certifi package is properly installed
pip3 show certifi || echo "Certifi package info unavailable"

# Test if reinstalling certifi fixes the issue
echo "=== CERTIFI REINSTALL TEST ==="
pip3 install --upgrade certifi
python3 -c "import certifi; print('Updated certifi path:', certifi.where())"
```

### Step 3: Implement Solution
```bash
# Apply the appropriate fix based on diagnosis

# Option 1: If certifi package issue
if [[ "$(python3 -c 'import certifi; print(certifi.where())' 2>/dev/null)" == "" ]]; then
    echo "Installing/upgrading certifi package..."
    pip3 install --upgrade certifi
fi

# Option 2: If system certificates needed
if [[ ! -f "$(python3 -c 'import certifi; print(certifi.where())' 2>/dev/null)" ]]; then
    echo "Certificate bundle missing, installing system certificates..."
    # Platform-specific certificate installation
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update && sudo apt-get install -y ca-certificates
    elif command -v brew >/dev/null 2>&1; then
        brew install ca-certificates
    fi
fi

# Verify fix worked
echo "=== POST-FIX VERIFICATION ==="
python3 -c "
import certifi
import requests
print('Certificate bundle:', certifi.where())
print('Bundle exists:', __import__('os').path.exists(certifi.where()))
try:
    resp = requests.get('https://httpbin.org/get', timeout=10)
    print('SSL test successful:', resp.status_code)
except Exception as e:
    print('SSL test failed:', e)
"
```

### Step 4: Update Setup Documentation
```bash
# Update the setup guide to include SSL certificate requirements
echo "=== UPDATING SETUP DOCUMENTATION ==="

# Add SSL requirements to setup guide
cat >> docs/guides/orchestration-setup-guide.md << 'EOF'

## SSL Certificate Requirements

For fresh environments, ensure SSL certificates are properly configured:

```bash
# Install/upgrade certificate bundle
pip3 install --upgrade certifi

# Verify SSL functionality
python3 -c "import certifi, requests; print('SSL ready:', requests.get('https://httpbin.org/get').status_code == 200)"
```

If SSL errors persist, install system certificates:
- Ubuntu/Debian: `sudo apt-get install ca-certificates`
- macOS: `brew install ca-certificates`
- Manual: Ensure certifi package has valid certificate bundle

EOF

# Show documentation update
echo "Updated setup guide with SSL requirements"
```

### Step 5: Test Complete Fresh Clone Setup
```bash
# Run complete setup process to verify SSL fix
echo "=== COMPLETE SETUP VERIFICATION ==="

# Re-run setup following updated documentation
source venv/bin/activate 2>/dev/null || python3 -m venv venv && source venv/bin/activate
pip3 install -r requirements.txt

# Test that SSL issue is resolved in context of full setup
python3 -c "
import requests
import sys
try:
    resp = requests.get('https://api.github.com', timeout=10)
    print('GitHub API SSL test: SUCCESS')
    print('Fresh clone setup: SSL issues resolved')
except Exception as e:
    print('SSL test failed:', e)
    sys.exit(1)
"
```

### Step 6: Document Solution and Evidence
```bash
# Create evidence package for SSL fix
echo "=== SSL FIX EVIDENCE PACKAGE ==="
echo "Before fix: SSL requests failed with certificate errors"
echo "After fix: SSL requests successful"

# Test final setup state
echo "=== FINAL VERIFICATION ==="
python3 -c "
import certifi
import ssl
import requests
print('✅ Certificate bundle available:', certifi.where())
print('✅ SSL context working:', ssl.create_default_context())
print('✅ HTTPS requests functional:', requests.get('https://httpbin.org/get').status_code == 200)
print('Fresh clone setup: SSL issues resolved!')
"
```

## Expected Outcomes

### Success Criteria
- [ ] SSL certificate issue diagnosed and root cause identified
- [ ] Certificate bundle accessible in fresh environments
- [ ] HTTPS requests functional without SSL errors
- [ ] Setup documentation updated with SSL requirements
- [ ] Fresh clone setup completes without issues
- [ ] Solution works in clean Python environments

### Evidence Package to Provide
1. **SSL diagnostic results**: Root cause identification
2. **Before/after testing**: SSL request failure → success
3. **Documentation updates**: Setup guide includes SSL requirements
4. **Fresh environment proof**: Clean setup completion without SSL errors

## Cross-Validation Preparation
Once SSL fixed, coordinate with Code's YAML fix for complete infrastructure resolution and fresh verification re-test.

## STOP Conditions
- If SSL issue is system-level requiring admin access
- If certificate bundle corruption cannot be resolved
- If solution affects application security configuration
- If fresh environment cannot be established for testing

## Success Definition
**Fresh clone setup without issues**: SSL certificate configuration resolved, enabling completion of "Fresh clone and setup works without issues" verification requirement.

---

**Mission**: Fix SSL certificate issue preventing fresh clone setup completion, enabling infrastructure blocker resolution for GREAT-1C verification.

**Evidence Standard**: SSL diagnostic proof, before/after functionality tests, documentation updates, clean environment verification.
