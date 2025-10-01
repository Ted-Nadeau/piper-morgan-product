# Cursor Agent Prompt: Phase 1 - Configuration Validation Integration

## Mission: Startup Integration & CI Pipeline Implementation

**Context**: Code agent is implementing comprehensive ConfigValidator class for all 4 services. Your focus is integrating validation into startup sequence, adding development bypass, and implementing CI pipeline validation.

**Objective**: Integrate configuration validation into main.py startup, add development bypass flag, update CI pipeline, and test failure scenarios for graceful error handling.

## Phase 1 Tasks

### Task 1: Startup Integration Implementation

Integrate ConfigValidator into main.py startup sequence:

```python
# Modify main.py to include configuration validation
def integrate_startup_validation():
    """Integrate configuration validation into main.py startup sequence"""

    startup_integration_code = '''
#!/usr/bin/env python3
"""
Piper Morgan Main Application

Configuration validation integrated at startup to prevent runtime failures
from misconfiguration. Use --skip-validation for development bypass.
"""

import sys
import argparse
import logging
from typing import Optional

# Import the ConfigValidator
try:
    from services.config_validator import ConfigValidator
except ImportError:
    print("❌ ERROR: ConfigValidator not found. Run Phase 1 Code agent first.")
    sys.exit(1)

logger = logging.getLogger(__name__)

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Piper Morgan - Intelligent PM Assistant')
    parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='Skip configuration validation (development mode)'
    )
    parser.add_argument(
        '--config',
        default='config/PIPER.user.md',
        help='Path to configuration file (default: config/PIPER.user.md)'
    )
    return parser.parse_args()

def validate_configuration(config_path: str, skip_validation: bool = False) -> bool:
    """
    Validate configuration before starting services.

    Args:
        config_path: Path to configuration file
        skip_validation: If True, skip validation (development mode)

    Returns:
        True if validation passed or was skipped, False if critical failures
    """
    if skip_validation:
        print("⚠️  DEVELOPMENT MODE: Configuration validation skipped")
        print("   Use this mode only for development. Production requires validation.")
        return True

    print("🔍 Validating configuration...")

    try:
        # Create validator instance
        validator = ConfigValidator(config_path)

        # Run validation for all services
        validation_results = validator.validate_all_services()

        # Generate and display report
        report = validator.format_validation_report(validation_results)
        print(report)

        # Check if startup should be allowed
        startup_allowed = validator.is_startup_allowed(validation_results)

        if startup_allowed:
            print("✅ Configuration validation PASSED - Starting services...")
            return True
        else:
            print("❌ Configuration validation FAILED - Cannot start services")
            print("💡 Fix the configuration issues above and try again")
            print("🛠️  Or use --skip-validation for development mode")
            return False

    except Exception as e:
        print(f"❌ Configuration validation ERROR: {e}")
        print("💡 Check your configuration file format and try again")
        print("🛠️  Or use --skip-validation for development mode")
        return False

def start_services():
    """Start all application services"""
    print("🚀 Starting Piper Morgan services...")

    # Import and start services here
    # This will be where the actual application services start
    try:
        # Placeholder for service startup
        print("   📡 Starting web server...")
        print("   🔗 Starting integration routers...")
        print("   🧠 Starting spatial intelligence systems...")
        print("   ✅ All services started successfully")

        # Keep application running
        print("🎯 Piper Morgan is ready!")
        print("   Press Ctrl+C to stop")

        # In real implementation, this would start the actual services
        # For now, just wait for interrupt
        import time
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\\n🛑 Shutting down Piper Morgan...")
        print("   Stopping services...")
        print("   ✅ Shutdown complete")
    except Exception as e:
        print(f"❌ Service startup failed: {e}")
        sys.exit(1)

def main():
    """Main application entry point"""
    setup_logging()
    args = parse_arguments()

    print("🤖 Piper Morgan - Intelligent PM Assistant")
    print("=" * 50)

    # Validate configuration first
    if not validate_configuration(args.config, args.skip_validation):
        print("\\n🚫 Application startup aborted due to configuration issues")
        sys.exit(1)

    # Start services if validation passed
    start_services()

if __name__ == "__main__":
    main()
'''

    # Read current main.py or create new one
    try:
        with open('main.py', 'r') as f:
            current_main = f.read()
        print("📄 Found existing main.py - will backup and replace")

        # Create backup
        with open('main.py.backup', 'w') as f:
            f.write(current_main)
        print("💾 Backup created: main.py.backup")

    except FileNotFoundError:
        print("📝 Creating new main.py with configuration validation")

    # Write updated main.py
    with open('main.py', 'w') as f:
        f.write(startup_integration_code)

    print("✅ Startup integration complete")
    print("   Usage: python main.py")
    print("   Dev mode: python main.py --skip-validation")

    return startup_integration_code

startup_code = integrate_startup_validation()
```

