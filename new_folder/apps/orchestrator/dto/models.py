from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class TaskRequest(BaseModel):
    task_id: str
    original_prompt: str
    workflow_type: str

class WorkflowStepResult(BaseModel):
    step_name: str
    mcp_tool_called: str
    mcp_arguments: Dict[str, Any]
    success: bool
    result_data: Any
    duration_ms: float
    error_message: Optional[str] = None

class ExecutionLog(BaseModel):
    task_id: str
    workflow_type: str
    start_time: datetime
    end_time: Optional[datetime] = None
    steps: List[WorkflowStepResult] = Field(default_factory=list)
    final_status: str = "In Progress"

class Recommendation(BaseModel):
    task_id: str
    workflow_type: str
    summary: str
    recommended_action: str
    operational_rationale: str
    execution_trace_summary: List[str]
