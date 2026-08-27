# AI Agent Guide

Complete guide for AI agents using x64dbg-mcp-x.

## Overview

x64dbg-mcp-x provides 181+ MCP tools for AI agents to control x64dbg for reverse engineering, malware analysis, and debugging tasks.

## Supported AI Platforms

- **Claude Code** (Anthropic)
- **Cursor** (cursor.sh)
- **Windsurf** (Codeium)
- **Cline** (VS Code extension)
- **Custom MCP clients**

## Configuration

### Claude Desktop

Add to `claude_desktop_config.json`:

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

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "x64dbg": {
      "command": "node",
      "args": ["/path/to/server/dist/index.js"]
    }
  }
}
```

## Tool Categories

### 1. Breakpoint Management (25+ tools)

```json
{
  "tool": "x64dbg.set_breakpoint",
  "arguments": {
    "address": "0x140001000",
    "type": "hardware",
    "condition": "rax == 0x42"
  }
}
```

**Available Tools:**
- `x64dbg.set_breakpoint` - Set hardware/software breakpoint
- `x64dbg.delete_breakpoint` - Remove breakpoint
- `x64dbg.list_breakpoints` - List all breakpoints
- `x64dbg.enable_breakpoint` - Enable disabled BP
- `x64dbg.disable_breakpoint` - Disable without deleting
- `x64dbg.set_memory_breakpoint` - Memory access BP
- `x64dbg.set_hardware_breakpoint` - Hardware BP (x86/x64)

### 2. Memory Operations (35+ tools)

```json
{
  "tool": "x64dbg.read_memory",
  "arguments": {
    "address": "0x140001000",
    "size": 512
  }
}
```

**Available Tools:**
- `x64dbg.read_memory` - Read memory region
- `x64dbg.write_memory` - Write to memory
- `x64dbg.search_memory` - Search for pattern
- `x64dbg.dump_memory` - Dump to file
- `x64dbg.protect_memory` - Change protection
- `x64dbg.find_pattern` - Pattern search with wildcards

### 3. Debug Control (30+ tools)

```json
{
  "tool": "x64dbg.start_debugging",
  "arguments": {
    "executable": "C:\\target.exe",
    "arguments": "--flag"
  }
}
```

**Available Tools:**
- `x64dbg.start_debugging` - Start debug session
- `x64dbg.stop_debugging` - Stop debugging
- `x64dbg.attach` - Attach to process
- `x64dbg.detach` - Detach from process
- `x64dbg.restart` - Restart debuggee
- `x64dbg.pause` - Pause execution

### 4. Disassembly (20+ tools)

```json
{
  "tool": "x64dbg.disassemble",
  "arguments": {
    "address": "0x140001000",
    "count": 20
  }
}
```

**Available Tools:**
- `x64dbg.disassemble` - Disassemble instructions
- `x64dbg.analyze_module` - Analyze module
- `x64dbg.find_references` - Find code references
- `x64dbg.get_function` - Get function boundaries

### 5. Tracing (25+ tools)

```json
{
  "tool": "x64dbg.step_into",
  "arguments": {}
}
```

**Available Tools:**
- `x64dbg.step_into` - Step into
- `x64dbg.step_over` - Step over
- `x64dbg.trace_execute` - Execute with trace
- `x64dbg.run_to_cursor` - Run to address

### 6. PE & Modules (15+ tools)

```json
{
  "tool": "x64dbg.list_modules",
  "arguments": {}
}
```

**Available Tools:**
- `x64dbg.list_modules` - List loaded modules
- `x64dbg.get_module_info` - Get module details
- `x64dbg.dump_pe` - Dump PE file
- `x64dbg.get_exports` - Get export table

### 7. Anti-Anti-Debug (10+ tools)

```json
{
  "tool": "x64dbg.bypass_peb",
  "arguments": {}
}
```

**Available Tools:**
- `x64dbg.bypass_peb` - Bypass PEB checks
- `x64dbg.bypass_ntquery` - Bypass NtQuery
- `x64dbg.bypass_outputdebugstring` - Bypass OutputDebugString

### 8. Registers (10+ tools)

```json
{
  "tool": "x64dbg.get_registers",
  "arguments": {}
}
```

**Available Tools:**
- `x64dbg.get_registers` - Get all registers
- `x64dbg.set_register` - Set register value
- `x64dbg.get_stack` - Get stack trace

## Best Practices

### 1. Error Handling

Always check for errors:

```json
{
  "tool": "x64dbg.read_memory",
  "arguments": {"address": "0x140001000", "size": 256}
}
```

Response:
```json
{
  "success": true,
  "data": "48 89 E5 48 83 EC 20..."
}
```

Or on error:
```json
{
  "success": false,
  "error": "ERR_DEBUGGER_NOT_RUNNING"
}
```

### 2. Batch Operations

For efficiency, batch related operations:

```json
[
  {"tool": "x64dbg.set_breakpoint", "arguments": {"address": "0x140001000"}},
  {"tool": "x64dbg.set_breakpoint", "arguments": {"address": "0x140002000"}},
  {"tool": "x64dbg.start_debugging", "arguments": {"executable": "target.exe"}}
]
```

### 3. Event Listening

Subscribe to SSE events for real-time updates:

```bash
# Connect to SSE endpoint
curl -N http://localhost:31964/sse
```

Events:
- `breakpoint.hit` - Breakpoint reached
- `debug.exception` - Exception occurred
- `module.load` - Module loaded
- `thread.create` - Thread created

### 4. Safety

⚠️ **Important Safety Guidelines:**

1. **Always validate addresses** before setting breakpoints
2. **Check debugger state** before operations
3. **Use hardware breakpoints** when possible (less intrusive)
4. **Monitor memory writes** to avoid crashes
5. **Detach cleanly** before closing

## Advanced Usage

### Conditional Breakpoints

```json
{
  "tool": "x64dbg.set_breakpoint",
  "arguments": {
    "address": "0x140001000",
    "type": "hardware",
    "condition": "rax == 0x42 && rbx != 0"
  }
}
```

### Memory Pattern Search

```json
{
  "tool": "x64dbg.search_memory",
  "arguments": {
    "pattern": "48 89 ?? 48 83 EC ??",
    "range": {
      "start": "0x140000000",
      "end": "0x140100000"
    }
  }
}
```

### Automated Analysis

```python
# Example: Automated function analysis
from x64dbg_automate import X64dbgClient

client = X64dbgClient('localhost', 31964)
client.attach(12345)

# Find function prologue
pattern = client.search_memory("48 89 E5", "0x140000000", "0x140100000")
for addr in pattern['matches']:
    print(f"Found function at: {addr}")
    disasm = client.disassemble(addr, 10)
    print(disasm)
```

## Troubleshooting

### "Debugger not running"

Ensure x64dbg is running and plugin is loaded.

### "Invalid address"

Validate address format (hex with 0x prefix).

### "Connection refused"

Check REST API is running: `curl http://localhost:31964/health`

## Resources

- [API Reference](API.md)
- [Tool Specifications](TOOLS.md)
- [Python Client](../clients/python/README.md)
- [Examples](../examples/)

---

**For AI Agents** | x64dbg-mcp-x v1.0.0
