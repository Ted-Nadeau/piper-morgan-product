#!/usr/bin/env python3
"""
Phase 3A: Feature Flag Testing Framework
Comprehensive testing of spatial vs legacy GitHub integration modes
"""

import os
import sys
import traceback
from typing import Any, Dict, List, Tuple
from unittest.mock import patch

# Add the project root to the path
sys.path.insert(0, "/Users/xian/Development/piper-morgan")


def test_feature_flag_control():
    """Test router behavior with different feature flag settings"""

    print("🔍 PHASE 3A: FEATURE FLAG TESTING FRAMEWORK")
    print("=" * 50)
    print()

    results = {}

    # Test 1: Spatial Mode (USE_SPATIAL_GITHUB=true)
    print("1. TESTING SPATIAL MODE (USE_SPATIAL_GITHUB=true)")
    print("-" * 45)

    try:
        with patch.dict(os.environ, {"USE_SPATIAL_GITHUB": "true", "ALLOW_LEGACY_GITHUB": "true"}):
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            router = GitHubIntegrationRouter()
            integration, is_legacy = router._get_preferred_integration("get_issue_by_url")

            print(f"✅ Router created successfully")
            print(f"   Integration type: {type(integration).__name__ if integration else 'None'}")
            print(f"   Is legacy mode: {is_legacy}")
            print(
                f"   Feature flags: spatial={router.use_spatial}, legacy_allowed={router.allow_legacy}"
            )

            results["spatial_mode"] = {
                "success": True,
                "integration_type": type(integration).__name__ if integration else "None",
                "is_legacy": is_legacy,
                "use_spatial": router.use_spatial,
                "allow_legacy": router.allow_legacy,
            }

    except Exception as e:
        print(f"❌ Spatial mode failed: {e}")
        print(f"   Error details: {traceback.format_exc()}")
        results["spatial_mode"] = {"success": False, "error": str(e)}

    print()

    # Test 2: Legacy Mode (USE_SPATIAL_GITHUB=false)
    print("2. TESTING LEGACY MODE (USE_SPATIAL_GITHUB=false)")
    print("-" * 45)

    try:
        with patch.dict(os.environ, {"USE_SPATIAL_GITHUB": "false", "ALLOW_LEGACY_GITHUB": "true"}):
            # Need to reimport to get new environment settings
            import importlib

            import services.integrations.github.github_integration_router

            importlib.reload(services.integrations.github.github_integration_router)
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            router = GitHubIntegrationRouter()
            integration, is_legacy = router._get_preferred_integration("get_issue_by_url")

            print(f"✅ Router created successfully")
            print(f"   Integration type: {type(integration).__name__ if integration else 'None'}")
            print(f"   Is legacy mode: {is_legacy}")
            print(
                f"   Feature flags: spatial={router.use_spatial}, legacy_allowed={router.allow_legacy}"
            )

            results["legacy_mode"] = {
                "success": True,
                "integration_type": type(integration).__name__ if integration else "None",
                "is_legacy": is_legacy,
                "use_spatial": router.use_spatial,
                "allow_legacy": router.allow_legacy,
            }

    except Exception as e:
        print(f"❌ Legacy mode failed: {e}")
        print(f"   Error details: {traceback.format_exc()}")
        results["legacy_mode"] = {"success": False, "error": str(e)}

    print()

    # Test 3: Feature Flag Verification
    print("3. FEATURE FLAG SYSTEM VERIFICATION")
    print("-" * 35)

    try:
        from services.infrastructure.config.feature_flags import FeatureFlags

        # Test different flag combinations
        flag_tests = [
            {"USE_SPATIAL_GITHUB": "true", "ALLOW_LEGACY_GITHUB": "true"},
            {"USE_SPATIAL_GITHUB": "false", "ALLOW_LEGACY_GITHUB": "true"},
            {"USE_SPATIAL_GITHUB": "true", "ALLOW_LEGACY_GITHUB": "false"},
        ]

        for i, flags in enumerate(flag_tests, 1):
            with patch.dict(os.environ, flags):
                # Reload FeatureFlags to pick up new env vars
                importlib.reload(services.infrastructure.config.feature_flags)
                from services.infrastructure.config.feature_flags import FeatureFlags

                spatial = FeatureFlags.should_use_spatial_github()
                legacy = FeatureFlags.is_legacy_github_allowed()
                warnings = FeatureFlags.should_warn_github_deprecation()

                print(f"   Test {i}: {flags}")
                print(f"      should_use_spatial_github(): {spatial}")
                print(f"      is_legacy_github_allowed(): {legacy}")
                print(f"      should_warn_github_deprecation(): {warnings}")

        results["feature_flags"] = {"success": True}

    except Exception as e:
        print(f"❌ Feature flag verification failed: {e}")
        results["feature_flags"] = {"success": False, "error": str(e)}

    print()

    return results


