import asyncio
import argparse
import sys
import json
import uuid
from datetime import datetime

# Adjust module path dynamically so we can run directly
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from apps.orchestrator.client.mcp_client import AsyncMCPClient
from apps.orchestrator.planner.task_planner import TaskPlanner
from apps.orchestrator.dto.models import ExecutionLog, Recommendation
from apps.orchestrator.executor.workflow_executor import WorkflowExecutor

# Workflow Implementations
from apps.orchestrator.workflows.missing_part import MissingPartWorkflow
from apps.orchestrator.workflows.delayed_shipment import DelayedShipmentWorkflow
from apps.orchestrator.workflows.at_risk_po import AtRiskPOWorkflow

async def run_orchestrator(task_prompt: str):
    task_id = str(uuid.uuid4())
    print("\n" + "="*80)
    print(f"[ORCHESTRATOR] Received Task: '{task_prompt}'")
    print("="*80)
    
    # 1. Plan
    planner = TaskPlanner()
    task_req = planner.classify_task(task_prompt, task_id)
    print(f"| Planning Phase | > Mapped Task to Type: {task_req.workflow_type}")
    
    if task_req.workflow_type == "UNKNOWN":
        print(f"| Error | > Unrecognized task pattern. Aborting.")
        return
        
    # 2. Setup Execution Bounds
    client = AsyncMCPClient()
    trace_log = ExecutionLog(
        task_id=task_id,
        workflow_type=task_req.workflow_type,
        start_time=datetime.now()
    )
    executor = WorkflowExecutor(trace_log, client)
    
    # 3. Instantiate Workflow
    workflow = None
    if task_req.workflow_type == "MISSING_CRITICAL_SPARE":
        workflow = MissingPartWorkflow(task_req, client, executor)
    elif task_req.workflow_type == "DELAYED_SHIPMENT":
        workflow = DelayedShipmentWorkflow(task_req, client, executor)
    elif task_req.workflow_type == "AT_RISK_PO":
        workflow = AtRiskPOWorkflow(task_req, client, executor)

    if not workflow:
        return
        
    print(f"| Execution Phase | > Chaining Async MCP Steps via Protocol Over Stdio...\n")
    
    try:
        recommendation: Recommendation = await workflow.run()
        trace_log.final_status = "Success"
        trace_log.end_time = datetime.now()
        
        # 4. Synthesize Final Report
        print(f"\n[RECOMMENDATION ENGINE]")
        print(f"Workflow:  {recommendation.workflow_type}")
        print(f"Summary:   {recommendation.summary}")
        print(f"Action:    {recommendation.recommended_action}")
        print(f"Rationale: {recommendation.operational_rationale}")
        print("\n[EXECUTION TRACE]")
        for idx, step_str in enumerate(recommendation.execution_trace_summary):
            print(f"  {idx+1}. {step_str}")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n[CRITICAL ERROR] Workflow crashed natively: {str(e)}")
        trace_log.final_status = "Failed"

def main():
    parser = argparse.ArgumentParser(description="Customs & Supply Chain Autonomous Agent (Orchestrator MVP)")
    parser.add_argument("--task", type=str, required=True, help="Describe the internal logistics disruption.")
    args = parser.parse_args()
    
    asyncio.run(run_orchestrator(args.task))

if __name__ == "__main__":
    main()
