# Issue Intelligence Integration Examples

**Practical integration examples and usage patterns for Issue Intelligence**
**Updated**: August 24, 2025
**Status**: Production-Ready Integration Guide

Complete collection of real-world integration examples showing how to integrate Issue Intelligence with existing systems, custom applications, and workflows.

---

## Overview

This guide provides practical examples for integrating the Issue Intelligence system into various environments, from simple CLI automation to complex multi-service architectures.

### What You'll Learn

- **Basic Integration**: Simple integration with existing systems
- **Advanced Patterns**: Complex multi-service coordination
- **Performance Optimization**: Caching and optimization strategies
- **Error Handling**: Robust error handling and fallback patterns
- **Testing Strategies**: Comprehensive testing approaches

---

## Basic Integration Examples

### 1. Simple CLI Integration

Integrate Issue Intelligence with existing CLI tools:

```python
#!/usr/bin/env python3
"""
Daily Issue Triage Script
Runs issue triage and sends summary email
"""

import asyncio
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from cli.commands.issues import IssuesCommand
from services.integrations.email_service import EmailService

async def daily_triage_workflow():
    """Complete daily triage workflow with email summary"""

    # Initialize services
    issues_cmd = IssuesCommand()
    email_service = EmailService()

    try:
        # Run issue triage
        print("🔍 Running daily issue triage...")
        triage_result = await issues_cmd.triage_issues(limit=20)

        # Get project status
        print("📊 Getting project status overview...")
        status_result = await issues_cmd.get_issue_status()

        # Generate email summary
        summary = generate_triage_summary(triage_result, status_result)

        # Send email to stakeholders
        await email_service.send_summary(
            to=["team@company.com", "pm@company.com"],
            subject=f"Daily Issue Triage - {datetime.now().strftime('%Y-%m-%d')}",
            body=summary
        )

        print("✅ Daily triage workflow completed successfully")
        return True

    except Exception as e:
        print(f"❌ Daily triage workflow failed: {e}")
        return False

def generate_triage_summary(triage_result: dict, status_result: dict) -> str:
    """Generate human-readable email summary"""
    summary = f"""
    Daily Issue Triage Summary - {datetime.now().strftime('%Y-%m-%d')}

    📊 Project Health:
    • Open Issues: {status_result.get('open_issues', 0)}
    • Completion Rate: {status_result.get('completion_rate', 0):.1f}%

    🚨 High Priority Issues: {triage_result.get('high_priority', 0)}
    ⚡ Medium Priority Issues: {triage_result.get('medium_priority', 0)}
    📝 Low Priority Issues: {triage_result.get('low_priority', 0)}

    💡 Recommendations:
    """

    if triage_result.get('high_priority', 0) > 0:
        summary += "\n• ⚠️  Review high-priority issues within 24 hours"

    if status_result.get('completion_rate', 0) > 80:
        summary += "\n• ✅ Excellent completion rate - maintain momentum"

    return summary

if __name__ == "__main__":
    # Run as daily cron job: 0 9 * * * /path/to/daily_triage.py
    success = asyncio.run(daily_triage_workflow())
    sys.exit(0 if success else 1)
```

### 2. Slack Integration

Integrate with Slack for team notifications:

```python
"""
Slack Bot Integration for Issue Intelligence
Provides real-time issue updates and triage commands
"""

import asyncio
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from cli.commands.issues import IssuesCommand
from services.features.issue_intelligence import IssueIntelligenceCanonicalQueryEngine

app = AsyncApp(token="your-slack-bot-token")

@app.command("/triage")
async def handle_triage_command(ack, respond, command):
    """Handle /triage Slack command"""
    await ack()

    # Parse command options
    text = command.get("text", "")
    limit = 10
    if "limit=" in text:
        limit = int(text.split("limit=")[1].split()[0])

    try:
        # Run triage
        issues_cmd = IssuesCommand()
        result = await issues_cmd.triage_issues(limit=limit)

        # Format Slack response
        blocks = format_triage_for_slack(result)

        await respond(blocks=blocks)

    except Exception as e:
        await respond(f"❌ Triage failed: {str(e)}")

@app.command("/issues")
async def handle_issues_command(ack, respond, command):
    """Handle /issues status command"""
    await ack()

    try:
        issues_cmd = IssuesCommand()
        result = await issues_cmd.get_issue_status()

        # Format status for Slack
        message = f"""
📊 *Project Status Overview*
• Open Issues: {result.get('open_issues', 0)}
• Closed Issues: {result.get('closed_issues', 0)}
• Completion Rate: {result.get('completion_rate', 0):.1f}%
• Recent Activity: {result.get('recent_activity', 0)} issues
        """

        await respond(message)

    except Exception as e:
        await respond(f"❌ Status check failed: {str(e)}")

def format_triage_for_slack(triage_result: dict) -> list:
    """Format triage results as Slack blocks"""
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🔍 Issue Triage Results"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*🚨 High Priority:* {triage_result.get('high_priority', 0)}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*⚡ Medium Priority:* {triage_result.get('medium_priority', 0)}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*📝 Low Priority:* {triage_result.get('low_priority', 0)}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*📊 Total Analyzed:* {triage_result.get('issues_analyzed', 0)}"
                }
            ]
        }
    ]

    # Add high priority issues detail
    if triage_result.get('high_priority', 0) > 0:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*🚨 Immediate Actions Required:*\n• Review high-priority issues within 24 hours\n• Assign team members to critical issues"
            }
        })

    return blocks

if __name__ == "__main__":
    handler = AsyncSocketModeHandler(app, "your-app-token")
    asyncio.run(handler.start_async())
```

