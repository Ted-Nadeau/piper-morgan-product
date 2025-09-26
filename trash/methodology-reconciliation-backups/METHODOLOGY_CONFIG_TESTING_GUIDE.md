# Methodology Configuration Service - Cross-Validation Guide

## Quick Cross-Validation Commands for Cursor Agent

### 1. Verify Implementation Exists
```bash
# Check service implementation
ls -la services/infrastructure/config/methodology_configuration.py

# Check test implementation
ls -la tests/infrastructure/config/test_methodology_configuration.py

# Verify classes importable
PYTHONPATH=. python -c "from services.infrastructure.config.methodology_configuration import get_methodology_config_service; print('✅ Import successful')"
```

### 2. Run Test Suite
```bash
# Run all methodology configuration tests
PYTHONPATH=. python -m pytest tests/infrastructure/config/test_methodology_configuration.py -v

# Expected: 15 PASSED, 2 warnings (thread stress test warnings are expected)
```

### 3. Test Basic Functionality
```bash
# Test basic service creation and configuration
PYTHONPATH=. python -c "
from services.infrastructure.config.methodology_configuration import get_methodology_config_service
service = get_methodology_config_service()
config = service.get_config()
print(f'Enforcement Level: {config.handoff_enforcement_level}')
print(f'Preferred Agents: {config.preferred_agents}')
print(f'Evidence Collection: {config.evidence_collection}')
print('✅ Basic functionality working')
"
```

### 4. Test PIPER.user.md Integration
```bash
# Create test config file
cat > test_config.md << 'EOF'
# Test Configuration

\`\`\`yaml
methodology:
  handoff_protocol:
    enforcement_level: "STRICT"
    verification_required: true
  agent_coordination:
    preferred_agents: ["Code", "Cursor"]
    multi_agent_threshold: 5
  verification_pyramid:
    evidence_collection: "MANDATORY"
\`\`\`
EOF

# Test loading configuration
PYTHONPATH=. python -c "
from services.infrastructure.config.methodology_configuration import MethodologyConfigurationService
from pathlib import Path
service = MethodologyConfigurationService()
service.load_from_file('test_config.md')
config = service.get_config()
print(f'Loaded Enforcement: {config.handoff_enforcement_level}')
print(f'Loaded Threshold: {config.multi_agent_threshold}')
print('✅ PIPER.user.md integration working')
"

# Cleanup
rm test_config.md
```

### 5. Test PM-138 Compatibility
```bash
# Test PM-138 mandatory handoff protocol compatibility
PYTHONPATH=. python -c "
from services.infrastructure.config.methodology_configuration import get_methodology_config_service, MethodologyValidationLevel
service = get_methodology_config_service()
result = service.validate(MethodologyValidationLevel.FULL)
print(f'PM-138 Compatible: {result.pm138_compatibility_result}')
print(f'Overall Valid: {result.is_valid()}')
if result.pm138_compatibility_result:
    print('✅ PM-138 compatibility validated')
else:
    print('❌ PM-138 compatibility failed')
    print(f'Errors: {result.errors}')
"
```

### 6. Performance Validation
```bash
# Test configuration access performance
PYTHONPATH=. python -c "
import time
from services.infrastructure.config.methodology_configuration import get_methodology_config_service
service = get_methodology_config_service()

start_time = time.time()
for i in range(1000):
    config = service.get_config()
end_time = time.time()

avg_time = (end_time - start_time) / 1000 * 1000  # Convert to ms
print(f'1000 reads in {(end_time - start_time)*1000:.1f}ms')
print(f'Average per read: {avg_time:.3f}ms')
print(f'Performance target (<1ms): {\"✅ PASS\" if avg_time < 1 else \"❌ FAIL\"}')
"
```

## Comprehensive Cross-Validation Scenarios

### Scenario 1: Team Configuration Loading
Test different team configurations work correctly:

1. **Strict Enforcement Team**:
   ```yaml
   methodology:
     handoff_protocol:
       enforcement_level: "STRICT"
       verification_required: true
   ```

2. **Progressive Enforcement Team**:
   ```yaml
   methodology:
     handoff_protocol:
       enforcement_level: "PROGRESSIVE"
       verification_required: true
   ```

3. **Multi-Agent Focused Team**:
   ```yaml
   methodology:
     agent_coordination:
       multi_agent_threshold: 2
       preferred_agents: ["Code", "Cursor", "Lead", "Chief"]
   ```

### Scenario 2: Validation Levels
Test all three validation levels work:

```bash
PYTHONPATH=. python -c "
from services.infrastructure.config.methodology_configuration import get_methodology_config_service, MethodologyValidationLevel
service = get_methodology_config_service()

for level in [MethodologyValidationLevel.BASIC, MethodologyValidationLevel.ENHANCED, MethodologyValidationLevel.FULL]:
    result = service.validate(level)
    print(f'{level.value}: Valid={result.is_valid()}, Errors={len(result.errors)}')
"
```

### Scenario 3: Configuration Change Events
Test event notification system:

```bash
PYTHONPATH=. python -c "
from services.infrastructure.config.methodology_configuration import get_methodology_config_service
service = get_methodology_config_service()

events = []
def event_handler(key, old_value, new_value):
    events.append(f'{key}: {old_value} -> {new_value}')

service.subscribe_to_changes(event_handler)
service.update_config({'handoff_enforcement_level': 'ADVISORY'})
print(f'Events captured: {len(events)}')
for event in events:
    print(f'  {event}')
"
```

## Expected Results Summary

| Test | Expected Result | Success Criteria |
|------|----------------|------------------|
| Import Test | ✅ Import successful | No import errors |
| Test Suite | 15 PASSED, 2 warnings | All tests pass |
| Basic Functionality | Config values displayed | Service creates and returns config |
| PIPER.user.md Integration | Loaded values displayed | Configuration loaded from YAML |
| PM-138 Compatibility | ✅ PM-138 compatibility validated | Validation passes |
| Performance | <1ms per read | Performance under target |

## Cross-Validation Checklist

- [ ] **Implementation files exist**: Both service and test files present
- [ ] **Imports work**: No import errors when loading service
- [ ] **Tests pass**: 15/15 tests passing with expected warnings only
- [ ] **Basic functionality**: Service creates, loads, and returns configurations
- [ ] **YAML integration**: PIPER.user.md methodology sections load correctly
- [ ] **Validation system**: All three validation levels work (BASIC/ENHANCED/FULL)
- [ ] **Event system**: Configuration changes trigger event notifications
- [ ] **Performance**: Configuration access under 1ms per operation
- [ ] **PM-138 compatibility**: Mandatory handoff protocol enforcement preserved
- [ ] **Thread safety**: Concurrent access works without errors
- [ ] **Hot-reload**: File modification detection and automatic reload working

## Failure Analysis Protocol

If any test fails, provide:

1. **Exact terminal output** showing the failure
2. **Specific error messages** with full stack traces
3. **Performance metrics** if performance tests fail
4. **Configuration values** that were loaded/expected vs actual
5. **PM-138 compatibility details** if validation fails

This enables rapid debugging and fixes based on concrete evidence.

## Ready for Production Deployment

Once cross-validation is complete with all checks passing, the MethodologyConfigurationService is ready for:

1. **Integration with AgentBridge** for agent coordination
2. **FTUX wizard implementation** for user onboarding
3. **PM-138 enhancement** with configurable enforcement levels
4. **Team-specific methodology customization** while preserving verification requirements
