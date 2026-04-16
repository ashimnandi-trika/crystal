#!/usr/bin/env python3
"""
Crystal CLI Backend Testing
Tests the Crystal CLI functionality as specified in the requirements.
"""

import subprocess
import sys
import os
from pathlib import Path

class CrystalCLITester:
    def __init__(self):
        self.crystal_dir = "/app/project-crystal/crystal-guard"
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, command, expected_exit_code=0, expected_output_contains=None):
        """Run a CLI test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            # Change to crystal directory
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.crystal_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == expected_exit_code
            
            if expected_output_contains:
                for expected in expected_output_contains:
                    if expected not in result.stdout:
                        success = False
                        print(f"❌ Failed - Expected output '{expected}' not found")
                        break
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Exit code: {result.returncode}")
                if expected_output_contains:
                    print(f"✅ All expected outputs found")
            else:
                print(f"❌ Failed - Expected exit code {expected_exit_code}, got {result.returncode}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
            
            return success, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            print(f"❌ Failed - Command timed out")
            return False, "", "Timeout"
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, "", str(e)

    def test_crystal_help(self):
        """Test crystal --help command"""
        return self.run_test(
            "Crystal Help",
            "crystal --help",
            expected_output_contains=["Crystal — Your AI coding buddy", "Commands"]
        )

    def test_crystal_check_good_project(self):
        """Test crystal check on good project - should return A (100/100)"""
        return self.run_test(
            "Crystal Check Good Project",
            "crystal check tests/fixtures/good_project",
            expected_output_contains=["A (100/100)", "Excellent structure"]
        )

    def test_crystal_architect_good_project(self):
        """Test crystal architect on good project - should generate architecture.md"""
        return self.run_test(
            "Crystal Architect Good Project",
            "crystal architect tests/fixtures/good_project",
            expected_output_contains=["Generated:", "architecture.md"]
        )

    def test_crystal_check_self(self):
        """Test crystal check on itself - should return A (100/100)"""
        return self.run_test(
            "Crystal Check Self",
            "crystal check .",
            expected_output_contains=["A (100/100)", "Excellent structure"]
        )

    def test_crystal_gates(self):
        """Test crystal gates command"""
        return self.run_test(
            "Crystal Gates",
            "crystal gates .",
            expected_output_contains=["CRYSTAL GUARD — 15 QUALITY GATES", "gates passed"]
        )

def main():
    """Run all CLI tests"""
    print("🚀 Starting Crystal CLI Tests")
    print(f"Testing Crystal CLI at: /app/project-crystal/crystal-guard")
    
    tester = CrystalCLITester()
    
    # Check if Crystal CLI is available
    if not os.path.exists(tester.crystal_dir):
        print(f"❌ Crystal directory not found: {tester.crystal_dir}")
        return 1
    
    # Run tests
    tests = [
        tester.test_crystal_help,
        tester.test_crystal_check_good_project,
        tester.test_crystal_architect_good_project,
        tester.test_crystal_check_self,
        tester.test_crystal_gates,
    ]
    
    for test in tests:
        test()
    
    # Print results
    print(f"\n📊 CLI Tests Results: {tester.tests_passed}/{tester.tests_run} passed")
    
    if tester.tests_passed == tester.tests_run:
        print("✅ All CLI tests passed!")
        return 0
    else:
        print("❌ Some CLI tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())