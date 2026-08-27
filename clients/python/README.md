# x64dbg-mcp-x Python Client

Python SDK for x64dbg-mcp-x unified MCP server (181+ tools).

## Installation

### With Poetry (Recommended)

```bash
cd clients/python
poetry install
```

### With pip

```bash
cd clients/python
pip install -e .
```

## Quick Start

```python
from x64dbg_automate import X64dbgClient

# Initialize client
client = X64dbgClient('localhost', 31964)

# Health check
print(client.health_check())

# Set breakpoint
client.set_breakpoint('0x140001000', 'hardware')

# Read memory
memory = client.read_memory('0x140001000', 256)
print(f"Data: {memory.data}")

# Disassemble
disasm = client.disassemble('0x140001000', 20)
print(disasm)
```

## High-Level API

```python
from x64dbg_automate import (
    init_client,
    set_breakpoint,
    read_memory,
    attach,
    disassemble
)

# Initialize
init_client('localhost', 31964)

# Use convenience functions
set_breakpoint('0x140001000', 'hardware')
memory = read_memory('0x140001000', 256)
```

## Async Client

```python
import asyncio
from x64dbg_automate import X64dbgAsyncClient

async def main():
    client = X64dbgAsyncClient('localhost', 31964)
    
    # Set breakpoint
    await client.set_breakpoint('0x140001000', 'hardware')
    
    # Read memory
    memory = await client.read_memory('0x140001000', 256)
    print(f"Data: {memory.data}")
    
    await client.close()

asyncio.run(main())
```

## Event System

```python
from x64dbg_automate import EventListener, EventType

def on_breakpoint(event):
    print(f"Breakpoint hit at: {event.data['address']}")

listener = EventListener('localhost', 31964)
listener.on(EventType.BREAKPOINT_HIT, on_breakpoint)
listener.start()
```

## CLI Tool

```bash
# Attach to process
x64dbg attach --pid 12345

# Set breakpoint
x64dbg bp 0x140001000

# Read memory
x64dbg mem read 0x140001000 256

# Disassemble
x64dbg disasm 0x140001000 20
```

## Examples

See `examples/` directory for complete examples:
- `dump_demo.py` - Memory dumping
- `python_client_http.py` - HTTP client usage
- `async_example.py` - Async client
- `event_listener.py` - Event system

## API Reference

### X64dbgClient

- `health_check()` - Check server health
- `set_breakpoint(address, type, condition)` - Set breakpoint
- `delete_breakpoint(address)` - Delete breakpoint
- `list_breakpoints()` - List all breakpoints
- `read_memory(address, size)` - Read memory
- `write_memory(address, data)` - Write memory
- `start_debugging(executable, arguments)` - Start debugging
- `stop_debugging()` - Stop debugging
- `attach(pid)` - Attach to process
- `detach()` - Detach from process
- `disassemble(address, count)` - Disassemble
- `list_modules()` - List modules
- `get_registers()` - Get CPU registers
- `step_into()` - Step into
- `step_over()` - Step over

### Models

- `Breakpoint` - Breakpoint information
- `MemoryRegion` - Memory region data
- `Module` - Loaded module info
- `RegisterState` - CPU register state
- `DebugEvent` - Debug event
- `DisassemblyInstruction` - Disassembled instruction

## Development

```bash
# Install dev dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Format code
poetry run black x64dbg_automate/

# Type checking
poetry run mypy x64dbg_automate/
```

## License

MIT - See LICENSE
