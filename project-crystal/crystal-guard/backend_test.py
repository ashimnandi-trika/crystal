#!/usr/bin/env python3
"""
Crystal Guard CLI Testing Suite
Tests all CLI commands and functionality
"""

import subprocess
import sys
import json
import tempfile
import os
from pathlib import Path
from datetime import datetime

class CrystalGuardTester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.project_root = Path("/app/project-crystal/crystal-guard").resolve()
        self.good_project = self.project_root / "tests/fixtures/good_project"
        self.bad_project = self.project_root / "tests/fixtures/bad_project"
        
    def run_test(self, name, command, expected_exit_code=0, check_output=None):
        """Run a single CLI test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"Command: {' '.join(command)}")
        
        try:
            # Change to project root for CLI execution
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=str(self.project_root),
                timeout=30
            )
            
            success = result.returncode == expected_exit_code
            
            if success and check_output:
                success = check_output(result.stdout, result.stderr)
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Exit code: {result.returncode}")
                if result.stdout.strip():
                    print(f"Output: {result.stdout.strip()[:200]}...")
            else:
                print(f"❌ Failed - Expected exit code {expected_exit_code}, got {result.returncode}")
                if result.stdout:
                    print(f"STDOUT: {result.stdout}")
                if result.stderr:
                    print(f"STDERR: {result.stderr}")
            
            return success, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            print(f"❌ Failed - Command timed out")
            return False, "", "Timeout"
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, "", str(e)

    def test_crystal_init_good_project(self):
        """Test crystal init on good project"""
        def check_init_output(stdout, stderr):
            return ("Detected stack:" in stdout and 
                    "Created .crystal/ configuration" in stdout and
                    "React" in stdout or "Python" in stdout or "MongoDB" in stdout)
        
        success, stdout, stderr = self.run_test(
            "crystal init tests/fixtures/good_project",
            ["crystal", "init", "tests/fixtures/good_project"],
            expected_exit_code=0,
            check_output=check_init_output
        )
        
        # Check if .crystal directory was created
        crystal_dir = self.good_project / ".crystal"
        if crystal_dir.exists():
            print("✅ .crystal/ directory created successfully")
        else:
            print("❌ .crystal/ directory not found")
            return False
            
        return success

    def test_crystal_check_good_project(self):
        """Test crystal check on good project - should return A grade"""
        def check_good_output(stdout, stderr):
            return ("A" in stdout and "100" in stdout) or ("PASS" in stdout)
        
        return self.run_test(
            "crystal check tests/fixtures/good_project (expecting A grade)",
            ["crystal", "check", "tests/fixtures/good_project"],
            expected_exit_code=0,
            check_output=check_good_output
        )[0]

    def test_crystal_check_bad_project(self):
        """Test crystal check on bad project - should catch issues"""
        def check_bad_output(stdout, stderr):
            # Should find issues and return F grade or show failures
            return ("F" in stdout or "FAIL" in stdout or 
                    "critical" in stdout.lower() or "error" in stdout.lower() or
                    "issue" in stdout.lower())
        
        return self.run_test(
            "crystal check tests/fixtures/bad_project (expecting F grade)",
            ["crystal", "check", "tests/fixtures/bad_project"],
            expected_exit_code=1,  # Should fail with issues
            check_output=check_bad_output
        )[0]

    def test_crystal_gates_bad_project(self):
        """Test crystal gates command showing individual gate status"""
        def check_gates_output(stdout, stderr):
            # Should show 15 gates with PASS/FAIL status
            return ("Gate" in stdout and 
                    ("PASS" in stdout or "FAIL" in stdout) and
                    "15" in stdout)
        
        return self.run_test(
            "crystal gates tests/fixtures/bad_project",
            ["crystal", "gates", "tests/fixtures/bad_project"],
            expected_exit_code=0,
            check_output=check_gates_output
        )[0]

    def test_crystal_handoff(self):
        """Test crystal handoff command"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            handoff_file = f.name
        
        try:
            def check_handoff_output(stdout, stderr):
                return "handoff" in stdout.lower() or "session" in stdout.lower()
            
            success = self.run_test(
                "crystal handoff with output file",
                ["crystal", "handoff", "tests/fixtures/bad_project", "--output", handoff_file],
                expected_exit_code=0,
                check_output=check_handoff_output
            )[0]
            
            # Check if handoff file was created and has content
            if os.path.exists(handoff_file):
                with open(handoff_file, 'r') as f:
                    content = f.read()
                if len(content) > 100 and "SESSION HANDOFF" in content:
                    print("✅ Handoff file created with valid content")
                    return success
                else:
                    print("❌ Handoff file created but content is invalid")
                    return False
            else:
                print("❌ Handoff file was not created")
                return False
                
        finally:
            if os.path.exists(handoff_file):
                os.unlink(handoff_file)

    def test_crystal_status(self):
        """Test crystal status command"""
        def check_status_output(stdout, stderr):
            return ("health" in stdout.lower() or "score" in stdout.lower() or 
                    "files:" in stdout.lower() or "tests:" in stdout.lower())
        
        return self.run_test(
            "crystal status tests/fixtures/good_project",
            ["crystal", "status", "tests/fixtures/good_project"],
            expected_exit_code=0,
            check_output=check_status_output
        )[0]

    def test_crystal_check_json_format(self):
        """Test crystal check with JSON output format"""
        def check_json_output(stdout, stderr):
            try:
                json.loads(stdout)
                return True
            except json.JSONDecodeError:
                return False
        
        return self.run_test(
            "crystal check --format json",
            ["crystal", "check", "tests/fixtures/good_project", "--format", "json"],
            expected_exit_code=0,
            check_output=check_json_output
        )[0]

    def test_crystal_check_markdown_format(self):
        """Test crystal check with markdown output format"""
        def check_markdown_output(stdout, stderr):
            return ("##" in stdout or "#" in stdout) and len(stdout) > 50
        
        return self.run_test(
            "crystal check --format markdown",
            ["crystal", "check", "tests/fixtures/good_project", "--format", "markdown"],
            expected_exit_code=0,
            check_output=check_markdown_output
        )[0]

    def test_crystal_help(self):
        """Test crystal help command"""
        def check_help_output(stdout, stderr):
            return ("crystal" in stdout.lower() and 
                    ("init" in stdout or "check" in stdout or "handoff" in stdout))
        
        return self.run_test(
            "crystal --help",
            ["crystal", "--help"],
            expected_exit_code=0,
            check_output=check_help_output
        )[0]

