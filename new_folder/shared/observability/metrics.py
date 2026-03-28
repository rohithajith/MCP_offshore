"""Lightweight in-memory metrics registry for FastMCP tools & resources."""
from threading import Lock
from collections import defaultdict
from typing import Dict, Any

class MetricsRegistry:
    def __init__(self):
        self.lock = Lock()
        
        self.total_tool_calls = 0
        self.total_resource_reads = 0
        
        # Maps name -> count
        self.calls_per_tool = defaultdict(int) 
        self.failures_per_tool = defaultdict(int)
        
        # Maps name -> total_ms
        self.duration_per_tool = defaultdict(float)
        
        self.count_writes = 0
        self.count_drafts = 0
        self.count_reads = 0

    def record_execution(self, tool_or_resource_name: str, duration_ms: float, success: bool, category: str, is_resource: bool):
        with self.lock:
            if is_resource:
                self.total_resource_reads += 1
            else:
                self.total_tool_calls += 1
                
            self.calls_per_tool[tool_or_resource_name] += 1
            
            if not success:
                self.failures_per_tool[tool_or_resource_name] += 1
                
            self.duration_per_tool[tool_or_resource_name] += duration_ms
            
            if category == "write":
                self.count_writes += 1
            elif category == "draft":
                self.count_drafts += 1
            elif category == "read":
                self.count_reads += 1

    def get_summary(self) -> Dict[str, Any]:
        with self.lock:
            avg_duration = {}
            for name, count in self.calls_per_tool.items():
                if count > 0:
                    avg_duration[name] = round(self.duration_per_tool[name] / count, 2)
                    
            return {
                "total_tool_calls": self.total_tool_calls,
                "total_resource_reads": self.total_resource_reads,
                "count_writes": self.count_writes,
                "count_drafts": self.count_drafts,
                "count_reads": self.count_reads,
                "failures_per_tool": dict(self.failures_per_tool),
                "calls_per_tool": dict(self.calls_per_tool),
                "avg_duration_ms_per_tool": avg_duration
            }

metrics_registry = MetricsRegistry()
