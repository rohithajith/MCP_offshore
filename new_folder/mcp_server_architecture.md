# MCP Server Architecture Skeleton: Maritime Fleet & Cargo

This document provides the foundational architecture for the local-first offshore maritime logistics intelligence platform MCP server. It enforces a strict separation of concerns, ensuring tools and resources are decoupled from direct database access.

---

## A. Folder Structure

The application follows a clean layout separating the core application layer (`apps/mcp_server`) from the business logic and database layers (`packages/`).

```text
mcp-offshore-server/
├── .env
├── requirements.txt
├── apps/
│   └── mcp_server/
│       ├── __init__.py
│       ├── server.py           # Entrypoint and bootstrap
│       ├── config.py           # Pydantic settings
│       ├── registry.py         # MCP Tool/Resource registration logic
│       ├── dependencies.py     # DI container (DB session provision)
│       ├── schema/             # MCP specific transport models
│       ├── resources/
│       │   ├── __init__.py
│       │   ├── fleet_resources.py
│       │   └── inventory_resources.py
│       └── tools/
│           ├── __init__.py
│           ├── fleet_tools.py
│           ├── inventory_tools.py
│           └── logistics_tools.py
└── packages/
    ├── db/
    │   ├── __init__.py
    │   ├── session.py          # Engine and sessionmaker setup
    │   ├── base.py             # SQLAlchemy DeclarativeBase
    │   ├── models/             # SQLAlchemy ORM definitions
    │   └── repositories/
    │       ├── __init__.py
    │       ├── base.py         # Generic BaseRepository(T)
    │       ├── fleet_repo.py
    │       ├── inventory_repo.py
    │       └── logistics_repo.py
    ├── domain/
    │   ├── __init__.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── fleet_service.py
    │   │   ├── inventory_service.py
    │   │   └── shipment_service.py
    │   ├── dto/
    │   │   ├── __init__.py
    │   │   └── fleet_dto.py
    │   │   └── inventory_dto.py
    │   │   └── common_dto.py
    │   ├── enums/
    │   └── exceptions/
    │       └── core_exceptions.py
    └── shared/
        ├── logging/
        │   └── logger.py
        └── utils/
```

---

## B. Code Files (Skeletons)

### 1. Configuration Layer (`apps/mcp_server/config.py`)
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Maritime Logistics MCP Server"
    ENVIRONMENT: str = "local"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///../offshore_logistics.db"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
```

### 2. Database & Repository Layer (`packages/db/session.py` & `repositories/base.py`)
```python
# packages/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from apps.mcp_server.config import settings

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
# packages/db/repositories/base.py
from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.orm import Session

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_by_id(self, id: str) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def list_all(self, limit: int = 100) -> List[T]:
        return self.db.query(self.model).limit(limit).all()

# Example Domain Repository (packages/db/repositories/inventory_repo.py)
from packages.db.repositories.base import BaseRepository
# from packages.db.models.inventory import InventoryStock 

class InventoryRepository(BaseRepository):
    def __init__(self, db: Session):
        # super().__init__(db, InventoryStock)
        pass

    def get_part_stock_across_warehouses(self, part_id: str):
        # Specific query logic executing joined loads
        pass
```

### 3. Domain DTOs (`packages/domain/dto/inventory_dto.py`)
```python
from pydantic import BaseModel
from typing import List, Optional

class WarehouseStockDTO(BaseModel):
    warehouse_name: str
    quantity_on_hand: int
    quantity_reserved: int
    net_available: int

class PartAvailabilityResultDTO(BaseModel):
    part_id: str
    sku: str
    part_name: str
    is_critical: bool
    total_global_available: int
    locations: List[WarehouseStockDTO]
```

### 4. Domain Services (`packages/domain/services/inventory_service.py`)
```python
from sqlalchemy.orm import Session
from packages.db.repositories.inventory_repo import InventoryRepository
from packages.domain.dto.inventory_dto import PartAvailabilityResultDTO
from packages.domain.exceptions.core_exceptions import NotFoundError

class InventoryService:
    def __init__(self, db: Session):
        self.inventory_repo = InventoryRepository(db)
        # self.part_repo = PartRepository(db)

    def check_part_availability(self, part_id: str, warehouse_id: str = None) -> PartAvailabilityResultDTO:
        """
        Business logic mapping. Fetches multiple entities, calculates net availability,
        and returns a clean structured DTO for the MCP layer.
        """
        # 1. Fetch data from repos
        # 2. Apply business logic (e.g. calc net available = on_hand - reserved)
        # 3. Handle errors (raise NotFoundError if part does not exist)
        # 4. Return PartAvailabilityResultDTO
        pass
```

### 5. Exception Handling (`packages/domain/exceptions/core_exceptions.py`)
```python
class DomainException(Exception):
    """Base exception for domain logic errors."""
    pass

class NotFoundError(DomainException):
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(f"{entity_name} with id {entity_id} not found.")

