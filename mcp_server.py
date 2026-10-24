"""MCP Stdio Server for Circuit Breaker Fault Sentinel.
100% Python Standard Library.
"""
import sys
import json
from client import CircuitBreakerFaultSentinel

sentinel = CircuitBreakerFaultSentinel()

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-circuit-breaker-fault-sentinel-skill", "version": "1.0.1"},
            "capabilities": {"tools": {}}
        }
        send_response(req_id, res)
    elif method == "tools/list":
        tools = [
            {
                "name": "can_execute",
                "description": "Check if request is permitted by circuit breaker (fails fast if OPEN)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service_name": {"type": "string"}
                    },
                    "required": ["service_name"]
                }
            },
            {
                "name": "record_result",
                "description": "Ingest execution success or failure outcome into circuit breaker state",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service_name": {"type": "string"},
                        "success": {"type": "boolean", "default": True},
                        "latency_ms": {"type": "number", "default": 0.0}
                    },
                    "required": ["service_name"]
                }
            },
            {
                "name": "get_state",
                "description": "Retrieve current circuit breaker state, failure counts, and cooldown timers",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service_name": {"type": "string"}
                    },
                    "required": ["service_name"]
                }
            },
            {
                "name": "reset",
                "description": "Force reset circuit to CLOSED state",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service_name": {"type": "string"}
                    },
                    "required": ["service_name"]
                }
            }
        ]
        send_response(req_id, {"tools": tools})
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "can_execute":
            out = {"service_name": args.get("service_name"), "allowed": sentinel.can_execute(args.get("service_name", ""))}
        elif name == "record_result":
            out = sentinel.record_result(args.get("service_name", ""), args.get("success", True), float(args.get("latency_ms", 0.0)))
        elif name == "get_state":
            out = sentinel.get_state(args.get("service_name", ""))
        elif name == "reset":
            out = sentinel.reset(args.get("service_name", ""))
        else:
            send_error(req_id, -32601, f"Unknown tool: {name}")
            return
        send_response(req_id, {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]})

def send_response(req_id, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}) + "\n")
    sys.stdout.flush()

def send_error(req_id, code, message):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
