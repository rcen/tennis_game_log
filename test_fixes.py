#!/usr/bin/env python3
"""
Test script to verify the three fixes:
1. Daily log files (new file each day)
2. Readable timestamp column
3. UNDO preserves notes and other data
"""

import os
import sys
import csv
from datetime import datetime
from tennis_logger.logger import MatchLogger
from tennis_logger.game_state import GameState

def test_daily_log_files():
    """Test that log files are created with date in filename"""
    print("\n=== Test 1: Daily Log Files ===")
    
    # Create logger with test filename
    logger = MatchLogger(base_filename="test_tennis_log")
    
    # Check if filename contains today's date
    today = datetime.now().strftime("%Y%m%d")
    expected_filename = f"test_tennis_log_{today}.csv"
    
    if logger.filename == expected_filename:
        print(f"✓ Logger creates daily file: {logger.filename}")
    else:
        print(f"✗ Expected {expected_filename}, got {logger.filename}")
        return False
    
    # Log a point and verify file is created
    test_data = {
        "set_no": 1,
        "game_no": 1,
        "score_before_point": "0 - 0",
        "server": "m",
        "serve_number": "1",
        "serve_code": "In (I)",
        "return_code": "In (I)",
        "rally_len_shots": "Short",
        "pattern": "Rally",
        "tactic_code": "Neutral",
        "pressure_flags": "",
        "final_shot_type": "Forehand",
        "final_outcome": "W",
        "court_pos_final": "",
        "notes": "Test note"
    }
    
    logger.log_point(test_data)
    
    if os.path.isfile(logger.filename):
        print(f"✓ File created: {logger.filename}")
        # Clean up
        if os.path.isfile(logger.filename):
            os.remove(logger.filename)
        return True
    else:
        print(f"✗ File not created: {logger.filename}")
        return False

def test_timestamp_column():
    """Test that timestamp column is added and has readable format"""
    print("\n=== Test 2: Readable Timestamp Column ===")
    
    logger = MatchLogger(base_filename="test_tennis_log_ts")
    
    # Check schema includes timestamp
    if "timestamp" in logger.SCHEMA_COLUMNS:
        print(f"✓ 'timestamp' column in schema at position {logger.SCHEMA_COLUMNS.index('timestamp')}")
    else:
        print("✗ 'timestamp' column not found in schema")
        return False
    
    # Verify it comes after point_id
    if logger.SCHEMA_COLUMNS[0] == "point_id" and logger.SCHEMA_COLUMNS[1] == "timestamp":
        print("✓ 'timestamp' is in correct position (after point_id)")
    else:
        print("✗ 'timestamp' is not in correct position")
        return False
    
    # Log a point and check the CSV
    test_data = {
        "set_no": 1,
        "game_no": 1,
        "score_before_point": "0 - 0",
        "server": "m",
        "serve_number": "1",
        "serve_code": "In (I)",
        "return_code": "In (I)",
        "rally_len_shots": "Short",
        "pattern": "Rally",
        "tactic_code": "Neutral",
        "pressure_flags": "",
        "final_shot_type": "Forehand",
        "final_outcome": "W",
        "court_pos_final": "",
        "notes": "Test note"
    }
    
    logger.log_point(test_data)
    
    # Read the CSV and verify timestamp format
    with open(logger.filename, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if rows:
            last_row = rows[-1]
            timestamp = last_row.get('timestamp', '')
            
            # Check timestamp format (YYYY-MM-DD HH:MM:SS)
            try:
                datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                print(f"✓ Timestamp has readable format: {timestamp}")
                success = True
            except ValueError:
                print(f"✗ Timestamp has invalid format: {timestamp}")
                success = False
        else:
            print("✗ No rows in CSV after logging")
            success = False
    
    # Clean up
    if os.path.isfile(logger.filename):
        os.remove(logger.filename)
    
    return success

def test_undo_preserves_data():
    """Test that UNDO preserves notes and other point data"""
    print("\n=== Test 3: UNDO Preserves Notes & Data ===")
    
    logger = MatchLogger(base_filename="test_tennis_log_undo")
    
    # Log a point with notes and specific data
    point_data = {
        "set_no": 1,
        "game_no": 1,
        "score_before_point": "15 - 0",
        "server": "m",
        "serve_number": "1",
        "serve_code": "In (I) [6]",
        "return_code": "In (I) [6]",
        "rally_len_shots": "Long [3]",
        "pattern": "First Strike (F)|Rally (R) [11]",
        "tactic_code": "Neutral (N) [13]",
        "pressure_flags": "",
        "final_shot_type": "Forehand (F) [7]",
        "final_outcome": "W",
        "court_pos_final": "",
        "notes": "Excellent winner from baseline"
    }
    
    logger.log_point(point_data)
    
    # Retrieve the last point data before undo
    last_data = logger.get_last_point_data()
    
    if not last_data:
        print("✗ Could not retrieve last point data")
        return False
    
    # Verify key fields are preserved
    checks = [
        ('notes', 'Excellent winner from baseline'),
        ('rally_len_shots', 'Long [3]'),
        ('serve_code', 'In (I) [6]'),
        ('pattern', 'First Strike (F)|Rally (R) [11]'),
        ('server', 'm'),
        ('score_before_point', '15 - 0')
    ]
    
    all_match = True
    for field, expected in checks:
        actual = last_data.get(field, '')
        if actual == expected:
            print(f"✓ {field}: '{actual}'")
        else:
            print(f"✗ {field}: expected '{expected}', got '{actual}'")
            all_match = False
    
    # Test undo removes the row
    removed_data = logger.undo_last_log()
    
    if removed_data and removed_data.get('notes') == point_data['notes']:
        print(f"✓ UNDO removed correct row with notes: '{removed_data['notes']}'")
    else:
        print("✗ UNDO did not preserve the data correctly")
        all_match = False
    
    # Clean up
    if os.path.isfile(logger.filename):
        os.remove(logger.filename)
    
    return all_match

def main():
    print("="*60)
    print("TESTING TENNIS GAME LOG FIXES")
    print("="*60)
    
    results = {
        "Daily Log Files": test_daily_log_files(),
        "Readable Timestamp": test_timestamp_column(),
        "UNDO Preserves Data": test_undo_preserves_data()
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
    
    all_pass = all(results.values())
    print("="*60)
    if all_pass:
        print("✓ ALL TESTS PASSED")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
