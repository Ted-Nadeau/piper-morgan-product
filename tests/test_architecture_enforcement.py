"""
Architecture Enforcement Tests - Phase 4A
Prevents regression to direct GitHubAgent imports
"""

import glob
import os
from typing import List

import pytest


class TestGitHubArchitectureEnforcement:
    """
    Comprehensive architectural enforcement for GitHub integration router pattern.

    These tests ensure that:
    1. Services never import GitHubAgent directly
    2. Services use GitHubIntegrationRouter instead
    3. The router architecture remains intact as code evolves
    """

    def test_no_direct_github_agent_imports(self):
        """
        CRITICAL: Prevent services from importing GitHubAgent directly.

        This test fails if any service bypasses the router architecture.
        Direct imports are prohibited to maintain feature flag control
        and spatial intelligence capabilities.
        """

        # Find all Python files in services directory
        service_files = glob.glob("services/**/*.py", recursive=True)

        # Files that are allowed to import GitHubAgent directly
        allowed_files = [
            "services/integrations/github/github_agent.py",  # The agent itself
            "services/integrations/github/github_integration_router.py",  # Router needs it for delegation
            "services/integrations/github/__init__.py",  # Module exports
        ]

        violations = []

        for file_path in service_files:
            # Skip test files and cache (specific patterns only)
            if file_path.startswith("tests/") or "__pycache__" in file_path:
                continue

            # Skip explicitly allowed files
            if any(allowed in file_path for allowed in allowed_files):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Skip binary files
                continue

            # Check for direct imports (multiple patterns)
            direct_import_patterns = [
                "from services.integrations.github.github_agent import GitHubAgent",
                "from .github_agent import GitHubAgent",
                "from github_agent import GitHubAgent",
                "import services.integrations.github.github_agent",
            ]

            for pattern in direct_import_patterns:
                if pattern in content:
                    violations.append(f"{file_path}: Direct GitHubAgent import found - '{pattern}'")

        if violations:
            violation_message = self._format_violation_message(violations)
            pytest.fail(violation_message)

    def test_services_use_router(self):
        """
        CRITICAL: Verify converted services use GitHubIntegrationRouter.

        All services that need GitHub functionality must use the router
        to ensure feature flag control and spatial intelligence work correctly.
        """

        # Services that were converted in Phase 2A and must use router
        required_router_services = [
            "services/orchestration/engine.py",
            "services/domain/github_domain_service.py",
            "services/domain/pm_number_manager.py",
            "services/domain/standup_orchestration_service.py",
            "services/integrations/github/issue_analyzer.py",
        ]

        missing_router_imports = []

        for file_path in required_router_services:
            if not os.path.exists(file_path):
                missing_router_imports.append(f"{file_path}: File not found")
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                missing_router_imports.append(f"{file_path}: Cannot read file")
                continue

            # Check for router import and usage
            if "GitHubIntegrationRouter" not in content:
                missing_router_imports.append(f"{file_path}: Missing GitHubIntegrationRouter usage")
            elif (
                "from services.integrations.github.github_integration_router import GitHubIntegrationRouter"
                not in content
            ):
                missing_router_imports.append(
                    f"{file_path}: Router imported but incorrect import statement"
                )

        if missing_router_imports:
            failure_message = self._format_router_missing_message(missing_router_imports)
            pytest.fail(failure_message)

    def test_router_architectural_integrity(self):
        """
        CRITICAL: Verify router maintains spatial-only architecture.

        Week 4 Complete (CORE-INT #109): Legacy code removed, router simplified.
        The router now delegates exclusively to GitHubSpatialIntelligence.
        """

        router_file = "services/integrations/github/github_integration_router.py"

        if not os.path.exists(router_file):
            pytest.fail(f"Router file not found: {router_file}")

        with open(router_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Critical patterns for Week 4 (spatial-only architecture)
        required_patterns = [
            "_get_integration",  # Simplified delegation method (Week 4)
            "FeatureFlags.should_use_spatial_github",  # Still used for compatibility
            "GitHubSpatialIntelligence",  # Spatial-only integration
            "raise RuntimeError",  # Proper error handling preserved
        ]

        # Patterns that MUST NOT exist after Week 4
        forbidden_patterns = [
            "_get_preferred_integration",  # Old delegation method (removed Week 4)
            "GitHubAgent",  # Legacy integration (removed Week 4)
            "_warn_deprecation_if_needed",  # Deprecation warnings (no longer needed)
        ]

        missing_patterns = []
        for pattern in required_patterns:
            if pattern not in content:
                missing_patterns.append(pattern)

        present_forbidden = []
        for pattern in forbidden_patterns:
            if pattern in content:
                present_forbidden.append(pattern)

        errors = []
        if missing_patterns:
            errors.append(f"Missing required patterns: {missing_patterns}")
        if present_forbidden:
            errors.append(f"Legacy patterns still present (should be removed): {present_forbidden}")

        if errors:
            pytest.fail(
                f"Router architectural integrity violated. {' | '.join(errors)}"
            )

    def test_critical_methods_preserved(self):
        """
        CRITICAL: Verify all critical GitHub methods remain available in router.

        These 5 methods were verified in Phase 3A and must remain available
        to prevent service functionality regression.
        """

        try:
            # Import with minimal environment impact
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )
        except ImportError as e:
            pytest.fail(f"Cannot import GitHubIntegrationRouter: {e}")

        # Critical methods that services depend on
        critical_methods = [
            "get_issue_by_url",  # Used by domain service & issue analyzer
            "get_open_issues",  # Used by domain service & PM manager
            "get_recent_issues",  # Used by domain service
            "get_recent_activity",  # Used by standup orchestration
            "list_repositories",  # Used by domain service
        ]

        missing_methods = []
        try:
            router = GitHubIntegrationRouter()
            for method_name in critical_methods:
                if not hasattr(router, method_name):
                    missing_methods.append(method_name)
        except Exception as e:
            pytest.fail(f"Router initialization failed: {e}")

        if missing_methods:
            pytest.fail(f"Critical methods missing from router: {missing_methods}")

    def test_feature_flag_integration_preserved(self):
        """
        CRITICAL: Verify feature flag system integration remains functional.

        The router must continue to respect USE_SPATIAL_GITHUB and other
        feature flags to maintain spatial intelligence capabilities.
        """

        try:
            from services.infrastructure.config.feature_flags import FeatureFlags
        except ImportError as e:
            pytest.fail(f"Cannot import FeatureFlags: {e}")

        # Critical feature flag methods
        required_flag_methods = [
            "should_use_spatial_github",
            "is_legacy_github_allowed",
            "should_warn_github_deprecation",
        ]

        missing_flag_methods = []
        for method_name in required_flag_methods:
            if not hasattr(FeatureFlags, method_name):
                missing_flag_methods.append(method_name)

        if missing_flag_methods:
            pytest.fail(f"Feature flag methods missing: {missing_flag_methods}")

    def _format_violation_message(self, violations: List[str]) -> str:
        """Format architectural violation message for clarity"""
        return "\n".join(
            [
                "🚨 ARCHITECTURAL VIOLATION: Direct GitHubAgent imports found!",
                "",
                "The router architecture has been bypassed. Services must use",
                "GitHubIntegrationRouter to maintain feature flag control and",
                "spatial intelligence capabilities.",
                "",
                "Violations found:",
            ]
            + [f"  ❌ {v}" for v in violations]
            + [
                "",
                "🔧 How to fix:",
                "  Replace:",
                "    from services.integrations.github.github_agent import GitHubAgent",
                "  With:",
                "    from services.integrations.github.github_integration_router import GitHubIntegrationRouter",
                "",
                "📖 See: docs/architecture/github-integration-router.md",
                "🐛 Issue: GitHub #193 - CORE-GREAT-2",
            ]
        )

    def _format_router_missing_message(self, missing: List[str]) -> str:
        """Format missing router usage message for clarity"""
        return "\n".join(
            [
                "🚨 ARCHITECTURAL VIOLATION: Services not using GitHubIntegrationRouter!",
                "",
                "These services were converted in Phase 2A and must use the router",
                "to ensure feature flag control and spatial intelligence work correctly.",
                "",
                "Missing router usage:",
            ]
            + [f"  ❌ {m}" for m in missing]
            + [
                "",
                "🔧 Services must import and use GitHubIntegrationRouter instead of GitHubAgent",
                "📖 See: docs/architecture/github-integration-router.md",
                "🐛 Issue: GitHub #193 - CORE-GREAT-2",
            ]
        )


