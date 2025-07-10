import json
from datetime import datetime
from typing import List, Optional

import asyncpg

from services.domain.models import (Workflow, WorkflowResult, WorkflowStatus,
                                    WorkflowType)


class WorkflowRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def save(self, workflow: Workflow) -> str:
        """Save workflow to database"""
        # Convert WorkflowResult to output_data
        output_data = None
        if workflow.result:
            output_data = {
                "success": workflow.result.success,
                "data": workflow.result.data,
                "error": workflow.result.error,
                "created_at": workflow.result.created_at.isoformat(),
            }

        async with self.db_pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO workflows (id, type, status, context, output_data, error, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (id) DO UPDATE SET
                    status = $3, context = $4, output_data = $5, error = $6
            """,
                workflow.id,
                workflow.type.value,
                workflow.status.value,
                json.dumps(workflow.context),
                json.dumps(output_data) if output_data else None,
                workflow.error,
                workflow.created_at,
            )
        return workflow.id

    async def find_by_id(self, workflow_id: str) -> Optional[Workflow]:
        """Find workflow by ID"""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM workflows WHERE id = $1", workflow_id
            )
            if row:
                return self._row_to_workflow(row)
        return None

    def _row_to_workflow(self, row) -> Workflow:
        """Convert database row to Workflow object"""
        # Handle enum name to value conversion
        workflow_type_str = row["type"]
        if workflow_type_str in [wt.name for wt in WorkflowType]:
            # Convert enum name to value
            workflow_type = WorkflowType[workflow_type_str]
        else:
            # Assume it's already a value
            workflow_type = WorkflowType(workflow_type_str)

        status_str = row["status"]
        if status_str in [ws.name for ws in WorkflowStatus]:
            # Convert enum name to value
            workflow_status = WorkflowStatus[status_str]
        else:
            # Assume it's already a value
            workflow_status = WorkflowStatus(status_str)

        # Convert output_data to WorkflowResult
        result = None
        if row["output_data"]:
            try:
                output_data = json.loads(row["output_data"])
                # Create WorkflowResult from output_data
                from services.domain.models import WorkflowResult

                result = WorkflowResult(
                    success=output_data.get("success", False),
                    data=output_data.get("data", {}),
                    error=output_data.get("error"),
                    created_at=row["created_at"] or datetime.now(),
                )
            except (json.JSONDecodeError, AttributeError, TypeError):
                # Handle invalid JSON or None values gracefully
                result = None

        return Workflow(
            id=row["id"],
            type=workflow_type,
            status=workflow_status,
            context=json.loads(row["context"]) if row["context"] else {},
            result=result,
            error=row["error"],
            intent_id=None,  # Not stored in database, would need separate query
            created_at=row["created_at"],
            updated_at=row["completed_at"]
            or row[
                "created_at"
            ],  # Use completed_at as updated_at, fallback to created_at
        )
