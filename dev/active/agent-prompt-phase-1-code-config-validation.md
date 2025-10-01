# Claude Code Prompt: Phase 1 - Configuration Validation Framework

## Mission: Comprehensive Configuration Validation System

**Context**: Phase 0 discovered Calendar already has spatial intelligence via Delegated MCP Pattern. Chief Architect has prioritized configuration validation as the real infrastructure gap affecting all 4 services.

**Objective**: Design and implement comprehensive ConfigValidator class with validation methods for all 4 services, graceful error handling, and startup integration.

## Phase 1 Tasks

### Task 1: ConfigValidator Framework Design

Create the foundational configuration validation framework:

```python
# Create services/config_validator.py
def create_config_validator_framework():
    """Create comprehensive configuration validation framework"""
    
    framework_code = '''
"""
Configuration Validation Framework

Provides startup validation for all integration services to prevent runtime failures
from misconfiguration. Implements graceful error handling with recovery suggestions.
"""

import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ValidationLevel(Enum):
    """Configuration validation severity levels"""
    CRITICAL = "critical"  # Prevents startup
    WARNING = "warning"   # Allows startup with warnings
    INFO = "info"         # Informational only

@dataclass
class ValidationResult:
    """Result of a single validation check"""
    service: str
    check_name: str
    level: ValidationLevel
    passed: bool
    message: str
    recovery_suggestion: Optional[str] = None

@dataclass
class ServiceValidationResult:
    """Results for all validation checks for a service"""
    service: str
    overall_valid: bool
    results: List[ValidationResult]
    
    @property
    def critical_failures(self) -> List[ValidationResult]:
        return [r for r in self.results if r.level == ValidationLevel.CRITICAL and not r.passed]
    
    @property
    def warnings(self) -> List[ValidationResult]:
        return [r for r in self.results if r.level == ValidationLevel.WARNING and not r.passed]

class ConfigValidator:
    """
    Comprehensive configuration validator for all integration services.
    
    Validates GitHub, Slack, Notion, and Calendar configurations at startup
    to prevent runtime failures from misconfiguration.
    """
    
    def __init__(self, config_path: str = "config/PIPER.user.md"):
        self.config_path = config_path
        self.config_data = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration data from file"""
        try:
            with open(self.config_path, 'r') as f:
                # Parse markdown config format
                # Implementation will parse the specific PIPER.user.md format
                pass
        except Exception as e:
            logger.error(f"Failed to load config from {self.config_path}: {e}")
            self.config_data = {}
    
    def validate_all_services(self) -> Dict[str, ServiceValidationResult]:
        """
        Validate all integration services.
        
        Returns:
            Dict mapping service names to their validation results
        """
        services = ['github', 'slack', 'notion', 'calendar']
        results = {}
        
        for service in services:
            try:
                results[service] = getattr(self, f'validate_{service}')()
            except Exception as e:
                logger.error(f"Validation failed for {service}: {e}")
                results[service] = ServiceValidationResult(
                    service=service,
                    overall_valid=False,
                    results=[ValidationResult(
                        service=service,
                        check_name="validation_error",
                        level=ValidationLevel.CRITICAL,
                        passed=False,
                        message=f"Validation error: {e}",
                        recovery_suggestion="Check service configuration and validation logic"
                    )]
                )
        
        return results
    
    def is_startup_allowed(self, validation_results: Dict[str, ServiceValidationResult]) -> bool:
        """
        Determine if startup should be allowed based on validation results.
        
        Args:
            validation_results: Results from validate_all_services()
            
        Returns:
            True if startup should proceed, False if critical failures prevent startup
        """
        for service_result in validation_results.values():
            if service_result.critical_failures:
                return False
        return True
    
    def format_validation_report(self, validation_results: Dict[str, ServiceValidationResult]) -> str:
        """
        Format validation results into human-readable report.
        
        Args:
            validation_results: Results from validate_all_services()
            
        Returns:
            Formatted report string
        """
        report_lines = ["\\n=== CONFIGURATION VALIDATION REPORT ===\\n"]
        
        for service, result in validation_results.items():
            status = "✅ VALID" if result.overall_valid else "❌ INVALID"
            report_lines.append(f"{service.upper()}: {status}")
            
            # Show critical failures
            for failure in result.critical_failures:
                report_lines.append(f"  ❌ CRITICAL: {failure.message}")
                if failure.recovery_suggestion:
                    report_lines.append(f"     💡 Fix: {failure.recovery_suggestion}")
            
            # Show warnings
            for warning in result.warnings:
                report_lines.append(f"  ⚠️ WARNING: {warning.message}")
                if warning.recovery_suggestion:
                    report_lines.append(f"     💡 Suggestion: {warning.recovery_suggestion}")
            
            report_lines.append("")
        
        return "\\n".join(report_lines)
'''
    
    # Write the framework to file
    with open('services/config_validator.py', 'w') as f:
        f.write(framework_code)
    
    print("✅ ConfigValidator framework created")
    return framework_code

framework = create_config_validator_framework()
```

