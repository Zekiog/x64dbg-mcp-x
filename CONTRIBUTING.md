# Contributing to x64dbg-mcp-x

Thank you for contributing to x64dbg-mcp-x! This project merges 5 major implementations into one unified MCP server.

## Project Structure

```
x64dbg-mcp-x/
├── server/           # TypeScript MCP server (181+ tools)
├── plugin/           # C++ x64dbg plugin
├── clients/          # Client libraries
│   └── python/       # Python client
├── docs/             # Documentation
│   ├── AGENTS.md     # AI agent guide
│   ├── CLAUDE.md     # Claude Code guide
│   ├── ATTACH.md     # Attach guide
│   └── case-studies/ # Real-world examples
├── examples/         # Usage examples
├── tests/            # Test suite
└── tools/            # Utility scripts
```

## Development Workflow

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/x64dbg-mcp-x.git
cd x64dbg-mcp-x
```

### 2. Set Up Development Environment

```bash
# Install dependencies
cd server
npm install

cd ../plugin
# Build plugin (see BUILD.md)

cd ../clients/python
poetry install
```

### 3. Make Changes

- Create a feature branch: `git checkout -b feature/your-feature`
- Make your changes
- Write/update tests
- Update documentation

### 4. Test

```bash
# Server tests
cd server
npm test

# Plugin tests
cd tests
mkdir build && cd build
cmake .. -DBUILD_TESTS=ON
cmake --build .
ctest

# Python tests
cd clients/python
poetry run pytest
```

### 5. Submit Pull Request

- Push to your fork
- Create a PR with clear description
- Link related issues
- Wait for review

## Code Style

### TypeScript

```typescript
// Use strict mode
'use strict';

// Type annotations
function add(a: number, b: number): number {
    return a + b;
}

// Async/await
async function fetchData(): Promise<any> {
    const res = await fetch(url);
    return res.json();
}
```

### C++

```cpp
// Use modern C++17
#include <optional>
#include <string_view>

// Namespaces
namespace ZBridge {
    void function();
}

// Smart pointers
std::unique_ptr<Server> server = std::make_unique<Server>();
```

### Python

```python
# Type hints
def add(a: int, b: int) -> int:
    return a + b

# Async/await
async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()
```

## Documentation

### Adding New Tools

1. Add tool definition in `server/src/index.ts`
2. Implement handler in plugin
3. Add documentation in `docs/TOOLS.md`
4. Add example in `examples/`
5. Update README.md tool count

### Writing Docs

- Use clear, concise language
- Include code examples
- Link related pages
- Keep up to date

## Testing

### Unit Tests

```cpp
// C++ test example
TEST_F(BreakpointTests, ValidBreakpoint) {
    bool result = setBreakpoint(0x140001000, BreakpointType::Hardware);
    EXPECT_TRUE(result);
}
```

```python
# Python test example
def test_read_memory():
    client = X64dbgClient('localhost', 31964)
    result = client.read_memory('0x140001000', 256)
    assert 'data' in result
```

### Integration Tests

Test full workflow:
1. Start x64dbg with plugin
2. Start MCP server
3. Run client
4. Verify expected behavior

## Release Process

1. Update version in `package.json`, `CMakeLists.txt`, `pyproject.toml`
2. Update CHANGELOG.md
3. Create release tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub release

## Questions?

- Open an issue
- Join discussions
- Check existing documentation

## Credits

This project merges:
- duty1g/x64dbg-mcp-server
- bromoket/x64dbg_mcp
- SetsunaYukiOvO/x64dbg-mcp
- wasdubya/x64dbgmcp
- dariushoule/x64dbg-automate-pyclient

Thank you to all contributors! 🎉

---

**x64dbg-mcp-x** | Unified MCP Server
