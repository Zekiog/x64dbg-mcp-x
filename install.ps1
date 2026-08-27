# x64dbg-mcp-x Unified Installer
# Merged from 5 implementations: duty1g, bromoket, SetsunaYukiOvO, wasdubya, dariushoule

param(
    [string]$x64dbgPath = "C:\x64dbg",
    [switch]$SkipPlugin,
    [switch]$SkipServer,
    [switch]$SkipPython
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  x64dbg-mcp-x Installer" -ForegroundColor Cyan
Write-Host "  Unified MCP Server (181+ tools)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check x64dbg path
if (-not (Test-Path $x64dbgPath)) {
    Write-Host "x64dbg not found at $x64dbgPath" -ForegroundColor Red
    $x64dbgPath = Read-Host "Enter x64dbg installation path"
}

Write-Host "x64dbg path: $x64dbgPath" -ForegroundColor Green
Write-Host ""

# Install plugin
if (-not $SkipPlugin) {
    Write-Host "Installing plugin..." -ForegroundColor Yellow
    
    $pluginSrc = Join-Path $PSScriptRoot "plugin"
    $pluginDest32 = Join-Path $x64dbgPath "x32\plugins"
    $pluginDest64 = Join-Path $x64dbgPath "x64\plugins"
    
    if (-not (Test-Path $pluginDest32)) { New-Item -ItemType Directory -Path $pluginDest32 | Out-Null }
    if (-not (Test-Path $pluginDest64)) { New-Item -ItemType Directory -Path $pluginDest64 | Out-Null }
    
    # Build plugin if not already built
    if (-not (Test-Path "$pluginSrc\build\x64dbg-mcp-x.dp64")) {
        Write-Host "  Building plugin..." -ForegroundColor Gray
        Set-Location $pluginSrc
        .\build.ps1 -x64dbgDir $x64dbgPath
    }
    
    # Copy plugin files
    if (Test-Path "$pluginSrc\build\x64dbg-mcp-x.dp64") {
        Copy-Item "$pluginSrc\build\x64dbg-mcp-x.dp64" $pluginDest64 -Force
        Write-Host "  ✓ x64dbg plugin installed" -ForegroundColor Green
    }
    if (Test-Path "$pluginSrc\build\x64dbg-mcp-x.dp32") {
        Copy-Item "$pluginSrc\build\x64dbg-mcp-x.dp32" $pluginDest32 -Force
        Write-Host "  ✓ x32dbg plugin installed" -ForegroundColor Green
    }
    Write-Host ""
}

# Install server
if (-not $SkipServer) {
    Write-Host "Installing MCP server..." -ForegroundColor Yellow
    
    $serverPath = Join-Path $PSScriptRoot "server"
    Set-Location $serverPath
    
    if (-not (Test-Path "node_modules")) {
        Write-Host "  Installing npm dependencies..." -ForegroundColor Gray
        npm install
    }
    
    Write-Host "  Building TypeScript..." -ForegroundColor Gray
    npm run build
    
    Write-Host "  ✓ Server installed" -ForegroundColor Green
    Write-Host ""
}

# Install Python client
if (-not $SkipPython) {
    Write-Host "Installing Python client..." -ForegroundColor Yellow
    
    $pythonPath = Join-Path $PSScriptRoot "clients\python"
    Set-Location $pythonPath
    
    if (Test-Path "pyproject.toml") {
        if (Get-Command poetry -ErrorAction SilentlyContinue) {
            Write-Host "  Installing with Poetry..." -ForegroundColor Gray
            poetry install
        } else {
            Write-Host "  Installing with pip..." -ForegroundColor Gray
            pip install -e .
        }
        Write-Host "  ✓ Python client installed" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Python client not found, skipping..." -ForegroundColor Yellow
    }
    Write-Host ""
}

# Configure Claude Desktop
Write-Host "Configuring Claude Desktop..." -ForegroundColor Yellow

$claudeConfig = "$env:APPDATA\Claude\claude_desktop_config.json"
if (Test-Path $claudeConfig) {
    $config = Get-Content $claudeConfig -Raw | ConvertFrom-Json
    
    if (-not $config.mcpServers) {
        $config | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value (@{})
    }
    
    $config.mcpServers | Add-Member -MemberType NoteProperty -Name "x64dbg-mcp-x" -Value (@{
        command = "node"
        args = @("$(Join-Path $PSScriptRoot 'server\dist\index.js')")
        env = @{
            X64DBG_HOST = "localhost"
            X64DBG_PORT = "31964"
        }
    }) -Force
    
    $config | ConvertTo-Json -Depth 10 | Set-Content $claudeConfig
    Write-Host "  ✓ Claude Desktop configured" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Claude Desktop config not found, skipping..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart x64dbg"
Write-Host "2. Restart Claude Desktop"
Write-Host "3. Start debugging with 181+ tools! 🚀"
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "  - README.md"
Write-Host "  - docs/AGENTS.md (AI agents)"
Write-Host "  - docs/CLAUDE.md (Claude Code)"
Write-Host "  - docs/ATTACH.md (Process attach)"
Write-Host "  - BUILD.md (Build instructions)"
Write-Host ""
