/**
 * x64dbg-mcp-x Plugin Entry Point
 * 
 * Merged from 5 implementations:
 * - duty1g/x64dbg-mcp-server
 * - bromoket/x64dbg_mcp
 * - SetsunaYukiOvO/x64dbg-mcp
 * - wasdubya/x64dbgmcp
 * - dariushoule/x64dbg-automate-pyclient
 * 
 * License: MIT
 */

#include <windows.h>
#include <string>
#include <cstdio>

#include "pluginbridge.h"
#include "plugin.h"
#include "rest_server.h"

// Global plugin state
static ZBridge::PluginState g_pluginState;

// Plugin exports for x64dbg
extern "C" {

__declspec(dllexport) bool CBPLUGIN(PluginInit, PLUG_INITSTRUCT* initStruct) {
    ZBridge::setState(g_pluginState);
    g_pluginState.pluginLoaded = true;
    g_pluginState.version = "1.0.0";
    
    printf("[x64dbg-mcp-x] Plugin initialized (v%s)\n", g_pluginState.version.c_str());
    
    // Initialize REST server
    if (!ZBridge::initRestServer()) {
        printf("[x64dbg-mcp-x] Failed to initialize REST server\n");
        return false;
    }
    
    return true;
}

__declspec(dllexport) void CBPLUGIN(PluginStop, PLUG_STOPSTRUCT* stopStruct) {
    g_pluginState.pluginLoaded = false;
    ZBridge::setState(g_pluginState);
    
    // Shutdown REST server
    ZBridge::shutdownRestServer();
    
    printf("[x64dbg-mcp-x] Plugin stopped\n");
}

__declspec(dllexport) void CBPLUGIN(PluginSetup, PLUG_SETUPSTRUCT* setupStruct) {
    printf("[x64dbg-mcp-x] Setup complete\n");
}

__declspec(dllexport) void CBPLUGIN(PluginBreak, PLUG_BREAKSTRUCT* breakStruct) {
    // Debugger break event
    if (ZBridge::g_restServer) {
        ZBridge::g_restServer->emitEvent("debug.break", "{}" );
    }
}

__declspec(dllexport) void CBPLUGIN(PluginContinue, PLUG_CONTINUESTRUCT* continueStruct) {
    // Debugger continue event
    if (ZBridge::g_restServer) {
        ZBridge::g_restServer->emitEvent("debug.continue", "{}" );
    }
}

__declspec(dllexport) void CBPLUGIN(DebuggingStarted, PLUG_DEBUGSTARTEDSTRUCT* startedStruct) {
    g_pluginState.debuggerActive = true;
    ZBridge::setState(g_pluginState);
    
    if (ZBridge::g_restServer) {
        ZBridge::g_restServer->emitEvent("debug.started", "{}" );
    }
    
    printf("[x64dbg-mcp-x] Debugging started\n");
}

__declspec(dllexport) void CBPLUGIN(DebuggingStopped, PLUG_DEBUGSTOPPEDSTRUCT* stoppedStruct) {
    g_pluginState.debuggerActive = false;
    ZBridge::setState(g_pluginState);
    
    if (ZBridge::g_restServer) {
        ZBridge::g_restServer->emitEvent("debug.stopped", "{}" );
    }
    
    printf("[x64dbg-mcp-x] Debugging stopped\n");
}

__declspec(dllexport) void CBPLUGIN(BreakpointReached, PLUG_BPTYPE* bpType) {
    // Breakpoint hit - emit event via REST
    if (ZBridge::g_restServer) {
        char buffer[256];
        sprintf_s(buffer, "{\"address\":\"0x%p\"}", (void*)Bridge::GetDebugData()->breakpoint);
        ZBridge::g_restServer->emitEvent("breakpoint.hit", buffer);
    }
}

__declspec(dllexport) void CBPLUGIN(ModuleLoad, PLUG_MODULEINFO* info) {
    // Module loaded
    if (ZBridge::g_restServer && info) {
        char buffer[512];
        sprintf_s(buffer, "{\"name\":\"%s\",\"base\":\"0x%p\",\"loaded\":true}", 
                  info->name, (void*)info->base);
        ZBridge::g_restServer->emitEvent("module.load", buffer);
    }
}

__declspec(dllexport) void CBPLUGIN(ModuleUnload, PLUG_MODULEINFO* info) {
    // Module unloaded
    if (ZBridge::g_restServer && info) {
        char buffer[512];
        sprintf_s(buffer, "{\"name\":\"%s\",\"base\":\"0x%p\",\"loaded\":false}", 
                  info->name, (void*)info->base);
        ZBridge::g_restServer->emitEvent("module.unload", buffer);
    }
}

} // extern "C"

// Plugin metadata
PLUG_EXPORT void CBPLUGIN(PluginGetInfo, PLUG_INFO* info) {
    if (info) {
        info->pluginVersion = 1;
        strcpy_s(info->pluginName, "x64dbg-mcp-x");
        strcpy_s(info->pluginDescription, "Unified MCP Server (181+ tools from 5 repos)");
    }
}
