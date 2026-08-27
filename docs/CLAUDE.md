# Claude Code Integration Guide

**Source:** dariushoule/x64dbg-automate-pyclient

## Quick Start

Add to your Claude Code configuration:

```json
{
  "mcpServers": {
    "x64dbg-mcp-x": {
      "command": "node",
      "args": ["/path/to/x64dbg-mcp-x/server/dist/index.js"],
      "env": {
        "X64DBG_HOST": "localhost",
        "X64DBG_PORT": "31964"
      }
    }
  }
}
```

## Available Tools

### Breakpoints

```
@x64dbg-mcp-x set_breakpoint address="0x140001000" type="hardware"
@x64dbg-mcp-x delete_breakpoint address="0x140001000"
@x64dbg-mcp-x list_breakpoints
```

### Memory

```
@x64dbg-mcp-x read_memory address="0x140001000" size=256
@x64dbg-mcp-x write_memory address="0x140001000" data="48 89 E5"
@x64dbg-mcp-x search_memory pattern="48 89 ??" range="0x140000000-0x140100000"
```

### Debug Control

```
@x64dbg-mcp-x start_debugging executable="C:\target.exe"
@x64dbg-mcp-x stop_debugging
@x64dbg-mcp-x attach pid=12345
@x64dbg-mcp-x detach
```

### Disassembly

```
@x64dbg-mcp-x disassemble address="0x140001000" count=20
@x64dbg-mcp-x analyze_module module_name="kernel32.dll"
```

### Tracing

```
@x64dbg-mcp-x step_into
@x64dbg-mcp-x step_over
@x64dbg-mcp-x trace_execute count=10
```

## Example Workflow

### Analyze Malware

```
# Start debugging malware
@x64dbg-mcp-x start_debugging executable="C:\malware.exe"

# Set breakpoint at entry point
@x64dbg-mcp-x set_breakpoint address="0x140001000" type="hardware"

# Wait for breakpoint, then read memory
@x64dbg-mcp-x read_memory address="0x140001000" size=512

# Disassemble to understand code flow
@x64dbg-mcp-x disassemble address="0x140001000" count=50

# Search for anti-debug checks
@x64dbg-mcp-x search_memory pattern="64 A1 30 00 00 00" range="0x140000000-0x140100000"

# Patch PEB BeingDebugged flag
@x64dbg-mcp-x write_memory address="0x7FFFFDF002" data="00"
```

### Reverse Engineering

```
# Attach to running process
@x64dbg-mcp-x attach pid=12345

# List loaded modules
@x64dbg-mcp-x list_modules

# Find interesting function
@x64dbg-mcp-x disassemble address="0x140005000" count=100

# Set breakpoint and trace
@x64dbg-mcp-x set_breakpoint address="0x140005100" type="hardware"
@x64dbg-mcp-x trace_execute count=50
```

## Best Practices

### 1. Be Specific with Addresses

✅ Good:
```
@x64dbg-mcp-x read_memory address="0x140001000" size=256
```

❌ Bad:
```
@x64dbg-mcp-x read_memory address="0x1000" size=256
```

### 2. Use Hardware Breakpoints

Hardware breakpoints are less detectable:

```
@x64dbg-mcp-x set_breakpoint address="0x140001000" type="hardware"
```

### 3. Batch Related Operations

Group related operations in one request:

```
@x64dbg-mcp-x start_debugging executable="target.exe"
@x64dbg-mcp-x set_breakpoint address="0x140001000" type="hardware"
@x64dbg-mcp-x set_breakpoint address="0x140002000" type="hardware"
```

### 4. Check Debugger State

Before operations:

```
@x64dbg-mcp-x list_breakpoints
```

### 5. Clean Up

Always detach/stop when done:

```
@x64dbg-mcp-x stop_debugging
```

## Advanced Usage

### Conditional Breakpoints

```
@x64dbg-mcp-x set_breakpoint address="0x140001000" type="hardware" condition="rax == 0x42"
```

### Memory Search with Wildcards

```
@x64dbg-mcp-x search_memory pattern="48 89 ?? 48 83 EC ??" range="0x140000000-0x140100000"
```

### Automated Analysis

Use Python client for complex workflows:

```python
from x64dbg_automate import X64dbgClient

client = X64dbgClient('localhost', 31964)
client.attach(12345)

# Automated function discovery
modules = client.list_modules()
for module in modules['modules']:
    print(f"Module: {module['name']} at {module['base']}")
```

## Troubleshooting

### "Debugger not running"

Start debugging first:
```
@x64dbg-mcp-x start_debugging executable="target.exe"
```

### "Invalid address"

Use full 64-bit addresses:
```
@x64dbg-mcp-x read_memory address="0x140001000" size=256
```

### "Connection refused"

Check server is running:
```bash
curl http://localhost:31964/health
```

## Resources

- [API Reference](API.md)
- [Tool Specifications](TOOLS.md)
- [AI Agent Guide](AGENTS.md)
- [Python Client](../clients/python/README.md)

---

**For Claude Code** | x64dbg-mcp-x v1.0.0
