from typing import Any
from apps.orchestrator.client.mcp_client import AsyncMCPClient
from apps.orchestrator.dto.models import Recommendation, TaskRequest
from apps.orchestrator.executor.workflow_executor import WorkflowExecutor

class BaseWorkflow:
    def __init__(self, request: TaskRequest, client: AsyncMCPClient, executor: WorkflowExecutor):
        self.request = request
        self.client = client
        self.executor = executor
        
    async def run(self) -> Recommendation:
        """Execute the workflow async sequentially and synthesize final result."""
        raise NotImplementedError("Each specific workflow must instantiate its own run bounds.")