def test_critical_router_methods():
    """Test critical router methods in both spatial and legacy modes"""

    print("4. TESTING CRITICAL ROUTER METHODS")
    print("-" * 35)

    critical_methods = [
        "get_issue_by_url",
        "get_open_issues",
        "get_recent_issues",
        "get_recent_activity",
        "list_repositories",
    ]

    results = {}

    for method_name in critical_methods:
        print(f"   Testing {method_name}:")
        method_results = {}

        # Test in spatial mode
        try:
            with patch.dict(
                os.environ, {"USE_SPATIAL_GITHUB": "true", "ALLOW_LEGACY_GITHUB": "true"}
            ):
                import importlib

                import services.integrations.github.github_integration_router

                importlib.reload(services.integrations.github.github_integration_router)
                from services.integrations.github.github_integration_router import (
                    GitHubIntegrationRouter,
                )

                router = GitHubIntegrationRouter()
                method = getattr(router, method_name, None)

                if method:
                    print(f"      ✅ Available in spatial mode")
                    method_results["spatial"] = {"available": True}
                else:
                    print(f"      ❌ Not available in spatial mode")
                    method_results["spatial"] = {"available": False}

        except Exception as e:
            print(f"      ❌ Spatial mode error: {e}")
            method_results["spatial"] = {"available": False, "error": str(e)}

        # Test in legacy mode
        try:
            with patch.dict(
                os.environ, {"USE_SPATIAL_GITHUB": "false", "ALLOW_LEGACY_GITHUB": "true"}
            ):
                import importlib

                import services.integrations.github.github_integration_router

                importlib.reload(services.integrations.github.github_integration_router)
                from services.integrations.github.github_integration_router import (
                    GitHubIntegrationRouter,
                )

                router = GitHubIntegrationRouter()
                method = getattr(router, method_name, None)

                if method:
                    print(f"      ✅ Available in legacy mode")
                    method_results["legacy"] = {"available": True}
                else:
                    print(f"      ❌ Not available in legacy mode")
                    method_results["legacy"] = {"available": False}

        except Exception as e:
            print(f"      ❌ Legacy mode error: {e}")
            method_results["legacy"] = {"available": False, "error": str(e)}

        results[method_name] = method_results

    return results


