# Orchestrator MVP Architecture

The **Customs & Supply Chain Autonomous Agent** orchestrator sits as a discrete client component completely insulated from the underlying Database logic. Instead of building massive internal agents bound closely to SQL, we constructed a strict **Model Context Protocol (MCP)** execution wrapper via `mcp.client.stdio_client`.

## Layer 1: Deterministic Plan Mapping (`TaskPlanner`)
Because we want to constrain outputs and verify stability before unleashing LLM logic natively, the MVP classifies English prompts (e.g. "Resolve missing spare part WO-204") natively matching prompt heuristics -> `MISSING_CRITICAL_SPARE`.

## Layer 2: Workflow Executions (`WorkflowExecutor` & `Workflows`)
A strict sequential workflow runs across `Apps/orchestrator/workflows/*.py`:
The executor yields `client.call_tool("tool_name")` over the async Stdio subprocess mapping. If the payload returns `"status": "error"`, it is captured safely within the `ExecutionLog` without tearing down the python thread, allowing the Orchestrator to decide if it should pivot or generate a fallback recommendation. 

## Layer 3: Pydantic DTO Contextualization
The output boundaries are normalized around `WorkflowStepResult` and `Recommendation` models ensuring they serialize consistently for frontends and dashboard demos natively. 

## Safety Mapping (Why not Database?)
By querying the MCP Tools exclusively, the orchestrator acts *exactly* like an external LLM platform would (e.g., Anthropic desktop app). This forces our backend constraints to prove their safety natively against the Orchestrator instead of exposing naked DB credentials globally. This keeps our domain service layers incredibly strict.
