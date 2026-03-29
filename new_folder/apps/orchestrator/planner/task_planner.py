from apps.orchestrator.dto.models import TaskRequest

class TaskPlanner:
    """Classifies string inputs natively mapping them to deterministic MVP orchestrator pipelines."""
    
    def classify_task(self, prompt: str, task_id: str) -> TaskRequest:
        prompt_lower = prompt.lower()
        if "missing" in prompt_lower or "spare" in prompt_lower or "wo-" in prompt_lower:
            workflow = "MISSING_CRITICAL_SPARE"
        elif "delay" in prompt_lower or "shp" in prompt_lower:
            workflow = "DELAYED_SHIPMENT"
        elif "po" in prompt_lower or "risk" in prompt_lower:
            workflow = "AT_RISK_PO"
        else:
            workflow = "UNKNOWN"
            
        return TaskRequest(task_id=task_id, original_prompt=prompt, workflow_type=workflow)
