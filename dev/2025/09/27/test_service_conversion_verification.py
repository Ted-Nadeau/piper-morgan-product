"""
Test each service can initialize and verify conversion status
"""


def test_service_initialization():
    """Verify all converted services can initialize without errors"""

    results = []

    try:
        # Test orchestration engine
        from services.orchestration.engine import OrchestrationEngine

        engine = OrchestrationEngine()
        print("✅ OrchestrationEngine initializes")
        results.append(("OrchestrationEngine", True))
    except Exception as e:
        print(f"❌ OrchestrationEngine failed: {e}")
        results.append(("OrchestrationEngine", False))

    try:
        # Test GitHub domain service
        from services.domain.github_domain_service import GitHubDomainService

        service = GitHubDomainService()
        print("✅ GitHubDomainService initializes")
        results.append(("GitHubDomainService", True))
    except Exception as e:
        print(f"❌ GitHubDomainService failed: {e}")
        results.append(("GitHubDomainService", False))

    try:
        # Test PM number manager
        from services.domain.pm_number_manager import PMNumberManager

        manager = PMNumberManager()
        print("✅ PMNumberManager initializes")
        results.append(("PMNumberManager", True))
    except Exception as e:
        print(f"❌ PMNumberManager failed: {e}")
        results.append(("PMNumberManager", False))

    try:
        # Test standup orchestration
        from services.domain.standup_orchestration_service import StandupOrchestrationService

        standup = StandupOrchestrationService()
        print("✅ StandupOrchestrationService initializes")
        results.append(("StandupOrchestrationService", True))
    except Exception as e:
        print(f"❌ StandupOrchestrationService failed: {e}")
        results.append(("StandupOrchestrationService", False))

    try:
        # Test issue analyzer
        from services.integrations.github.issue_analyzer import IssueAnalyzer

        analyzer = IssueAnalyzer()
        print("✅ IssueAnalyzer initializes")
        results.append(("IssueAnalyzer", True))
    except Exception as e:
        print(f"❌ IssueAnalyzer failed: {e}")
        results.append(("IssueAnalyzer", False))

    # Summary
    passing = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nService Initialization Summary: {passing}/{total} passing")

    return results


def check_conversion_status():
    """Check if services are actually using router or still using agent"""

    print("\n=== CONVERSION STATUS CHECK ===")

    # Check what each service is actually using
    services_info = []

    try:
        from services.orchestration.engine import OrchestrationEngine

        engine = OrchestrationEngine()
        # Check if it has router or agent
        has_router = hasattr(engine, "github_router") or hasattr(
            engine, "github_integration_router"
        )
        has_agent = hasattr(engine, "github_agent") or hasattr(engine, "github")
        services_info.append(("OrchestrationEngine", has_router, has_agent))
        print(f"OrchestrationEngine - Router: {has_router}, Agent: {has_agent}")
    except Exception as e:
        print(f"OrchestrationEngine check failed: {e}")

    try:
        from services.domain.github_domain_service import GitHubDomainService

        service = GitHubDomainService()
        has_router = hasattr(service, "github_router") or hasattr(
            service, "github_integration_router"
        )
        has_agent = hasattr(service, "_github_agent") or hasattr(service, "github_agent")
        services_info.append(("GitHubDomainService", has_router, has_agent))
        print(f"GitHubDomainService - Router: {has_router}, Agent: {has_agent}")
    except Exception as e:
        print(f"GitHubDomainService check failed: {e}")

    # Check what they're actually using internally
    print(f"\nConversion Status Summary:")
    for service_name, has_router, has_agent in services_info:
        if has_router and not has_agent:
            print(f"  ✅ {service_name}: Converted to router")
        elif has_agent and not has_router:
            print(f"  ❌ {service_name}: Still using agent")
        elif has_router and has_agent:
            print(f"  ⚠️  {service_name}: Mixed (both router and agent)")
        else:
            print(f"  ❓ {service_name}: Unknown state")


if __name__ == "__main__":
    print("=== SERVICE CONVERSION VERIFICATION ===")
    test_service_initialization()
    check_conversion_status()
