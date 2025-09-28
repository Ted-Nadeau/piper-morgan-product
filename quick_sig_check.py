#!/usr/bin/env python3
"""Quick signature check"""

# GitHubAgent signatures (from comparison output)
agent_sigs = {
    "create_issue": "def create_issue( self, repo_name: str, title: str, body: str, labels: Optional[List[str]] = None ) -> Dict[str, Any]:",
    "create_issue_from_work_item": "def create_issue_from_work_item( self, repo_name: str, work_item: Dict[str, Any] ) -> Dict[str, Any]:",
    "create_pm_issue": "def create_pm_issue( self, repo_name: str, pm_number: str, title: str, body: str, labels: Optional[List[str]] = None, assignees: Optional[List[str]] = None, ) -> Dict[str, Any]:",
    "get_issue": "def get_issue(self, repo_name: str, issue_number: int) -> Dict[str, Any]:",
}

# Router signatures (need to check)
with open("services/integrations/github/github_integration_router.py", "r") as f:
    content = f.read()

print("🔍 Quick Signature Check")
print("=" * 30)

for method in agent_sigs:
    if f"def {method}(" in content:
        print(f"✅ {method} - method exists")
        # Check if it uses repo_name
        if "repo_name" in content:
            print(f"   repo_name parameter found")
    else:
        print(f"❌ {method} - method missing")

print()
print("Parameter checks:")
print(f"repo_name mentions: {content.count('repo_name')}")
print(f"repository mentions: {content.count('repository')}")
