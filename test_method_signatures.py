"""
Verify router method signatures match GitHubAgent exactly
"""

import inspect


def test_method_signature_consistency():
    """Verify router methods have same signatures as GitHubAgent"""
    from services.integrations.github.github_agent import GitHubAgent
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    agent = GitHubAgent()
    router = GitHubIntegrationRouter()

    agent_methods = [m for m in dir(agent) if not m.startswith("_") and callable(getattr(agent, m))]

    signature_mismatches = []
    signature_matches = 0

    for method_name in agent_methods:
        if hasattr(router, method_name):
            try:
                agent_method = getattr(agent, method_name)
                router_method = getattr(router, method_name)

                agent_sig = inspect.signature(agent_method)
                router_sig = inspect.signature(router_method)

                if agent_sig != router_sig:
                    signature_mismatches.append(
                        {
                            "method": method_name,
                            "agent_sig": str(agent_sig),
                            "router_sig": str(router_sig),
                        }
                    )
                    print(f"⚠️  {method_name} signature mismatch:")
                    print(f"    Agent:  {agent_sig}")
                    print(f"    Router: {router_sig}")
                else:
                    print(f"✅ {method_name} - signature matches")
                    signature_matches += 1

            except Exception as e:
                print(f"❌ {method_name} - error checking signature: {e}")
        else:
            print(f"❌ {method_name} - missing from router")

    print(f"\nSignature Summary:")
    print(f"  Matches: {signature_matches}")
    print(f"  Mismatches: {len(signature_mismatches)}")

    return len(signature_mismatches) == 0


if __name__ == "__main__":
    print("=== Method Signature Verification ===")
    signatures_ok = test_method_signature_consistency()

    if signatures_ok:
        print("\n🎉 Method signature verification PASSED")
    else:
        print("\n❌ Method signature verification FAILED")
