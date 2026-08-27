cmake_minimum_required(VERSION 3.20)
project(x64dbg-mcp-x VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# x64dbg SDK path
if(NOT DEFINED x64dbgDir)
    set(x64dbgDir "C:/x64dbg" CACHE PATH "x64dbg installation directory")
endif()

# Find x64dbg SDK
find_path(X64DBG_SDK_DIR 
    NAMES "x64dbg_bridge.h" "x64dbg_plugin.h"
    PATHS "${x64dbgDir}/src/sdk" "${x64dbgDir}/sdk"
    DOC "x64dbg SDK directory"
)

if(NOT X64DBG_SDK_DIR)
    message(WARNING "x64dbg SDK not found. Plugin will build but may not load.")
    set(X64DBG_SDK_DIR "")
endif()

# Plugin sources (unified from 5 implementations)
set(PLUGIN_SOURCES
    src/main.cpp
    src/plugin.cpp
    src/plugin.h
    src/rest_server.cpp
    src/rest_server.h
    src/breakpoints.cpp
    src/breakpoints.h
    src/memory.cpp
    src/memory.h
    src/debugger.cpp
    src/debugger.h
    src/disasm.cpp
    src/disasm.h
    src/modules.cpp
    src/modules.h
    src/registers.cpp
    src/registers.h
)

# x64dbg plugin (x64)
add_library(x64dbg-mcp-x-x64 SHARED ${PLUGIN_SOURCES})
target_include_directories(x64dbg-mcp-x-x64 PRIVATE
    ${X64DBG_SDK_DIR}
    include
    ../include
)
target_compile_definitions(x64dbg-mcp-x-x64 PRIVATE
    _WIN32
    WIN32
    _WINDOWS
    UNICODE
    _UNICODE
    BUILDING_DLL
    _HAS_EXCEPTIONS=0
)
target_link_libraries(x64dbg-mcp-x-x64 PRIVATE
    ws2_32
    wsock32
)
set_target_properties(x64dbg-mcp-x-x64 PROPERTIES
    OUTPUT_NAME "x64dbg-mcp-x"
    SUFFIX ".dp64"
    PREFIX ""
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
    RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_BINARY_DIR}"
)

# x32dbg plugin (x86)
add_library(x64dbg-mcp-x-x32 SHARED ${PLUGIN_SOURCES})
target_include_directories(x64dbg-mcp-x-x32 PRIVATE
    ${X64DBG_SDK_DIR}
    include
    ../include
)
target_compile_definitions(x64dbg-mcp-x-x32 PRIVATE
    _WIN32
    WIN32
    _WINDOWS
    UNICODE
    _UNICODE
    BUILDING_DLL
    _M_IX86
    _HAS_EXCEPTIONS=0
)
target_link_libraries(x64dbg-mcp-x-x32 PRIVATE
    ws2_32
    wsock32
)
set_target_properties(x64dbg-mcp-x-x32 PROPERTIES
    OUTPUT_NAME "x64dbg-mcp-x"
    SUFFIX ".dp32"
    PREFIX ""
    WIN32_EXECUTABLE TRUE
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
    RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_BINARY_DIR}"
)

# Install targets
install(TARGETS x64dbg-mcp-x-x64
    LIBRARY DESTINATION "${x64dbgDir}/x64/plugins"
    COMPONENT x64dbg
)
install(TARGETS x64dbg-mcp-x-x32
    LIBRARY DESTINATION "${x64dbgDir}/x32/plugins"
    COMPONENT x32dbg
)

# Tests
option(BUILD_TESTS "Build test suite" OFF)
if(BUILD_TESTS)
    add_subdirectory(../tests tests)
endif()

message(STATUS "========================================")
message(STATUS "x64dbg-mcp-x Plugin Configuration")
message(STATUS "========================================")
message(STATUS "x64dbg SDK: ${X64DBG_SDK_DIR}")
message(STATUS "x64dbg Dir: ${x64dbgDir}")
message(STATUS "Build Tests: ${BUILD_TESTS}")
message(STATUS "Output:")
message(STATUS "  - x64dbg-mcp-x.dp64 (x64dbg)")
message(STATUS "  - x64dbg-mcp-x.dp32 (x32dbg)")
message(STATUS "========================================")
