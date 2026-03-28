# Architecture & Data Flow

This project implements a Model Context Protocol (MCP) server designated to act as the **Operational Intelligence Layer** between an LLM Orchestrator (Client) and an offshore maritime database.

## Layered Design Pattern
The server strictly enforces domain-driven bounds to ensure AI interactions remain secure, predictable, and fully decoupled from underlying storage schemas.

```mermaid
graph TD
    subgraph Client [LLM Orchestrator / MCP Client]
        A[Context Engine]
        B[Function Caller]
    end

    subgraph FastMCP [MCP Server Layer]
        C((stdio Interface))
        D[Tools API]
        E[Resources API]
    end

    subgraph Services [Domain Operations]
        F[Inventory Service]
        G[Procurement Service]
        H[Logistics Service]
        I[Maintenance Service]
        J[Fleet Service]
    end

    subgraph Data [Repository Layer]
        K[Database Repositories]
        L[(SQLite: offshore_logistics.db)]
        M[ActionAudit DB Ledgers]
    end

    A -->|Reads Context URIs| E
    B -->|Executes Filtered Actions| D
    D -->|Intercepted by Metric Decorators| F & G & H & I & J
    E -->|Intercepted by Metric Decorators| F & G & H & I & J
    F & G & H & I & J -->|Strict Pydantic DTOs| D & E
    F & G & H & I & J --> K
    K --> L & M
```

### 1. Database as Operational Truth (Data Layer)
All actual logistics telemetry (shipments, warehouses, critical events) resides strictly in the relational SQLite database setup by `schema.sql`.

### 2. Repositories (Data Access)
Repositories (`inventory_repo.py`, etc) are the exclusive entry point for SQLAlchemy queries and database joins. They map complex SQL queries mapping to raw Data Models.

### 3. Business Service Layer
Services orchestrate logic bridging raw data models and external requirements. Because this is an *AI-first* backend, Services perform specific heuristic calculations:
- `ProcurementService`: Derives **`operational_risk_status`** natively by weighing the `expected_delivery` timestamps against today's date rather than relying on standard DB statuses.
- `InventoryService`: Validates numeric feasibility constraints during a `reserve_stock` attempt and gracefully translates insufficient funds into specific `DomainExceptions` rather than raw SQL failures.

### 4. FastMCP Handlers
The entry point script handles stdio handshakes natively using `mcp[cli]`. Functions wrapped in `@mcp.tool()` act strictly as parameter validation and Error-Catchers, shielding the host platform from unexpected tracebacks. No logic lives inside the handler!
