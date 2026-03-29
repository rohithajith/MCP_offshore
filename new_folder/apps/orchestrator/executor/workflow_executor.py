import time
import json
from datetime import datetime
from typing import Any, Dict

from apps.orchestrator.client.mcp_client import AsyncMCPClient
from apps.orchestrator.dto.models import WorkflowStepResult, ExecutionLog

class WorkflowExecutor:
    """Manages the execution lifecycle logging traces asynchronously."""
    
    def __init__(self, trace_log: ExecutionLog, client: AsyncMCPClient):
        self.trace_log = trace_log
        self.client = client
        
    async def execute_tool(self, step_name: str, tool_name: str, arguments: Dict[str, Any]) -> Any:
        start_time = time.time()
        success = True
        error_msg = None
        result_json = None
        
        try:
            result_json = await self.client.call_tool(tool_name, arguments)
            # Basic parse to check if 'status' == 'error' from our FastMCP architecture wrappers
            parsed = json.loads(result_json)
            if isinstance(parsed, dict) and parsed.get("status") == "error":
                success = False
                error_msg = parsed.get("message", "Unknown operational error.")
        except Exception as e:
            success = False
            error_msg = str(e)
            result_json = json.dumps({"status": "error", "message": error_msg})
            
        duration_ms = (time.time() - start_time) * 1000
        
        step_result = WorkflowStepResult(
            step_name=step_name,
            mcp_tool_called=tool_name,
            mcp_arguments=arguments,
            success=success,
            result_data=result_json,
            duration_ms=duration_ms,
            error_message=error_msg
        )
        self.trace_log.steps.append(step_result)
        return step_result

    async def read_resource(self, step_name: str, resource_uri: str) -> Any:
        start_time = time.time()
        success = True
        error_msg = None
        result_json = None
        
        try:
            result_json = await self.client.read_resource(resource_uri)
            parsed = json.loads(result_json)
            if isinstance(parsed, dict) and parsed.get("status") == "error":
                success = False
                error_msg = parsed.get("message", "Unknown operational error reading resource.")
        except Exception as e:
            success = False
            error_msg = str(e)
            result_json = json.dumps({"status": "error", "message": error_msg})

        duration_ms = (time.time() - start_time) * 1000
        
        step_result = WorkflowStepResult(
            step_name=step_name,
            mcp_tool_called=f"READ {resource_uri}",
            mcp_arguments={},
            success=success,
            result_data=result_json,
            duration_ms=duration_ms,
            error_message=error_msg
        )
        self.trace_log.steps.append(step_result)
        return step_result
