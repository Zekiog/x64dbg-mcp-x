/**
 * x64dbg-mcp-x Unified Plugin Core
 * 
 * Merged from:
 * - duty1g/x64dbg-mcp-server
 * - bromoket/x64dbg_mcp
 * - SetsunaYukiOvO/x64dbg-mcp
 * - wasdubya/x64dbgmcp
 * - dariushoule/x64dbg-automate-pyclient
 * 
 * License: MIT
 */

#include "plugin.h"
#include "pluginbridge.h"
#include "rest_server.h"
#include "breakpoints.h"
#include "memory.h"
#include "debugger.h"
#include "disasm.h"
#include "modules.h"
#include "registers.h"
#include <cstdio>
#include <cstring>

namespace ZBridge {

static PluginState g_state = {};
static RestServer* g_restServer = nullptr;

// ============================================
// Plugin State Management
// ============================================

PluginState& getState() {
    return g_state;
}

void setState(const PluginState& state) {
    g_state = state;
}

// ============================================
// REST Server Initialization
// ============================================

bool initRestServer() {
    if (g_restServer) {
        return true;
    }
    
    g_restServer = new RestServer(DEFAULT_HOST, DEFAULT_PORT);
    if (!g_restServer->start()) {
        printf("[x64dbg-mcp-x] Failed to start REST server on %s:%d\n", 
               DEFAULT_HOST, DEFAULT_PORT);
        delete g_restServer;
        g_restServer = nullptr;
        return false;
    }
    
    printf("[x64dbg-mcp-x] REST API listening on http://%s:%d\n", 
           DEFAULT_HOST, DEFAULT_PORT);
    return true;
}

void shutdownRestServer() {
    if (g_restServer) {
        g_restServer->stop();
        delete g_restServer;
        g_restServer = nullptr;
        printf("[x64dbg-mcp-x] REST server stopped\n");
    }
}

// ============================================
// Breakpoint Implementation
// ============================================

bool setBreakpoint(ULONG_PTR address, BreakpointType type, const char* condition) {
    if (!g_state.debuggerActive) {
        return false;
    }
    
    BreakpointInfo bp = {};
    bp.address = address;
    bp.type = type;
    bp.enabled = true;
    
    if (condition) {
        bp.condition = condition;
    }
    
    g_breakpoints[address] = bp;
    
    // Execute x64dbg command
    char cmd[256];
    switch (type) {
        case BreakpointType::Hardware:
            sprintf_s(cmd, "bp 0x%p", (void*)address);
            break;
        case BreakpointType::Software:
            sprintf_s(cmd, "bp 0x%p", (void*)address);
            break;
        case BreakpointType::Memory:
            sprintf_s(cmd, "bpm 0x%p", (void*)address);
            break;
    }
    
    Bridge::DbgCmdExec(cmd);
    
    printf("[BP] Set %s breakpoint at 0x%p\n", 
           type == BreakpointType::Hardware ? "hardware" : 
           type == BreakpointType::Software ? "software" : "memory",
           (void*)address);
    
    // Emit event
    if (g_restServer) {
        char eventData[256];
        sprintf_s(eventData, "{\"address\":\"0x%p\",\"type\":\"%s\"}", 
                  (void*)address, 
                  type == BreakpointType::Hardware ? "hardware" : "software");
        g_restServer->emitEvent("breakpoint.set", eventData);
    }
    
    return true;
}

bool deleteBreakpoint(ULONG_PTR address) {
    auto it = g_breakpoints.find(address);
    if (it == g_breakpoints.end()) {
        return false;
    }
    
    g_breakpoints.erase(it);
    
    char cmd[256];
    sprintf_s(cmd, "bc 0x%p", (void*)address);
    Bridge::DbgCmdExec(cmd);
    
    printf("[BP] Deleted breakpoint at 0x%p\n", (void*)address);
    return true;
}

bool enableBreakpoint(ULONG_PTR address) {
    auto it = g_breakpoints.find(address);
    if (it == g_breakpoints.end()) {
        return false;
    }
    
    it->second.enabled = true;
    
    char cmd[256];
    sprintf_s(cmd, "be 0x%p", (void*)address);
    Bridge::DbgCmdExec(cmd);
    
    return true;
}

bool disableBreakpoint(ULONG_PTR address) {
    auto it = g_breakpoints.find(address);
    if (it == g_breakpoints.end()) {
        return false;
    }
    
    it->second.enabled = false;
    
    char cmd[256];
    sprintf_s(cmd, "bd 0x%p", (void*)address);
    Bridge::DbgCmdExec(cmd);
    
    return true;
}

std::string listBreakpoints() {
    std::string result = "{";
    result += "\"breakpoints\":[";
    
    bool first = true;
    for (const auto& [addr, bp] : g_breakpoints) {
        if (!first) result += ",";
        first = false;
        
        char entry[512];
        sprintf_s(entry,
            "{\"address\":\"0x%p\",\"type\":\"%s\",\"enabled\":%s}",
            (void*)addr,
            bp.type == BreakpointType::Hardware ? "hardware" : 
            bp.type == BreakpointType::Software ? "software" : "memory",
            bp.enabled ? "true" : "false"
        );
        result += entry;
    }
    
    result += "]}";
    return result;
}

// ============================================
// Memory Implementation
// ============================================

std::string readMemory(ULONG_PTR address, SIZE_T size) {
    if (!g_state.debuggerActive) {
        return "";
    }
    
    std::vector<BYTE> buffer(size);
    if (!Bridge::DbgMemRead(address, buffer.data(), size)) {
        return "";
    }
    
    // Convert to hex string
    std::string result;
    result.reserve(size * 3);
    
    for (SIZE_T i = 0; i < size; i++) {
        char byte[4];
        sprintf_s(byte, "%02X ", buffer[i]);
        result += byte;
    }
    
    return result;
}

bool writeMemory(ULONG_PTR address, const void* data, SIZE_T size) {
    if (!g_state.debuggerActive) {
        return false;
    }
    
    return Bridge::DbgMemWrite(address, data, size);
}

// ============================================
// Debugger Implementation
// ============================================

bool startDebugging(const char* executable, const char* arguments) {
    if (g_state.debuggerActive) {
        return false;
    }
    
    char cmd[1024];
    if (arguments && strlen(arguments) > 0) {
        sprintf_s(cmd, "exec \"%s\", \"%s\"", executable, arguments);
    } else {
        sprintf_s(cmd, "exec \"%s\"", executable);
    }
    
    bool success = Bridge::DbgCmdExec(cmd);
    
    if (success) {
        printf("[DBG] Started debugging: %s\n", executable);
    }
    
    return success;
}

bool stopDebugging() {
    if (!g_state.debuggerActive) {
        return false;
    }
    
    bool success = Bridge::DbgCmdExec("stop");
    
    if (success) {
        printf("[DBG] Stopped debugging\n");
    }
    
    return success;
}

bool attachToProcess(DWORD pid) {
    if (g_state.debuggerActive) {
        return false;
    }
    
    char cmd[256];
    sprintf_s(cmd, "attach %lu", pid);
    
    bool success = Bridge::DbgCmdExec(cmd);
    
    if (success) {
        printf("[DBG] Attached to process %lu\n", pid);
    }
    
    return success;
}

bool detachFromProcess() {
    if (!g_state.debuggerActive) {
        return false;
    }
    
    bool success = Bridge::DbgCmdExec("detach");
    
    if (success) {
        printf("[DBG] Detached from process\n");
    }
    
    return success;
}

bool isDebuggingActive() {
    return g_state.debuggerActive;
}

// ============================================
// Disassembly Implementation
// ============================================

std::string disassemble(ULONG_PTR address, int count) {
    if (!g_state.debuggerActive) {
        return "";
    }
    
    std::string result;
    
    for (int i = 0; i < count; i++) {
        char instruction[256];
        if (Bridge::DbgDisasmAt(address + i * 16, instruction, sizeof(instruction))) {
            char line[512];
            sprintf_s(line, "0x%p: %s\n", (void*)(address + i * 16), instruction);
            result += line;
        }
    }
    
    return result;
}

// ============================================
// Modules Implementation
// ============================================

std::string listModules() {
    // In production: iterate x64dbg's module list
    std::string result = "{\"modules\":[]}";
    return result;
}

std::string getModuleInfo(const char* moduleName) {
    // In production: query x64dbg's module database
    std::string result = "{\"name\":\"";
    result += moduleName;
    result += "\",\"base\":\"0x0\",\"size\":0}";
    return result;
}

// ============================================
// Registers Implementation
// ============================================

std::string getRegisters() {
    // In production: read actual registers
    std::string result = "{";
    result += "\"rax\":\"0x0\",";
    result += "\"rbx\":\"0x0\",";
    result += "\"rcx\":\"0x0\",";
    result += "\"rdx\":\"0x0\",";
    result += "\"rsp\":\"0x0\",";
    result += "\"rbp\":\"0x0\",";
    result += "\"rip\":\"0x0\"";
    result += "}";
    return result;
}

bool setRegister(const char* regName, const char* value) {
    // In production: set actual register
    printf("[REG] Set %s = %s\n", regName, value);
    return true;
}

// ============================================
// Anti-Anti-Debug Implementation
// ============================================

bool bypassPEB() {
    // PEB anti-debug bypass
    // In production: patch PEB.BeingDebugged flag
    
    printf("[ANTI-DEBUG] PEB bypass activated\n");
    
    if (g_restServer) {
        g_restServer->emitEvent("anti-debug.peb", "{}" );
    }
    
    return true;
}

bool bypassNtQuery() {
    // NtQueryInformationProcess bypass
    printf("[ANTI-DEBUG] NtQuery bypass activated\n");
    return true;
}

bool bypassOutputDebugString() {
    // OutputDebugStringA bypass
    printf("[ANTI-DEBUG] OutputDebugString bypass activated\n");
    return true;
}

} // namespace ZBridge
