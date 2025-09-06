"""
PiperConfigLoader - Loads and manages PIPER.md configuration for conversation context

This service provides:
- PIPER.md markdown parsing and conversion to system prompt format
- Hot-reload capability for configuration changes
- Caching for performance
- Integration with conversation initialization
"""

import os
import re
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

import structlog
import yaml

logger = structlog.get_logger()


class PiperConfigLoader:
    """
    Loads and manages PIPER.md configuration for enhanced conversation context

    Features:
    - Markdown parsing and system prompt conversion
    - Hot-reload capability
    - Performance caching
    - Error handling and fallbacks
    """

    def __init__(self, config_path: str = None):
        # Auto-detect user config with fallback to default
        if config_path is None:
            user_config = Path("config/PIPER.user.md")
            default_config = Path("config/PIPER.md")
            if user_config.exists():
                config_path = str(user_config)
                logger.debug("Using user configuration", path=config_path)
            else:
                config_path = str(default_config)
                logger.debug("Using default configuration (no user config found)", path=config_path)

        self.config_path = Path(config_path)
        self.last_modified = 0
        self.cached_config = None
        self.cached_system_prompt = None
        self.cache_ttl = 300  # 5 minutes

        # Ensure config directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("PiperConfigLoader initialized", config_path=str(self.config_path))

    def load_config(self) -> Optional[Dict[str, str]]:
        """
        Load PIPER.md configuration and parse into structured format

        Returns:
            Dictionary with parsed configuration sections
        """
        try:
            if not self.config_path.exists():
                logger.warning(
                    "PIPER.md not found, using default configuration", path=str(self.config_path)
                )
                return self._get_default_config()

            # Check if file has been modified
            current_mtime = self.config_path.stat().st_mtime
            if (
                self.cached_config
                and current_mtime <= self.last_modified
                and time.time() - self.last_modified < self.cache_ttl
            ):
                logger.debug("Using cached PIPER.md configuration")
                return self.cached_config

            # Parse the markdown file
            config = self._parse_piper_md()
            if config:
                self.cached_config = config
                self.last_modified = current_mtime
                logger.info("PIPER.md configuration loaded successfully", sections=len(config))
                return config
            else:
                logger.warning("Failed to parse PIPER.md, using default configuration")
                return self._get_default_config()

        except Exception as e:
            logger.error("Error loading PIPER.md configuration", error=str(e))
            return self._get_default_config()

    def get_system_prompt(self) -> str:
        """
        Convert PIPER.md configuration to system prompt format

        Returns:
            Formatted system prompt string
        """
        config = self.load_config()
        if not config:
            return self._get_default_system_prompt()

        try:
            system_prompt = self._format_system_prompt(config)
            self.cached_system_prompt = system_prompt
            return system_prompt
        except Exception as e:
            logger.error("Error formatting system prompt", error=str(e))
            return self._get_default_system_prompt()

    def _parse_piper_md(self) -> Optional[Dict[str, str]]:
        """
        Parse PIPER.md markdown file into structured configuration

        Returns:
            Dictionary with section names as keys and content as values
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse markdown sections
            sections = {}
            current_section = None
            current_content = []

            in_code_block = False
            for original_line in content.split("\n"):
                # Preserve indentation in code blocks, strip elsewhere
                if original_line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    line = original_line.strip()
                elif in_code_block:
                    line = original_line  # Preserve indentation in code blocks
                else:
                    line = original_line.strip()

                # Check for section headers (## or ###)
                if line.startswith("## "):
                    # Save previous section
                    if current_section and current_content:
                        sections[current_section] = "\n".join(current_content).strip()

                    # Start new section
                    current_section = line[3:].strip().replace("*", "").replace("**", "")
                    current_content = []

                elif line.startswith("### "):
                    # Subsection - append to current section
                    if current_section:
                        current_content.append(line)

                elif current_section:
                    # Content for current section
                    current_content.append(line)

            # Save last section
            if current_section and current_content:
                sections[current_section] = "\n".join(current_content).strip()

            return sections

        except Exception as e:
            logger.error("Error parsing PIPER.md", error=str(e))
            return None

    def _format_system_prompt(self, config: Dict[str, str]) -> str:
        """
        Format configuration into system prompt

        Args:
            config: Parsed configuration dictionary

        Returns:
            Formatted system prompt string
        """
        prompt_parts = [
            "You are Piper Morgan, an intelligent product management assistant for Christian.",
            "Use the following context to provide personalized, context-aware assistance:",
            "",
        ]

        # Add user context
        if "User Context" in config:
            prompt_parts.extend(["## USER CONTEXT", config["User Context"], ""])

        # Add current focus
        if "Current Focus (Q4 2025)" in config:
            prompt_parts.extend(["## CURRENT FOCUS", config["Current Focus (Q4 2025)"], ""])

        # Add project portfolio
        if "Project Portfolio" in config:
            prompt_parts.extend(["## PROJECT PORTFOLIO", config["Project Portfolio"], ""])

        # Add standing priorities
        if "Standing Priorities" in config:
            prompt_parts.extend(["## STANDING PRIORITIES", config["Standing Priorities"], ""])

        # Add calendar patterns
        if "Calendar Patterns" in config:
            prompt_parts.extend(["## CALENDAR PATTERNS", config["Calendar Patterns"], ""])

        # Add knowledge sources
        if "Knowledge Sources" in config:
            prompt_parts.extend(["## KNOWLEDGE SOURCES", config["Knowledge Sources"], ""])

        # Add personality and behavior guidelines
        prompt_parts.extend(
            [
                "## BEHAVIOR GUIDELINES",
                "- Be direct and efficiency-focused",
                "- Provide evidence-based responses",
                "- Reference specific projects, priorities, and context",
                "- Maintain professional but personable tone",
                "- Suggest next steps when appropriate",
                "- Use Christian's name and refer to specific projects",
                "",
            ]
        )

        return "\n".join(prompt_parts)

    def _get_default_config(self) -> Dict[str, str]:
        """
        Get default configuration when PIPER.md is not available

        Returns:
            Default configuration dictionary
        """
        return {
            "User Context": "Christian is a Product Manager/Developer working on Piper Morgan platform",
            "Current Focus": "MCP implementation and UX enhancement",
            "Project Portfolio": "Piper Morgan (primary), OneJob, Content Creation",
            "Standing Priorities": "Enhanced conversational context, MCP deployment, pattern validation",
            "Calendar Patterns": "Daily standup at 6 AM PT, development focus blocks",
            "Knowledge Sources": "Pattern index, architecture guides, session logs",
        }

    def _get_default_system_prompt(self) -> str:
        """
        Get default system prompt when configuration is not available

        Returns:
            Default system prompt string
        """
        return """You are Piper Morgan, an intelligent product management assistant for Christian.