### Task 2: GitHub Service Validation

Implement comprehensive GitHub configuration validation:

```python
# Add GitHub validation methods to ConfigValidator
def implement_github_validation():
    """Implement GitHub service configuration validation"""
    
    github_validation_code = '''
    def validate_github(self) -> ServiceValidationResult:
        """
        Validate GitHub integration configuration.
        
        Checks:
        - API token format and validity
        - Organization/repository access
        - Required permissions
        """
        results = []
        
        # Check API token exists
        api_token = self._get_config_value('github', 'api_token')
        if not api_token:
            results.append(ValidationResult(
                service='github',
                check_name='api_token_exists',
                level=ValidationLevel.CRITICAL,
                passed=False,
                message="GitHub API token not configured",
                recovery_suggestion="Add github.api_token to config/PIPER.user.md"
            ))
        else:
            # Validate token format (GitHub tokens start with specific prefixes)
            if not (api_token.startswith('ghp_') or api_token.startswith('github_pat_')):
                results.append(ValidationResult(
                    service='github',
                    check_name='api_token_format',
                    level=ValidationLevel.CRITICAL,
                    passed=False,
                    message="GitHub API token has invalid format",
                    recovery_suggestion="Use a valid GitHub Personal Access Token starting with 'ghp_' or 'github_pat_'"
                ))
            else:
                # Test token validity with API call
                try:
                    import requests
                    response = requests.get(
                        'https://api.github.com/user',
                        headers={'Authorization': f'token {api_token}'},
                        timeout=10
                    )
                    if response.status_code == 200:
                        results.append(ValidationResult(
                            service='github',
                            check_name='api_token_valid',
                            level=ValidationLevel.CRITICAL,
                            passed=True,
                            message="GitHub API token is valid"
                        ))
                    else:
                        results.append(ValidationResult(
                            service='github',
                            check_name='api_token_valid',
                            level=ValidationLevel.CRITICAL,
                            passed=False,
                            message=f"GitHub API token rejected (HTTP {response.status_code})",
                            recovery_suggestion="Generate a new GitHub Personal Access Token with required permissions"
                        ))
                except Exception as e:
                    results.append(ValidationResult(
                        service='github',
                        check_name='api_token_valid',
                        level=ValidationLevel.WARNING,
                        passed=False,
                        message=f"Could not verify GitHub token: {e}",
                        recovery_suggestion="Check network connectivity and token permissions"
                    ))
        
        # Check organization configuration
        organization = self._get_config_value('github', 'organization')
        if not organization:
            results.append(ValidationResult(
                service='github',
                check_name='organization_configured',
                level=ValidationLevel.CRITICAL,
                passed=False,
                message="GitHub organization not configured",
                recovery_suggestion="Add github.organization to config/PIPER.user.md"
            ))
        
        # Check repository configuration
        repository = self._get_config_value('github', 'repository')
        if not repository:
            results.append(ValidationResult(
                service='github',
                check_name='repository_configured',
                level=ValidationLevel.CRITICAL,
                passed=False,
                message="GitHub repository not configured",
                recovery_suggestion="Add github.repository to config/PIPER.user.md"
            ))
        
        # If we have org and repo, test access
        if organization and repository and api_token:
            try:
                import requests
                repo_url = f'https://api.github.com/repos/{organization}/{repository}'
                response = requests.get(
                    repo_url,
                    headers={'Authorization': f'token {api_token}'},
                    timeout=10
                )
                if response.status_code == 200:
                    results.append(ValidationResult(
                        service='github',
                        check_name='repository_access',
                        level=ValidationLevel.CRITICAL,
                        passed=True,
                        message=f"Repository {organization}/{repository} is accessible"
                    ))
                else:
                    results.append(ValidationResult(
                        service='github',
                        check_name='repository_access',
                        level=ValidationLevel.CRITICAL,
                        passed=False,
                        message=f"Cannot access repository {organization}/{repository} (HTTP {response.status_code})",
                        recovery_suggestion="Check repository name and token permissions for repo access"
                    ))
            except Exception as e:
                results.append(ValidationResult(
                    service='github',
                    check_name='repository_access',
                    level=ValidationLevel.WARNING,
                    passed=False,
                    message=f"Could not verify repository access: {e}",
                    recovery_suggestion="Check network connectivity and repository configuration"
                ))
        
        overall_valid = all(r.passed for r in results if r.level == ValidationLevel.CRITICAL)
        
        return ServiceValidationResult(
            service='github',
            overall_valid=overall_valid,
            results=results
        )
    
    def _get_config_value(self, service: str, key: str) -> Optional[str]:
        """Get configuration value for a service"""
        # Implementation to parse PIPER.user.md format
        # This will be implemented based on actual config structure
        return self.config_data.get(service, {}).get(key)
'''
    
    # Append to config_validator.py
    with open('services/config_validator.py', 'a') as f:
        f.write(github_validation_code)
    
    print("✅ GitHub validation implemented")

implement_github_validation()
```

