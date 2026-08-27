# x64dbg-mcp-x

**Unified x64dbg MCP Server** - Merged from 5 implementations: duty1g, bromoket, SetsunaYukiOvO, wasdubya, and dariushoule.

**181+ MCP Tools** for AI-powered reverse engineering and debugging.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Server](https://img.shields.io/badge/MCP-Server-blue)](https://modelcontextprotocol.io)

## 🚀 Features

- **181+ MCP Tools** - Unified from 5 major implementations
- **Multi-Language Clients** - TypeScript, Python, Zig
- **Dual Architecture** - Zig (native) + TypeScript (npm) + C++ (plugin)
- **HTTP + SSE + stdio** - Multiple transport protocols
- **x32 & x64 Support** - Full debugger coverage
- **Test Suite** - Comprehensive testing (C++ + Python)
- **Professional Docs** - MkDocs, AGENTS.md, CLAUDE.md

## 📦 Quick Start

```powershell
git clone https://github.com/Zekiog/x64dbg-mcp-x.git
cd x64dbg-mcp-x
.\install.ps1
```

## 🏗️ Architecture

```
AI Client (Claude/Cursor) → MCP Server (TypeScript/Zig) → REST API → x64dbg Plugin (C++)
                              ↓
                      Python Client (optional)
```

## 📚 Documentation

- [API Reference](docs/API.md)
- [Tool Specifications](docs/TOOLS.md)
- [AI Agent Guide](docs/AGENTS.md)
- [Attach Guide](docs/ATTACH.md)
- [Python Client](clients/python/README.md)
- [Case Studies](docs/case-studies/)

## 🔧 Installation

See [BUILD.md](BUILD.md) for detailed build instructions.

## 📊 Merged Implementations

| Repo | Tools | Contribution |
|------|-------|-------------|
| duty1g/x64dbg-mcp-server | 71 | Zig server, HTTP+SSE |
| bromoket/x64dbg_mcp | 23 | TypeScript server, REST API |
| SetsunaYukiOvO/x64dbg-mcp | 40+ | C++ plugin, tests, examples |
| wasdubya/x64dbgmcp | 40+ | Advanced CMake, case studies |
| dariushoule/x64dbg-automate-pyclient | 30+ | Python client, MkDocs |

**Total: 181+ unified tools**

## 🎯 Tool Categories

- **Breakpoints**: 25+ tools
- **Memory**: 35+ tools
- **Debug Control**: 30+ tools
- **Disassembly**: 20+ tools
- **Tracing**: 25+ tools
- **PE & Modules**: 15+ tools
- **Anti-Anti-Debug**: 10+ tools
- **Registers**: 10+ tools
- **Events**: 22+ callbacks

## 🌟 Example Usage

### TypeScript
```typescript
import { X64dbgClient } from '@x64dbg-mcp-x/client';

const client = new X64dbgClient('localhost', 31964);
await client.setBreakpoint('0x140001000', 'hardware');
const memory = await client.readMemory('0x140001000', 256);
```

### Python
```python
from x64dbg_automate import X64dbgClient

client = X64dbgClient('localhost', 31964)
client.set_breakpoint('0x140001000', 'hardware')
memory = client.read_memory('0x140001000', 256)
```

### Claude Code
```json
{
  "tool": "x64dbg.set_breakpoint",
  "arguments": {
    "address": "0x140001000",
    "type": "hardware"
  }
}
```

## 🤝 Credits

This project merges and optimizes:
- [`duty1g/x64dbg-mcp-server`](https://github.com/duty1g/x64dbg-mcp-server)
- [`bromoket/x64dbg_mcp`](https://github.com/bromoket/x64dbg_mcp)
- [`SetsunaYukiOvO/x64dbg-mcp`](https://github.com/SetsunaYukiOvO/x64dbg-mcp)
- [`wasdubya/x64dbgmcp`](https://github.com/wasdubya/x64dbgmcp)
- [`dariushoule/x64dbg-automate-pyclient`](https://github.com/dariushoule/x64dbg-automate-pyclient)

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Built with ❤️ by Zekiog** | [GitHub](https://github.com/Zekiog/x64dbg-mcp-x)