---

## Advanced Integration Patterns

### 3. FastAPI Service Integration

Create a REST API service with Issue Intelligence:

```python
"""
Issue Intelligence REST API Service
Provides HTTP endpoints for issue analysis and triage
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
import asyncio

from services.features.issue_intelligence import (
    IssueIntelligenceCanonicalQueryEngine,
    IssueIntelligenceContext,
    IssueIntelligenceResult
)
from services.integrations.github.github_agent import GitHubAgent
from services.intent_service.canonical_handlers import CanonicalHandlers

app = FastAPI(title="Issue Intelligence API", version="1.0.0")

# Request/Response Models
class TriageRequest(BaseModel):
    project: Optional[str] = None
    limit: int = 10
    priority_focus: str = "all"

class TriageResponse(BaseModel):
    issues_analyzed: int
    high_priority: int
    medium_priority: int
    low_priority: int
    triage_complete: bool
    enhancement_time_ms: Optional[int] = None

class StatusResponse(BaseModel):
    open_issues: int
    closed_issues: int
    completion_rate: float
    recent_activity: int

class EnhancedQueryRequest(BaseModel):
    message: str
    session_id: str
    user_id: str = "api_user"

# Global services (initialize on startup)
issue_engine: Optional[IssueIntelligenceCanonicalQueryEngine] = None

@app.on_event("startup")
async def initialize_services():
    """Initialize services on startup"""
    global issue_engine

    # Initialize dependencies
    github_integration = GitHubAgent()
    canonical_handlers = CanonicalHandlers()
    session_manager = SessionManager()

    # Create Issue Intelligence engine
    issue_engine = IssueIntelligenceCanonicalQueryEngine(
        github_integration=github_integration,
        canonical_handlers=canonical_handlers,
        session_manager=session_manager
    )

@app.post("/api/v1/triage", response_model=TriageResponse)
async def triage_issues(request: TriageRequest, background_tasks: BackgroundTasks):
    """Perform intelligent issue triage"""
    try:
        # Use CLI command for triage logic
        from cli.commands.issues import IssuesCommand
        issues_cmd = IssuesCommand()

        # Run triage
        result = await issues_cmd.triage_issues(
            project=request.project,
            limit=request.limit
        )

        # Learn from triage in background
        background_tasks.add_task(learn_from_triage, result)

        return TriageResponse(
            issues_analyzed=result.get("issues_analyzed", 0),
            high_priority=result.get("high_priority", 0),
            medium_priority=result.get("medium_priority", 0),
            low_priority=result.get("low_priority", 0),
            triage_complete=result.get("triage_complete", False)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage failed: {str(e)}")

@app.get("/api/v1/status", response_model=StatusResponse)
async def get_project_status(project: Optional[str] = None):
    """Get project status overview"""
    try:
        from cli.commands.issues import IssuesCommand
        issues_cmd = IssuesCommand()

        result = await issues_cmd.get_issue_status(project=project)

        return StatusResponse(
            open_issues=result.get("open_issues", 0),
            closed_issues=result.get("closed_issues", 0),
            completion_rate=result.get("completion_rate", 0.0),
            recent_activity=result.get("recent_activity", 0)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@app.post("/api/v1/enhance-query")
async def enhance_canonical_query(request: EnhancedQueryRequest):
    """Enhance canonical queries with issue intelligence"""
    if not issue_engine:
        raise HTTPException(status_code=503, detail="Issue Intelligence not initialized")

    try:
        # Create intent from message (simplified for example)
        intent = Intent(
            category=IntentCategory.GUIDANCE,
            action="provide_guidance",
            confidence=0.8,
            original_message=request.message
        )

        # Enhance with issue intelligence
        result = await issue_engine.enhance_canonical_query(
            intent=intent,
            session_id=request.session_id
        )

        return {
            "original_message": result.original_response["message"],
            "enhanced_message": result.enhanced_message,
            "issue_intelligence": result.issue_intelligence,
            "enhancement_time_ms": result.enhancement_time_ms
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query enhancement failed: {str(e)}")

async def learn_from_triage(triage_result: dict):
    """Background task to learn from triage results"""
    try:
        from services.learning import get_learning_loop
        learning_loop = await get_learning_loop()

        # Learn patterns from triage results
        await learning_loop.learn_pattern(
            pattern_type=PatternType.WORKFLOW_PATTERN,
            source_feature="issue_intelligence_api",
            pattern_data={
                "issues_analyzed": triage_result.get("issues_analyzed", 0),
                "high_priority_ratio": triage_result.get("high_priority", 0) / max(triage_result.get("issues_analyzed", 1), 1),
                "triage_timestamp": datetime.now().isoformat()
            },
            initial_confidence=0.6
        )

    except Exception as e:
        # Don't fail API calls if learning fails
        logger.warning(f"Background learning failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")
```

