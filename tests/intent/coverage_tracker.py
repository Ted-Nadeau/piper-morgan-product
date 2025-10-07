"""Track test coverage for GREAT-4E validation"""

from dataclasses import dataclass
from typing import Set

from tests.intent.test_constants import (
    CATEGORY_COUNT,
    CONTRACT_TESTS,
    INTERFACE_COUNT,
    INTERFACE_TESTS,
)


@dataclass
class CoverageStats:
    categories_tested: Set[str]
    interfaces_tested: Set[str]
    interface_tests_passed: int
    contract_tests_passed: int

    @property
    def category_coverage(self) -> float:
        return len(self.categories_tested) / CATEGORY_COUNT

    @property
    def interface_coverage(self) -> float:
        return len(self.interfaces_tested) / INTERFACE_COUNT

    @property
    def interface_test_coverage(self) -> float:
        return self.interface_tests_passed / INTERFACE_TESTS

    @property
    def contract_test_coverage(self) -> float:
        return self.contract_tests_passed / CONTRACT_TESTS

    @property
    def total_coverage(self) -> float:
        total_possible = INTERFACE_TESTS + CONTRACT_TESTS
        total_passed = self.interface_tests_passed + self.contract_tests_passed
        return total_passed / total_possible

    def report(self) -> str:
        """Generate coverage report."""
        return f"""
GREAT-4E Coverage Report
========================
Categories:    {len(self.categories_tested)}/{CATEGORY_COUNT} ({self.category_coverage:.0%})
Interfaces:    {len(self.interfaces_tested)}/{INTERFACE_COUNT} ({self.interface_coverage:.0%})
Interface Tests: {self.interface_tests_passed}/{INTERFACE_TESTS} ({self.interface_test_coverage:.0%})
Contract Tests:  {self.contract_tests_passed}/{CONTRACT_TESTS} ({self.contract_test_coverage:.0%})
TOTAL:         {self.interface_tests_passed + self.contract_tests_passed}/{INTERFACE_TESTS + CONTRACT_TESTS} ({self.total_coverage:.0%})
"""


# Global tracker instance
coverage = CoverageStats(
    categories_tested=set(),
    interfaces_tested=set(),
    interface_tests_passed=0,
    contract_tests_passed=0,
)
