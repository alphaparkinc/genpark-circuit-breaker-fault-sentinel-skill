# GenPark Circuit Breaker Fault Sentinel

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Standard Library](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![GenPark](https://img.shields.io/badge/GenPark-Official-purple.svg)](https://www.genpark.ai)

Three-state circuit breaker with failure rate tripping and automatic half-open probe recovery for resilient agent calls.

Part of the **GenPark AI Agent Skills Ecosystem**.

---

## 🌟 Key Features
- **100% Python Standard Library**: Zero third-party runtime dependencies.
- **MCP Native**: Plugs directly into Claude Desktop, Cursor, LobeChat, and autonomous agent DAGs.
- **Production Resilience**: Strict schema conformance, zero data loss, enterprise hardened.

## 🚀 Installation & Usage

Run as an MCP server:
```bash
python mcp_server.py
```

Use directly as a library:
```python
from client import *
```

See `example_usage.py` for comprehensive integration demonstrations.

## 📄 License
MIT License. Maintained by [GenPark AI](https://www.genpark.ai).