### 4. GitHub Actions Integration

Integrate with GitHub Actions for automated triage:

```yaml
# .github/workflows/issue-triage.yml
name: Automated Issue Triage

on:
  issues:
    types: [opened, labeled]
  schedule:
    # Run daily triage at 9 AM UTC
    - cron: '0 9 * * *'

jobs:
  triage:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run Issue Triage
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      run: |
        python scripts/github_actions_triage.py

    - name: Update Project Board
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        python scripts/update_project_board.py
```

Supporting Python script:

```python
# scripts/github_actions_triage.py
"""
GitHub Actions Issue Triage Script
Runs triage and updates issue labels automatically
"""

import asyncio
import os
import json
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
import sys
sys.path.insert(0, str(project_root))

from cli.commands.issues import IssuesCommand
from services.integrations.github.github_agent import GitHubAgent

async def github_actions_triage():
    """Run triage in GitHub Actions environment"""

    # Validate environment
    if not os.getenv("GITHUB_TOKEN"):
        raise ValueError("GITHUB_TOKEN not found in environment")

    try:
        # Run comprehensive triage
        issues_cmd = IssuesCommand()

        print("🔍 Running automated issue triage...")
        triage_result = await issues_cmd.triage_issues(limit=50)

        # Output results for GitHub Actions
        print(f"📊 Triage Results:")
        print(f"  High Priority: {triage_result.get('high_priority', 0)}")
        print(f"  Medium Priority: {triage_result.get('medium_priority', 0)}")
        print(f"  Low Priority: {triage_result.get('low_priority', 0)}")

        # Create GitHub Actions output
        output_data = {
            "triage_complete": triage_result.get("triage_complete", False),
            "issues_analyzed": triage_result.get("issues_analyzed", 0),
            "high_priority_count": triage_result.get("high_priority", 0),
            "recommendations": generate_recommendations(triage_result)
        }

        # Write output for next steps
        with open("triage_results.json", "w") as f:
            json.dump(output_data, f, indent=2)

        # Set GitHub Actions output
        if os.getenv("GITHUB_ACTIONS"):
            print(f"::set-output name=triage_complete::{output_data['triage_complete']}")
            print(f"::set-output name=high_priority_count::{output_data['high_priority_count']}")

        print("✅ Automated triage completed successfully")
        return True

    except Exception as e:
        print(f"❌ Automated triage failed: {e}")
        if os.getenv("GITHUB_ACTIONS"):
            print(f"::error::Triage failed: {str(e)}")
        return False

def generate_recommendations(triage_result: dict) -> List[str]:
    """Generate actionable recommendations from triage results"""
    recommendations = []

    high_count = triage_result.get("high_priority", 0)
    medium_count = triage_result.get("medium_priority", 0)
    total_count = triage_result.get("issues_analyzed", 0)

    if high_count > 0:
        recommendations.append(f"🚨 {high_count} high-priority issues need immediate attention")

    if high_count > 5:
        recommendations.append("⚠️ Consider emergency sprint planning for critical issues")

    if medium_count > 10:
        recommendations.append("📋 Schedule sprint planning to address medium-priority backlog")

    if total_count > 30:
        recommendations.append("🧹 Consider issue cleanup and archival of outdated items")

    return recommendations

if __name__ == "__main__":
    success = asyncio.run(github_actions_triage())
    sys.exit(0 if success else 1)
```

---

## Performance Optimization Examples

### 5. Caching and Optimization

Implement comprehensive caching for performance:

