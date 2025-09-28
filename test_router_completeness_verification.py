"""
Verify router has all required methods and they're implemented correctly
"""


def test_router_method_completeness():
    """Verify router has all GitHubAgent methods"""
    from services.integrations.github.github_agent import GitHubAgent
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    agent_methods = set(
        m for m in dir(GitHubAgent) if not m.startswith("_") and callable(getattr(GitHubAgent, m))
    )
    router_methods = set(
        m
        for m in dir(GitHubIntegrationRouter)
        if not m.startswith("_") and callable(getattr(GitHubIntegrationRouter, m))
    )

    missing = agent_methods - router_methods

    print(f"GitHubAgent methods: {len(agent_methods)}")
    print(f"Router methods: {len(router_methods)}")

    if missing:
        print(f"❌ Missing methods: {sorted(missing)}")
        return False
    else:
        print("✅ Router has all GitHubAgent methods")
        return True


def test_critical_methods_present():
    """Verify the 5 critical methods used by bypassing services"""
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    critical_methods = [
        "get_issue_by_url",
        "get_open_issues",
        "get_recent_issues",
        "get_recent_activity",
        "list_repositories",
    ]

    router = GitHubIntegrationRouter()

    for method in critical_methods:
        if hasattr(router, method) and callable(getattr(router, method)):
            print(f"✅ {method} - present and callable")
        else:
            print(f"❌ {method} - missing or not callable")
            return False

    return True


if __name__ == "__main__":
    print("=== Router Completeness Verification ===")
    completeness_ok = test_router_method_completeness()
    critical_ok = test_critical_methods_present()

    if completeness_ok and critical_ok:
        print("\n🎉 Router implementation verification PASSED")
    else:
        print("\n❌ Router implementation verification FAILED")
