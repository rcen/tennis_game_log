#!/usr/bin/env python3
"""
Test script to verify the app initializes without crashes
"""

import sys
import os

# Suppress tkinter GUI from showing
os.environ['DISPLAY'] = ''

print("Testing Tennis Logger App Initialization...")
print("=" * 60)

try:
    print("1. Importing modules...")
    from tennis_logger.gui import TennisLoggerApp
    from tennis_logger.game_state import GameState
    from tennis_logger.logger import MatchLogger
    print("   ✓ Imports successful")
    
    print("\n2. Testing GameState...")
    game_state = GameState()
    print(f"   ✓ GameState created: {game_state.get_display_score()}")
    
    print("\n3. Testing Logger...")
    logger = MatchLogger()
    print(f"   ✓ Logger created: {logger.filename}")
    
    print("\n4. Testing logger methods...")
    # Test log_point
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
        "notes": "Test"
    }
    logger.log_point(test_data)
    print("   ✓ Point logged")
    
    # Test get_last_point_data
    last_point = logger.get_last_point_data()
    if last_point:
        print(f"   ✓ Retrieved last point with timestamp: {last_point.get('timestamp')}")
    else:
        print("   ✗ Failed to retrieve last point")
        sys.exit(1)
    
    # Test undo
    removed = logger.undo_last_log()
    if removed:
        print("   ✓ Undo successful")
    else:
        print("   ✗ Undo failed")
        sys.exit(1)
    
    print("\n5. Creating GUI instance (no display)...")
    # Create app but don't show it
    app = TennisLoggerApp()
    print("   ✓ TennisLoggerApp created successfully")
    
    print("\n6. Verifying GUI components...")
    if hasattr(app, 'lbl_timestamp'):
        print("   ✓ Timestamp label found")
    else:
        print("   ✗ Timestamp label not found")
        sys.exit(1)
    
    if hasattr(app, '_update_timestamp_display'):
        print("   ✓ Timestamp update method found")
    else:
        print("   ✗ Timestamp update method not found")
        sys.exit(1)
    
    print("\n7. Testing timestamp display...")
    # This should work without recursion now
    app._update_timestamp_display()
    print("   ✓ Timestamp display updated without errors")
    
    # Clean up
    app.destroy()
    if os.path.isfile(logger.filename):
        os.remove(logger.filename)
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED - App is working correctly!")
    print("=" * 60)
    sys.exit(0)

except RecursionError as e:
    print(f"\n✗ RECURSION ERROR: {e}")
    print("   This means there's still a recursive call somewhere")
    sys.exit(1)

except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
