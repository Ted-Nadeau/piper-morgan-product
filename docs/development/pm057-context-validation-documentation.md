# PM-057 Context Validation Documentation

## Overview

The PM-057 Context Validation system enhances the WorkflowFactory with pre-execution validation to prevent workflow failures by ensuring required context is available before workflow creation.

## Purpose

- **Prevent Workflow Failures**: Validates context before workflow execution
- **User Experience**: Provides clear error messages and helpful suggestions
- **Fail-fast Approach**: Raises errors early to prevent downstream issues
- **Performance Optimization**: Configurable validation performance thresholds

## Architecture

### Validation Registry

The WorkflowFactory maintains a validation registry that defines requirements for each WorkflowType:

```python
validation_registry = {
    WorkflowType.CREATE_TICKET: {
        "context_requirements": {
            "critical": ["original_message"],
            "important": ["project_id", "repository"],
            "optional": ["labels", "priority", "assignee"]
        },
        "performance_threshold_ms": 50,
        "pre_execution_checks": ["project_resolution", "repository_access"]
    }
}
```

### Field Categories

- **Critical Fields**: Required for workflow execution (raises error if missing)
- **Important Fields**: Recommended for optimal execution (warns if missing)
- **Optional Fields**: Nice to have but not required

## Usage

### Automatic Validation

Context validation is automatically performed in `WorkflowFactory.create_from_intent()`:

```python
# Validation happens automatically
workflow = workflow_factory.create_from_intent(intent, project_context)
```

### Manual Validation

```python
from services.orchestration.workflow_factory import WorkflowFactory
from services.orchestration.validation import ContextValidationError

workflow_factory = WorkflowFactory()

try:
    workflow_factory._validate_workflow_context(
        WorkflowType.CREATE_TICKET,
        intent,
        project_context
    )
except ContextValidationError as e:
    print(f"Validation failed: {e.user_message}")
```

## Workflow Type Requirements

### CREATE_TICKET

**Critical Fields:**
- `original_message`: User's request message

**Important Fields:**
- `project_id`: Project identifier for context
- `repository`: Repository name or URL

**Optional Fields:**
- `labels`: Issue labels
- `priority`: Issue priority
- `assignee`: Assigned person

### LIST_PROJECTS

**Critical Fields:**
- `original_message`: User's request message

**Optional Fields:**
- `filter_criteria`: Project filtering criteria
- `sort_order`: Project sorting order

### ANALYZE_FILE

**Critical Fields:**
- `original_message`: User's request message

**Important Fields:**
- `file_id`: File identifier
- `resolved_file_id`: Resolved file identifier

**Optional Fields:**
- `analysis_type`: Type of analysis to perform
- `depth_level`: Analysis depth

### GENERATE_REPORT

**Critical Fields:**
- `original_message`: User's request message

**Important Fields:**
- `data_source`: Source of data for report

**Optional Fields:**
- `report_format`: Desired report format
- `include_charts`: Whether to include charts

## Error Handling

### ContextValidationError

The system raises `ContextValidationError` with user-friendly messages:

```python
class ContextValidationError(APIError):
    def __init__(
        self,
        workflow_type: WorkflowType,
        missing_fields: List[str],
        suggestions: List[str],
        details: Dict[str, Any] = None
    ):
        # Creates user-friendly error message
        self.user_message = self._create_user_message(workflow_type, missing_fields, suggestions)
```

### User-Friendly Messages

The system generates contextual error messages:

- **Missing original_message**: "To create a ticket, I need to know what you want me to do. Please provide more details about your request."
- **Missing project_id**: "To create a ticket, I need to know which project. Try: 'create ticket for project [project name]'"
- **Missing file_id**: "To analyze a file, I need to know which file to analyze. Try: 'analyze the uploaded [filename]'"

## Performance Thresholds

Each workflow type has configurable performance thresholds:

```python
def get_performance_threshold(self, workflow_type: WorkflowType) -> int:
    """Get performance threshold for validation in milliseconds"""
    requirements = self.get_validation_requirements(workflow_type)
    return requirements.get("performance_threshold_ms", 100) if requirements else 100
```

## Testing

### Running Tests

```bash
# Run context validation tests
pytest tests/validation/test_pm057_context_validation.py -v

# Run with coverage
pytest tests/validation/test_pm057_context_validation.py --cov=services.orchestration.workflow_factory
```

### Test Scenarios

The test suite covers:

- **Validation Requirements**: Registration and retrieval of requirements
- **Field Validation**: Critical, important, and optional field validation
- **Error Messages**: User-friendly error message generation
- **Integration Scenarios**: End-to-end workflow creation with validation
- **Performance**: Validation performance and thresholds

## Integration

### WorkflowFactory Integration

Context validation is integrated into the workflow creation process:

```python
async def create_from_intent(self, intent: Intent, project_context: Optional[Dict[str, Any]] = None) -> Optional[Workflow]:
    # PM-057: Pre-execution context validation
    try:
        self._validate_workflow_context(workflow_type, intent, project_context)
        print(f"  ✅ Context validation passed")
    except ContextValidationError as e:
        print(f"  ❌ Context validation failed: {e.user_message}")
        raise e

    # Continue with workflow creation...
```

### API Integration

Context validation errors are handled by the API error middleware:

```python
# services/api/errors.py
"CONTEXT_VALIDATION_FAILED": "Context validation failed: {details}",
```

## Configuration

### Adding New Workflow Types

1. Add validation requirements to `_register_validation_requirements()`:

```python
WorkflowType.NEW_WORKFLOW: {
    "context_requirements": {
        "critical": ["required_field"],
        "important": ["important_field"],
        "optional": ["optional_field"]
    },
    "performance_threshold_ms": 75,
    "pre_execution_checks": ["custom_check"]
}
```

2. Add workflow mapping to `_register_default_workflows()`:

```python
"new_workflow_action": WorkflowType.NEW_WORKFLOW,
```

3. Add tests for the new workflow type.

### Custom Field Validation

Extend field validation logic in `_field_exists_and_valid()`:

```python
def _field_exists_and_valid(self, context: Dict[str, Any], field: str) -> bool:
    # Add custom validation logic here
    if field == "custom_field":
        return self._validate_custom_field(context[field])
    return super()._field_exists_and_valid(context, field)
```

## Monitoring

### Validation Metrics

Track validation performance and success rates:

```python
# Add to validation method
self.metrics.record_context_validation(
    workflow_type=workflow_type,
    success=True,
    validation_time_ms=validation_time
)
```

### Logging

Context validation events are logged for debugging:

```python
logger.log_behavior_pattern(
    "context_validation",
    {
        "workflow_type": workflow_type.value,
        "missing_fields": missing_critical,
        "validation_time_ms": validation_time
    }
)
```

## Troubleshooting

### Common Issues

1. **Missing Critical Fields**: Ensure all critical fields are provided in intent context
2. **Performance Issues**: Adjust performance thresholds for complex validations
3. **Error Message Clarity**: Update suggestion generation for better user experience
4. **Workflow Type Mapping**: Verify workflow type is correctly mapped from intent action

### Debug Mode

Enable debug output for validation:

```python
# Add debug flag to WorkflowFactory
workflow_factory.debug = True
workflow_factory.create_from_intent(intent)
```

## Related Documentation

- [PM-057 Issue](https://github.com/mediajunkie/piper-morgan-product/issues/26)
- WorkflowFactory Documentation - needed
- [API Reference](../architecture/api-reference.md)
- [Intent Classification Patterns](../architecture/intent-patterns.md)
