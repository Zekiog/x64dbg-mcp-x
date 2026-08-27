"""
x64dbg-mcp-x Event System

Event-driven architecture for debugging events.
"""

import asyncio
from typing import Callable, Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import json


class EventType(str, Enum):
    BREAKPOINT_HIT = "breakpoint.hit"
    DEBUG_STARTED = "debug.started"
    DEBUG_STOPPED = "debug.stopped"
    DEBUG_EXCEPTION = "debug.exception"
    MODULE_LOAD = "module.load"
    MODULE_UNLOAD = "module.unload"
    THREAD_CREATE = "thread.create"
    THREAD_EXIT = "thread.exit"
    OUTPUT_STRING = "output.string"


@dataclass
class DebugEvent:
    """Debug event data"""
    event_type: EventType
    timestamp: float
    data: Dict[str, Any]


EventCallback = Callable[[DebugEvent], None]


class EventListener:
    """SSE event listener for x64dbg events"""
    
    def __init__(self, host: str = 'localhost', port: int = 31964):
        self.base_url = f'http://{host}:{port}'
        self.callbacks: Dict[EventType, List[EventCallback]] = {}
        self.running = False
    
    def on(self, event_type: EventType, callback: EventCallback):
        """Register event callback"""
        if event_type not in self.callbacks:
            self.callbacks[event_type] = []
        self.callbacks[event_type].append(callback)
    
    def off(self, event_type: EventType, callback: Optional[EventCallback] = None):
        """Unregister event callback"""
        if event_type in self.callbacks:
            if callback:
                self.callbacks[event_type].remove(callback)
            else:
                self.callbacks[event_type] = []
    
    def _emit(self, event: DebugEvent):
        """Emit event to callbacks"""
        if event.event_type in self.callbacks:
            for callback in self.callbacks[event.event_type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Event callback error: {e}")
    
    def start(self):
        """Start listening to SSE events"""
        import requests
        from sseclient import SSEClient
        
        self.running = True
        url = f'{self.base_url}/sse'
        
        try:
            session = requests.Session()
            messages = SSEClient(url, session=session)
            
            for msg in messages:
                if not self.running:
                    break
                
                try:
                    data = json.loads(msg.data)
                    event = DebugEvent(
                        event_type=EventType(msg.event),
                        timestamp=msg.timestamp,
                        data=data
                    )
                    self._emit(event)
                except Exception as e:
                    print(f"Event parse error: {e}")
        except Exception as e:
            print(f"SSE connection error: {e}")
    
    def stop(self):
        """Stop listening"""
        self.running = False


class AsyncEventListener:
    """Async SSE event listener"""
    
    def __init__(self, host: str = 'localhost', port: int = 31964):
        self.base_url = f'http://{host}:{port}'
        self.callbacks: Dict[EventType, List[EventCallback]] = {}
        self.running = False
    
    def on(self, event_type: EventType, callback: EventCallback):
        if event_type not in self.callbacks:
            self.callbacks[event_type] = []
        self.callbacks[event_type].append(callback)
    
    async def start(self):
        import aiohttp
        
        self.running = True
        url = f'{self.base_url}/sse'
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                async for line in resp.content:
                    if not self.running:
                        break
                    
                    line = line.decode('utf-8').strip()
                    if line.startswith('data:'):
                        data = json.loads(line[5:])
                        event = DebugEvent(
                            event_type=EventType(resp.headers.get('event', 'unknown')),
                            timestamp=asyncio.get_event_loop().time(),
                            data=data
                        )
                        self._emit(event)
    
    def _emit(self, event: DebugEvent):
        if event.event_type in self.callbacks:
            for callback in self.callbacks[event.event_type]:
                asyncio.create_task(self._call_callback(callback, event))
    
    async def _call_callback(self, callback: EventCallback, event: DebugEvent):
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(event)
            else:
                callback(event)
        except Exception as e:
            print(f"Async callback error: {e}")
    
    def stop(self):
        self.running = False