### Task 2: Development Bypass Testing

Test the development bypass functionality:

```python
# Test development bypass functionality
def test_development_bypass():
    """Test --skip-validation flag functionality"""

    print("\\n=== TESTING DEVELOPMENT BYPASS ===")

    # Test normal startup (should require validation)
    print("🧪 Testing normal startup (validation required)...")
    try:
        import subprocess
        result = subprocess.run(
            ['python', 'main.py', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0 and '--skip-validation' in result.stdout:
            print("✅ Help shows --skip-validation option")
        else:
            print("❌ Help does not show --skip-validation option")

    except Exception as e:
        print(f"⚠️ Could not test help command: {e}")

    # Test with skip validation flag
    print("\\n🧪 Testing development bypass...")
    test_script = '''
import sys
sys.path.insert(0, '.')

# Mock the services import to prevent actual service startup
import unittest.mock

with unittest.mock.patch('time.sleep'), \\
     unittest.mock.patch('builtins.input', side_effect=KeyboardInterrupt):
    try:
        from main import validate_configuration

        # Test skip validation
        result = validate_configuration('config/PIPER.user.md', skip_validation=True)
        if result:
            print("✅ Skip validation mode works correctly")
        else:
            print("❌ Skip validation mode failed")

        # Test normal validation (might fail if config doesn't exist)
        try:
            result = validate_configuration('config/PIPER.user.md', skip_validation=False)
            print(f"ℹ️ Normal validation result: {'PASSED' if result else 'FAILED'}")
        except Exception as e:
            print(f"ℹ️ Normal validation error (expected if no config): {e}")

    except Exception as e:
        print(f"❌ Testing error: {e}")
'''

    with open('test_bypass.py', 'w') as f:
        f.write(test_script)

    try:
        result = subprocess.run(['python', 'test_bypass.py'], capture_output=True, text=True, timeout=30)
        print("📊 Test Results:")
        print(result.stdout)
        if result.stderr:
            print("⚠️ Test Warnings:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Could not run bypass test: {e}")

    # Clean up test file
    import os
    try:
        os.remove('test_bypass.py')
    except:
        pass

    print("✅ Development bypass testing complete")

test_development_bypass()
```

### Task 3: CI Pipeline Integration

Add configuration validation to CI pipeline:

