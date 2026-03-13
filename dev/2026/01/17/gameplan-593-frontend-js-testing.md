# Gameplan: Issue #593 - Frontend JavaScript Testing Framework

**Issue**: #593 TEST-INFRA: Add frontend JavaScript testing framework
**Priority**: P3 (Infrastructure improvement)
**Type**: Test Infrastructure
**Estimated Effort**: 1-2 hours
**Created**: 2026-01-17

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI with Jinja2 templates
- [x] Frontend: Vanilla JavaScript (no React/Vue/Angular)
- [x] JS files location: `web/static/js/` (17 files, ~130KB total)
- [x] Existing package.json: Yes, but for Next.js marketing site (not main app)
- [x] Python testing: pytest (1763+ tests)
- [x] Node.js: Required (for any JS testing framework)

**My understanding of the task**:
- Need to add JavaScript testing capability for vanilla JS files
- Target files are in `web/static/js/` (chat.js, toast.js, dialog.js, etc.)
- Should integrate with existing CI/CD
- Should NOT conflict with existing Next.js setup (marketing site)

**Key Files to Test**:
| File | Size | Testable Functions |
|------|------|-------------------|
| `chat.js` | 16KB | `appendMessage()`, `renderBotMessage()`, session mgmt |
| `setup.js` | 32KB | Form validation, wizard flow, API calls |
| `dialog.js` | 8KB | Modal management, event handling |
| `toast.js` | 5KB | Notification display, auto-dismiss |
| `form-validation.js` | 6KB | Validation rules, error display |
| `permissions.js` | 3KB | Role formatting, badge display |

### Part A.2: Work Characteristics Assessment

**Worktree Assessment**:
- [ ] Multiple agents in parallel - No
- [x] Task duration >30 minutes - Yes
- [ ] Multi-component work - No
- [ ] Exploratory/risky - Somewhat (new infra)

**Assessment**: **SKIP WORKTREE** - Single agent, sequential work, low risk

### Part B: PM Verification Required

**PM, please confirm**:

1. **Scope**: Should testing cover ALL 17 JS files or start with critical subset?
   - Recommendation: Start with `chat.js`, `toast.js`, `form-validation.js` (most used)

2. **Framework preference**:
   - [ ] Jest (most popular, good ecosystem)
   - [ ] Vitest (faster, modern)
   - [ ] Mocha + Chai (classic, flexible)
   - [ ] PM's choice: ____________

3. **Integration level**:
   - [ ] Standalone npm scripts only
   - [ ] Integrated with pytest (via subprocess)
   - [ ] CI/CD integration required now
   - [ ] CI/CD integration deferred

4. **Conflict resolution**: The root `package.json` is for Next.js marketing site.
   - [ ] Create separate `web/static/js/package.json` for app JS
   - [ ] Add to root package.json (may conflict)
   - [ ] Create `tests/frontend/package.json` (isolated)

---

## Phase 0: Initial Bookending

### 0.1 GitHub Issue Verification

```bash
gh issue view 593
```

### 0.2 Codebase Investigation

```bash
# Check existing JS structure
ls -la web/static/js/

# Check for existing test patterns in JS files
grep -n "test\|describe\|it(" web/static/js/*.js

# Check if any JS files export modules
grep -n "export\|module.exports" web/static/js/*.js

# Check how JS files are included in templates
grep -n "static/js" templates/*.html | head -10
```

### 0.3 Current JS Architecture Analysis

**Key observations**:
1. Files use IIFE or global scope patterns (no ES modules)
2. DOM manipulation is direct (no virtual DOM)
3. `fetch()` used for API calls
4. Event listeners attached to specific elements
5. No build step (files served directly)

**Testing challenges**:
- Need jsdom or similar for DOM simulation
- Need to mock `fetch()` for API tests
- Global scope means careful test isolation needed

---

## Phase 0.5: Framework Selection Decision

### Option A: Jest + jsdom (Recommended)

**Pros**:
- Industry standard
- Excellent jsdom integration
- Built-in mocking
- Good error messages
- Large community

