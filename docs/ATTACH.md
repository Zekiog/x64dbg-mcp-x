# Process Attach Guide

How to attach x64dbg-mcp-x to running processes.

## Quick Start

### Attach by PID

```json
{
  "tool": "x64dbg.attach",
  "arguments": {
    "pid": 12345
  }
}
```

### Attach by Process Name

```json
{
  "tool": "x64dbg.attach_by_name",
  "arguments": {
    "name": "target.exe"
  }
}
```

## Methods

### 1. REST API Attach

```bash
curl -X POST http://localhost:31964/debug/attach \
  -H "Content-Type: application/json" \
  -d '{"pid": 12345}'
```

### 2. Python Client

```python
from x64dbg_automate import X64dbgClient

client = X64dbgClient('localhost', 31964)
client.attach(12345)
```

### 3. MCP Tool

```json
{
  "tool": "x64dbg.attach",
  "arguments": {
    "pid": 12345
  }
}
```

## Finding Process ID

### Windows Task Manager

1. Press `Ctrl+Shift+Esc`
2. Find process in Details tab
3. Note PID column

### PowerShell

```powershell
# By name
Get-Process -Name "target" | Select-Object Id, Name

# By PID
Get-Process -Id 12345
```

### Command Prompt

```cmd
tasklist /FI "IMAGENAME eq target.exe"
```

## Common Issues

### "Access Denied"

**Cause:** Insufficient privileges

**Solution:**
1. Run x64dbg as Administrator
2. Ensure plugin has debug privileges

### "Process Not Found"

**Cause:** PID doesn't exist or process exited

**Solution:**
1. Verify PID is correct
2. Check process is still running

### "Already Debugged"

**Cause:** Another debugger attached

**Solution:**
1. Detach other debugger first
2. Or use `x64dbg.force_attach` (advanced)

## Detach

```json
{
  "tool": "x64dbg.detach",
  "arguments": {}
}
```

## Best Practices

1. **Always detach cleanly** before closing
2. **Check process state** before attaching
3. **Use hardware breakpoints** for less intrusion
4. **Monitor for exceptions** after attach

---

**x64dbg-mcp-x** | Attach Guide v1.0.0