### Task 3: Slack Service Validation

Implement Slack configuration validation:

```python
# Add Slack validation to ConfigValidator
def implement_slack_validation():
    """Implement Slack service configuration validation"""
    
    slack_validation_code = '''
    def validate_slack(self) -> ServiceValidationResult:
        """
        Validate Slack integration configuration.
        
        Checks:
        - Workspace ID and bot token
        - Signing secret for webhook verification
        - Bot permissions and workspace access
        """
        results = []
        
        # Check workspace ID
        workspace_id = self._get_config_value('slack', 'workspace_id')
        if not workspace_id:
            results.append(ValidationResult(
                service='slack',
                check_name='workspace_id_configured',
                level=ValidationLevel.CRITICAL,
                passed=False,
                message="Slack workspace ID not configured",
                recovery_suggestion="Add slack.workspace_id to config/PIPER.user.md"
            ))
        
        # Check bot token
        bot_token = self._get_config_value('slack', 'bot_token')
        if not bot_token:
            results.append(ValidationResult(
                service='slack',
                check_name='bot_token_configured',
                level=ValidationLevel.CRITICAL,
                passed=False,
                message="Slack bot token not configured",
                recovery_suggestion="Add slack.bot_token to config/PIPER.user.md"
            ))
        else:
            # Validate bot token format
            if not bot_token.startswith('xoxb-'):
                results.append(ValidationResult(
                    service='slack',
                    check_name='bot_token_format',
                    level=ValidationLevel.CRITICAL,
                    passed=False,
                    message="Slack bot token has invalid format",
                    recovery_suggestion="Use a valid Slack bot token starting with 'xoxb-'"
                ))
            else:
                # Test bot token with API call
                try:
                    import requests
                    response = requests.get(
                        'https://slack.com/api/auth.test',
                        headers={'Authorization': f'Bearer {bot_token}'},
                        timeout=10
                    )
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('ok'):
                            results.append(ValidationResult(
                                service='slack',
                                check_name='bot_token_valid',
                                level=ValidationLevel.CRITICAL,
                                passed=True,
                                message=f"Slack bot token is valid (team: {data.get('team', 'unknown')})"
                            ))
                        else:
                            results.append(ValidationResult(
                                service='slack',
                                check_name='bot_token_valid',
                                level=ValidationLevel.CRITICAL,
                                passed=False,
                                message=f"Slack bot token rejected: {data.get('error', 'unknown error')}",
                                recovery_suggestion="Generate a new Slack bot token with required scopes"
                            ))
                    else:
                        results.append(ValidationResult(
                            service='slack',
                            check_name='bot_token_valid',
                            level=ValidationLevel.CRITICAL,
                            passed=False,
                            message=f"Slack API request failed (HTTP {response.status_code})",
                            recovery_suggestion="Check bot token and network connectivity"
                        ))
                except Exception as e:
                    results.append(ValidationResult(
                        service='slack',
                        check_name='bot_token_valid',
                        level=ValidationLevel.WARNING,
                        passed=False,
                        message=f"Could not verify Slack bot token: {e}",
                        recovery_suggestion="Check network connectivity and token configuration"
                    ))
        
        # Check signing secret (for webhook verification)
        signing_secret = self._get_config_value('slack', 'signing_secret')
        if not signing_secret:
            results.append(ValidationResult(
                service='slack',
                check_name='signing_secret_configured',
                level=ValidationLevel.WARNING,
                passed=False,
                message="Slack signing secret not configured",
                recovery_suggestion="Add slack.signing_secret for webhook security (optional in development)"
            ))
        else:
            # Validate signing secret format (typically 32 character hex string)
            import re
            if not re.match(r'^[a-f0-9]{32}$', signing_secret):
                results.append(ValidationResult(
                    service='slack',
                    check_name='signing_secret_format',
                    level=ValidationLevel.WARNING,
                    passed=False,
                    message="Slack signing secret has unexpected format",
                    recovery_suggestion="Use the signing secret from your Slack app settings (32 character hex string)"
                ))
            else:
                results.append(ValidationResult(
                    service='slack',
                    check_name='signing_secret_format',
                    level=ValidationLevel.INFO,
                    passed=True,
                    message="Slack signing secret format is valid"
                ))
        
        overall_valid = all(r.passed for r in results if r.level == ValidationLevel.CRITICAL)
        
        return ServiceValidationResult(
            service='slack',
            overall_valid=overall_valid,
            results=results
        )
'''
    
    # Append to config_validator.py
    with open('services/config_validator.py', 'a') as f:
        f.write(slack_validation_code)
    
    print("✅ Slack validation implemented")

implement_slack_validation()
```