**Cons**:
- Heavier than alternatives
- Config can be complex

**Setup**:
```json
{
  "devDependencies": {
    "jest": "^29.0.0",
    "jest-environment-jsdom": "^29.0.0",
    "@testing-library/dom": "^9.0.0"
  }
}
```

### Option B: Vitest + jsdom

**Pros**:
- Very fast (native ESM)
- Modern API
- Compatible with Jest API
- Lighter weight

**Cons**:
- Requires ESM or config for CommonJS
- Smaller community
- Our vanilla JS isn't ESM

### Option C: Mocha + Chai + jsdom

**Pros**:
- Very flexible
- Minimal opinions
- Long history

**Cons**:
- More setup required
- Need separate assertion library
- Less integrated mocking

### Recommendation

**Jest** is recommended because:
1. Best jsdom integration out of the box
2. Built-in mocking for `fetch()` and timers
3. Works well with non-module JS via script transform
4. Most documentation/examples available

---

## Phase 1: Setup Implementation

### 1.1 Create Test Infrastructure

**Directory structure**:
```
tests/
├── frontend/           # New directory
│   ├── package.json    # Isolated from root Next.js
│   ├── jest.config.js
│   ├── setup.js        # jsdom setup, global mocks
│   ├── __mocks__/
│   │   └── fetchMock.js
│   └── unit/
│       ├── chat.test.js
│       ├── toast.test.js
│       └── form-validation.test.js
```

### 1.2 Package Configuration

**tests/frontend/package.json**:
```json
{
  "name": "piper-morgan-frontend-tests",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0",
    "@testing-library/dom": "^9.3.0"
  }
}
```

### 1.3 Jest Configuration

**tests/frontend/jest.config.js**:
```javascript
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['./setup.js'],
  testMatch: ['**/*.test.js'],
  moduleDirectories: ['node_modules', '../../web/static/js'],
  collectCoverageFrom: ['../../web/static/js/**/*.js'],
  coverageDirectory: './coverage',
  // Transform vanilla JS files
  transform: {},
  // Mock fetch globally
  globals: {
    fetch: jest.fn()
  }
};
```

### 1.4 Test Setup File

**tests/frontend/setup.js**:
```javascript
// Mock fetch globally
global.fetch = jest.fn();

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn()
};
global.localStorage = localStorageMock;

// Reset mocks before each test
beforeEach(() => {
  jest.clearAllMocks();
  document.body.innerHTML = '';
});
```

---

## Phase 2: Example Tests

### 2.1 Toast Test Example

**tests/frontend/unit/toast.test.js**:
```javascript
// Load the toast.js file
const fs = require('fs');
const path = require('path');
const toastCode = fs.readFileSync(
  path.join(__dirname, '../../../web/static/js/toast.js'),
  'utf8'
);

describe('Toast Notifications', () => {
  beforeEach(() => {
    // Create toast container
    document.body.innerHTML = '<div id="toast-container"></div>';
    // Execute toast.js code
    eval(toastCode);
  });

  test('showToast creates toast element', () => {
    window.showToast('Test message', 'success');

    const toast = document.querySelector('.toast');
    expect(toast).toBeTruthy();
    expect(toast.textContent).toContain('Test message');
  });

  test('toast auto-dismisses after timeout', () => {
    jest.useFakeTimers();

    window.showToast('Auto dismiss', 'info', 3000);

    expect(document.querySelector('.toast')).toBeTruthy();

    jest.advanceTimersByTime(3500);

    expect(document.querySelector('.toast')).toBeFalsy();

    jest.useRealTimers();
  });
});
```

### 2.2 Form Validation Test Example

