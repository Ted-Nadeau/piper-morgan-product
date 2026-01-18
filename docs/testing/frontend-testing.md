# Frontend JavaScript Testing Guide

This document describes the JavaScript testing infrastructure for the Piper Morgan web application.

## Overview

The frontend uses vanilla JavaScript (no React/Vue/Angular framework). JavaScript files are located in `web/static/js/` and are tested using Jest with jsdom.

## Quick Start

```bash
# Navigate to test directory
cd tests/frontend

# Install dependencies (first time only)
npm install

# Run tests
npm test

# Run tests in watch mode (for development)
npm run test:watch

# Run tests with coverage report
npm run test:coverage
```

## Directory Structure

```
tests/frontend/
├── package.json          # Node dependencies and scripts
├── jest.config.js        # Jest configuration
├── setup.js              # Global test setup (mocks, helpers)
├── unit/                 # Unit tests
│   ├── toast.test.js     # Toast notification tests
│   └── form-validation.test.js  # Form validation tests
└── coverage/             # Coverage reports (generated)
```

## Writing Tests

### Loading Source Files

Use the `loadScript()` helper to load JavaScript files from `web/static/js/`:

```javascript
beforeEach(() => {
  // Load the source file
  global.loadScript('toast.js');
});

test('Toast.success creates success toast', () => {
  Toast.success('Title', 'Message');
  expect(document.querySelector('.toast-success')).toBeTruthy();
});
```

### DOM Setup

For components that require specific DOM elements, set them up in `beforeEach`:

```javascript
beforeEach(() => {
  // Set up required DOM elements
  document.body.innerHTML = `
    <form id="test-form">
      <input name="email" type="email">
      <button type="submit">Submit</button>
    </form>
  `;

  // Load the source file
  global.loadScript('form-validation.js');
});
```

### Using Helpers

The `setup.js` file provides several helpers:

- `global.loadScript(path)` - Loads a JS file from `web/static/js/`
- `global.createToastContainer()` - Creates toast DOM structure
- `global.fetch` - Mocked fetch function
- `global.localStorage` - Mocked localStorage
- `global.sessionStorage` - Mocked sessionStorage

### Testing Async Code

Use Jest's fake timers for testing timeouts and intervals:

```javascript
test('toast auto-dismisses after duration', () => {
  jest.useFakeTimers();

  Toast.show('success', 'Title', 'Message', 3000);
  expect(document.querySelector('.toast')).toBeTruthy();

  jest.advanceTimersByTime(3500);
  expect(document.querySelector('.toast')).toBeFalsy();

  jest.useRealTimers();
});
```

### Testing Fetch Calls

The fetch mock can be configured per test:

```javascript
test('handles API response', async () => {
  global.fetch.mockResolvedValueOnce({
    ok: true,
    json: () => Promise.resolve({ data: 'test' })
  });

  // Your test code that calls fetch

  expect(global.fetch).toHaveBeenCalledWith('/api/endpoint');
});
```

## Available Test Files

| Source File | Test File | Description |
|-------------|-----------|-------------|
| `toast.js` | `toast.test.js` | Toast notification system |
| `form-validation.js` | `form-validation.test.js` | Form validation and validators |

## Adding New Tests

1. Create a new test file in `tests/frontend/unit/` with `.test.js` extension
2. Load the source file using `loadScript()`
3. Set up any required DOM structure
4. Write tests using Jest matchers

Example template:

```javascript
/**
 * [Component Name] Tests
 * Tests web/static/js/[filename].js
 */

describe('[Component Name]', () => {
  beforeEach(() => {
    // Set up DOM if needed
    document.body.innerHTML = `<div id="container"></div>`;

    // Load source file
    global.loadScript('[filename].js');
  });

  describe('[Method or feature]', () => {
    test('does something expected', () => {
      // Arrange
      // Act
      // Assert
    });
  });
});
```

## Coverage

Run `npm run test:coverage` to generate a coverage report. The report is saved to `tests/frontend/coverage/`.

Current coverage thresholds (defined in `jest.config.js`):
- Statements: 10%
- Branches: 10%
- Functions: 10%
- Lines: 10%

These are starter thresholds; increase them as test coverage improves.

## CI/CD Integration

To integrate with CI/CD, add a step to run frontend tests:

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

## Troubleshooting

### "ReferenceError: [Name] is not defined"

Ensure you're calling `loadScript()` in `beforeEach()`, not at the top level. The setup file clears globals between tests.

### DOM elements not found

Set up required DOM elements before loading the script. Many scripts attach event listeners on load.

### Fetch not mocked

The global `fetch` mock is set up in `setup.js`. If you need custom behavior, use `mockResolvedValueOnce()` or `mockRejectedValueOnce()`.