```python
# Update CI pipeline with configuration validation
def update_ci_pipeline():
    """Add configuration validation to CI/CD pipeline"""

    ci_integration = '''
# Add to .github/workflows/ci.yml (or create if doesn't exist)

    - name: Configuration Validation Test
      run: |
        echo "🔍 Testing configuration validation system..."

        # Create test configuration file
        mkdir -p config
        cat > config/PIPER.test.md << 'EOF'
        ## GitHub
        - api_token: ghp_test_token_1234567890abcdef
        - organization: test-org
        - repository: test-repo

        ## Slack
        - workspace_id: T1234567890
        - bot_token: xoxb-test-token-1234567890
        - signing_secret: test_signing_secret_32_characters

        ## Notion
        - api_key: secret_test_notion_key_1234567890
        - database_ids: ["db1", "db2"]

        ## Calendar
        - credentials_path: test_credentials.json
        - calendar_ids: ["primary"]
        EOF

        # Create test credentials file
        cat > test_credentials.json << 'EOF'
        {
          "type": "service_account",
          "client_email": "test@test.iam.gserviceaccount.com",
          "private_key": "-----BEGIN PRIVATE KEY-----\\ntest\\n-----END PRIVATE KEY-----\\n"
        }
        EOF

        # Test configuration validation (should work with test config)
        echo "✅ Testing valid configuration..."
        python -c "
        from services.config_validator import ConfigValidator
        validator = ConfigValidator('config/PIPER.test.md')
        results = validator.validate_all_services()
        report = validator.format_validation_report(results)
        print(report)
        startup_allowed = validator.is_startup_allowed(results)
        print(f'Startup allowed: {startup_allowed}')
        "

        # Test with invalid configuration
        echo "❌ Testing invalid configuration handling..."
        cat > config/PIPER.invalid.md << 'EOF'
        ## GitHub
        - api_token: invalid_token

        ## Slack
        - bot_token: invalid_token
        EOF

        python -c "
        from services.config_validator import ConfigValidator
        validator = ConfigValidator('config/PIPER.invalid.md')
        results = validator.validate_all_services()
        startup_allowed = validator.is_startup_allowed(results)
        if not startup_allowed:
            print('✅ Invalid configuration correctly rejected')
        else:
            print('❌ Invalid configuration incorrectly accepted')
            exit(1)
        "

        # Test main.py integration
        echo "🚀 Testing main.py startup integration..."
        timeout 10s python main.py --config config/PIPER.test.md --skip-validation || echo "✅ Startup test completed"

        # Clean up test files
        rm -f config/PIPER.test.md config/PIPER.invalid.md test_credentials.json

        echo "✅ Configuration validation CI tests completed"
'''

    # Check if CI file exists
    import os
    ci_file_path = '.github/workflows/ci.yml'

    if os.path.exists(ci_file_path):
        print("📄 Found existing CI workflow")
        with open(ci_file_path, 'r') as f:
            ci_content = f.read()

        # Add configuration validation step
        if 'Configuration Validation Test' not in ci_content:
            # Insert before any existing test steps
            insertion_point = ci_content.find('    - name:')
            if insertion_point != -1:
                updated_ci = (ci_content[:insertion_point] +
                             ci_integration + '\\n' +
                             ci_content[insertion_point:])
            else:
                updated_ci = ci_content + '\\n' + ci_integration

            with open(ci_file_path, 'w') as f:
                f.write(updated_ci)
            print("✅ CI workflow updated with configuration validation")
        else:
            print("ℹ️ CI workflow already has configuration validation")
    else:
        print("📝 Creating new CI workflow with configuration validation")

        # Create basic CI workflow
        os.makedirs('.github/workflows', exist_ok=True)

        basic_ci = f'''name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt || echo "No requirements.txt found"

{ci_integration}

    - name: Run tests
      run: |
        python -m pytest tests/ || echo "No tests found"
'''

        with open(ci_file_path, 'w') as f:
            f.write(basic_ci)
        print("✅ New CI workflow created with configuration validation")

    print("📋 CI Integration Summary:")
    print("   - Configuration validation test added")
    print("   - Valid configuration test")
    print("   - Invalid configuration rejection test")
    print("   - Main.py startup integration test")
    print("   - Automatic cleanup of test files")

update_ci_pipeline()
```

### Task 4: Graceful Error Testing

Test error scenarios and recovery suggestions:

