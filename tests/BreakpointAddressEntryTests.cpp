/**
 * x64dbg-mcp-x Breakpoint Address Entry Tests
 * 
 * Merged from SetsunaYukiOvO/x64dbg-mcp
 */

#include <gtest/gtest.h>
#include "breakpoints.h"
#include "pluginbridge.h"

namespace ZBridge {
namespace Tests {

class BreakpointAddressEntryTests : public ::testing::Test {
protected:
    void SetUp() override {
        // Initialize test state
    }
    
    void TearDown() override {
        // Clean up
    }
};

TEST_F(BreakpointAddressEntryTests, ValidHardwareBreakpoint) {
    // Test setting a valid hardware breakpoint
    ULONG_PTR address = 0x140001000;
    bool result = setBreakpoint(address, BreakpointType::Hardware);
    
    EXPECT_TRUE(result);
    EXPECT_FALSE(listBreakpoints().empty());
}

TEST_F(BreakpointAddressEntryTests, ValidSoftwareBreakpoint) {
    // Test setting a valid software breakpoint
    ULONG_PTR address = 0x140002000;
    bool result = setBreakpoint(address, BreakpointType::Software);
    
    EXPECT_TRUE(result);
}

TEST_F(BreakpointAddressEntryTests, InvalidAddress) {
    // Test with invalid address (0x0)
    ULONG_PTR address = 0x0;
    bool result = setBreakpoint(address, BreakpointType::Hardware);
    
    EXPECT_FALSE(result);
}

TEST_F(BreakpointAddressEntryTests, DeleteBreakpoint) {
    // Test deleting a breakpoint
    ULONG_PTR address = 0x140003000;
    setBreakpoint(address, BreakpointType::Hardware);
    
    bool deleteResult = deleteBreakpoint(address);
    EXPECT_TRUE(deleteResult);
}

TEST_F(BreakpointAddressEntryTests, EnableDisableBreakpoint) {
    // Test enabling/disabling
    ULONG_PTR address = 0x140004000;
    setBreakpoint(address, BreakpointType::Hardware);
    
    bool disableResult = disableBreakpoint(address);
    EXPECT_TRUE(disableResult);
    
    bool enableResult = enableBreakpoint(address);
    EXPECT_TRUE(enableResult);
}

} // namespace Tests
} // namespace ZBridge