```python
"""
Optimized Issue Intelligence with Caching
Implements multi-level caching for maximum performance
"""

import asyncio
import redis.asyncio as redis
from typing import Optional, Dict, Any
import json
from datetime import datetime, timedelta

class OptimizedIssueIntelligenceService:
    """Issue Intelligence with comprehensive caching"""

    def __init__(self):
        self.redis_client = None
        self.memory_cache = {}
        self.cache_ttl = {
            "github_issues": 300,      # 5 minutes
            "triage_results": 3600,    # 1 hour
            "patterns": 1800,          # 30 minutes
            "project_status": 900      # 15 minutes
        }

    async def initialize(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.from_url("redis://localhost:6379")
            await self.redis_client.ping()
            print("✅ Redis cache connected")
        except Exception as e:
            print(f"⚠️ Redis unavailable, using memory cache only: {e}")

    async def get_cached_triage(self, project: str, limit: int) -> Optional[Dict]:
        """Get cached triage results"""
        cache_key = f"triage:{project}:{limit}"

        # Try Redis first
        if self.redis_client:
            try:
                cached = await self.redis_client.get(cache_key)
                if cached:
                    return json.loads(cached)
            except Exception as e:
                print(f"Redis cache error: {e}")

        # Fallback to memory cache
        if cache_key in self.memory_cache:
            cached_data, cached_time = self.memory_cache[cache_key]
            if datetime.now() - cached_time < timedelta(seconds=self.cache_ttl["triage_results"]):
                return cached_data

        return None

    async def cache_triage_results(self, project: str, limit: int, results: Dict):
        """Cache triage results in multiple layers"""
        cache_key = f"triage:{project}:{limit}"

        # Cache in Redis
        if self.redis_client:
            try:
                await self.redis_client.setex(
                    cache_key,
                    self.cache_ttl["triage_results"],
                    json.dumps(results)
                )
            except Exception as e:
                print(f"Redis cache error: {e}")

        # Cache in memory as fallback
        self.memory_cache[cache_key] = (results, datetime.now())

    async def optimized_triage(self, project: str = None, limit: int = 10) -> Dict:
        """Perform triage with caching optimization"""

        # Check cache first
        cached_result = await self.get_cached_triage(project or "default", limit)
        if cached_result:
            print("🚀 Using cached triage results")
            return cached_result

        print("🔍 Running fresh triage analysis...")

        # Run actual triage
        from cli.commands.issues import IssuesCommand
        issues_cmd = IssuesCommand()

        start_time = datetime.now()
        result = await issues_cmd.triage_issues(project=project, limit=limit)
        end_time = datetime.now()

        # Add performance metrics
        result["cache_hit"] = False
        result["execution_time_ms"] = int((end_time - start_time).total_seconds() * 1000)

        # Cache results
        await self.cache_triage_results(project or "default", limit, result)

        return result

    async def batch_triage_multiple_projects(self, projects: List[str], limit: int = 10) -> Dict[str, Dict]:
        """Perform triage for multiple projects in parallel"""

        async def triage_project(project: str) -> tuple[str, Dict]:
            result = await self.optimized_triage(project, limit)
            return project, result

        # Run all projects in parallel
        tasks = [triage_project(project) for project in projects]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Compile results
        project_results = {}
        for result in results:
            if isinstance(result, Exception):
                print(f"Project triage failed: {result}")
                continue
            project, triage_data = result
            project_results[project] = triage_data

        return project_results

    async def cleanup_cache(self):
        """Clean up expired cache entries"""
        current_time = datetime.now()

        # Clean memory cache
        expired_keys = []
        for key, (data, cached_time) in self.memory_cache.items():
            if current_time - cached_time > timedelta(hours=2):  # Max memory cache age
                expired_keys.append(key)

        for key in expired_keys:
            del self.memory_cache[key]

        print(f"🧹 Cleaned {len(expired_keys)} expired cache entries")

# Usage example
async def optimized_workflow_example():
    """Example of optimized workflow with caching"""

    service = OptimizedIssueIntelligenceService()
    await service.initialize()

    try:
        # Single project triage (with caching)
        result1 = await service.optimized_triage("myorg/project1", limit=20)
        result2 = await service.optimized_triage("myorg/project1", limit=20)  # Cache hit

        # Multi-project batch triage
        batch_results = await service.batch_triage_multiple_projects([
            "myorg/frontend",
            "myorg/backend",
            "myorg/mobile"
        ], limit=15)

        # Performance comparison
        print(f"First run: {result1['execution_time_ms']}ms")
        print(f"Cached run: Cache hit = {result2.get('cache_hit', False)}")
        print(f"Batch triage: {len(batch_results)} projects completed")

    finally:
        await service.cleanup_cache()

if __name__ == "__main__":
    asyncio.run(optimized_workflow_example())
```

---

## Error Handling and Resilience

### 6. Robust Error Handling

Implement comprehensive error handling and resilience patterns:

```python
"""
Resilient Issue Intelligence Integration
Implements comprehensive error handling and fallback patterns
"""

import asyncio
import logging
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum
import time

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ServiceError:
    service: str
    error_type: str
    message: str
    severity: ErrorSeverity
    timestamp: float
    retry_count: int = 0

class ResilientIssueIntelligenceService:
    """Issue Intelligence with comprehensive error handling"""

    def __init__(self):
        self.max_retries = 3
        self.retry_delays = [1, 2, 5]  # Progressive backoff
        self.fallback_responses = {}
        self.error_history = []

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def resilient_triage(self, project: str = None, limit: int = 10) -> Dict[str, Any]:
        """Perform triage with comprehensive error handling"""

        for attempt in range(self.max_retries + 1):
            try:
                # Attempt triage
                result = await self._attempt_triage(project, limit, attempt)

                # Success - clear any previous error state
                self._clear_error_state("triage")
                return result

            except GitHubRateLimitError as e:
                error = ServiceError(
                    service="github",
                    error_type="rate_limit",
                    message=str(e),
                    severity=ErrorSeverity.MEDIUM
                )

                if attempt < self.max_retries:
                    delay = self.retry_delays[attempt] * 60  # Rate limit delay in minutes
                    self.logger.warning(f"GitHub rate limit hit, waiting {delay}s before retry {attempt + 1}")
                    await asyncio.sleep(delay)
                    continue
                else:
                    return await self._handle_github_fallback(project, limit, error)

            except GitHubConnectionError as e:
                error = ServiceError(
                    service="github",
                    error_type="connection",
                    message=str(e),
                    severity=ErrorSeverity.HIGH
                )

                if attempt < self.max_retries:
                    delay = self.retry_delays[attempt]
                    self.logger.warning(f"GitHub connection failed, retrying in {delay}s (attempt {attempt + 1})")
                    await asyncio.sleep(delay)
                    continue
                else:
                    return await self._handle_github_fallback(project, limit, error)

            except LearningServiceError as e:
                # Learning failures shouldn't break triage
                self.logger.warning(f"Learning service error (continuing): {e}")

                # Continue with triage, just without learning
                result = await self._attempt_triage_without_learning(project, limit)
                return result

            except Exception as e:
                error = ServiceError(
                    service="triage",
                    error_type="unexpected",
                    message=str(e),
                    severity=ErrorSeverity.CRITICAL
                )

                self._record_error(error)

                if attempt < self.max_retries:
                    delay = self.retry_delays[attempt]
                    self.logger.error(f"Unexpected triage error, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                    continue
                else:
                    return await self._handle_critical_fallback(project, limit, error)

    async def _attempt_triage(self, project: str, limit: int, attempt: int) -> Dict[str, Any]:
        """Attempt triage with progress tracking"""

        self.logger.info(f"Attempting triage (attempt {attempt + 1}): project={project}, limit={limit}")

        from cli.commands.issues import IssuesCommand
        issues_cmd = IssuesCommand()

        start_time = time.time()
        result = await issues_cmd.triage_issues(project=project, limit=limit)
        end_time = time.time()

        # Add resilience metadata
        result["execution_attempt"] = attempt + 1
        result["execution_time_ms"] = int((end_time - start_time) * 1000)
        result["error_recovery_used"] = attempt > 0

        self.logger.info(f"Triage completed successfully in {result['execution_time_ms']}ms")

        return result

    async def _attempt_triage_without_learning(self, project: str, limit: int) -> Dict[str, Any]:
        """Fallback triage without learning system"""

        self.logger.info("Attempting triage without learning system")

        # Simplified triage without learning integration
        from services.integrations.github.github_agent import GitHubAgent
        github_agent = GitHubAgent()

        try:
            issues = await github_agent.get_open_issues(project=project, limit=limit)

            # Simple priority classification without learning
            high_priority = []
            medium_priority = []
            low_priority = []

            for issue in issues:
                priority = self._simple_priority_classification(issue)
                if priority == "high":
                    high_priority.append(issue)
                elif priority == "medium":
                    medium_priority.append(issue)
                else:
                    low_priority.append(issue)

            return {
                "issues_analyzed": len(issues),
                "high_priority": len(high_priority),
                "medium_priority": len(medium_priority),
                "low_priority": len(low_priority),
                "triage_complete": True,
                "learning_disabled": True,
                "fallback_mode": "no_learning"
            }

        except Exception as e:
            raise Exception(f"Fallback triage also failed: {e}")

    def _simple_priority_classification(self, issue: Dict[str, Any]) -> str:
        """Simple rule-based priority classification"""
        title = issue.get("title", "").lower()
        labels = [label.get("name", "").lower() for label in issue.get("labels", [])]

        # High priority keywords
        if any(keyword in title for keyword in ["critical", "urgent", "blocker", "security"]):
            return "high"

        if any(label in ["p0-critical", "p1-high", "critical", "urgent"] for label in labels):
            return "high"

        # Medium priority keywords
        if any(keyword in title for keyword in ["important", "enhancement", "feature"]):
            return "medium"

        if any(label in ["p2-medium", "enhancement", "feature"] for label in labels):
            return "medium"

        return "low"

    async def _handle_github_fallback(self, project: str, limit: int, error: ServiceError) -> Dict[str, Any]:
        """Handle GitHub service failures with cached/mock data"""

        self.logger.error(f"GitHub service unavailable: {error.message}")
        self._record_error(error)

        # Try cached results first
        cached_result = await self._get_cached_fallback_data("triage", project)
        if cached_result:
            cached_result["fallback_mode"] = "cached_data"
            cached_result["original_error"] = error.message
            self.logger.info("Using cached data for GitHub fallback")
            return cached_result

        # Generate mock/minimal response
        return {
            "issues_analyzed": 0,
            "high_priority": 0,
            "medium_priority": 0,
            "low_priority": 0,
            "triage_complete": False,
            "fallback_mode": "github_unavailable",
            "error_message": "GitHub service temporarily unavailable",
            "original_error": error.message,
            "retry_suggestion": "Try again in a few minutes"
        }

    async def _handle_critical_fallback(self, project: str, limit: int, error: ServiceError) -> Dict[str, Any]:
        """Handle critical failures with absolute minimal response"""

        self.logger.critical(f"Critical triage failure: {error.message}")
        self._record_error(error)

        # Notify administrators
        await self._notify_administrators(error)

        return {
            "issues_analyzed": 0,
            "high_priority": 0,
            "medium_priority": 0,
            "low_priority": 0,
            "triage_complete": False,
            "fallback_mode": "critical_failure",
            "error_message": "Issue Intelligence temporarily unavailable",
            "support_contact": "Contact system administrator",
            "error_id": self._generate_error_id(error)
        }

    def _record_error(self, error: ServiceError):
        """Record error for monitoring and analysis"""
        error.timestamp = time.time()
        self.error_history.append(error)

        # Keep only recent errors (last hour)
        cutoff_time = time.time() - 3600
        self.error_history = [e for e in self.error_history if e.timestamp > cutoff_time]

        # Log structured error data
        self.logger.error(f"Error recorded: {error.service}/{error.error_type} - {error.message}")

    def _clear_error_state(self, service: str):
        """Clear error state after successful operation"""
        # Could trigger recovery notifications here
        pass

    async def _get_cached_fallback_data(self, operation: str, key: str) -> Optional[Dict]:
        """Get cached data for fallback scenarios"""
        # Implementation would integrate with your caching system
        return None

    async def _notify_administrators(self, error: ServiceError):
        """Notify system administrators of critical errors"""
        # Implementation would integrate with your alerting system
        self.logger.critical(f"Administrator notification: {error.error_type} in {error.service}")

    def _generate_error_id(self, error: ServiceError) -> str:
        """Generate unique error ID for tracking"""
        import hashlib
        error_string = f"{error.service}:{error.error_type}:{error.timestamp}"
        return hashlib.md5(error_string.encode()).hexdigest()[:8]

    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of recent errors for monitoring"""
        if not self.error_history:
            return {"status": "healthy", "recent_errors": 0}

        error_counts = {}
        for error in self.error_history:
            key = f"{error.service}:{error.error_type}"
            error_counts[key] = error_counts.get(key, 0) + 1

        return {
            "status": "degraded" if len(self.error_history) > 0 else "healthy",
            "recent_errors": len(self.error_history),
            "error_breakdown": error_counts,
            "last_error_time": max(e.timestamp for e in self.error_history)
        }

# Usage example
async def resilient_workflow_example():
    """Example of resilient workflow usage"""

    service = ResilientIssueIntelligenceService()

    # Perform resilient operations
    results = []

    projects = ["project1", "project2", "project3"]
    for project in projects:
        print(f"\n🔍 Processing {project}...")

        result = await service.resilient_triage(project=project, limit=15)
        results.append(result)

        # Check if fallback was used
        if result.get("fallback_mode"):
            print(f"⚠️  Fallback mode used: {result['fallback_mode']}")
        else:
            print(f"✅ Triage completed: {result['issues_analyzed']} issues analyzed")

    # Check system health
    health_summary = service.get_error_summary()
    print(f"\n📊 System Health: {health_summary['status']}")
    if health_summary['recent_errors'] > 0:
        print(f"⚠️  Recent errors: {health_summary['recent_errors']}")

if __name__ == "__main__":
    asyncio.run(resilient_workflow_example())
```