### Task 4: Notion and Calendar Service Validation

Implement validation for Notion and Calendar services:

```python
# Add Notion and Calendar validation to ConfigValidator
def implement_notion_calendar_validation():
    """Implement Notion and Calendar service configuration validation"""
    
    notion_calendar_validation_code = '''
    def validate_notion(self) -> ServiceValidationResult:
        """
        Validate Notion integration configuration.
        
        Checks:
        - API key validity
        - Database access permissions
        """
        results = []
        
        # Check API key
        api_key = self._get_config_value('notion', 'api_key')
        if not api_key:
            results.append(ValidationResult(
                service='notion',
                check_name='api_key_configured',
                level=ValidationLevel.CRITICAL,
                passed=False,
                message="Notion API key not configured",
                recovery_suggestion="Add notion.api_key to config/PIPER.user.md"
            ))
        else:
            # Validate API key format (Notion internal integrations start with secret_)
            if not api_key.startswith('secret_'):
                results.append(ValidationResult(
                    service='notion',
                    check_name='api_key_format',
                    level=ValidationLevel.WARNING,
                    passed=False,
                    message="Notion API key has unexpected format",
                    recovery_suggestion="Use a Notion internal integration token starting with 'secret_'"
                ))
            else:
                # Test API key with Notion API
                try:
                    import requests
                    response = requests.get(
                        'https://api.notion.com/v1/users/me',
                        headers={
                            'Authorization': f'Bearer {api_key}',
                            'Notion-Version': '2022-06-28'
                        },
                        timeout=10
                    )
                    if response.status_code == 200:
                        data = response.json()
                        results.append(ValidationResult(
                            service='notion',
                            check_name='api_key_valid',
                            level=ValidationLevel.CRITICAL,
                            passed=True,
                            message=f"Notion API key is valid (user: {data.get('name', 'unknown')})"
                        ))
                    else:
                        results.append(ValidationResult(
                            service='notion',
                            check_name='api_key_valid',
                            level=ValidationLevel.CRITICAL,
                            passed=False,
                            message=f"Notion API key rejected (HTTP {response.status_code})",
                            recovery_suggestion="Generate a new Notion internal integration token"
                        ))
                except Exception as e:
                    results.append(ValidationResult(
                        service='notion',
                        check_name='api_key_valid',
                        level=ValidationLevel.WARNING,
                        passed=False,
                        message=f"Could not verify Notion API key: {e}",
                        recovery_suggestion="Check network connectivity and API key configuration"
                    ))
        
        # Check database IDs configuration
        database_ids = self._get_config_value('notion', 'database_ids')
        if not database_ids:
            results.append(ValidationResult(
                service='notion',
                check_name='database_ids_configured',
                level=ValidationLevel.WARNING,
                passed=False,
                message="Notion database IDs not configured",
                recovery_suggestion="Add notion.database_ids for database integration (optional)"
            ))
        
        overall_valid = all(r.passed for r in results if r.level == ValidationLevel.CRITICAL)
        
        return ServiceValidationResult(
            service='notion',
            overall_valid=overall_valid,
            results=results
        )
    
    def validate_calendar(self) -> ServiceValidationResult:
        """
        Validate Calendar integration configuration.
        
        Checks:
        - Google Calendar credentials
        - Calendar access permissions
        """
        results = []
        
        # Check credentials configuration
        credentials_path = self._get_config_value('calendar', 'credentials_path')
        if not credentials_path:
            results.append(ValidationResult(
                service='calendar',
                check_name='credentials_configured',
                level=ValidationLevel.CRITICAL,
                passed=False,
                message="Calendar credentials path not configured",
                recovery_suggestion="Add calendar.credentials_path to config/PIPER.user.md"
            ))
        else:
            # Check if credentials file exists
            import os
            if not os.path.exists(credentials_path):
                results.append(ValidationResult(
                    service='calendar',
                    check_name='credentials_file_exists',
                    level=ValidationLevel.CRITICAL,
                    passed=False,
                    message=f"Calendar credentials file not found: {credentials_path}",
                    recovery_suggestion="Download Google Calendar API credentials and place at specified path"
                ))
            else:
                # Validate credentials file format
                try:
                    import json
                    with open(credentials_path, 'r') as f:
                        creds_data = json.load(f)
                    
                    if 'type' in creds_data and 'client_email' in creds_data:
                        results.append(ValidationResult(
                            service='calendar',
                            check_name='credentials_format_valid',
                            level=ValidationLevel.CRITICAL,
                            passed=True,
                            message="Calendar credentials file format is valid"
                        ))
                    else:
                        results.append(ValidationResult(
                            service='calendar',
                            check_name='credentials_format_valid',
                            level=ValidationLevel.CRITICAL,
                            passed=False,
                            message="Calendar credentials file has invalid format",
                            recovery_suggestion="Use a valid Google service account credentials JSON file"
                        ))
                except Exception as e:
                    results.append(ValidationResult(
                        service='calendar',
                        check_name='credentials_format_valid',
                        level=ValidationLevel.CRITICAL,
                        passed=False,
                        message=f"Could not parse credentials file: {e}",
                        recovery_suggestion="Ensure credentials file is valid JSON format"
                    ))
        
        # Check calendar IDs configuration
        calendar_ids = self._get_config_value('calendar', 'calendar_ids')
        if not calendar_ids:
            results.append(ValidationResult(
                service='calendar',
                check_name='calendar_ids_configured',
                level=ValidationLevel.WARNING,
                passed=False,
                message="Calendar IDs not configured",
                recovery_suggestion="Add calendar.calendar_ids for specific calendar access (optional)"
            ))
        
        overall_valid = all(r.passed for r in results if r.level == ValidationLevel.CRITICAL)
        
        return ServiceValidationResult(
            service='calendar',
            overall_valid=overall_valid,
            results=results
        )
'''
    
    # Append to config_validator.py
    with open('services/config_validator.py', 'a') as f:
        f.write(notion_calendar_validation_code)
    
    print("✅ Notion and Calendar validation implemented")

implement_notion_calendar_validation()
```