def main():
    """Run all Crystal Guard CLI tests"""
    print("🔬 Crystal Guard CLI Test Suite")
    print("=" * 50)
    
    tester = CrystalGuardTester()
    
    # Verify we're in the right directory and crystal is available
    print(f"Working directory: {tester.project_root}")
    print(f"Good project: {tester.good_project}")
    print(f"Bad project: {tester.bad_project}")
    
    # Check if crystal command is available
    try:
        result = subprocess.run(["crystal", "--help"], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("❌ Crystal command not available or not working")
            return 1
        print("✅ Crystal command is available")
    except Exception as e:
        print(f"❌ Error checking crystal command: {e}")
        return 1
    
    # Run all tests
    tests = [
        tester.test_crystal_help,
        tester.test_crystal_init_good_project,
        tester.test_crystal_check_good_project,
        tester.test_crystal_check_bad_project,
        tester.test_crystal_gates_bad_project,
        tester.test_crystal_handoff,
        tester.test_crystal_status,
        tester.test_crystal_check_json_format,
        tester.test_crystal_check_markdown_format,
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    # Print results
    print("\n" + "=" * 50)
    print(f"📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    success_rate = (tester.tests_passed / tester.tests_run * 100) if tester.tests_run > 0 else 0
    print(f"Success rate: {success_rate:.1f}%")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())