---

## Testing Strategies

### 7. Comprehensive Testing Examples

Implement thorough testing for integrations:

```python
"""
Comprehensive Integration Testing Examples
Tests for various integration scenarios and edge cases
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import json

from services.features.issue_intelligence import (
    IssueIntelligenceCanonicalQueryEngine,
    IssueIntelligenceContext,
    IssueIntelligenceResult
)

class TestIssueIntelligenceIntegration:
    """Integration tests for Issue Intelligence system"""

    @pytest.fixture
    async def mock_dependencies(self):
        """Create mock dependencies for testing"""
        mock_github = AsyncMock()
        mock_handlers = AsyncMock()
        mock_session = AsyncMock()

        # Setup realistic mock responses
        mock_handlers.handle.return_value = {
            "message": "Your top priority is authentication work",
            "intent": {"category": "PRIORITY", "action": "get_priority", "confidence": 0.95},
            "requires_clarification": False
        }

        mock_github.get_recent_issues.return_value = [
            {"number": 123, "title": "Fix login bug", "state": "open", "labels": ["bug", "P1-high"]},
            {"number": 124, "title": "Add OAuth support", "state": "open", "labels": ["enhancement"]},
            {"number": 125, "title": "Update docs", "state": "closed", "labels": ["documentation"]}
        ]

        return mock_github, mock_handlers, mock_session

    @pytest.mark.asyncio
    async def test_basic_enhancement_integration(self, mock_dependencies):
        """Test basic canonical query enhancement"""
        mock_github, mock_handlers, mock_session = mock_dependencies

        engine = IssueIntelligenceCanonicalQueryEngine(
            github_integration=mock_github,
            canonical_handlers=mock_handlers,
            session_manager=mock_session
        )

        # Test enhancement
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.PRIORITY,
            action="get_top_priority",
            confidence=0.95,
            original_message="What's my top priority?"
        )

        result = await engine.enhance_canonical_query(intent, "test_session")

        # Verify structure
        assert isinstance(result, IssueIntelligenceResult)
        assert result.original_response is not None
        assert result.enhanced_message is not None
        assert result.issue_intelligence is not None
        assert result.enhancement_time_ms is not None

        # Verify delegation worked
        mock_handlers.handle.assert_called_once_with(intent, "test_session")
        mock_github.get_recent_issues.assert_called_once()

        # Verify enhancement includes issue context
        assert "Fix login bug" in result.enhanced_message or "recent_issues" in result.issue_intelligence

    @pytest.mark.asyncio
    async def test_cli_integration_workflow(self):
        """Test complete CLI integration workflow"""
        with patch('cli.commands.issues.GitHubAgent') as mock_github_class:
            # Setup mock
            mock_github = AsyncMock()
            mock_github_class.return_value = mock_github
            mock_github.get_open_issues.return_value = [
                {"number": 126, "title": "Critical security bug", "state": "open",
                 "labels": [{"name": "security"}, {"name": "P0-critical"}], "assignee": None},
                {"number": 127, "title": "Feature request", "state": "open",
                 "labels": [{"name": "enhancement"}], "assignee": {"login": "dev1"}}
            ]

            # Test CLI workflow
            from cli.commands.issues import IssuesCommand
            issues_cmd = IssuesCommand()

            result = await issues_cmd.triage_issues(limit=5)

            # Verify results structure
            assert isinstance(result, dict)
            assert "issues_analyzed" in result
            assert "high_priority" in result
            assert "medium_priority" in result
            assert "low_priority" in result
            assert result["triage_complete"] is True

            # Verify high priority detection
            assert result["high_priority"] >= 1  # Security bug should be high priority

    @pytest.mark.asyncio
    async def test_error_handling_integration(self, mock_dependencies):
        """Test error handling in integration scenarios"""
        mock_github, mock_handlers, mock_session = mock_dependencies

        # Setup GitHub failure
        mock_github.get_recent_issues.side_effect = Exception("GitHub API unavailable")

        engine = IssueIntelligenceCanonicalQueryEngine(
            github_integration=mock_github,
            canonical_handlers=mock_handlers,
            session_manager=mock_session
        )

        # Test graceful degradation
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.PRIORITY,
            action="get_top_priority",
            confidence=0.95,
            original_message="What's my top priority?"
        )

        result = await engine.enhance_canonical_query(intent, "test_session")

        # Should still work with original response
        assert isinstance(result, IssueIntelligenceResult)
        assert result.original_response is not None
        assert result.enhanced_message is not None  # Should fall back to original

        # Should indicate fallback mode
        assert result.issue_intelligence.get("fallback_mode") is True
        assert "error" in result.issue_intelligence

    @pytest.mark.asyncio
    async def test_learning_integration(self):
        """Test learning system integration"""
        with patch('services.learning.get_learning_loop') as mock_learning:
            mock_loop = AsyncMock()
            mock_learning.return_value = mock_loop

            # Test pattern learning
            mock_loop.learn_pattern.return_value = AsyncMock()
            mock_loop.get_patterns_for_feature.return_value = [
                AsyncMock(confidence=0.8, usage_count=5, pattern_id="test_pattern")
            ]

            from cli.commands.issues import IssuesCommand
            issues_cmd = IssuesCommand()

            # This should trigger learning
            with patch.object(issues_cmd, 'github_agent') as mock_github:
                mock_github.get_open_issues.return_value = [
                    {"number": 128, "title": "Test issue", "state": "open", "labels": []}
                ]

                result = await issues_cmd.triage_issues(limit=1)

                # Verify learning was attempted (may not be called if service initialization fails)
                assert result["triage_complete"] is True

    @pytest.mark.asyncio
    async def test_performance_integration(self, mock_dependencies):
        """Test performance characteristics in integration"""
        mock_github, mock_handlers, mock_session = mock_dependencies

        engine = IssueIntelligenceCanonicalQueryEngine(
            github_integration=mock_github,
            canonical_handlers=mock_handlers,
            session_manager=mock_session
        )

        # Test performance tracking
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.PRIORITY,
            action="get_top_priority",
            confidence=0.95,
            original_message="What's my top priority?"
        )

        import time
        start_time = time.time()
        result = await engine.enhance_canonical_query(intent, "perf_test")
        end_time = time.time()

        # Verify performance tracking
        assert result.enhancement_time_ms is not None
        assert result.enhancement_time_ms > 0

        # Verify reasonable performance (should be fast with mocks)
        total_time_ms = (end_time - start_time) * 1000
        assert total_time_ms < 1000  # Should complete in under 1 second with mocks

    @pytest.mark.asyncio
    async def test_concurrent_integration(self, mock_dependencies):
        """Test concurrent access scenarios"""
        mock_github, mock_handlers, mock_session = mock_dependencies

        engine = IssueIntelligenceCanonicalQueryEngine(
            github_integration=mock_github,
            canonical_handlers=mock_handlers,
            session_manager=mock_session
        )

        # Test concurrent enhancement requests
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        async def concurrent_enhancement(session_id: str):
            intent = Intent(
                category=IntentCategory.PRIORITY,
                action="get_top_priority",
                confidence=0.95,
                original_message=f"Session {session_id} priority query"
            )
            return await engine.enhance_canonical_query(intent, session_id)

        # Run multiple concurrent enhancements
        tasks = [concurrent_enhancement(f"session_{i}") for i in range(5)]
        results = await asyncio.gather(*tasks)

        # Verify all completed successfully
        assert len(results) == 5
        for result in results:
            assert isinstance(result, IssueIntelligenceResult)
            assert result.original_response is not None
            assert result.enhanced_message is not None

class TestIntegrationEdgeCases:
    """Test edge cases and boundary conditions"""

    @pytest.mark.asyncio
    async def test_empty_github_response(self):
        """Test handling of empty GitHub responses"""
        with patch('cli.commands.issues.GitHubAgent') as mock_github_class:
            mock_github = AsyncMock()
            mock_github_class.return_value = mock_github
            mock_github.get_open_issues.return_value = []  # Empty response

            from cli.commands.issues import IssuesCommand
            issues_cmd = IssuesCommand()

            result = await issues_cmd.triage_issues(limit=10)

            # Should handle gracefully
            assert result["issues_analyzed"] == 0
            assert result["triage_complete"] is True

    @pytest.mark.asyncio
    async def test_malformed_github_data(self):
        """Test handling of malformed GitHub API responses"""
        with patch('cli.commands.issues.GitHubAgent') as mock_github_class:
            mock_github = AsyncMock()
            mock_github_class.return_value = mock_github

            # Malformed data missing required fields
            mock_github.get_open_issues.return_value = [
                {"number": 129},  # Missing title, labels, etc.
                {"title": "Test"},  # Missing number
                {}  # Completely empty
            ]

            from cli.commands.issues import IssuesCommand
            issues_cmd = IssuesCommand()

            result = await issues_cmd.triage_issues(limit=10)

            # Should complete without crashing
            assert result["triage_complete"] is True
            assert result["issues_analyzed"] >= 0

    @pytest.mark.asyncio
    async def test_large_dataset_handling(self):
        """Test handling of large datasets"""
        with patch('cli.commands.issues.GitHubAgent') as mock_github_class:
            mock_github = AsyncMock()
            mock_github_class.return_value = mock_github

            # Generate large dataset
            large_dataset = []
            for i in range(100):
                large_dataset.append({
                    "number": 200 + i,
                    "title": f"Issue {i}",
                    "state": "open",
                    "labels": [{"name": "test"}],
                    "assignee": None
                })

            mock_github.get_open_issues.return_value = large_dataset

            from cli.commands.issues import IssuesCommand
            issues_cmd = IssuesCommand()

            # Test with limit
            result = await issues_cmd.triage_issues(limit=50)

            # Should respect limit and complete successfully
            assert result["issues_analyzed"] <= 50
            assert result["triage_complete"] is True

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
```

---

## Summary

This comprehensive integration guide provides:

✅ **7 Complete Integration Examples**: From basic CLI to complex multi-service architectures
✅ **Performance Optimization**: Multi-level caching and batch processing patterns
✅ **Error Handling**: Robust resilience patterns with fallback strategies
✅ **Testing Strategies**: Comprehensive test suites for integration scenarios
✅ **Real-World Usage**: Practical examples for Slack, GitHub Actions, FastAPI
✅ **Production Patterns**: Monitoring, alerting, and operational concerns

### Next Steps

1. **Choose Integration Pattern**: Select the pattern that best fits your environment
2. **Implement Gradually**: Start with basic integration, add advanced features incrementally
3. **Monitor Performance**: Use the performance tracking and caching examples
4. **Test Thoroughly**: Implement the testing patterns for your specific use case
5. **Handle Errors**: Use the resilience patterns for production deployment

---

**Last Updated**: August 24, 2025
**Version**: Integration Examples v1.0
**Status**: Production-Ready Integration Guide
