# x64dbg-mcp-x Test Suite
# Merged from SetsunaYukiOvO implementation

cmake_minimum_required(VERSION 3.20)
project(x64dbg_mcp_x_tests LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Test executable
add_executable(x64dbg-mcp-x-tests
    ArchitectureRegisterNamesTests.cpp
    BreakpointAddressEntryTests.cpp
    BreakpointArchitectureTests.cpp
    RegisterValueValidationTests.cpp
    RequestAddressValidationTests.cpp
    StackRangeTests.cpp
    TargetValueValidationTests.cpp
)

# Include directories
target_include_directories(x64dbg-mcp-x-tests PRIVATE
    ${CMAKE_SOURCE_DIR}/../include
    ${CMAKE_SOURCE_DIR}/../src
)

# Link libraries
target_link_libraries(x64dbg-mcp-x-tests PRIVATE
    x64dbg-mcp-x
    gtest
    gtest_main
)

# Enable testing
enable_testing()
add_test(
    NAME x64dbg-mcp-x-tests
    COMMAND x64dbg-mcp-x-tests
)

# Test discovery
include(GoogleTest)
gtest_discover_tests(x64dbg-mcp-x-tests)
