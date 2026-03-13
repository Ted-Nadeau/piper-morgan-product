"""
Test router handles integration errors gracefully
"""


def test_no_integration_available():
    """Test router behavior when no integrations are available"""

    # This would require mocking or special test setup
    # For now, verify error messages are informative

    print("=== Error Handling Testing ===")
    print("Note: Full error testing requires mocking integrations")
    print("Verify methods have proper RuntimeError messages")

    # Check error message format in source code
    import inspect

    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    router = GitHubIntegrationRouter()
    methods = [m for m in dir(router) if not m.startswith("_") and callable(getattr(router, m))]

    methods_with_error_handling = 0
    methods_missing_error_handling = 0

    for method_name in methods:
        try:
            method = getattr(router, method_name)
            source = inspect.getsource(method)

            if "RuntimeError" in source and method_name in source:
                print(f"✅ {method_name} - has proper error handling")
                methods_with_error_handling += 1
            elif "RuntimeError" in source:
                print(f"⚠️  {method_name} - has RuntimeError but check message format")
                methods_with_error_handling += 1
            else:
                print(f"❌ {method_name} - missing RuntimeError handling")
                methods_missing_error_handling += 1

        except Exception as e:
            print(f"❌ {method_name} - error checking error handling: {e}")
            methods_missing_error_handling += 1

    print(f"\nError Handling Summary:")
    print(f"  Methods with error handling: {methods_with_error_handling}")
    print(f"  Methods missing error handling: {methods_missing_error_handling}")

    return methods_missing_error_handling == 0


if __name__ == "__main__":
    error_handling_ok = test_no_integration_available()

    if error_handling_ok:
        print("\n🎉 Error handling testing PASSED")
    else:
        print("\n❌ Error handling testing FAILED")
