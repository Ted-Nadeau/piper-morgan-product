from typing import Optional

from services.integrations.github.github_agent import GitHubAgent


class OrchestrationEngine:
    def __init__(self):
        self.github_analyzer = GitHubIssueAnalyzer()
        self.github_agent = GitHubAgent()

    async def _create_github_issue(self, workflow: Workflow, task: Task) -> TaskResult:
        """Create a GitHub issue from workflow context."""
        try:
            # Extract required fields from context
            repository = workflow.context.get("repository")
            title = workflow.context.get("title", "New Issue")
            body = workflow.context.get("body", "")
            labels = workflow.context.get("labels", [])

            # Validate required fields
            if not repository:
                return TaskResult(
                    success=False, error="Repository not specified in workflow context"
                )

            # Create the issue
            issue_data = await self.github_agent.create_issue(
                repo_name=repository, title=title, body=body, labels=labels
            )

            return TaskResult(
                success=True,
                output_data={
                    "issue_number": issue_data.get("number"),
                    "issue_url": issue_data.get("html_url"),
                    "issue_data": issue_data,
                },
            )

        except Exception as e:
            logger.error(f"Failed to create GitHub issue: {str(e)}")
            return TaskResult(success=False, error=f"GitHub API error: {str(e)}")

    async def create_workflow_from_intent(self, intent: Intent) -> Optional[Workflow]:
        """Create appropriate workflow based on intent with database persistence"""
        workflow = await self.factory.create_from_intent(intent)
        if workflow:
            # Enrich CREATE_TICKET workflows with repository from project
            if workflow.type == WorkflowType.CREATE_TICKET:
                project_id = intent.context.get("project_id")
                if project_id:
                    try:
                        repos = await RepositoryFactory.get_repositories()
                        project_repo = repos["projects"]
                        project = await project_repo.get_by_id(project_id)
                        if project:
                            repository = project.get_github_repository()
                            if repository:
                                workflow.context["repository"] = repository
                                logger.info(
                                    f"Enriched CREATE_TICKET workflow with repository: {repository}"
                                )
                            else:
                                logger.warning(
                                    f"Project {project_id} has no GitHub repository configured"
                                )
                        else:
                            logger.warning(f"Project {project_id} not found")
                    except Exception as e:
                        logger.error(f"Failed to enrich workflow with repository: {str(e)}")
                        # Continue without repository - handler will provide appropriate error
            # Store in memory for execution
            self.workflows[workflow.id] = workflow
            # Persist to database using repository pattern
            await self._persist_workflow_to_database(workflow)
        return workflow
