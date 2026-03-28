import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from apps.mcp_server.server import run_local_simulator

def test_all():
    print("--- 1. Testing check_part_availability ---")
    run_local_simulator("check_part_availability", {"part_id": "VALVE-CRIT-001"})
    
    print("\n--- 2. Testing list_open_work_orders ---")
    run_local_simulator("list_open_work_orders", {"priority": "Emergency"})
    
    print("\n--- 3. Testing trace_shipment ---")
    run_local_simulator("trace_shipment", {"shipment_id": "TRK-DELAY-999"})
    
    print("\nTests complete.")

if __name__ == "__main__":
    test_all()