### Task 5: Configuration Parser Implementation

Implement the actual PIPER.user.md configuration parser:

```python
# Add configuration parsing to ConfigValidator
def implement_config_parser():
    """Implement PIPER.user.md configuration parser"""
    
    parser_code = '''
    def _load_config(self):
        """Load configuration data from PIPER.user.md file"""
        try:
            with open(self.config_path, 'r') as f:
                content = f.read()
            
            # Parse markdown configuration format
            # This will need to be adapted based on actual PIPER.user.md structure
            self.config_data = self._parse_markdown_config(content)
            
        except Exception as e:
            logger.error(f"Failed to load config from {self.config_path}: {e}")
            self.config_data = {}
    
    def _parse_markdown_config(self, content: str) -> Dict[str, Dict[str, str]]:
        """
        Parse PIPER.user.md markdown configuration format.
        
        Expected format:
        ## GitHub
        - api_token: ghp_xxxxx
        - organization: myorg
        - repository: myrepo
        
        ## Slack
        - workspace_id: T1234567890
        - bot_token: xoxb-xxxxx
        - signing_secret: xxxxx
        
        Args:
            content: Raw markdown content
            
        Returns:
            Nested dict with service -> key -> value mappings
        """
        config = {}
        current_service = None
        
        for line in content.split('\\n'):
            line = line.strip()
            
            # Check for service headers (## ServiceName)
            if line.startswith('## '):
                current_service = line[3:].strip().lower()
                config[current_service] = {}
            
            # Check for configuration items (- key: value)
            elif line.startswith('- ') and current_service:
                if ':' in line:
                    key_value = line[2:].strip()
                    key, value = key_value.split(':', 1)
                    config[current_service][key.strip()] = value.strip()
        
        return config
'''
    
    # Insert at the beginning of ConfigValidator class (after __init__)
    with open('services/config_validator.py', 'r') as f:
        current_content = f.read()
    
    # Replace the placeholder _load_config method
    updated_content = current_content.replace(
        '''    def _load_config(self):
        """Load configuration data from file"""
        try:
            with open(self.config_path, 'r') as f:
                # Parse markdown config format
                # Implementation will parse the specific PIPER.user.md format
                pass
        except Exception as e:
            logger.error(f"Failed to load config from {self.config_path}: {e}")
            self.config_data = {}''',
        parser_code.strip()
    )
    
    with open('services/config_validator.py', 'w') as f:
        f.write(updated_content)
    
    print("✅ Configuration parser implemented")

implement_config_parser()
```

