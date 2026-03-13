# Claude Code Prompt: Phase 3 - TBD-SECURITY-02 Security Fix

## Mission: Re-enable Slack Webhook Verification (HIGH PRIORITY)

**Context**: Phases 1-2 confirmed both Slack and Notion spatial systems are fully operational. Phase 0 precisely located TBD-SECURITY-02 security vulnerability. Now safe to re-enable webhook verification without breaking spatial functionality.

**Objective**: Re-enable Slack webhook signature verification by uncommenting 4 lines in webhook_router.py (lines 184-189), test the fix, and verify security without breaking spatial systems.

## Phase 3 Tasks

### Task 1: Locate and Analyze Current Security State

Examine the webhook verification code and current security state:

```python
# Analyze current webhook security implementation
def analyze_webhook_security_state():
    """Analyze current webhook verification implementation"""

    print("=== TBD-SECURITY-02 ANALYSIS ===")

    # Locate the webhook router file
    webhook_file = 'services/integrations/slack/webhook_router.py'

    try:
        with open(webhook_file, 'r') as f:
            content = f.read()
            lines = content.split('\n')

        print(f"📁 Analyzing: {webhook_file}")
        print(f"📊 Total lines: {len(lines)}")

        # Focus on lines 180-195 (around the target area)
        print(f"\n🔍 EXAMINING LINES 180-195 (TARGET AREA):")

        for i in range(179, min(195, len(lines))):  # 0-indexed, so 179 = line 180
            line_num = i + 1
            line_content = lines[i]
            is_commented = line_content.strip().startswith('#')

            if 184 <= line_num <= 189:
                marker = "🎯 TARGET" if is_commented else "✅ ACTIVE"
                print(f"  {marker} Line {line_num}: {line_content}")
            else:
                print(f"      Line {line_num}: {line_content}")

        # Look for verification method signatures
        print(f"\n🔍 SEARCHING FOR VERIFICATION METHODS:")
        verification_patterns = [
            'verify_signature',
            'validate_webhook',
            'check_signature',
            'authenticate_webhook',
            'verify_slack_signature'
        ]

        for pattern in verification_patterns:
            if pattern in content:
                print(f"  ✅ Found method pattern: {pattern}")
                # Find the line numbers
                for i, line in enumerate(lines):
                    if pattern in line and ('def' in line or 'async def' in line):
                        print(f"    Line {i+1}: {line.strip()}")

        # Check current webhook endpoints behavior
        print(f"\n🔍 ANALYZING CURRENT ENDPOINT BEHAVIOR:")

        # Look for endpoint definitions
        endpoint_patterns = ['/webhooks/', '/slack/webhooks/', 'webhook']
        for pattern in endpoint_patterns:
            if pattern in content:
                print(f"  📍 Found endpoint pattern: {pattern}")

        return content, lines

    except Exception as e:
        print(f"❌ Error analyzing webhook file: {e}")
        return None, None

content, lines = analyze_webhook_security_state()
```

### Task 2: Implement Security Fix

Re-enable webhook verification by uncommenting the identified lines:

```python
# Implement TBD-SECURITY-02 fix
def implement_webhook_security_fix():
    """Re-enable Slack webhook verification"""

    print("\n=== IMPLEMENTING TBD-SECURITY-02 FIX ===")

    webhook_file = 'services/integrations/slack/webhook_router.py'
    backup_file = f'{webhook_file}.backup'

    try:
        # Create backup first
        import shutil
        shutil.copy2(webhook_file, backup_file)
        print(f"✅ Backup created: {backup_file}")

        # Read current content
        with open(webhook_file, 'r') as f:
            content = f.read()
            lines = content.split('\n')

        print(f"📝 Processing lines 184-189...")

        # Track changes
        changes_made = []

        # Uncomment lines 184-189 (convert to 0-indexed)
        for line_num in range(183, 189):  # 183-188 in 0-indexed = lines 184-189
            if line_num < len(lines):
                original_line = lines[line_num]

                # Check if line is commented
                if original_line.strip().startswith('#'):
                    # Uncomment the line
                    # Remove the first # and any following spaces
                    uncommented = original_line.lstrip('#').lstrip()
                    # Preserve original indentation
                    indent = len(original_line) - len(original_line.lstrip())
                    lines[line_num] = ' ' * indent + uncommented

                    changes_made.append({
                        'line_num': line_num + 1,
                        'original': original_line,
                        'modified': lines[line_num]
                    })
                    print(f"  ✅ Line {line_num + 1}: Uncommented")
                else:
                    print(f"  ℹ️ Line {line_num + 1}: Already active")

        if changes_made:
            # Write the modified content
            modified_content = '\n'.join(lines)

            with open(webhook_file, 'w') as f:
                f.write(modified_content)

            print(f"\n📝 CHANGES APPLIED:")
            for change in changes_made:
                print(f"  Line {change['line_num']}:")
                print(f"    Before: {change['original']}")
                print(f"    After:  {change['modified']}")

            print(f"\n✅ TBD-SECURITY-02 fix applied ({len(changes_made)} lines modified)")
            return True, changes_made
        else:
            print(f"\n⚠️ No changes needed - verification may already be enabled")
            return False, []

    except Exception as e:
        print(f"❌ Error implementing fix: {e}")
        print(f"🔄 Restoring backup...")
        try:
            shutil.copy2(backup_file, webhook_file)
            print(f"✅ Backup restored")
        except:
            print(f"❌ Could not restore backup")
        return False, []

fix_applied, changes = implement_webhook_security_fix()
```

