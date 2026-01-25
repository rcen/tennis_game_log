#!/usr/bin/env python3
"""
Test script to verify timestamp display in GUI
"""

import os
import sys
from datetime import datetime
from tennis_logger.logger import MatchLogger

def test_timestamp_display():
    """Test that timestamp can be retrieved and displayed"""
    print("\n=== Test: Timestamp Display in GUI ===")
    
    logger = MatchLogger(base_filename="test_gui_timestamp")
    
    # Log a test point
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
        "notes": "Test point"
    }
    
    logger.log_point(test_data)
    
    # Retrieve and display the timestamp
    last_point = logger.get_last_point_data()
    
    if last_point:
        timestamp = last_point.get('timestamp', 'NOT FOUND')
        print(f"✓ Retrieved timestamp: {timestamp}")
        
        # Verify format
        try:
            datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            print(f"✓ Timestamp format is valid (YYYY-MM-DD HH:MM:SS)")
            
            # Show what the GUI would display
            display_text = f"Last Point: {timestamp}"
            print(f"✓ GUI Display would show: '{display_text}'")
            
            # Clean up
            if os.path.isfile(logger.filename):
                os.remove(logger.filename)
            
            return True
        except ValueError:
            print(f"✗ Invalid timestamp format")
            return False
    else:
        print("✗ Could not retrieve last point data")
        return False

def main():
    print("="*60)
    print("TESTING TIMESTAMP DISPLAY FUNCTIONALITY")
    print("="*60)
    
    result = test_timestamp_display()
    
    print("\n" + "="*60)
    if result:
        print("✓ TEST PASSED - Timestamp display ready for GUI")
        return 0
    else:
        print("✗ TEST FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
