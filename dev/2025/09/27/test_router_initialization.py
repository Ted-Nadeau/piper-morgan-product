"""
Test router initializes correctly and handles different configurations
"""


def test_router_basic_initialization():
    """Test router can be initialized without errors"""
    try:
        from services.integrations.github.github_integration_router import GitHubIntegrationRouter

        router = GitHubIntegrationRouter()

        print("✅ Router initialized successfully")
        print(f"   Spatial available: {router.spatial_github is not None}")
        print(f"   Legacy available: {router.legacy_github is not None}")
        print(f"   Use spatial: {router.use_spatial}")
        print(f"   Allow legacy: {router.allow_legacy}")

        return True
    except Exception as e:
        print(f"❌ Router initialization failed: {e}")
        return False


def test_router_method_access():
    """Test all router methods can be accessed without errors"""
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    router = GitHubIntegrationRouter()
    methods = [m for m in dir(router) if not m.startswith("_") and callable(getattr(router, m))]

    accessible_count = 0
    for method_name in methods:
        try:
            method = getattr(router, method_name)
            print(f"✅ {method_name} - accessible")
            accessible_count += 1
        except Exception as e:
            print(f"❌ {method_name} - error accessing: {e}")
            return False

    print(f"\nTotal accessible methods: {accessible_count}")
    return True


if __name__ == "__main__":
    print("=== Router Initialization Testing ===")
    init_ok = test_router_basic_initialization()
    access_ok = test_router_method_access()

    if init_ok and access_ok:
        print("\n🎉 Router initialization testing PASSED")
    else:
        print("\n❌ Router initialization testing FAILED")
