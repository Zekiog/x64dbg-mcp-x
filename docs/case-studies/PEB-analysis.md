# PEB Analysis Case Study

**Source:** wasdubya/x64dbgmcp - Cursor.Opus4.5-Find-PEB.md

## Overview

This case study demonstrates how to use x64dbg-mcp-x to find and analyze the Process Environment Block (PEB) for anti-anti-debug bypass.

## Background

The PEB is a data structure in Windows that contains process information, including:
- `BeingDebugged` flag (offset 0x2 in PEB)
- Process parameters
- Loaded modules list
- Heap information

Malware and protected software often check `PEB.BeingDebugged` to detect debuggers.

## Objective

Find the PEB address and patch the `BeingDebugged` flag.

## Method

### Step 1: Get PEB Address

```json
{
  "tool": "x64dbg.get_registers",
  "arguments": {}
}
```

On x64, PEB is at `gs:[0x60]`
On x86, PEB is at `fs:[0x30]`

### Step 2: Read PEB

```json
{
  "tool": "x64dbg.read_memory",
  "arguments": {
    "address": "0x7FFFFDF000",
    "size": 256
  }
}
```

### Step 3: Check BeingDebugged Flag

Offset 0x2 contains the flag:
- `0x00` = Not being debugged
- `0x01` = Being debugged

### Step 4: Patch Flag

```json
{
  "tool": "x64dbg.write_memory",
  "arguments": {
    "address": "0x7FFFFDF002",
    "data": "00"
  }
}
```

### Step 5: Verify

```json
{
  "tool": "x64dbg.read_memory",
  "arguments": {
    "address": "0x7FFFFDF002",
    "size": 1
  }
}
```

Expected: `00`

## Alternative: Automatic Bypass

```json
{
  "tool": "x64dbg.bypass_peb",
  "arguments": {}
}
```

This automatically patches the PEB.BeingDebugged flag.

## Results

- PEB found at: `0x7FFFFDF000`
- BeingDebugged patched: `0x01` → `0x00`
- Anti-debug check bypassed: ✓

## Code Example

```python
from x64dbg_automate import X64dbgClient

client = X64dbgClient('localhost', 31964)
client.attach(12345)

# Get PEB address (x64: gs:[0x60])
regs = client.get_registers()
peb_base = int(regs['gs_base']) + 0x60

# Read PEB
peb_data = client.read_memory(peb_base, 256)

# Check BeingDebugged flag
being_debugged = peb_data['data'][4:6]  # offset 0x2
print(f"BeingDebugged: {being_debugged}")

# Patch if needed
if being_debugged != "00":
    client.write_memory(peb_base + 2, "00")
    print("PEB patched!")
```

## Conclusion

x64dbg-mcp-x makes PEB analysis straightforward with:
- Register access
- Memory read/write
- Automatic bypass tools

---

**Case Study** | x64dbg-mcp-x v1.0.0
