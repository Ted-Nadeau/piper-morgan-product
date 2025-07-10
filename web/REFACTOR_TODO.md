# Response Path Unification Refactor

**Context**: Currently there are two disconnected response paths in `web/app.py` that handle bot messages inconsistently, leading to formatting bugs and code duplication.

## Problem
- **Direct Response Path** (line ~370): Has markdown rendering, debug logging
- **Workflow Response Path** (line ~310): Originally missing markdown rendering, different formatting logic
- This causes inconsistent UX and maintenance burden

## Refactor Tasks

### Task 1: Create Unified Response Handler
- [ ] **File**: `web/app.py`
- [ ] **Location**: Add after line 189 (after sessionId declaration)
- [ ] **Action**: Create new function `displayBotMessage(message, isSuccess = true, isThinking = false)`
- [ ] **Implementation**:
  ```javascript
  function displayBotMessage(message, isSuccess = true, isThinking = false) {
      // Apply markdown rendering if function exists
      let processedMessage = message;
      if (typeof renderMarkdown === 'function' && !isThinking) {
          processedMessage = renderMarkdown(message);
      }
      
      // Return formatted HTML with consistent styling
      const cssClass = isThinking ? 'thinking' : (isSuccess ? 'success' : 'error');
      return `<div class="result ${cssClass}">${processedMessage}</div>`;
  }
  ```

### Task 2: Refactor Direct Response Path
- [ ] **File**: `web/app.py`  
- [ ] **Location**: Lines ~367-378 (direct response handling)
- [ ] **Action**: Replace existing logic with unified handler
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
      thinkingDiv.innerHTML = result.message; // Fallback to raw
  }
  ```
- [ ] **After**:
  ```javascript
  // Debug logging (keep for now)
  console.log('Direct response:', result.message);
  
  thinkingDiv.innerHTML = displayBotMessage(result.message, true);
  ```

### Task 3: Refactor Workflow Response Path
- [ ] **File**: `web/app.py`
- [ ] **Location**: Lines ~311-338 (workflow completion handling)  
- [ ] **Action**: Replace complex conditional logic with unified handler
- [ ] **Before**: Complex if/else with different message processing
- [ ] **After**: 
  ```javascript
  if (data.status === 'completed') {
      console.log('Workflow response:', data.message);
      
      if (data.type === 'analyze_file' || data.type === 'generate_report') {
          finalHTML = displayBotMessage(data.message || 'File analysis completed successfully!');
      } else {
          // GitHub issue logic (keep existing)
          const finalResult = data.tasks && data.tasks[data.tasks.length - 1]?.result?.issue;
          if (finalResult && finalResult.url) {
              finalHTML = `<div class="result success">
                  <strong>✅ GitHub Issue Created!</strong><br>
                  <strong>#${finalResult.number}:</strong> ${finalResult.title}<br>
                  <strong>URL:</strong> <a href="${finalResult.url}" target="_blank">View on GitHub</a>
              </div>`;
          } else {
              finalHTML = displayBotMessage(data.message || 'Workflow completed successfully!');
          }
      }
  }
  ```

### Task 4: Update Error Handling
- [ ] **File**: `web/app.py`
- [ ] **Location**: Lines ~376-382 (error handling in direct path)
- [ ] **Action**: Use unified handler for errors
- [ ] **Replace**: 
  ```javascript
  thinkingDiv.innerHTML = `<div class="result error">...</div>`;
  ```
- [ ] **With**:
  ```javascript
  thinkingDiv.innerHTML = displayBotMessage(error.message, false);
  ```

### Task 5: Update Thinking/Loading States
- [ ] **File**: `web/app.py`
- [ ] **Location**: Lines where "Thinking..." is set
- [ ] **Action**: Use unified handler for thinking states
- [ ] **Implementation**:
  ```javascript
  const thinkingDiv = appendMessage('Thinking...');
  thinkingDiv.innerHTML = displayBotMessage('Thinking...', true, true);
  thinkingDiv.classList.add('thinking');
  ```

### Task 6: Clean Up Debug Logging (Optional)
- [ ] **File**: `web/app.py`
- [ ] **Action**: Remove or consolidate debug console.log statements
- [ ] **Keep**: Core functionality logging
- [ ] **Remove**: Redundant "renderMarkdown function exists" checks

## Testing Checklist
- [ ] Test direct API responses (simple queries)
- [ ] Test workflow responses (file summarization)  
- [ ] Test error responses
- [ ] Test thinking/loading states
- [ ] Verify markdown rendering works in all paths
- [ ] Check browser console for any JavaScript errors

## Success Criteria
- [ ] ✅ Consistent markdown rendering across all response types
- [ ] ✅ Reduced code duplication
- [ ] ✅ Easier maintenance (single function to update)
- [ ] ✅ Same UX regardless of response path
- [ ] ✅ All existing functionality preserved

**Estimated Time**: 30-45 minutes
**Priority**: High (fixes user-facing bugs)
**Dependencies**: Current markdown rendering fix must be working