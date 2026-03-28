import logging
import sys

def get_stderr_logger(name: str = "mcp_server") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        # ONLY log to stderr to prevent MCP JSON-RPC protocol corruption
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger

log = get_stderr_logger()
