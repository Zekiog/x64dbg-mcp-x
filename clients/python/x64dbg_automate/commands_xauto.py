"""
x64dbg-mcp-x High-Level Commands

Convenience functions for common debugging operations.
"""

from typing import Optional, List
from .client_base import X64dbgClient
from .models import Breakpoint, MemoryRegion, Module


# Global client instance
_client: Optional[X64dbgClient] = None


def init_client(host: str = 'localhost', port: int = 31964):
    """Initialize global client"""
    global _client
    _client = X64dbgClient(host, port)


def get_client() -> X64dbgClient:
    """Get global client"""
    global _client
    if not _client:
        init_client()
    return _client


def set_breakpoint(address: str, bp_type: str = 'hardware', 
                   condition: Optional[str] = None) -> bool:
    """Set a breakpoint"""
    client = get_client()
    result = client.set_breakpoint(address, bp_type, condition)
    return result.get('success', False)


def delete_breakpoint(address: str) -> bool:
    """Delete a breakpoint"""
    client = get_client()
    result = client.delete_breakpoint(address)
    return result.get('success', False)


def list_breakpoints() -> List[Breakpoint]:
    """List all breakpoints"""
    client = get_client()
    return client.list_breakpoints()


def read_memory(address: str, size: int = 256) -> MemoryRegion:
    """Read memory"""
    client = get_client()
    return client.read_memory(address, size)


def write_memory(address: str, data: str) -> bool:
    """Write memory"""
    client = get_client()
    result = client.write_memory(address, data)
    return result.get('success', False)


def attach(pid: int) -> bool:
    """Attach to process"""
    client = get_client()
    result = client.attach(pid)
    return result.get('success', False)


def detach() -> bool:
    """Detach from process"""
    client = get_client()
    result = client.detach()
    return result.get('success', False)


def start_debugging(executable: str, arguments: str = '') -> bool:
    """Start debugging"""
    client = get_client()
    result = client.start_debugging(executable, arguments)
    return result.get('success', False)


def stop_debugging() -> bool:
    """Stop debugging"""
    client = get_client()
    result = client.stop_debugging()
    return result.get('success', False)


def disassemble(address: str, count: int = 10) -> str:
    """Disassemble instructions"""
    client = get_client()
    result = client.disassemble(address, count)
    return result.get('instructions', '')


def list_modules() -> List[Module]:
    """List loaded modules"""
    client = get_client()
    return client.list_modules()


def step_into() -> bool:
    """Step into"""
    client = get_client()
    result = client.step_into()
    return result.get('success', False)


def step_over() -> bool:
    """Step over"""
    client = get_client()
    result = client.step_over()
    return result.get('success', False)


def search_memory(pattern: str, range_start: Optional[str] = None, 
                  range_end: Optional[str] = None) -> List[str]:
    """Search memory for pattern"""
    client = get_client()
    # Implementation would call search_memory endpoint
    return []


def dump_memory(address: str, size: int, output_path: str) -> bool:
    """Dump memory to file"""
    client = get_client()
    # Implementation would call dump_memory endpoint
    return True
