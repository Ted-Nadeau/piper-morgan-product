"""Validate contract test structure is correct"""

import os
import sys


def check_contract_structure():
    """Verify all contract test files exist"""

    base = "tests/plugins/contract"
    required_files = [
        "__init__.py",
        "conftest.py",
        "test_plugin_interface_contract.py",
        "test_lifecycle_contract.py",
        "test_configuration_contract.py",
        "test_isolation_contract.py",
    ]

    missing = []
    for file in required_files:
        path = os.path.join(base, file)
        if not os.path.exists(path):
            missing.append(path)

    if missing:
        print(f"❌ Missing files: {missing}")
        return False

    print("✅ All contract test files exist")
    return True


def check_pytest_markers():
    """Verify pytest.ini has contract marker"""

    with open("pytest.ini", "r") as f:
        content = f.read()

    if "contract:" in content:
        print("✅ Contract marker added to pytest.ini")
        return True
    else:
        print("❌ Contract marker missing from pytest.ini")
        return False


if __name__ == "__main__":
    os.chdir("/Users/xian/Development/piper-morgan")

    structure_ok = check_contract_structure()
    markers_ok = check_pytest_markers()

    if structure_ok and markers_ok:
        print("\n✅ Contract test structure validated!")
        sys.exit(0)
    else:
        print("\n❌ Validation failed")
        sys.exit(1)