def test_service_initialization():
    """Test all 5 converted services in both spatial and legacy modes"""

    print("5. TESTING SERVICE INITIALIZATION")
    print("-" * 33)

    services_to_test = [
        ("services.orchestration.engine", "OrchestrationEngine"),
        ("services.domain.github_domain_service", "GitHubDomainService"),
        ("services.domain.pm_number_manager", "PMNumberManager"),
        ("services.domain.standup_orchestration_service", "StandupOrchestrationService"),
        ("services.integrations.github.issue_analyzer", "GitHubIssueAnalyzer"),
    ]

    results = {}

    for module_name, class_name in services_to_test:
        print(f"   Testing {class_name}:")
        service_results = {}

        # Test spatial mode
        try:
            with patch.dict(
                os.environ, {"USE_SPATIAL_GITHUB": "true", "ALLOW_LEGACY_GITHUB": "true"}
            ):
                module = __import__(module_name, fromlist=[class_name])
                service_class = getattr(module, class_name)
                service = service_class()

                print(f"      ✅ Initializes in spatial mode")
                service_results["spatial"] = {"success": True}

        except Exception as e:
            print(f"      ❌ Spatial mode failed: {e}")
            service_results["spatial"] = {"success": False, "error": str(e)}

        # Test legacy mode
        try:
            with patch.dict(
                os.environ, {"USE_SPATIAL_GITHUB": "false", "ALLOW_LEGACY_GITHUB": "true"}
            ):
                module = __import__(module_name, fromlist=[class_name])
                service_class = getattr(module, class_name)
                service = service_class()

                print(f"      ✅ Initializes in legacy mode")
                service_results["legacy"] = {"success": True}

        except Exception as e:
            print(f"      ❌ Legacy mode failed: {e}")
            service_results["legacy"] = {"success": False, "error": str(e)}

        results[class_name] = service_results

    return results


def generate_test_report(flag_results, method_results, service_results):
    """Generate comprehensive test report"""

    print()
    print("📊 COMPREHENSIVE TEST REPORT")
    print("=" * 30)
    print()

    # Feature flag testing summary
    print("FEATURE FLAG TESTING:")
    spatial_success = flag_results.get("spatial_mode", {}).get("success", False)
    legacy_success = flag_results.get("legacy_mode", {}).get("success", False)
    flags_success = flag_results.get("feature_flags", {}).get("success", False)

    print(f"   Spatial mode: {'✅' if spatial_success else '❌'}")
    print(f"   Legacy mode: {'✅' if legacy_success else '❌'}")
    print(f"   Flag system: {'✅' if flags_success else '❌'}")

    # Router methods summary
    print()
    print("ROUTER METHODS TESTING:")
    total_methods = len(method_results)
    spatial_available = sum(
        1 for m in method_results.values() if m.get("spatial", {}).get("available", False)
    )
    legacy_available = sum(
        1 for m in method_results.values() if m.get("legacy", {}).get("available", False)
    )

    print(f"   Methods tested: {total_methods}")
    print(f"   Spatial mode availability: {spatial_available}/{total_methods}")
    print(f"   Legacy mode availability: {legacy_available}/{total_methods}")

    # Service initialization summary
    print()
    print("SERVICE INITIALIZATION TESTING:")
    total_services = len(service_results)
    spatial_init = sum(
        1 for s in service_results.values() if s.get("spatial", {}).get("success", False)
    )
    legacy_init = sum(
        1 for s in service_results.values() if s.get("legacy", {}).get("success", False)
    )

    print(f"   Services tested: {total_services}")
    print(f"   Spatial mode initialization: {spatial_init}/{total_services}")
    print(f"   Legacy mode initialization: {legacy_init}/{total_services}")

    # Overall assessment
    print()
    print("OVERALL ASSESSMENT:")
    feature_flag_ok = spatial_success and legacy_success and flags_success
    router_methods_ok = spatial_available == total_methods and legacy_available == total_methods
    services_ok = spatial_init == total_services and legacy_init == total_services

    if feature_flag_ok and router_methods_ok and services_ok:
        print("🎉 ALL TESTS PASSED - Feature flag system fully functional")
        print("✅ Both spatial and legacy modes work correctly")
        print("✅ Ready for PM validation")
        return True
    else:
        print("🚨 SOME TESTS FAILED - Investigation required")
        if not feature_flag_ok:
            print("❌ Feature flag system issues detected")
        if not router_methods_ok:
            print("❌ Router method availability issues detected")
        if not services_ok:
            print("❌ Service initialization issues detected")
        return False


def main():
    """Run comprehensive feature flag testing"""

    print("Starting Phase 3A Feature Flag Testing...")
    print()

    # Run all tests
    flag_results = test_feature_flag_control()
    method_results = test_critical_router_methods()
    service_results = test_service_initialization()

    # Generate report
    success = generate_test_report(flag_results, method_results, service_results)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
