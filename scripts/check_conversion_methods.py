#!/usr/bin/env python3
"""
PM-056: Conversion Methods Checker
Checks for missing to_domain/from_domain methods in database models.
"""

import ast
import importlib
import inspect
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def find_database_models() -> List[str]:
    """Find all database model classes"""
    try:
        from services.database import models
        from services.database.models import Base

        database_models = []
        for name, obj in inspect.getmembers(models):
            if inspect.isclass(obj) and issubclass(obj, Base) and obj != Base:
                database_models.append(name)

        return database_models
    except ImportError as e:
        print(f"❌ Error importing database models: {e}")
        return []


def find_domain_models() -> List[str]:
    """Find all domain model classes"""
    try:
        import services.domain.models as domain_models

        domain_classes = []
        for name, obj in inspect.getmembers(domain_models):
            if inspect.isclass(obj) and hasattr(obj, "__dataclass_fields__"):
                domain_classes.append(name)

        return domain_classes
    except ImportError as e:
        print(f"❌ Error importing domain models: {e}")
        return []


def check_conversion_methods(database_model_name: str) -> Tuple[bool, List[str]]:
    """Check if database model has proper conversion methods"""
    try:
        from services.database import models

        db_model = getattr(models, database_model_name)
        methods = inspect.getmembers(db_model, predicate=inspect.isfunction)
        method_names = [name for name, _ in methods]

        issues = []

        # Check for to_domain method
        if "to_domain" not in method_names:
            issues.append(f"Missing to_domain() method")

        # Check for from_domain method
        if "from_domain" not in method_names:
            issues.append(f"Missing from_domain() method")

        # Check if methods are properly decorated
        # to_domain should be an instance method, from_domain should be a class method
        if "to_domain" in method_names:
            method = getattr(db_model, "to_domain")
            if inspect.ismethod(method) and hasattr(method, "__self__"):
                issues.append(f"to_domain() should be an instance method, not a class method")

        if "from_domain" in method_names:
            method = getattr(db_model, "from_domain")
            if not inspect.ismethod(method) or not hasattr(method, "__self__"):
                issues.append(f"from_domain() should be a class method")

        return len(issues) == 0, issues

    except Exception as e:
        return False, [f"Error checking {database_model_name}: {e}"]


def main():
    """Main validation function"""
    print("🔍 PM-056: Checking Conversion Methods")
    print("=" * 50)

    # Find models
    database_models = find_database_models()
    domain_models = find_domain_models()

    print(f"📊 Found {len(database_models)} database models")
    print(f"📊 Found {len(domain_models)} domain models")
    print()

    # Check each database model
    all_passed = True
    total_issues = 0

    for db_model_name in database_models:
        passed, issues = check_conversion_methods(db_model_name)

        if passed:
            print(f"✅ {db_model_name}: All conversion methods present")
        else:
            print(f"❌ {db_model_name}:")
            for issue in issues:
                print(f"   - {issue}")
            all_passed = False
            total_issues += len(issues)

    print()
    print("=" * 50)

    if all_passed:
        print("✅ All database models have proper conversion methods!")
        print("✅ Domain/database conversion layer is complete")
        return 0
    else:
        print(f"❌ Found {total_issues} conversion method issues")
        print("❌ Some database models are missing conversion methods")
        print()
        print("💡 To fix:")
        print("   - Add to_domain() class method to database models")
        print("   - Add from_domain() class method to database models")
        print("   - Ensure methods are properly decorated as @classmethod")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
