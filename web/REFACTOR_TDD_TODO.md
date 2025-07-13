# Response Path Unification - DDD TDD Refactor

## Domain Analysis

**Domain**: Web UI Response Handling
**Aggregate Root**: BotMessage
**Problem**: Two disconnected paths for rendering bot responses leading to inconsistent UX

**Current Architecture Issues:**
- Violation of DRY principle (Don't Repeat Yourself)
- Inconsistent message formatting across response types
- Scattered business logic for message rendering

## Domain Model

```typescript
// Domain concept we're implementing
interface BotMessage {
    content: string;
    type: 'success' | 'error' | 'thinking';
    isMarkdownEnabled: boolean;
    render(): string;
}
```

## TDD Refactor Steps

### Phase 1: Red Phase - Write Failing Tests

#### Test 1: Create Message Renderer Test
- [ ] **File**: `web/test-message-renderer.js`
- [ ] **Test**: Message renderer function exists and handles basic cases
- [ ] **Implementation**:
```javascript
// Test framework
function test(name, fn) {
    try {
        fn();
        console.log(`✅ ${name}`);
    } catch (error) {
        console.error(`❌ ${name}: ${error.message}`);
    }
}

function assertEqual(actual, expected, message) {
    if (actual !== expected) {
        throw new Error(`${message}: expected "${expected}", got "${actual}"`);
    }
}

// Test cases
test('renderBotMessage exists', () => {
    assertEqual(typeof renderBotMessage, 'function', 'renderBotMessage should be a function');
});

test('renders success message with markdown', () => {
    const result = renderBotMessage('# Hello **World**', 'success', false);
    assertEqual(result.includes('<h1>'), true, 'Should render markdown headers');
    assertEqual(result.includes('<strong>'), true, 'Should render markdown bold');
    assertEqual(result.includes('result success'), true, 'Should have success CSS class');
});

test('renders error message without markdown', () => {
    const result = renderBotMessage('Error: Something failed', 'error', false);
    assertEqual(result.includes('<h1>'), false, 'Should not render markdown in errors');
    assertEqual(result.includes('result error'), true, 'Should have error CSS class');
});

test('renders thinking message as-is', () => {
    const result = renderBotMessage('Thinking...', 'success', true);
    assertEqual(result.includes('thinking'), true, 'Should have thinking CSS class');
    assertEqual(result, 'Thinking...', 'Should not process thinking messages');
});
```

#### Test 2: Create Integration Test
- [ ] **File**: `web/test-response-integration.js`
- [ ] **Test**: Both response paths use the same renderer
- [ ] **Implementation**:
```javascript
// Mock DOM elements
const mockElements = {
    direct: { innerHTML: '', classList: { add: () => {}, remove: () => {} } },
    workflow: { innerHTML: '', classList: { add: () => {}, remove: () => {} } }
};

test('direct response path uses unified renderer', () => {
    // Simulate direct response
    simulateDirectResponse('# Test Response', mockElements.direct);
    assertEqual(mockElements.direct.innerHTML.includes('<h1>'), true, 'Direct path should render markdown');
});

test('workflow response path uses unified renderer', () => {
    // Simulate workflow response
    simulateWorkflowResponse('# Test Response', mockElements.workflow);
    assertEqual(mockElements.workflow.innerHTML.includes('<h1>'), true, 'Workflow path should render markdown');
});

test('both paths produce identical output', () => {
    const message = '# Test\n**Bold** text';
    simulateDirectResponse(message, mockElements.direct);
    simulateWorkflowResponse(message, mockElements.workflow);
    assertEqual(mockElements.direct.innerHTML, mockElements.workflow.innerHTML, 'Both paths should produce identical output');
});
```

### Phase 2: Green Phase - Implement Unified Renderer

#### Step 1: Create Domain-Driven Message Renderer
- [ ] **File**: `web/app.py`
- [ ] **Location**: After line 197 (after DOMContentLoaded)
- [ ] **Implementation**:
```javascript
/**
 * Domain-driven bot message renderer
 * Encapsulates all message rendering logic in one place
 * @param {string} content - The message content
 * @param {string} type - 'success', 'error', 'thinking'
 * @param {boolean} isThinking - Whether this is a thinking/loading state
 * @returns {string} - Rendered HTML
 */
function renderBotMessage(content, type = 'success', isThinking = false) {
    // Guard clauses
    if (!content) return '';
    if (isThinking) return content; // Don't process thinking messages

    // Domain logic: Apply markdown only to success messages
    let processedContent = content;
    if (type === 'success' && typeof marked !== 'undefined') {
        try {
            processedContent = marked.parse(content);
        } catch (error) {
            console.warn('Markdown parsing failed:', error);
            processedContent = content; // Fallback to raw content
        }
    }

    // Domain logic: Apply consistent CSS classes
    const cssClasses = ['result', type];
    if (isThinking) cssClasses.push('thinking');

    return `<div class="${cssClasses.join(' ')}">${processedContent}</div>`;
}
```

#### Step 2: Create Response Path Abstractions
- [ ] **File**: `web/app.py`
- [ ] **Location**: After renderBotMessage function
- [ ] **Implementation**:
```javascript
/**
 * Handle direct API responses
 * @param {Object} result - API response object
 * @param {HTMLElement} element - DOM element to update
 */
function handleDirectResponse(result, element) {
    console.log('Direct response:', result.message);
    element.innerHTML = renderBotMessage(result.message, 'success', false);
}

/**
 * Handle workflow completion responses
 * @param {Object} data - Workflow data object
 * @param {HTMLElement} element - DOM element to update
 */
function handleWorkflowResponse(data, element) {
    console.log('Workflow response:', data.message);

    if (data.type === 'analyze_file' || data.type === 'generate_report') {
        const message = data.message || 'File analysis completed successfully!';
        element.innerHTML = renderBotMessage(message, 'success', false);
    } else {
        // GitHub issue logic (keep existing special case)
        const finalResult = data.tasks && data.tasks[data.tasks.length - 1]?.result?.issue;
        if (finalResult && finalResult.url) {
            element.innerHTML = `
                <div class="result success">
                    <strong>✅ GitHub Issue Created!</strong><br>
                    <strong>#${finalResult.number}:</strong> ${finalResult.title}<br>
                    <strong>URL:</strong> <a href="${finalResult.url}" target="_blank">View on GitHub</a>
                </div>`;
        } else {
            const message = data.message || 'Workflow completed successfully!';
            element.innerHTML = renderBotMessage(message, 'success', false);
        }
    }
}

/**
 * Handle error responses
 * @param {Error} error - Error object
 * @param {HTMLElement} element - DOM element to update
 */
function handleErrorResponse(error, element) {
    console.error('Error response:', error.message);
    element.innerHTML = renderBotMessage(error.message, 'error', false);
}
```

### Phase 3: Blue Phase - Refactor Existing Code

#### Step 3: Replace Direct Response Path
- [ ] **File**: `web/app.py`
- [ ] **Location**: Lines ~366-378 (in chatForm event listener)
- [ ] **Before**:
```javascript
// Debug logging
console.log('Raw result.message:', result.message);
console.log('renderMarkdown function exists:', typeof renderMarkdown === 'function');

if (typeof renderMarkdown === 'function') {
    const rendered = renderMarkdown(result.message);
    console.log('Rendered output:', rendered);
    thinkingDiv.innerHTML = rendered;
} else {
    console.error('renderMarkdown function not found!');
    thinkingDiv.innerHTML = result.message;
}
```
- [ ] **After**:
```javascript
handleDirectResponse(result, thinkingDiv);
```

#### Step 4: Replace Workflow Response Path
- [ ] **File**: `web/app.py`
- [ ] **Location**: Lines ~305-342 (in pollWorkflowStatus function)
- [ ] **Before**: Complex conditional logic for workflow completion
- [ ] **After**:
```javascript
if (data.status === 'completed') {
    handleWorkflowResponse(data, elementToUpdate);
} else {
    elementToUpdate.innerHTML = renderBotMessage(`Workflow Failed: ${data.message}`, 'error', false);
}
```

#### Step 5: Replace Error Handling
- [ ] **File**: `web/app.py`
- [ ] **Location**: Lines ~379-384 (error catch block)
- [ ] **Before**:
```javascript
thinkingDiv.innerHTML = `
    <div class="result error">
        <strong>❌ Error</strong><br>
        ${error.message}
    </div>`;
```
- [ ] **After**:
```javascript
handleErrorResponse(error, thinkingDiv);
```

### Phase 4: Integration Testing

#### Test 3: Run Integration Tests
- [ ] **Action**: Load test files in browser
- [ ] **URL**: `http://localhost:8081/test-message-renderer.js`
- [ ] **URL**: `http://localhost:8081/test-response-integration.js`
- [ ] **Expected**: All tests pass

#### Test 4: Manual Testing
- [ ] **Test Case 1**: Direct response (simple query)
  - [ ] Action: Ask "Hello, how are you?"
  - [ ] Expected: Response renders with proper formatting

- [ ] **Test Case 2**: Workflow response (file analysis)
  - [ ] Action: "Please summarize that file I uploaded recently"
  - [ ] Expected: Markdown renders properly (headers, bullets, bold)

- [ ] **Test Case 3**: Error response
  - [ ] Action: Trigger an error condition
  - [ ] Expected: Error displays without markdown processing

- [ ] **Test Case 4**: Thinking state
  - [ ] Action: Submit any query
  - [ ] Expected: "Thinking..." shows without markdown processing

### Phase 5: Cleanup

#### Step 6: Remove Obsolete Code
- [ ] **File**: `web/app.py`
- [ ] **Action**: Remove old renderMarkdown function definition (if any)
- [ ] **Action**: Remove redundant debug logging
- [ ] **Action**: Remove unused CSS classes or consolidate

#### Step 7: Update Documentation
- [ ] **File**: `web/REFACTOR_TDD_TODO.md`
- [ ] **Action**: Add completion notes and any lessons learned
- [ ] **Action**: Document the new architecture for future developers

## Success Criteria

### Functional Requirements
- [ ] ✅ All response types render markdown consistently
- [ ] ✅ Error messages don't process markdown
- [ ] ✅ Thinking states don't process markdown
- [ ] ✅ GitHub issue responses maintain special formatting
- [ ] ✅ No JavaScript errors in browser console

### Non-Functional Requirements
- [ ] ✅ Code is DRY (no duplication)
- [ ] ✅ Single responsibility principle (one function per concern)
- [ ] ✅ Consistent error handling
- [ ] ✅ Maintainable (easy to modify message rendering)
- [ ] ✅ Testable (isolated functions)

### Domain Model Validation
- [ ] ✅ Message rendering logic is encapsulated
- [ ] ✅ Response path logic is abstracted
- [ ] ✅ Error handling is consistent
- [ ] ✅ Business rules are clearly expressed in code

## Rollback Plan

If tests fail or issues arise:
1. **Immediate**: Comment out new functions, restore old code
2. **Debug**: Use browser console to identify specific failures
3. **Incremental**: Apply changes one function at a time
4. **Validate**: Test each change before proceeding to next

## Time Estimate

- **Phase 1 (Tests)**: 15 minutes
- **Phase 2 (Implementation)**: 20 minutes
- **Phase 3 (Refactor)**: 15 minutes
- **Phase 4 (Testing)**: 10 minutes
- **Phase 5 (Cleanup)**: 5 minutes

**Total**: ~65 minutes with testing
**Critical Path**: Message renderer implementation
