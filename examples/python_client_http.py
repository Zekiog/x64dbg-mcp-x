#!/usr/bin/env python3
"""
x64dbg-mcp-x Python HTTP Client

Simple HTTP client for interacting with the x64dbg MCP server.
"""

import requests
import json
from typing import Optional, Dict, Any

class X64dbgClient:
    """HTTP client for x64dbg-mcp-x REST API"""
    
    def __init__(self, host='localhost', port=31964):
        self.base_url = f'http://{host}:{port}'
    
    def health_check(self) -> Dict[str, Any]:
        """Check server health"""
        response = requests.get(f'{self.base_url}/health')
        return response.json()
    
    def set_breakpoint(self, address: str, bp_type: str = 'hardware', 
                       condition: Optional[str] = None) -> Dict[str, Any]:
        """Set a breakpoint"""
        payload = {
            'address': address,
            'type': bp_type
        }
        if condition:
            payload['condition'] = condition
        
        response = requests.post(
            f'{self.base_url}/breakpoint/set',
            json=payload
        )
        return response.json()
    
    def delete_breakpoint(self, address: str) -> Dict[str, Any]:
        """Delete a breakpoint"""
        response = requests.post(
            f'{self.base_url}/breakpoint/delete',
            json={'address': address}
        )
        return response.json()
    
    def list_breakpoints(self) -> Dict[str, Any]:
        """List all breakpoints"""
        response = requests.get(f'{self.base_url}/breakpoint/list')
        return response.json()
    
    def read_memory(self, address: str, size: int = 256) -> Dict[str, Any]:
        """Read memory"""
        response = requests.post(
            f'{self.base_url}/memory/read',
            json={'address': address, 'size': size}
        )
        return response.json()
    
    def write_memory(self, address: str, data: str) -> Dict[str, Any]:
        """Write memory"""
        response = requests.post(
            f'{self.base_url}/memory/write',
            json={'address': address, 'data': data}
        )
        return response.json()
    
    def start_debugging(self, executable: str, arguments: str = '') -> Dict[str, Any]:
        """Start debugging"""
        response = requests.post(
            f'{self.base_url}/debug/start',
            json={'executable': executable, 'arguments': arguments}
        )
        return response.json()
    
    def stop_debugging(self) -> Dict[str, Any]:
        """Stop debugging"""
        response = requests.post(f'{self.base_url}/debug/stop')
        return response.json()
    
    def attach(self, pid: int) -> Dict[str, Any]:
        """Attach to process"""
        response = requests.post(
            f'{self.base_url}/debug/attach',
            json={'pid': pid}
        )
        return response.json()
    
    def detach(self) -> Dict[str, Any]:
        """Detach from process"""
        response = requests.post(f'{self.base_url}/debug/detach')
        return response.json()
    
    def disassemble(self, address: str, count: int = 10) -> Dict[str, Any]:
        """Disassemble instructions"""
        response = requests.post(
            f'{self.base_url}/disasm',
            json={'address': address, 'count': count}
        )
        return response.json()
    
    def list_modules(self) -> Dict[str, Any]:
        """List loaded modules"""
        response = requests.get(f'{self.base_url}/modules/list')
        return response.json()
    
    def step_into(self) -> Dict[str, Any]:
        """Step into instruction"""
        response = requests.post(f'{self.base_url}/step/into')
        return response.json()
    
    def step_over(self) -> Dict[str, Any]:
        """Step over instruction"""
        response = requests.post(f'{self.base_url}/step/over')
        return response.json()


def main():
    """Example usage"""
    client = X64dbgClient('localhost', 31964)
    
    # Health check
    print("Health check:", client.health_check())
    
    # Set breakpoint
    print("Setting breakpoint...")
    result = client.set_breakpoint('0x140001000', 'hardware')
    print("Result:", result)
    
    # Read memory
    print("Reading memory...")
    result = client.read_memory('0x140001000', 64)
    print("Memory:", result)
    
    # List breakpoints
    print("Listing breakpoints...")
    result = client.list_breakpoints()
    print("Breakpoints:", result)


if __name__ == '__main__':
    main()
