"""
PiperConfigLoader - Loads and manages PIPER.md configuration for conversation context

This service provides:
- PIPER.md markdown parsing and conversion to system prompt format
- Hot-reload capability for configuration changes
- Caching for performance
- Integration with conversation initialization
"""

import os
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

import structlog

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

    def __init__(self, config_path: str = "config/PIPER.md"):
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

            for line in content.split("\n"):
                line = line.strip()

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


# Global instance for easy access
piper_config_loader = PiperConfigLoader()