## USER CONTEXT
Christian is a Product Manager/Developer working on Piper Morgan platform.

## CURRENT FOCUS
MCP implementation and UX enhancement.

## PROJECT PORTFOLIO
Piper Morgan (primary), OneJob, Content Creation.

## STANDING PRIORITIES
Enhanced conversational context, MCP deployment, pattern validation.

## BEHAVIOR GUIDELINES
- Be direct and efficiency-focused
- Provide evidence-based responses
- Reference specific projects and priorities
- Maintain professional but personable tone"""

    def is_config_modified(self) -> bool:
        """
        Check if PIPER.md has been modified since last load

        Returns:
            True if file has been modified
        """
        if not self.config_path.exists():
            return False

        current_mtime = self.config_path.stat().st_mtime
        return current_mtime > self.last_modified

    def reload_if_modified(self) -> bool:
        """
        Reload configuration if file has been modified

        Returns:
            True if configuration was reloaded
        """
        if self.is_config_modified():
            logger.info("PIPER.md modified, reloading configuration")
            self.cached_config = None
            self.cached_system_prompt = None
            return True
        return False

    def get_config_summary(self) -> Dict[str, any]:
        """
        Get configuration summary for monitoring

        Returns:
            Configuration status and metadata
        """
        return {
            "config_path": str(self.config_path),
            "exists": self.config_path.exists(),
            "last_modified": self.last_modified,
            "cached": self.cached_config is not None,
            "cache_age": time.time() - self.last_modified if self.last_modified else 0,
            "sections_count": len(self.cached_config) if self.cached_config else 0,
        }

    def load_github_config(self):
        """
        Load GitHub configuration from PIPER.user.md

        Extracts YAML configuration from GitHub Integration section.
        Falls back to defaults if no configuration found.

        Returns:
            GitHubConfiguration instance with user settings or defaults
        """
        try:
            # Load the markdown configuration
            config = self.load_config()
            if not config:
                from services.config.github_config import GitHubConfiguration

                logger.debug("No PIPER.md config found, using GitHub defaults")
                return GitHubConfiguration.create_default()

            # Look for GitHub Integration section
            github_section_content = None
            for section_name, content in config.items():
                if "github" in section_name.lower() and "integration" in section_name.lower():
                    github_section_content = content
                    break

            if not github_section_content:
                from services.config.github_config import GitHubConfiguration

                logger.debug("No GitHub Integration section found, using defaults")
                return GitHubConfiguration.create_default()

            # Extract YAML from markdown code blocks (more robust)
            yaml_match = re.search(r"```yaml.*?```", github_section_content, re.DOTALL)
            if not yaml_match:
                from services.config.github_config import GitHubConfiguration

                logger.debug("No YAML configuration found in GitHub section, using defaults")
                return GitHubConfiguration.create_default()

            # Extract YAML content by removing markdown markers
            full_yaml_block = yaml_match.group(0)
            yaml_content = full_yaml_block.replace("```yaml", "").replace("```", "").strip()
            github_config_data = yaml.safe_load(yaml_content)

            if not github_config_data or "github" not in github_config_data:
                from services.config.github_config import GitHubConfiguration

                logger.debug("No github section in YAML, using defaults")
                return GitHubConfiguration.create_default()

            github_section = github_config_data["github"]
            if not isinstance(github_section, dict):
                from services.config.github_config import GitHubConfiguration

                logger.debug("GitHub section is not a dictionary, using defaults")
                return GitHubConfiguration.create_default()

            pm_numbers = github_section.get("pm_numbers", {})
            if not isinstance(pm_numbers, dict):
                pm_numbers = {}

            # Create GitHubConfiguration from user settings
            from services.config.github_config import GitHubConfiguration

            github_config = GitHubConfiguration(
                default_repository=github_section.get(
                    "default_repository", "mediajunkie/piper-morgan-product"
                ),
                owner=github_section.get("owner", "mediajunkie"),
                pm_prefix=pm_numbers.get("prefix", "PM-"),
                pm_start=pm_numbers.get("start_number", 1),
                pm_padding=pm_numbers.get("padding", 3),
                api_base=github_section.get("api_base", "https://api.github.com"),
                default_labels=github_section.get("default_labels", ["enhancement"]),
            )

            logger.info(
                "GitHub configuration loaded from PIPER.user.md",
                repository=github_config.default_repository,
                pm_format=github_config.format_pm_number(1),
            )

            return github_config

        except Exception as e:
            from services.config.github_config import GitHubConfiguration

            logger.error("Error loading GitHub configuration, using defaults", error=str(e))
            return GitHubConfiguration.create_default()


# Global instance for easy access
piper_config_loader = PiperConfigLoader()
