import os
import sys


def test_syspath_in_project():
    """Debug sys.path when pytest runs from project"""
    print(f"\nCWD: {os.getcwd()}")
    print(f"sys.path[0:5]: {sys.path[0:5]}")

    try:
        from services.integrations.github.github_integration_router import GitHubIntegrationRouter

        print("✓ SUCCESS: Can import GitHubIntegrationRouter")
    except ImportError as e:
        print(f"✗ FAILED: {e}")
        # Check if file exists
        test_path = os.path.join(
            os.getcwd(), "services/integrations/github/github_integration_router.py"
        )
        print(f"File exists at expected path: {os.path.exists(test_path)}")
        raise