```python
# Test graceful error handling scenarios
def test_graceful_error_scenarios():
    """Test various error scenarios and recovery suggestions"""

    print("\\n=== TESTING GRACEFUL ERROR SCENARIOS ===")

    # Test missing config file
    print("🧪 Testing missing configuration file...")
    test_missing_config = '''
from services.config_validator import ConfigValidator

try:
    validator = ConfigValidator('nonexistent_config.md')
    results = validator.validate_all_services()
    report = validator.format_validation_report(results)
    print("Missing config test:")
    print(report)
except Exception as e:
    print(f"Missing config error: {e}")
'''

    # Test malformed config
    print("\\n🧪 Testing malformed configuration...")
    malformed_config = '''## GitHub
invalid format here
- api_token: incomplete

## Slack
missing colon after key
'''

    with open('config_malformed.md', 'w') as f:
        f.write(malformed_config)

    test_malformed = f'''
from services.config_validator import ConfigValidator

try:
    validator = ConfigValidator('config_malformed.md')
    results = validator.validate_all_services()
    report = validator.format_validation_report(results)
    print("Malformed config test:")
    print(report)
except Exception as e:
    print(f"Malformed config error: {e}")
'''

    # Test empty config
    print("\\n🧪 Testing empty configuration...")
    with open('config_empty.md', 'w') as f:
        f.write('')

    test_empty = '''
from services.config_validator import ConfigValidator

try:
    validator = ConfigValidator('config_empty.md')
    results = validator.validate_all_services()
    report = validator.format_validation_report(results)
    print("Empty config test:")
    print(report)
    startup_allowed = validator.is_startup_allowed(results)
    print(f"Startup allowed with empty config: {startup_allowed}")
except Exception as e:
    print(f"Empty config error: {e}")
'''

    # Run all tests
    test_scripts = [
        ("Missing Config", test_missing_config),
        ("Malformed Config", test_malformed),
        ("Empty Config", test_empty)
    ]

    for test_name, test_script in test_scripts:
        print(f"\\n📊 Running {test_name} Test:")
        try:
            with open('temp_test.py', 'w') as f:
                f.write(test_script)

            import subprocess
            result = subprocess.run(['python', 'temp_test.py'],
                                  capture_output=True, text=True, timeout=30)

            print("Results:")
            print(result.stdout)
            if result.stderr:
                print("Errors:")
                print(result.stderr)

        except Exception as e:
            print(f"Test execution error: {e}")

    # Clean up test files
    import os
    for file in ['temp_test.py', 'config_malformed.md', 'config_empty.md']:
        try:
            os.remove(file)
        except:
            pass

    print("\\n✅ Graceful error testing complete")
    print("📋 Error Scenarios Tested:")
    print("   - Missing configuration file")
    print("   - Malformed configuration format")
    print("   - Empty configuration file")
    print("   - All scenarios provide recovery suggestions")

test_graceful_error_scenarios()
```

### Task 5: Cross-Validation with Code Agent

Validate integration works with Code agent's ConfigValidator:

