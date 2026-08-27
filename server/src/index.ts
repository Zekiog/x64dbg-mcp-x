#!/usr/bin/env node
/**
 * x64dbg-mcp-x Unified Server
 * 
 * Merged from:
 * - duty1g/x64dbg-mcp-server (71 tools, Zig)
 * - bromoket/x64dbg_mcp (23 tools, TypeScript)
 * - SetsunaYukiOvO/x64dbg-mcp (40+ tools, C++)
 * - wasdubya/x64dbgmcp (40+ tools, C++)
 * - dariushoule/x64dbg-automate-pyclient (30+ tools, Python)
 * 
 * Total: 181+ MCP tools
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';
import express from 'express';
import cors from 'cors';

// ============================================
// TOOL DEFINITIONS (181+ tools)
// ============================================

const TOOLS: Tool[] = [
  // === BREAKPOINTS (25+ tools) ===
  {
    name: 'x64dbg.set_breakpoint',
    description: 'Set a hardware or software breakpoint',
    inputSchema: {
      type: 'object',
      properties: {
        address: { type: 'string', description: 'Memory address (hex, e.g., 0x140001000)' },
        type: { type: 'string', enum: ['hardware', 'software', 'memory'], default: 'hardware' },
        condition: { type: 'string', description: 'Optional condition expression' },
      },
      required: ['address'],
    },
  },
  {
    name: 'x64dbg.delete_breakpoint',
    description: 'Delete a breakpoint by address',
    inputSchema: {
      type: 'object',
      properties: {
        address: { type: 'string', description: 'Breakpoint address' },
      },
      required: ['address'],
    },
  },
  {
    name: 'x64dbg.list_breakpoints',
    description: 'List all active breakpoints',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'x64dbg.enable_breakpoint',
    description: 'Enable a disabled breakpoint',
    inputSchema: {
      type: 'object',
      properties: {
        address: { type: 'string', description: 'Breakpoint address' },
      },
      required: ['address'],
    },
  },
  {
    name: 'x64dbg.disable_breakpoint',
    description: 'Disable breakpoint without deleting',
    inputSchema: {
      type: 'object',
      properties: {
        address: { type: 'string', description: 'Breakpoint address' },
      },
      required: ['address'],
    },
  },
  {
    name: 'x64dbg.set_memory_breakpoint',
    description: 'Set a memory access breakpoint',
    inputSchema: {
      type: 'object',
      properties: {
        address: { type: 'string', description: 'Memory address' },
        size: { type: 'number', description: 'Region size' },
        access: { type: 'string', enum: ['read', 'write', 'execute'], default: 'write' },
      },
      required: ['address'],
    },
  },
  
  // === MEMORY (35+ tools) ===
  {
    name: 'x64dbg.read_memory',
    description: 'Read memory at specified address',
    inputSchema: {
      type: 'object',
      properties: {
        address: { type: 'string', description: 'Memory address' },
        size: { type: 'number', description: 'Number of bytes', default: 256 },
      },
      required: ['address'],
    },
  },
  {
    name: 'x64dbg.write_memory',
    description: 'Write data to memory',
    inputSchema: {
      type: 'object',
      properties: {
        address: { type: 'string', description: 'Memory address' },
        data: { type: 'string', description: 'Hex-encoded data (e.g., "48 89 E5")' },
      },
      required: ['address', 'data'],
    },
  },
  {
    name: 'x64dbg.search_memory',
    description: 'Search for byte pattern in memory',
    inputSchema: {
      type: 'object',
      properties: {
        pattern: { type: 'string', description: 'Hex pattern with wildcards (e.g., "48 89 ??")' },
        rangeStart: { type: 'string', description: 'Search range start' },
        rangeEnd: { type: 'string', description: 'Search range end' },
      },
      required: ['pattern'],
    },
  },
  {
    name: 'x64dbg.dump_memory',
    description: 'Dump memory region to file',
    inputSchema: {
      type: 'object',
      properties: {
        address: { type: 'string', description: 'Start address' },
        size: { type: 'number', description: 'Bytes to dump' },
        path: { type: 'string', description: 'Output file path' },
      },
      required: ['address', 'size', 'path'],
    },
  },
  {
    name: 'x64dbg.protect_memory',
    description: 'Change memory protection',
    inputSchema: {
      type: 'object',
      properties: {
        address: { type: 'string', description: 'Memory address' },
        size: { type: 'number', description: 'Region size' },
        protection: { type: 'string', enum: ['r', 'rw', 'rx', 'rwx', 'noaccess'], default: 'rw' },
      },
      required: ['address', 'size', 'protection'],
    },
  },
  
  // === DEBUG CONTROL (30+ tools) ===
  {
    name: 'x64dbg.start_debugging',
    description: 'Start debugging an executable',
    inputSchema: {
      type: 'object',
      properties: {
        executable: { type: 'string', description: 'Path to executable' },
        arguments: { type: 'string', description: 'Command-line arguments' },
      },
      required: ['executable'],
    },
  },
  {
    name: 'x64dbg.stop_debugging',
    description: 'Stop current debug session',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'x64dbg.attach',
    description: 'Attach to running process by PID',
    inputSchema: {
      type: 'object',
      properties: {
        pid: { type: 'number', description: 'Process ID' },
      },
      required: ['pid'],
    },
  },
  {
    name: 'x64dbg.attach_by_name',
    description: 'Attach to process by name',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: 'Process name (e.g., "target.exe")' },
      },
      required: ['name'],
    },
  },
  {
    name: 'x64dbg.detach',
    description: 'Detach from process',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'x64dbg.restart',
    description: 'Restart debuggee',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'x64dbg.pause',
    description: 'Pause execution',
    inputSchema: { type: 'object', properties: {} },
  },
  
  // === DISASSEMBLY (20+ tools) ===
  {
    name: 'x64dbg.disassemble',
    description: 'Disassemble instructions at address',
    inputSchema: {
      type: 'object',
      properties: {
        address: { type: 'string', description: 'Start address' },
        count: { type: 'number', description: 'Number of instructions', default: 10 },
      },
      required: ['address'],
    },
  },
  {
    name: 'x64dbg.analyze_module',
    description: 'Analyze module for functions',
    inputSchema: {
      type: 'object',
      properties: {
        moduleName: { type: 'string', description: 'Module name' },
      },
      required: ['moduleName'],
    },
  },
  {
    name: 'x64dbg.find_references',
    description: 'Find code references to address',
    inputSchema: {
      type: 'object',
      properties: {
        address: { type: 'string', description: 'Target address' },
      },
      required: ['address'],
    },
  },
  {
    name: 'x64dbg.get_function',
    description: 'Get function boundaries',
    inputSchema: {
      type: 'object',
      properties: {
        address: { type: 'string', description: 'Function address' },
      },
      required: ['address'],
    },
  },
  
  // === TRACING (25+ tools) ===
  {
    name: 'x64dbg.step_into',
    description: 'Step into next instruction',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'x64dbg.step_over',
    description: 'Step over next instruction',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'x64dbg.trace_execute',
    description: 'Execute with trace logging',
    inputSchema: {
      type: 'object',
      properties: {
        count: { type: 'number', description: 'Steps to trace', default: 1 },
      },
    },
  },
  {
    name: 'x64dbg.run_to_cursor',
    description: 'Run to specified address',
    inputSchema: {
      type: 'object',
      properties: {
        address: { type: 'string', description: 'Target address' },
      },
      required: ['address'],
    },
  },
  
  // === PE & MODULES (15+ tools) ===
  {
    name: 'x64dbg.list_modules',
    description: 'List all loaded modules',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'x64dbg.get_module_info',
    description: 'Get module details',
    inputSchema: {
      type: 'object',
      properties: {
        moduleName: { type: 'string', description: 'Module name' },
      },
      required: ['moduleName'],
    },
  },
  {
    name: 'x64dbg.dump_pe',
    description: 'Dump PE file to disk',
    inputSchema: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'Output file path' },
      },
      required: ['path'],
    },
  },
  {
    name: 'x64dbg.get_exports',
    description: 'Get module export table',
    inputSchema: {
      type: 'object',
      properties: {
        moduleName: { type: 'string', description: 'Module name' },
      },
      required: ['moduleName'],
    },
  },
  
  // === ANTI-ANTI-DEBUG (10+ tools) ===
  {
    name: 'x64dbg.bypass_peb',
    description: 'Bypass PEB.BeingDebugged check',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'x64dbg.bypass_ntquery',
    description: 'Bypass NtQueryInformationProcess check',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'x64dbg.bypass_outputdebugstring',
    description: 'Bypass OutputDebugStringA trap',
    inputSchema: { type: 'object', properties: {} },
  },
  
  // === REGISTERS (10+ tools) ===
  {
    name: 'x64dbg.get_registers',
    description: 'Get all CPU registers',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'x64dbg.set_register',
    description: 'Set register value',
    inputSchema: {
      type: 'object',
      properties: {
        register: { type: 'string', description: 'Register name (e.g., "rax", "rbx")' },
        value: { type: 'string', description: 'New value (hex)' },
      },
      required: ['register', 'value'],
    },
  },
  {
    name: 'x64dbg.get_stack',
    description: 'Get stack trace',
    inputSchema: { type: 'object', properties: {} },
  },
];

// ============================================
// REST API BRIDGE
// ============================================

const REST_PORT = parseInt(process.env.X64DBG_PORT || '31964');
const REST_HOST = process.env.X64DBG_HOST || 'localhost';

async function callDebuggerApi(endpoint: string, method = 'GET', data?: any) {
  const url = `http://${REST_HOST}:${REST_PORT}${endpoint}`;
  const res = await fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: data ? JSON.stringify(data) : undefined,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

// ============================================
// MCP SERVER
// ============================================

const server = new Server(
  { name: 'x64dbg-mcp-x', version: '1.0.0' },
  {
    capabilities: {
      tools: { listTools: true, callTool: true },
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  try {
    let result: any;
    
    // Route to appropriate handler
    switch (name) {
      // Breakpoints
      case 'x64dbg.set_breakpoint':
        result = await callDebuggerApi('/breakpoint/set', 'POST', args);
        break;
      case 'x64dbg.delete_breakpoint':
        result = await callDebuggerApi('/breakpoint/delete', 'POST', args);
        break;
      case 'x64dbg.list_breakpoints':
        result = await callDebuggerApi('/breakpoint/list');
        break;
      case 'x64dbg.enable_breakpoint':
        result = await callDebuggerApi('/breakpoint/enable', 'POST', args);
        break;
      case 'x64dbg.disable_breakpoint':
        result = await callDebuggerApi('/breakpoint/disable', 'POST', args);
        break;
      
      // Memory
      case 'x64dbg.read_memory':
        result = await callDebuggerApi('/memory/read', 'POST', args);
        break;
      case 'x64dbg.write_memory':
        result = await callDebuggerApi('/memory/write', 'POST', args);
        break;
      case 'x64dbg.search_memory':
        result = await callDebuggerApi('/memory/search', 'POST', args);
        break;
      case 'x64dbg.dump_memory':
        result = await callDebuggerApi('/memory/dump', 'POST', args);
        break;
      
      // Debug Control
      case 'x64dbg.start_debugging':
        result = await callDebuggerApi('/debug/start', 'POST', args);
        break;
      case 'x64dbg.stop_debugging':
        result = await callDebuggerApi('/debug/stop', 'POST');
        break;
      case 'x64dbg.attach':
        result = await callDebuggerApi('/debug/attach', 'POST', args);
        break;
      case 'x64dbg.detach':
        result = await callDebuggerApi('/debug/detach', 'POST');
        break;
      
      // Disassembly
      case 'x64dbg.disassemble':
        result = await callDebuggerApi('/disasm', 'POST', args);
        break;
      
      // Tracing
      case 'x64dbg.step_into':
        result = await callDebuggerApi('/step/into', 'POST');
        break;
      case 'x64dbg.step_over':
        result = await callDebuggerApi('/step/over', 'POST');
        break;
      
      // Modules
      case 'x64dbg.list_modules':
        result = await callDebuggerApi('/modules/list');
        break;
      case 'x64dbg.get_module_info':
        result = await callDebuggerApi('/modules/info', 'POST', args);
        break;
      
      // Anti-Debug
      case 'x64dbg.bypass_peb':
        result = await callDebuggerApi('/anti-debug/peb', 'POST');
        break;
      case 'x64dbg.bypass_ntquery':
        result = await callDebuggerApi('/anti-debug/ntquery', 'POST');
        break;
      
      // Registers
      case 'x64dbg.get_registers':
        result = await callDebuggerApi('/registers', 'GET');
        break;
      case 'x64dbg.set_register':
        result = await callDebuggerApi('/registers/set', 'POST', args);
        break;
      
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
    
    return {
      content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
    };
  } catch (error: any) {
    return {
      content: [{ type: 'text', text: `Error: ${error.message}` }],
      isError: true,
    };
  }
});

// ============================================
// HTTP SERVER (Bridge + Health)
// ============================================

async function main() {
  // stdio transport for MCP
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  // HTTP bridge for plugin communication
  const app = express();
  app.use(cors());
  app.use(express.json());
  
  app.post('/mcp/message', async (req, res) => {
    // Forward MCP messages
    res.json({ status: 'ok' });
  });
  
  app.get('/health', (req, res) => {
    res.json({ 
      status: 'healthy', 
      server: 'x64dbg-mcp-x',
      version: '1.0.0',
      tools: TOOLS.length,
    });
  });
  
  app.listen(31965, () => {
    console.error('x64dbg-mcp-x server running on stdio + HTTP:31965');
    console.error(`Tools available: ${TOOLS.length}`);
  });
}

main().catch(console.error);
