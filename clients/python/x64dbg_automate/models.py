"""
x64dbg-mcp-x Data Models

Pydantic models for x64dbg data structures.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class BreakpointType(str, Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    MEMORY = "memory"


class Breakpoint(BaseModel):
    """Breakpoint information"""
    address: str = Field(..., description="Breakpoint address (hex)")
    type: BreakpointType = Field(..., description="Breakpoint type")
    enabled: bool = Field(default=True, description="Whether breakpoint is enabled")
    condition: Optional[str] = Field(None, description="Conditional expression")
    hit_count: int = Field(default=0, description="Number of times hit")


class MemoryRegion(BaseModel):
    """Memory region information"""
    address: str = Field(..., description="Start address")
    size: int = Field(..., description="Size in bytes")
    data: str = Field(..., description="Hex-encoded data")
    protection: Optional[str] = Field(None, description="Memory protection")


class Module(BaseModel):
    """Loaded module information"""
    name: str = Field(..., description="Module name")
    base: str = Field(..., description="Base address")
    size: int = Field(..., description="Module size")
    path: Optional[str] = Field(None, description="Full path")


class RegisterState(BaseModel):
    """CPU register state"""
    rax: str = Field(default="0x0")
    rbx: str = Field(default="0x0")
    rcx: str = Field(default="0x0")
    rdx: str = Field(default="0x0")
    rsi: str = Field(default="0x0")
    rdi: str = Field(default="0x0")
    rsp: str = Field(default="0x0")
    rbp: str = Field(default="0x0")
    rip: str = Field(default="0x0")
    rflags: Optional[str] = Field(None)
    
    def get(self, name: str) -> str:
        return getattr(self, name.lower(), "0x0")


class DebugEvent(BaseModel):
    """Debug event information"""
    event_type: str = Field(..., description="Event type")
    timestamp: float = Field(..., description="Event timestamp")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event data")


class DisassemblyInstruction(BaseModel):
    """Disassembled instruction"""
    address: str = Field(..., description="Instruction address")
    mnemonic: str = Field(..., description="Instruction mnemonic")
    operands: str = Field(default="", description="Instruction operands")
    bytes: str = Field(default="", description="Instruction bytes (hex)")
    
    def __str__(self):
        return f"{self.address}: {self.mnemonic} {self.operands}"


class DebugStatus(BaseModel):
    """Debugger status"""
    active: bool = Field(default=False)
    pid: Optional[int] = Field(None)
    tid: Optional[int] = Field(None)
    executable: Optional[str] = Field(None)
    exit_code: Optional[int] = Field(None)


class SearchPattern(BaseModel):
    """Memory search pattern"""
    pattern: str = Field(..., description="Hex pattern with wildcards (??)")
    range_start: Optional[str] = Field(None, description="Search range start")
    range_end: Optional[str] = Field(None, description="Search range end")
    matches: List[str] = Field(default_factory=list, description="Match addresses")