### Task 3: Test Security Fix Implementation

Verify the webhook verification is now active:

```python
# Test webhook security after fix
def test_webhook_security_fix():
    """Test that webhook verification is now working"""

    print("\n=== TESTING WEBHOOK SECURITY FIX ===")

    try:
        # Import and test the webhook router
        from services.integrations.slack.webhook_router import SlackWebhookRouter

        webhook_router = SlackWebhookRouter()
        print("✅ SlackWebhookRouter imported successfully")

        # Check if verification methods are available
        router_methods = [method for method in dir(webhook_router)
                         if not method.startswith('_')]

        verification_methods = [method for method in router_methods
                               if any(keyword in method.lower()
                                     for keyword in ['verify', 'validate', 'authenticate', 'signature'])]

        print(f"🔧 Verification methods available: {len(verification_methods)}")
        for method in verification_methods:
            print(f"  - {method}")

        # Test signature verification if method exists
        if hasattr(webhook_router, 'verify_signature'):
            print("\n🔐 Testing signature verification method...")
            try:
                # Test with invalid signature (should fail)
                test_headers = {'X-Slack-Signature': 'invalid_signature'}
                test_body = b'test_payload'

                # This should return False or raise an exception
                result = webhook_router.verify_signature(test_headers, test_body)
                print(f"  Invalid signature test: {result} (should be False)")

                if result is False:
                    print("  ✅ Signature verification correctly rejects invalid signatures")
                else:
                    print("  ⚠️ Signature verification may not be working correctly")

            except Exception as e:
                print(f"  ✅ Signature verification correctly raises exception: {type(e).__name__}")

        return True

    except Exception as e:
        print(f"❌ Error testing webhook security: {e}")
        return False

security_test_passed = test_webhook_security_fix()
```

### Task 4: Test Spatial System Compatibility

Ensure the security fix doesn't break spatial functionality:

```python
# Test spatial systems still work after security fix
def test_spatial_compatibility_after_security_fix():
    """Ensure spatial systems still work after security fix"""

    print("\n=== TESTING SPATIAL COMPATIBILITY AFTER FIX ===")

    compatibility_results = []

    # Test Slack spatial system
    print("🔧 Testing Slack spatial system compatibility...")
    try:
        import os
        os.environ['USE_SPATIAL_SLACK'] = 'true'

        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

        slack_router = SlackIntegrationRouter()
        spatial_adapter = slack_router.get_spatial_adapter()

        if spatial_adapter:
            print("  ✅ Slack spatial adapter still accessible")
            compatibility_results.append(('slack_spatial', True))
        else:
            print("  ❌ Slack spatial adapter not accessible")
            compatibility_results.append(('slack_spatial', False))

    except Exception as e:
        print(f"  ❌ Slack spatial system error: {e}")
        compatibility_results.append(('slack_spatial', False))

    # Test Notion spatial system
    print("\n🔧 Testing Notion spatial system compatibility...")
    try:
        os.environ['USE_SPATIAL_NOTION'] = 'true'

        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

        notion_router = NotionIntegrationRouter()
        print("  ✅ Notion router still functional")
        compatibility_results.append(('notion_spatial', True))

    except Exception as e:
        print(f"  ❌ Notion spatial system error: {e}")
        compatibility_results.append(('notion_spatial', False))

    # Test webhook router still works
    print("\n🔧 Testing webhook router functionality...")
    try:
        from services.integrations.slack.webhook_router import SlackWebhookRouter

        webhook_router = SlackWebhookRouter()
        print("  ✅ Webhook router still functional")
        compatibility_results.append(('webhook_router', True))

    except Exception as e:
        print(f"  ❌ Webhook router error: {e}")
        compatibility_results.append(('webhook_router', False))

    # Summary
    print(f"\n📊 COMPATIBILITY TEST SUMMARY:")
    all_passed = True
    for test_name, passed in compatibility_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n🎉 All spatial systems compatible with security fix!")
    else:
        print("\n⚠️ Some compatibility issues detected - may need rollback")

    return all_passed, compatibility_results

compatibility_passed, compatibility_results = test_spatial_compatibility_after_security_fix()
```