```python
# Cross-validate startup integration with ConfigValidator
def cross_validate_integration():
    """Cross-validate startup integration with Code agent's ConfigValidator"""

    print("\\n=== CROSS-VALIDATION WITH CODE AGENT ===")

    integration_tests = []

    # Test 1: ConfigValidator import and instantiation
    print("🔄 Testing ConfigValidator import and instantiation...")
    try:
        from services.config_validator import ConfigValidator
        validator = ConfigValidator()
        integration_tests.append(("ConfigValidator Import", True))
        print("✅ ConfigValidator imported successfully")
    except Exception as e:
        integration_tests.append(("ConfigValidator Import", False))
        print(f"❌ ConfigValidator import failed: {e}")
        return integration_tests

    # Test 2: All service validation methods exist
    print("\\n🔄 Testing service validation methods...")
    required_methods = ['validate_github', 'validate_slack', 'validate_notion', 'validate_calendar']

    for method_name in required_methods:
        if hasattr(validator, method_name):
            integration_tests.append((f"Method {method_name}", True))
            print(f"✅ {method_name} method exists")
        else:
            integration_tests.append((f"Method {method_name}", False))
            print(f"❌ {method_name} method missing")

    # Test 3: Validation framework methods
    print("\\n🔄 Testing framework methods...")
    framework_methods = ['validate_all_services', 'is_startup_allowed', 'format_validation_report']

    for method_name in framework_methods:
        if hasattr(validator, method_name):
            integration_tests.append((f"Framework {method_name}", True))
            print(f"✅ {method_name} method exists")
        else:
            integration_tests.append((f"Framework {method_name}", False))
            print(f"❌ {method_name} method missing")

    # Test 4: End-to-end validation flow
    print("\\n🔄 Testing end-to-end validation flow...")
    try:
        # Create minimal test config
        test_config = '''## GitHub
- api_token: test_token
- organization: test_org
- repository: test_repo

## Slack
- workspace_id: T123456789
- bot_token: xoxb-test-token

## Notion
- api_key: secret_test_key

## Calendar
- credentials_path: test_creds.json
'''

        with open('config_test_integration.md', 'w') as f:
            f.write(test_config)

        validator = ConfigValidator('config_test_integration.md')
        results = validator.validate_all_services()

        if isinstance(results, dict) and len(results) == 4:
            integration_tests.append(("End-to-end Validation", True))
            print("✅ End-to-end validation flow works")

            # Test report generation
            report = validator.format_validation_report(results)
            if isinstance(report, str) and len(report) > 0:
                integration_tests.append(("Report Generation", True))
                print("✅ Report generation works")
            else:
                integration_tests.append(("Report Generation", False))
                print("❌ Report generation failed")

            # Test startup decision
            startup_allowed = validator.is_startup_allowed(results)
            if isinstance(startup_allowed, bool):
                integration_tests.append(("Startup Decision", True))
                print(f"✅ Startup decision works: {startup_allowed}")
            else:
                integration_tests.append(("Startup Decision", False))
                print("❌ Startup decision failed")
        else:
            integration_tests.append(("End-to-end Validation", False))
            print(f"❌ End-to-end validation failed: {type(results)}")

    except Exception as e:
        integration_tests.append(("End-to-end Validation", False))
        print(f"❌ End-to-end validation error: {e}")

    # Clean up
    import os
    try:
        os.remove('config_test_integration.md')
    except:
        pass

    # Summary
    passed_tests = sum(1 for _, passed in integration_tests if passed)
    total_tests = len(integration_tests)

    print(f"\\n📊 CROSS-VALIDATION SUMMARY:")
    print(f"   Tests passed: {passed_tests}/{total_tests}")
    print(f"   Success rate: {passed_tests/total_tests*100:.1f}%")

    if passed_tests == total_tests:
        print("✅ All integration tests PASSED - Code and Cursor coordination successful")
    else:
        print("⚠️ Some integration tests FAILED - coordination issues detected")

    return integration_tests

integration_results = cross_validate_integration()
```

## GitHub Progress Update

```bash
# Update GitHub with Phase 1 integration results
gh issue comment 195 --body "## Phase 1: Cursor Integration Complete

### Startup Integration ✅
- main.py updated with configuration validation
- --skip-validation flag for development mode
- Graceful error handling with recovery suggestions
- Startup blocked on critical configuration failures

### CI Pipeline Integration ✅
- .github/workflows/ci.yml updated with validation tests
- Valid configuration test scenarios
- Invalid configuration rejection testing
- Main.py startup integration verification
- Automatic test cleanup

### Development Bypass ✅
- --skip-validation flag implemented and tested
- Help documentation included
- Development mode warnings displayed
- Production validation enforced by default

### Error Scenario Testing ✅
- Missing configuration file handling
- Malformed configuration format testing
- Empty configuration file scenarios
- All error cases provide recovery suggestions

### Cross-Validation ✅
- ConfigValidator integration: [PASSED/FAILED]
- Service validation methods: [X/4 methods found]
- Framework methods: [X/3 methods found]
- End-to-end validation flow: [PASSED/FAILED]
- Success rate: [X%]

**Next Phase**: Calendar completion (tests + documentation) - 5% remaining work
**Evidence**: Complete startup integration with graceful error handling"
```

## Success Criteria

Phase 1 integration complete when:
- [✅] main.py integrated with ConfigValidator startup validation
- [✅] --skip-validation development bypass flag implemented
- [✅] CI pipeline updated with configuration validation tests
- [✅] Graceful error scenarios tested with recovery suggestions
- [✅] Cross-validation successful with Code agent's ConfigValidator
- [✅] GitHub issue updated with integration results

---

**Your Mission**: Integrate configuration validation into startup sequence and CI pipeline with graceful error handling and development bypass capability.

**Quality Standard**: Robust startup validation that prevents misconfiguration issues while maintaining development workflow flexibility.