**tests/frontend/unit/form-validation.test.js**:
```javascript
describe('Form Validation', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <form id="test-form">
        <input id="email" type="email" required>
        <input id="password" type="password" minlength="8">
        <button type="submit">Submit</button>
      </form>
    `;
    // Load form-validation.js
    require('../../../web/static/js/form-validation.js');
  });

  test('validates required email field', () => {
    const emailInput = document.getElementById('email');
    emailInput.value = '';

    const isValid = FormValidation.validateField(emailInput);

    expect(isValid).toBe(false);
  });

  test('validates password minimum length', () => {
    const passwordInput = document.getElementById('password');
    passwordInput.value = 'short';

    const isValid = FormValidation.validateField(passwordInput);

    expect(isValid).toBe(false);
  });
});
```

---

## Phase 3: Integration

### 3.1 NPM Scripts (Standalone)

```bash
# From tests/frontend/
npm install
npm test
npm run test:coverage
```

### 3.2 Python Integration (Optional)

**tests/conftest.py** addition:
```python
import subprocess
import pytest

@pytest.fixture(scope="session", autouse=False)
def run_frontend_tests():
    """Run frontend JS tests as part of full test suite."""
    result = subprocess.run(
        ["npm", "test"],
        cwd="tests/frontend",
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        pytest.fail(f"Frontend tests failed:\n{result.stderr}")
```

### 3.3 CI/CD Integration

**Add to GitHub Actions workflow**:
```yaml
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        working-directory: tests/frontend
        run: npm ci
      - name: Run tests
        working-directory: tests/frontend
        run: npm test
```

---

## Phase Z: Acceptance Criteria

### Required for Completion

- [ ] `tests/frontend/package.json` created with Jest dependencies
- [ ] `tests/frontend/jest.config.js` configured for jsdom
- [ ] `tests/frontend/setup.js` with global mocks (fetch, localStorage)
- [ ] At least 3 example tests demonstrating pattern:
  - [ ] `toast.test.js` - DOM manipulation testing
  - [ ] `form-validation.test.js` - Input validation testing
  - [ ] `chat.test.js` - Async/fetch testing (optional stretch)
- [ ] `npm test` runs successfully from `tests/frontend/`
- [ ] Documentation in `docs/testing/frontend-testing.md`
- [ ] All existing Python tests still pass

### Evidence Required

```bash
# Show test output
cd tests/frontend && npm test

# Show coverage report
npm run test:coverage

# Verify no Python test regressions
python -m pytest tests/unit -q --tb=no
```

---

## Gameplan Template Audit

### Sections Present

| Template Section | Present | Notes |
|-----------------|---------|-------|
| Phase -1: Infrastructure | ✓ | PM verification questions ready |
| Phase 0: Initial Bookending | ✓ | Investigation commands defined |
| Phase 0.5: Frontend-Backend Contract | N/A | No API changes |
| Phase 0.6: Data Flow | N/A | Test infrastructure only |
| Phase 0.7: Conversation Design | N/A | Not conversational |
| Phase 0.8: Post-Completion | N/A | No database changes |
| Phases 1-N: Development | ✓ | Clear implementation steps |
| Phase Z: Final Bookending | ✓ | Acceptance criteria with checkboxes |

### Template Compliance

- ✓ Worktree assessment completed (SKIP - single agent)
- ✓ STOP conditions implicit (framework selection depends on PM)
- ✓ Evidence requirements specified (test output, coverage)
- ✓ Multi-agent: Not needed (single agent, sequential work)
- ✓ Documentation update included in acceptance criteria

### Sections Adapted for Infrastructure Issue

Since this is infrastructure (not a feature), the following adaptations were made:

1. **No Phase 0.5-0.8**: These phases are for features with API/data/conversation components
2. **Framework Selection Section Added**: Critical decision point for infrastructure
3. **Example Tests Section**: Demonstrates patterns (equivalent to "happy path" for features)
4. **Integration Section**: Shows how new infrastructure connects to existing systems

### Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Conflicts with root package.json | Isolated package.json in tests/frontend/ |
| Vanilla JS hard to test | jsdom + careful script loading |
| Global scope pollution | Reset mocks and DOM in beforeEach |
| CI/CD integration complexity | Start with standalone, add CI later |

---

## Open Questions for PM

1. **Scope**: Full 17 files or critical subset for MVP?
2. **Framework**: Jest (recommended) or alternative?
3. **CI/CD**: Required now or Phase 2?
4. **Coverage threshold**: Required percentage?

---

*Gameplan ready for PM review and approval*