### Task 5: Verify Security Endpoints

Test that webhook endpoints now properly authenticate:

```bash
# Test webhook endpoints with security enabled
echo "=== TESTING WEBHOOK ENDPOINT SECURITY ==="

# Test webhook endpoints without authentication (should fail)
echo "Testing unauthenticated webhook requests (should return 401/403)..."

# Test main webhook endpoints
curl -X POST http://localhost:8001/slack/webhooks/events \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}' \
  -w "Status: %{http_code}\n" || echo "Request failed as expected"

curl -X POST http://localhost:8001/slack/webhooks/commands \
  -H "Content-Type: application/json" \
  -d '{"test": "command"}' \
  -w "Status: %{http_code}\n" || echo "Request failed as expected"

# Test interactive endpoint
curl -X POST http://localhost:8001/slack/webhooks/interactive \
  -H "Content-Type: application/json" \
  -d '{"test": "interactive"}' \
  -w "Status: %{http_code}\n" || echo "Request failed as expected"

echo ""
echo "Expected behavior: All requests should return 401/403 (unauthorized) instead of 200 OK"
echo "This confirms webhook verification is now active"
```

## GitHub Evidence Update

```bash
# Update GitHub issue with Phase 3 security fix results
gh issue comment 194 --body "## Phase 3: TBD-SECURITY-02 Security Fix Complete

### Security Fix Implementation ✅
- Target file: webhook_router.py lines 184-189
- Action taken: [X lines uncommented to re-enable verification]
- Backup created: webhook_router.py.backup
- Changes applied: [describe specific changes]

### Security Testing ✅
- Verification methods: [list available methods]
- Invalid signature test: [PASS/FAIL]
- Authentication behavior: [working/issues]

### Spatial System Compatibility ✅
- Slack spatial system: [COMPATIBLE/ISSUES]
- Notion spatial system: [COMPATIBLE/ISSUES]
- Webhook router: [FUNCTIONAL/ISSUES]

### Endpoint Security Verification ✅
- /slack/webhooks/events: [401/403 vs previous 200]
- /slack/webhooks/commands: [401/403 vs previous 200]
- /slack/webhooks/interactive: [401/403 vs previous 200]

**TBD-SECURITY-02 Status**: [FIXED/ISSUES_FOUND]
**Spatial Systems**: [STILL_OPERATIONAL/NEED_ATTENTION]
**Security Posture**: [IMPROVED/NEEDS_WORK]"
```

## Anti-80% Safeguards

**Mandatory Security Fix Verification**:
```
Security Component | Fixed | Tested | Compatible | Status
------------------ | ----- | ------ | ---------- | ------
Webhook verification | [ ] | [ ]    | [ ]        |
Signature validation | [ ] | [ ]    | [ ]        |
Endpoint authentication | [ ] | [ ] | [ ]        |
Slack spatial system | [ ] | [ ]    | [ ]        |
Notion spatial system | [ ] | [ ]   | [ ]        |
TOTAL: 5/5 = 100% REQUIRED
```

## Success Criteria

Phase 3 complete when:
- [✅] TBD-SECURITY-02 fix implemented (4 lines uncommented)
- [✅] Webhook verification methods active and tested
- [✅] Spatial systems remain fully compatible
- [✅] Webhook endpoints properly authenticate (401/403)
- [✅] No regression in spatial functionality
- [✅] GitHub issue #194 updated with security evidence

## STOP Conditions

Stop immediately if:
- Security fix breaks spatial systems
- Webhook router becomes non-functional
- Cannot restore from backup
- Critical spatial functionality lost
- Authentication completely broken

---

**Your Mission**: Re-enable Slack webhook verification safely while preserving spatial system functionality.

**Quality Standard**: Security vulnerability closed with zero impact on operational spatial systems.
