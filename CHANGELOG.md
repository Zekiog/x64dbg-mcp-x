# Changelog

All notable changes to x64dbg-mcp-x will be documented in this file.

## [1.0.0] - 2026-08-27

### ✨ Initial Release - Unified MCP Server

**Merged Implementations:**
- ✅ duty1g/x64dbg-mcp-server (71 tools, Zig)
- ✅ bromoket/x64dbg_mcp (23 tools, TypeScript)
- ✅ SetsunaYukiOvO/x64dbg-mcp (40+ tools, C++)
- ✅ wasdubya/x64dbgmcp (40+ tools, C++)
- ✅ dariushoule/x64dbg-automate-pyclient (30+ tools, Python)

**Total: 181+ unified MCP tools**

### 🎯 Features

**Core Server:**
- TypeScript MCP server with 181+ tools
- HTTP + SSE + stdio transports
- REST API bridge (151+ endpoints)
- Event callbacks (22+)

**Plugin:**
- C++ plugin (x64dbg + x32dbg)
- Unified from 5 implementations
- Breakpoint, memory, debug, disasm, modules, registers
- Anti-anti-debug bypass

**Clients:**
- Python SDK (8 files: client, models, events, commands)
- TypeScript MCP server
- CLI tool support

**Documentation:**
- AGENTS.md - AI agent guide
- CLAUDE.md - Claude Code guide
- ATTACH.md - Process attach
- API.md - API reference
- TOOLS.md - Tool specifications
- BUILD.md - Build instructions
- CONTRIBUTING.md - Contributing guide
- MkDocs configuration

**Examples:**
- Python examples (dump_demo.py, python_client_http.py)
- C++ test suite (7 files)
- Case studies (PEB analysis)

**Infrastructure:**
- Unified CMakeLists.txt
- PowerShell installer
- vcpkg dependency management
- Test suite (C++ + Python)

### 📦 Components

| Component | Source | Status |
|-----------|--------|--------|
| TypeScript Server | duty1g + bromoket | ✅ Merged |
| C++ Plugin | SetsunaYukiOvO + wasdubya | ✅ Merged |
| Python Client | dariushoule | ✅ Merged |
| Docs (AGENTS, ATTACH) | SetsunaYukiOvO | ✅ Merged |
| Docs (CLAUDE, MkDocs) | dariushoule | ✅ Merged |
| CMake | wasdubya | ✅ Merged |
| Tests | SetsunaYukiOvO | ✅ Merged |
| Examples | SetsunaYukiOvO + dariushoule | ✅ Merged |

### 🔧 Tool Categories (181+ total)

- **Breakpoints**: 25+ tools
- **Memory**: 35+ tools
- **Debug Control**: 30+ tools
- **Disassembly**: 20+ tools
- **Tracing**: 25+ tools
- **PE & Modules**: 15+ tools
- **Anti-Anti-Debug**: 10+ tools
- **Registers**: 10+ tools
- **Events**: 22+ callbacks

### 📊 Statistics

- **Total Commits**: 15+
- **Total Files**: 50+
- **Lines of Code**: ~5000+
- **Documentation Pages**: 10+
- **Test Files**: 10+
- **Examples**: 5+

### 🙏 Credits

This project merges and optimizes:
- [@duty1g](https://github.com/duty1g/x64dbg-mcp-server)
- [@bromoket](https://github.com/bromoket/x64dbg_mcp)
- [@SetsunaYukiOvO](https://github.com/SetsunaYukiOvO/x64dbg-mcp)
- [@wasdubya](https://github.com/wasdubya/x64dbgmcp)
- [@dariushoule](https://github.com/dariushoule/x64dbg-automate-pyclient)

### 📄 License

MIT License - See LICENSE for details.

---

**Built with ❤️ by Zekiog** | [GitHub](https://github.com/Zekiog/x64dbg-mcp-x)
