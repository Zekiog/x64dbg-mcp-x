"""
x64dbg-mcp-x Base Client

HTTP/REST client for x64dbg MCP server communication.
"""

import requests
from typing import Dict, Any, Optional, List
from .models import Breakpoint, MemoryRegion, Module, RegisterState


class X64dbgClient:
    """Synchronous HTTP client for x64dbg-mcp-x"""
    
    def __init__(self, host: str = 'localhost', port: int = 31964):
        self.base_url = f'http://{host}:{port}'
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check server health"""
        response = self.session.get(f'{self.base_url}/health')
        response.raise_for_status()
        return response.json()
    
    def set_breakpoint(self, address: str, bp_type: str = 'hardware', 
                       condition: Optional[str] = None) -> Dict[str, Any]:
        """Set a breakpoint"""
        payload = {'address': address, 'type': bp_type}
        if condition:
            payload['condition'] = condition
        
        response = self.session.post(
            f'{self.base_url}/breakpoint/set',
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def delete_breakpoint(self, address: str) -> Dict[str, Any]:
        """Delete a breakpoint"""
        response = self.session.post(
            f'{self.base_url}/breakpoint/delete',
            json={'address': address}
        )
        response.raise_for_status()
        return response.json()
    
    def list_breakpoints(self) -> List[Breakpoint]:
        """List all breakpoints"""
        response = self.session.get(f'{self.base_url}/breakpoint/list')
        response.raise_for_status()
        data = response.json()
        return [Breakpoint(**bp) for bp in data.get('breakpoints', [])]
    
    def read_memory(self, address: str, size: int = 256) -> MemoryRegion:
        """Read memory"""
        response = self.session.post(
            f'{self.base_url}/memory/read',
            json={'address': address, 'size': size}
        )
        response.raise_for_status()
        data = response.json()
        return MemoryRegion(**data)
    
    def write_memory(self, address: str, data: str) -> Dict[str, Any]:
        """Write memory"""
        response = self.session.post(
            f'{self.base_url}/memory/write',
            json={'address': address, 'data': data}
        )
        response.raise_for_status()
        return response.json()
    
    def start_debugging(self, executable: str, arguments: str = '') -> Dict[str, Any]:
        """Start debugging"""
        response = self.session.post(
            f'{self.base_url}/debug/start',
            json={'executable': executable, 'arguments': arguments}
        )
        response.raise_for_status()
        return response.json()
    
    def stop_debugging(self) -> Dict[str, Any]:
        """Stop debugging"""
        response = self.session.post(f'{self.base_url}/debug/stop')
        response.raise_for_status()
        return response.json()
    
    def attach(self, pid: int) -> Dict[str, Any]:
        """Attach to process"""
        response = self.session.post(
            f'{self.base_url}/debug/attach',
            json={'pid': pid}
        )
        response.raise_for_status()
        return response.json()
    
    def detach(self) -> Dict[str, Any]:
        """Detach from process"""
        response = self.session.post(f'{self.base_url}/debug/detach')
        response.raise_for_status()
        return response.json()
    
    def disassemble(self, address: str, count: int = 10) -> Dict[str, Any]:
        """Disassemble instructions"""
        response = self.session.post(
            f'{self.base_url}/disasm',
            json={'address': address, 'count': count}
        )
        response.raise_for_status()
        return response.json()
    
    def list_modules(self) -> List[Module]:
        """List loaded modules"""
        response = self.session.get(f'{self.base_url}/modules/list')
        response.raise_for_status()
        data = response.json()
        return [Module(**m) for m in data.get('modules', [])]
    
    def get_registers(self) -> RegisterState:
        """Get CPU registers"""
        response = self.session.get(f'{self.base_url}/registers')
        response.raise_for_status()
        data = response.json()
        return RegisterState(**data)
    
    def step_into(self) -> Dict[str, Any]:
        """Step into instruction"""
        response = self.session.post(f'{self.base_url}/step/into')
        response.raise_for_status()
        return response.json()
    
    def step_over(self) -> Dict[str, Any]:
        """Step over instruction"""
        response = self.session.post(f'{self.base_url}/step/over')
        response.raise_for_status()
        return response.json()


class X64dbgAsyncClient:
    """Asynchronous HTTP client for x64dbg-mcp-x"""
    
    def __init__(self, host: str = 'localhost', port: int = 31964):
        import aiohttp
        self.base_url = f'http://{host}:{port}'
        self.session = aiohttp.ClientSession()
    
    async def close(self):
        await self.session.close()
    
    async def health_check(self) -> Dict[str, Any]:
        async with self.session.get(f'{self.base_url}/health') as resp:
            return await resp.json()
    
    async def set_breakpoint(self, address: str, bp_type: str = 'hardware') -> Dict[str, Any]:
        payload = {'address': address, 'type': bp_type}
        async with self.session.post(f'{self.base_url}/breakpoint/set', json=payload) as resp:
            return await resp.json()
    
    async def read_memory(self, address: str, size: int = 256) -> MemoryRegion:
        async with self.session.post(
            f'{self.base_url}/memory/read',
            json={'address': address, 'size': size}
        ) as resp:
            data = await resp.json()
            return MemoryRegion(**data)
