#!/usr/bin/env python3
"""
x64dbg-mcp-x Python Client

Unified Python SDK for x64dbg MCP Server (181+ tools)
Merged from dariushoule/x64dbg-automate-pyclient
"""

from .client_base import X64dbgClient, X64dbgAsyncClient
from .models import (
    Breakpoint,
    MemoryRegion,
    Module,
    RegisterState,
    DebugEvent,
    DisassemblyInstruction,
)
from .events import EventListener, EventCallback
from .commands_xauto import (
    set_breakpoint,
    delete_breakpoint,
    read_memory,
    write_memory,
    attach,
    detach,
    start_debugging,
    stop_debugging,
)

__version__ = "1.0.0"
__author__ = "Zekiog"
__all__ = [
    "X64dbgClient",
    "X64dbgAsyncClient",
    "Breakpoint",
    "MemoryRegion",
    "Module",
    "RegisterState",
    "DebugEvent",
    "DisassemblyInstruction",
    "EventListener",
    "EventCallback",
    "set_breakpoint",
    "delete_breakpoint",
    "read_memory",
    "write_memory",
    "attach",
    "detach",
    "start_debugging",
    "stop_debugging",
]
