#!/usr/bin/env python3
"""
Test script to verify that the data.json handling fix works correctly.
"""

import os
import sys
import tempfile
import shutil

# Add the extensions directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'extensions'))

def test_data_json_creation():
    """Test that data.json is created when it doesn't exist"""
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Import the module (this will trigger data.json creation if it doesn't exist)
            from turn_on import load_data, ensure_data_file_exists
            
            # Ensure data.json doesn't exist initially
            if os.path.exists('data.json'):
                os.remove('data.json')
            
            print("Testing data.json creation when file doesn't exist...")
            
            # This should create the file
            data = load_data()
            
            # Verify the file was created
            assert os.path.exists('data.json'), "data.json was not created"
            print("✅ data.json was successfully created")
            
            # Verify the structure
            assert 'devices' in data, "devices key missing from data"
            assert 'settings' in data, "settings key missing from data"
            assert 'version' in data, "version key missing from data"
            print("✅ data.json has correct structure")
            
            # Test that it doesn't overwrite existing data
            original_data = data.copy()
            data2 = load_data()
            assert data == data2, "Data was modified unexpectedly"
            print("✅ Existing data is preserved")
            
            print("\n🎉 All tests passed! The fix works correctly.")
            
        finally:
            os.chdir(original_cwd)

if __name__ == "__main__":
    test_data_json_creation()