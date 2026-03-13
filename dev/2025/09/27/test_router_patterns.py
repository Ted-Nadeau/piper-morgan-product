"""
Test router follows consistent delegation patterns
"""


def test_delegation_pattern_consistency():
    """Test all methods follow the same delegation pattern"""
    import ast
    import inspect

    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    router = GitHubIntegrationRouter()
    router_methods = [
        m for m in dir(router) if not m.startswith("_") and callable(getattr(router, m))
    ]

    pattern_compliant = 0
    pattern_issues = 0

    # Check each method's source for delegation pattern
    for method_name in router_methods:
        try:
            method = getattr(router, method_name)
            source = inspect.getsource(method)

            # Check for delegation pattern elements
            has_get_preferred = "_get_preferred_integration" in source
            has_warning = "_warn_deprecation_if_needed" in source
            has_runtime_error = "RuntimeError" in source

            if has_get_preferred and has_warning and has_runtime_error:
                print(f"✅ {method_name} - follows delegation pattern")
                pattern_compliant += 1
            else:
                print(f"⚠️  {method_name} - pattern issues:")
                if not has_get_preferred:
                    print(f"    Missing _get_preferred_integration")
                if not has_warning:
                    print(f"    Missing deprecation warning")
                if not has_runtime_error:
                    print(f"    Missing RuntimeError handling")
                pattern_issues += 1

        except Exception as e:
            print(f"❌ {method_name} - error checking pattern: {e}")
            pattern_issues += 1

    print(f"\nPattern Summary:")
    print(f"  Compliant methods: {pattern_compliant}")
    print(f"  Methods with issues: {pattern_issues}")

    return pattern_issues == 0


if __name__ == "__main__":
    print("=== Router Pattern Consistency Testing ===")
    patterns_ok = test_delegation_pattern_consistency()

    if patterns_ok:
        print("\n🎉 Pattern consistency testing PASSED")
    else:
        print("\n❌ Pattern consistency testing FAILED")
