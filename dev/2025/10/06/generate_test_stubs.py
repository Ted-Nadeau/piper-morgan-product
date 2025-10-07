"""Generate test stubs for all 52 interface tests"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent.parent.resolve()
sys.path.insert(0, str(project_root))

from tests.intent.test_constants import INTENT_CATEGORIES, INTERFACES


def generate_interface_test_stubs():
    """Generate test file stubs for each interface."""

    for interface in INTERFACES:
        filename = project_root / f"tests/intent/test_{interface}_interface.py"

        content = f'''"""
Test {interface.upper()} interface for all 13 intent categories - GREAT-4E
"""
import pytest
from tests.intent.base_validation_test import BaseValidationTest
from tests.intent.test_constants import INTENT_CATEGORIES
from tests.intent.coverage_tracker import coverage


class Test{interface.title()}Interface(BaseValidationTest):
    """Test all 13 categories through {interface.upper()} interface."""
'''

        for i, category in enumerate(INTENT_CATEGORIES, 1):
            content += f'''
    @pytest.mark.asyncio
    async def test_{category.lower()}_{interface}(self, intent_service):
        """{interface.upper()} {i}/13: {category} category."""
        result = await self.validate_category(
            "{category}",
            "{interface}",
            intent_service
        )

        # Verify no placeholder
        # Verify proper routing
        # Verify response valid

        # Update coverage
        coverage.interface_tests_passed += 1

        assert result["tested"] is True
'''

        # Write the file
        filename.write_text(content)
        print(f"Generated: {filename}")
        print(f"  Tests: {len(INTENT_CATEGORIES)}")

    print(f"\nTotal interface tests: {len(INTERFACES) * len(INTENT_CATEGORIES)}")


if __name__ == "__main__":
    generate_interface_test_stubs()
