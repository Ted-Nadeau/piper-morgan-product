# Domain/Database Field Mappings

This documents field mappings between domain models and database models where field names differ.

## Field Name Mappings

### WorkItem Model
- Domain: `metadata: Dict[str, Any]`
- Database: `item_metadata: Column(JSON)`
- Mapping: Handled in `to_domain()` and `from_domain()` conversion methods

### UploadedFile Model
- Domain: `metadata: Dict[str, Any]` and `file_metadata: Dict[str, Any]`
- Database: `file_metadata: Column(JSON)`
- Mapping: Domain `metadata` maps to database `file_metadata`

### Workflow Model
- Domain: `intent_id: Optional[str]`
- Database: Relationship via `Intent.workflow_id` (reverse relationship)
- Mapping: `intent_id` populated through relationship in conversion methods

## Schema Validator Notes

The PM-056 schema validator currently reports these as critical errors because it performs direct field name matching. The conversion methods properly handle the mappings, so these "errors" are actually false positives.

Future enhancement: Update validator to understand field mappings defined in conversion methods.
