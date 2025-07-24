# Handoff Prompt - PM-021 List Projects Workflow Completion

**Date**: July 23, 2025
**Time**: 4:30 PM Pacific
**From**: Cursor Assistant (PM-021 Implementation Session)
**To**: Successor for PM-021 Completion Session

---

## 🎯 **PM-021 STATUS: 85% COMPLETE - ERROR HANDLING ISSUE REMAINING**

### **Current Session Achievements (10:00 AM - 4:30 PM Pacific)**

#### **🚀 PM-021 Core Implementation Complete** ✅

- **Workflow Factory Mapping**: `list_projects` intent → `WorkflowType.LIST_PROJECTS`
- **Task Type Addition**: `LIST_PROJECTS` added to `TaskType` enum
- **Engine Handler**: `_list_projects` method implemented with proper error handling
- **Database Integration**: Uses `ProjectRepository.list_active_projects()` with session management
- **Error Handling**: Returns `TaskResult(success=False, error=f"Project listing error: {str(e)}")`

#### **📋 Comprehensive Test Suite Complete** ✅

- **Test File**: `tests/domain/test_pm021_list_projects_workflow.py` (224 lines)
- **6 Test Scenarios**: 5 passing, 1 failing
- **Mock Infrastructure**: Proper `mock_project_repository` and `sample_projects` fixtures
- **Intent Mapping**: Validated `list_projects`, `list_all_projects`, `show_projects` → `LIST_PROJECTS`
- **Error Scenario Testing**: Database connection failure simulation
- **Context Preservation**: Validated workflow context maintenance

#### **🔍 Debug Infrastructure Established** ✅

- **Debug Script**: `debug_test.py` for isolated error investigation
- **Error Analysis**: Identified TaskFailedError handling issue in engine
- **Traceback Analysis**: Detailed investigation of error propagation flow

---

## 🚨 **CRITICAL ISSUE: ERROR HANDLING BUG**

### **Problem Summary**

- **Test**: `test_list_projects_error_handling` is failing
- **Expected**: `"Project listing error: Database connection failed"` in `exc_info.value.details["error"]`
- **Actual**: `KeyError: 'error'` - error message is in `exc_info.value.details["original_error"]`

### **Root Cause Analysis**

The TaskFailedError is being caught by the general exception handler and re-wrapped, causing the error message to be moved from `"error"` to `"original_error"` in the details dictionary.

### **Error Flow (Current Buggy State)**

1. `_list_projects` returns correct TaskResult with error message ✅
2. Engine sets `task.error = result.error` ✅
3. TaskFailedError raised with `details={"task_id": task.id, "error": task.error}` ✅
4. **BUG**: TaskFailedError gets caught by general exception handler ❌
5. **BUG**: General handler creates new TaskFailedError with `details={"original_error": str(e)}` ❌

### **Debug Evidence**

```
result = TaskResult(
    success=False,
    output_data=None,
    error='Project listing error: Database connection failed'
)
```

But `task.error` becomes `'API Error [TASK_FAILED]'` instead of the original error message.

---

## 🎯 **IMMEDIATE PRIORITIES FOR NEXT SESSION**

### **Priority 1: Fix Error Handling Bug** 🔧

#### **Investigation Steps**

1. **Examine `_execute_task` method** in `services/orchestration/engine.py`
2. **Identify why TaskFailedError is caught** by general exception handler
3. **Check exception handling flow** around lines 312-353
4. **Verify exception hierarchy** - TaskFailedError should not be caught by general handler

#### **Expected Fix**

- Ensure TaskFailedError is not caught by general exception handler
- Preserve original error message in `details["error"]` field
- Maintain proper error propagation flow

#### **Files to Focus On**

- `services/orchestration/engine.py` (lines 285-360)
- `services/api/errors.py` (TaskFailedError definition)
- `tests/domain/test_pm021_list_projects_workflow.py` (line 175 - test assertion)

### **Priority 2: Complete PM-021 Implementation** ✅

#### **Validation Steps**

1. **Run failing test**: `python -m pytest tests/domain/test_pm021_list_projects_workflow.py::TestPM021ListProjectsWorkflow::test_list_projects_error_handling -v`
2. **Fix error handling issue** based on investigation
3. **Run full test suite**: `python -m pytest tests/domain/test_pm021_list_projects_workflow.py -v`
4. **Verify all 6 tests pass** consistently

#### **Success Criteria**

- All 6 PM-021 tests pass ✅
- Error handling works correctly in production scenarios ✅
- Workflow can handle database connection failures gracefully ✅

### **Priority 3: Production Validation** 🚀

#### **End-to-End Testing**

1. **Test with real database** to validate workflow
2. **Verify error scenarios** work correctly
3. **Test intent mapping** with various natural language inputs
4. **Validate context preservation** during workflow execution

---

## 📁 **KEY FILES AND LOCATIONS**

### **Implementation Files**

- `services/orchestration/engine.py`: `_list_projects` method (lines 884-905)
- `services/domain/models.py`: `LIST_PROJECTS` enum addition
- `services/orchestration/workflow_factory.py`: Intent mapping

### **Test Files**

- `tests/domain/test_pm021_list_projects_workflow.py`: Complete test suite
- `debug_test.py`: Debug script for error investigation

### **Error Handling Investigation**

- `services/orchestration/engine.py`: `_execute_task` method (lines 285-360)
- `services/api/errors.py`: TaskFailedError class definition

---

## 🔧 **DEBUGGING TOOLS AVAILABLE**

### **Debug Script**

```bash
python debug_test.py
```

This script reproduces the error handling issue in isolation.

### **Test Commands**

```bash
# Run failing test
python -m pytest tests/domain/test_pm021_list_projects_workflow.py::TestPM021ListProjectsWorkflow::test_list_projects_error_handling -v

# Run all PM-021 tests
python -m pytest tests/domain/test_pm021_list_projects_workflow.py -v
```

### **Error Investigation Commands**

```bash
# Check TaskFailedError definition
grep -A 10 "class TaskFailedError" services/api/errors.py

# Check exception handling in engine
sed -n '310,320p' services/orchestration/engine.py
sed -n '350,365p' services/orchestration/engine.py
```

---

## 🎯 **SUCCESS METRICS**

### **Immediate Success**

- ✅ All 6 PM-021 tests pass
- ✅ Error handling preserves original error messages
- ✅ TaskFailedError is not re-wrapped by general exception handler

### **Completion Criteria**

- ✅ PM-021 workflow is 100% functional
- ✅ Error handling works correctly in all scenarios
- ✅ Ready for production deployment
- ✅ Comprehensive test coverage maintained

---

## 🚀 **STRATEGIC CONTEXT**

**PM-021** is a foundational workflow that enables users to list projects from the database using natural language. This is a core PM functionality that will be used frequently.

**Current Status**: 85% complete with a clear, isolated error handling issue that needs fixing.

**Impact**: Once complete, this provides the foundation for other project-related workflows and demonstrates the workflow orchestration pattern for future implementations.

---

**Handoff Complete**: 4:30 PM Pacific
**Next Session Goal**: Complete PM-021 implementation by fixing error handling issue
**Expected Duration**: 1-2 hours to resolve the error handling bug and validate completion
