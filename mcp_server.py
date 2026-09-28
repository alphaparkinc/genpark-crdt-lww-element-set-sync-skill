import sys, json
from client import LWWElementSet

crdt = LWWElementSet()

def handle_jsonrpc(line):
    global crdt
    try:
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "genpark-crdt-lww-element-set-sync-skill", "version": "1.0.0"}, "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                {"name": "crdt_add", "description": "Add an element.", "inputSchema": {"type": "object", "properties": {"element": {"type": "string"}, "timestamp": {"type": "number"}}, "required": ["element"]}},
                {"name": "crdt_remove", "description": "Remove an element.", "inputSchema": {"type": "object", "properties": {"element": {"type": "string"}, "timestamp": {"type": "number"}}, "required": ["element"]}},
                {"name": "crdt_elements", "description": "List all active surviving elements.", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "benchmark_crdt_sync", "description": "Run CRDT sync benchmark.", "inputSchema": {"type": "object", "properties": {}}}
            ]}}
        elif method == "tools/call":
            params = req.get("params", {})
            tool = params.get("name")
            args = params.get("arguments", {})
            if tool == "crdt_add":
                res = crdt.add(args.get("element"), args.get("timestamp"))
            elif tool == "crdt_remove":
                res = crdt.remove(args.get("element"), args.get("timestamp"))
            elif tool == "crdt_elements":
                res = {"elements": crdt.elements()}
            elif tool == "benchmark_crdt_sync":
                res = crdt.benchmark_crdt_sync()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_jsonrpc(line.strip())), flush=True)

if __name__ == "__main__":
    main()
