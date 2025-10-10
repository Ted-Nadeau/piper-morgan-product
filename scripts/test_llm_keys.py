#!/usr/bin/env python3
"""
Test LLM API Keys

Validates that API keys are accessible and work with actual provider APIs.

Usage:
    python scripts/test_llm_keys.py

    # Test specific providers
    python scripts/test_llm_keys.py --providers openai anthropic
"""

import argparse
import asyncio
import sys
from pathlib import Path
from typing import List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.config.llm_config_service import LLMConfigService

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
END = "\033[0m"


def print_header():
    """Print script header"""
    print(f"\n{BOLD}{BLUE}╔═══════════════════════════════════════════════╗")
    print(f"║   Piper Morgan - API Key Validator           ║")
    print(f"║   Test keys from keychain and environment    ║")
    print(f"╚═══════════════════════════════════════════════╝{END}\n")


async def test_keys(providers: List[str] = None):
    """Test API keys for all or specific providers"""
    print_header()

    config_service = LLMConfigService()

    # Get providers to test
    if providers:
        test_providers = providers
    else:
        test_providers = ["openai", "anthropic", "gemini", "perplexity"]

    print(f"{BOLD}Testing API Keys{END}")
    print("─" * 40)

    results = await config_service.validate_all_providers()

    success_count = 0
    for provider in test_providers:
        if provider in results:
            result = results[provider]

            # Show where key came from
            key = config_service.get_api_key(provider)
            source = (
                "keychain"
                if config_service._keychain_service.get_api_key(provider)
                else "environment"
            )

            if result.is_valid:
                print(f"{GREEN}✓{END} {provider:12} - Valid (from {source})")
                success_count += 1
            else:
                print(f"{RED}✗{END} {provider:12} - {result.error_message}")
        else:
            print(f"{YELLOW}⚠{END} {provider:12} - Not configured")

    print()
    print(f"Results: {GREEN}{success_count}{END}/{len(test_providers)} providers valid")

    return success_count == len(test_providers)


def main():
    """Main test script"""
    parser = argparse.ArgumentParser(description="Test LLM API keys")
    parser.add_argument("--providers", nargs="+", help="Specific providers to test (default: all)")

    args = parser.parse_args()

    try:
        success = asyncio.run(test_keys(args.providers))
        return 0 if success else 1
    except Exception as e:
        print(f"{RED}✗{END} Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