class InsufficientStockError(DomainException):
    def __init__(self, part_id: str, required: int, available: int):
        super().__init__(f"Cannot reserve {required} units for part {part_id}. Only {available} available.")
```

### 6. MCP Registry (`apps/mcp_server/registry.py`)
```python
from typing import Callable, Dict, Any, List

class MCPRegistry:
    def __init__(self):
        self.tools: Dict[str, dict] = {}
        self.resources: Dict[str, dict] = {}

    def register_tool(self, name: str, description: str, handler: Callable, input_schema: Any = None):
        self.tools[name] = {
            "description": description,
            "handler": handler,
            "schema": input_schema
        }
        print(f"Registered Tool: {name}")

    def register_resource(self, uri: str, name: str, description: str, handler: Callable):
        self.resources[uri] = {
            "name": name,
            "description": description,
            "handler": handler
        }
        print(f"Registered Resource: {uri}")

mcp_registry = MCPRegistry()
```

### 7. MCP Tools Handler Layer (`apps/mcp_server/tools/inventory_tools.py`)
```python
from sqlalchemy.orm import Session
from apps.mcp_server.registry import mcp_registry
from packages.domain.services.inventory_service import InventoryService
from packages.domain.exceptions.core_exceptions import DomainException

def check_part_availability_handler(db: Session, args: dict) -> dict:
    """Thin wrapper connecting the MCP protocol signature to the business service."""
    try:
        part_id = args.get("part_id")
        warehouse_id = args.get("warehouse_id")
        
        service = InventoryService(db)
        dto_result = service.check_part_availability(part_id, warehouse_id)
        
        # Output optimized for AI consumption
        return {
            "status": "success",
            "data": dto_result.model_dump()
        }
    except DomainException as e:
        return {"status": "error", "message": str(e)}

# Registration at module load time
mcp_registry.register_tool(
    name="check_part_availability",
    description="Check stock availability for a specific part across all local warehouses.",
    handler=check_part_availability_handler
)
```

### 8. Server Entrypoint (`apps/mcp_server/server.py`)
```python
from apps.mcp_server.config import settings
from apps.mcp_server.registry import mcp_registry
from packages.db.session import SessionLocal

# Import modules to execute their registry.register_... calls
import apps.mcp_server.tools.inventory_tools
# import apps.mcp_server.resources.fleet_resources

def bootstrap_server():
    print(f"Starting {settings.APP_NAME} in {settings.ENVIRONMENT} mode...")
    print(f"Loaded {len(mcp_registry.tools)} tools and {len(mcp_registry.resources)} resources.")
    
    # -------------------------------------------------------------
    # Simulated MCP runtime connection loop
    # In a real environment, this connects to stdio / sse handlers
    # -------------------------------------------------------------
    
    # Example simulated execution:
    # db = SessionLocal()
    # tool = mcp_registry.tools["check_part_availability"]
    # result = tool["handler"](db, {"part_id": "VALVE-CRIT-001"})
    # print(result)
    # db.close()

if __name__ == "__main__":
    bootstrap_server()
```

---

## C. Explanations of Layers

1. **`db/repositories`**: Owns all SQLAlchemy ORM imports and complex queries. It abstracts SQL/joins away from the rest of the application. It returns raw models or tuples to the layer above.
2. **`domain/services`**: The core brain. It asks repositories for data, performs calculations (e.g., determining delays, verifying stock availability vs reservations), and maps the data into Pydantic DTOs.
3. **`domain/dto`**: Response models explicitly designed to present clean, structured nested JSON that an LLM can parse and summarize easily. It ensures the raw database UUIDs and timestamps are formatted logically.
4. **`mcp_server/tools & resources`**: The thin "controller" layer. It unpacks dictionary arguments natively passed in by the MCP server, acquires a database session, calls a service method, catches `DomainExceptions`, and serializes the Pydantic DTO back into a plain dictionary wrapper for the MCP protocol transport.
5. **`registry.py`**: A unified discovery layer. Before the server starts receiving JSON-RPC streams, it knows exactly what tools exist, what their names/descriptions are, and which python function to route them to.

---

## D. Extension Notes

**How to add a new domain/tool later (e.g., Procurement Status Tool):**
1. Add `ProcurementRepository` inside `packages/db/repositories/procurement_repo.py` to handle queries for PO tables.
2. Define the expected AI response schema in `packages/domain/dto/procurement_dto.py` (e.g., `POLineStatusDTO`).
3. Create `ProcurementService.get_po_status(po_id)` in `domain/services/`. It instantiates `ProcurementRepository`, checks `expected_delivery` against today's date, and outputs the DTO.
4. Create `apps/mcp_server/tools/procurement_tools.py`. Write a fast handler that extracts `po_id` from the MCP `args`, injects the DB session, calls the service, and catches errors. Call `mcp_registry.register_tool()`.
5. Import `procurement_tools.py` in `server.py` to ensure it registers at boot. Done.
