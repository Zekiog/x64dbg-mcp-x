#!/usr/bin/env python3
"""
x64dbg-mcp-x Memory Dump Demo

Demonstrates memory reading and dumping using the MCP server.
"""

import requests
import json

X64DBG_HOST = 'localhost'
X64DBG_PORT = 31964

def read_memory(address, size=256):
    """Read memory at specified address"""
    url = f'http://{X64DBG_HOST}:{X64DBG_PORT}/memory/read'
    payload = {
        'address': address,
        'size': size
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def dump_memory(address, size, output_file):
    """Dump memory to file"""
    url = f'http://{X64DBG_HOST}:{X64DBG_PORT}/memory/dump'
    payload = {
        'address': address,
        'size': size,
        'path': output_file
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Memory dumped to: {output_file}")
        return True
    else:
        print(f"Error: {response.status_code}")
        return False

def set_breakpoint(address, bp_type='hardware'):
    """Set a breakpoint"""
    url = f'http://{X64DBG_HOST}:{X64DBG_PORT}/breakpoint/set'
    payload = {
        'address': address,
        'type': bp_type
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Breakpoint set at: {address}")
        return True
    else:
        print(f"Error: {response.status_code}")
        return False

def main():
    print("x64dbg-mcp-x Memory Dump Demo")
    print("=" * 40)
    
    # Check health
    health_url = f'http://{X64DBG_HOST}:{X64DBG_PORT}/health'
    try:
        response = requests.get(health_url)
        if response.status_code == 200:
            print(f"✓ Server healthy: {response.json()}")
        else:
            print("✗ Server not responding")
            return
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return
    
    # Example: Read memory at 0x140001000
    print("\nReading memory at 0x140001000...")
    result = read_memory('0x140001000', 64)
    if result and result.get('success'):
        print(f"Data: {result['data']}")
    
    # Example: Set breakpoint
    print("\nSetting hardware breakpoint at 0x140001000...")
    set_breakpoint('0x140001000', 'hardware')
    
    # Example: Dump memory
    print("\nDumping 1KB of memory to dump.bin...")
    dump_memory('0x140001000', 1024, 'dump.bin')
    
    print("\nDemo complete!")

if __name__ == '__main__':
    main()