class TestArchitecturalRegression:
    """
    Additional regression tests to catch common architectural violations.

    These tests catch subtle ways the architecture could be compromised
    beyond direct import violations.
    """

    def test_no_github_agent_instantiation(self):
        """
        Detect GitHubAgent() instantiation even without direct imports.

        Catches cases where GitHubAgent might be imported indirectly
        and then instantiated, bypassing the router.
        """

        service_files = glob.glob("services/**/*.py", recursive=True)

        # Files allowed to instantiate GitHubAgent
        allowed_files = [
            "services/integrations/github/github_agent.py",
            "services/integrations/github/github_integration_router.py",
        ]

        violations = []

        for file_path in service_files:
            if file_path.startswith("tests/") or "__pycache__" in file_path:
                continue

            if any(allowed in file_path for allowed in allowed_files):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                continue

            # Look for GitHubAgent instantiation patterns
            instantiation_patterns = [
                "GitHubAgent()",
                "github_agent = GitHubAgent",
                "= GitHubAgent(",
            ]

            for pattern in instantiation_patterns:
                if pattern in content:
                    violations.append(f"{file_path}: GitHubAgent instantiation found - '{pattern}'")

        if violations:
            pytest.fail(
                f"GitHubAgent instantiation found (should use GitHubIntegrationRouter): {violations}"
            )

    def test_router_delegation_pattern_preserved(self):
        """
        Verify router maintains simplified spatial-only delegation pattern.

        Week 4 (CORE-INT #109): Simplified from complex spatial/legacy routing
        to direct spatial delegation. Methods now use _get_integration() for
        clean, straightforward delegation to GitHubSpatialIntelligence.
        """

        router_file = "services/integrations/github/github_integration_router.py"

        with open(router_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Count methods that should follow delegation pattern
        import re

        method_matches = re.findall(
            r"def (get_\w+|create_\w+|list_\w+|parse_\w+|test_\w+)\(", content
        )

        # Exclude router-specific methods and module-level functions
        excluded_methods = [
            "get_integration_status",  # Special status method
            "get_deprecation_week",  # Timeline helper
            "create_github_integration",  # Factory function
            "get_integration",  # Internal delegation method itself
        ]
        delegation_methods = [m for m in method_matches if m not in excluded_methods]

        # Week 4 pattern: Simple delegation to spatial via _get_integration()
        pattern_violations = []
        for method in delegation_methods:
            method_pattern = rf"def {re.escape(method)}\([^)]*\).*?(?=def|\Z)"
            method_match = re.search(method_pattern, content, re.DOTALL)

            if method_match:
                method_body = method_match.group(0)

                # Week 4 requires: _get_integration() call (simplified pattern)
                if "_get_integration(" not in method_body:
                    pattern_violations.append(
                        f"Method {method} missing _get_integration() call (Week 4 pattern)"
                    )

                # Week 4 forbids: Old complex routing patterns
                forbidden_patterns = [
                    "_get_preferred_integration(",  # Old pattern
                    "_warn_deprecation_if_needed(",  # No longer needed
                ]
                for forbidden in forbidden_patterns:
                    if forbidden in method_body:
                        pattern_violations.append(
                            f"Method {method} contains legacy pattern: {forbidden}"
                        )

        if pattern_violations:
            pytest.fail(f"Router delegation pattern violations: {pattern_violations}")


if __name__ == "__main__":
    # Allow running tests directly for verification
    pytest.main([__file__, "-v"])
