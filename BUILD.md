# Build Instructions

Complete guide for building x64dbg-mcp-x.

## Prerequisites

### Windows (Plugin)
- **Visual Studio 2022** with C++ workload
- **CMake 3.20+**
- **x64dbg** (C:\x64dbg)
- **vcpkg** (optional, for dependencies)

### Server (TypeScript)
- **Node.js 20+**
- **npm** or **pnpm**

### Python Client
- **Python 3.9+**
- **Poetry** (optional)

## Quick Build

### 1. Build Plugin

```powershell
cd plugin
.\build.ps1 -x64dbgDir "C:\x64dbg"
```

### 2. Build Server

```powershell
cd server
npm install
npm run build
```

### 3. Install Python Client

```bash
cd clients/python
poetry install
```

## Manual Build

### Plugin (CMake)

```bash
cd plugin
mkdir build
cd build

# Configure
cmake .. -G "Visual Studio 17 2022" -A x64 -Dx64dbgDir="C:/x64dbg"

# Build
cmake --build . --config Release

# Output
# - x64dbg-mcp-x.dp64
# - x64dbg-mcp-x.dp32
```

### Server (TypeScript)

```bash
cd server
npm install
npm run build

# Output: dist/index.js
```

### Tests

```bash
cd tests
mkdir build
cd build

# Configure
cmake .. -G "Visual Studio 17 2022" -A x64

# Build and test
cmake --build . --config Release
ctest
```

## Installation

### 1. Install Plugin

Copy to x64dbg:
```
build/x64dbg-mcp-x.dp64 → C:\x64dbg\x64\plugins\
build/x64dbg-mcp-x.dp32 → C:\x64dbg\x32\plugins\
```

### 2. Configure Claude Desktop

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "x64dbg-mcp-x": {
      "command": "node",
      "args": ["C:/path/to/x64dbg-mcp-x/server/dist/index.js"],
      "env": {
        "X64DBG_HOST": "localhost",
        "X64DBG_PORT": "31964"
      }
    }
  }
}
```

### 3. Restart Applications

1. Restart x64dbg
2. Restart Claude Desktop
3. Start debugging!

## Testing

### Health Check

```bash
curl http://localhost:31964/health
# Expected: {"status":"healthy","server":"x64dbg-mcp-x"}
```

### Run Tests

```bash
cd tests/build
ctest --verbose
```

### Python Client Test

```python
from x64dbg_automate import X64dbgClient

client = X64dbgClient('localhost', 31964)
print(client.health_check())
```

## Troubleshooting

### CMake Errors

```bash
cmake .. -DX64DBG_SDK_DIR="C:/x64dbg/src/sdk"
```

### TypeScript Build Errors

```bash
cd server
rm -rf node_modules
npm install
npm run build
```

### Plugin Not Loading

- Check x64dbg log (Help > About > Log)
- Verify `.dp64` in correct folder
- Ensure architecture matches (x64 vs x32)

## Clean Build

```bash
# Plugin
cd plugin
rm -rf build

# Server
cd server
rm -rf node_modules dist

# Tests
cd tests
rm -rf build

# Full clean
git clean -fdx
```

---

**x64dbg-mcp-x** | Build Guide v1.0.0
