# Observability & Audit Layer

The orchestration integrations rely heavily on logging structured constraints back to the operations side. Without observability, AI tooling actions are a black box. Our architecture tackles this natively and asynchronously.

## 📝 Tool Invocation Logging
Every MCP Tool and Resource is prefixed with standard Python `sys.stderr` writes generating a unique UUID correlation id on invocation, capturing `start` and `end` times, and `success` mappings organically. 
Since `stdio` communication happens over standard output (`stdout`), piping logs into `sys.stderr` guarantees they never corrupt JSON-RPC traces expected by tools like Anthropic's host platform. 

### Payload Sanitization
Payloads passed inside the `@observable_action` dynamically drop keys mapped as `secret`, `password`, `key` entirely to protect sensitive data structures being indexed in bare metal logs. 

## ⚖️ Audit Tracking (Post-Mortem Verification)
The SQLite schema binds `ActionAudit` tracking exclusively when the action wrapper flags the `category` as `"write"` or `"draft"`. Action mutations write their input keys and deterministic statuses automatically natively avoiding DB rollbacks since they intercept at the service level. This generates persistent SQL rows containing deterministic payload shapes allowing support ops to audit specifically what the AI "tried" to accomplish (example: `create_transfer_plan` failure strings are saved to the log!)

## 📊 In-Memory Metrics Registry
The `shared.observability.metrics` dictionary captures live-state counts (how many `drafts` versus `writes`, the average duration `time.time() - start_time` logic across operations) globally. This natively hooks inside MCP via internal endpoints like `ops://recent_tool_activity`!