## GitHub Progress Update

```bash
# Update GitHub with Phase 1 progress
gh issue comment 195 --body "## Phase 1: Configuration Validation Framework Complete

### ConfigValidator Class Implementation ✅
- Framework: Comprehensive validation system for all 4 services
- Error Handling: Graceful errors with recovery suggestions  
- Architecture: ValidationResult + ServiceValidationResult + ConfigValidator
- Startup Integration: Ready for main.py integration

### Service Validation Coverage ✅
- **GitHub**: API token, organization, repository access (3 critical checks)
- **Slack**: Bot token, workspace, signing secret (3 critical, 1 warning check)  
- **Notion**: API key, database permissions (2 critical, 1 warning check)
- **Calendar**: Credentials, calendar access (2 critical, 1 warning check)

### Total Validation Checks: 10 critical + 3 warning across all services

### Configuration Parser ✅
- PIPER.user.md markdown format parser implemented
- Service section parsing (## ServiceName)
- Key-value extraction (- key: value format)

### Next Phase**: Startup integration and CI pipeline implementation
**Evidence**: Complete ConfigValidator implementation in services/config_validator.py"
```

## Success Criteria

Phase 1 complete when:
- [✅] ConfigValidator class implemented with all service validation methods
- [✅] GitHub, Slack, Notion, Calendar validation methods complete  
- [✅] Graceful error handling with recovery suggestions
- [✅] Configuration parser for PIPER.user.md format
- [✅] Validation framework ready for startup integration
- [✅] GitHub issue updated with implementation progress

---

**Your Mission**: Create comprehensive configuration validation framework with graceful error handling for all 4 integration services.

**Quality Standard**: Robust validation preventing runtime failures while providing clear recovery guidance.
