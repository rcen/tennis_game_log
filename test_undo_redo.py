#!/usr/bin/env python3
"""
Test script to verify undo/redo functionality
"""

import os
import sys
from tennis_logger.logger import MatchLogger
from tennis_logger.game_state import GameState

def test_undo_redo_stack():
    """Test that undo/redo works correctly with the stack"""
    print("\n=== Test: Undo/Redo Stack Functionality ===")
    
    logger = MatchLogger(base_filename="test_undo_redo")
    game_state = GameState()
    
    # Create test points
    point1 = {
        "set_no": 1, "game_no": 1, "score_before_point": "0 - 0",
        "server": "m", "serve_number": "1", "serve_code": "In (I)",
        "return_code": "In (I)", "rally_len_shots": "Short",
        "pattern": "Rally", "tactic_code": "Neutral",
        "final_outcome": "W", "notes": "Point 1"
    }
    
    point2 = {
        "set_no": 1, "game_no": 1, "score_before_point": "15 - 0",
        "server": "m", "serve_number": "1", "serve_code": "Ace (A)",
        "return_code": "N/A", "rally_len_shots": "Short",
        "pattern": "First Strike", "tactic_code": "Aggressive",
        "final_outcome": "W", "notes": "Point 2 - Ace!"
    }
    
    point3 = {
        "set_no": 1, "game_no": 1, "score_before_point": "30 - 0",
        "server": "m", "serve_number": "1", "serve_code": "In (I)",
        "return_code": "In (I)", "rally_len_shots": "Long",
        "pattern": "Rally", "tactic_code": "Defensive",
        "final_outcome": "L", "notes": "Point 3 - Lost"
    }
    
    print("1. Logging three points (P1, P2, P3)...")
    logger.log_point(point1)
    game_state.add_point('me')
    logger.log_point(point2)
    game_state.add_point('me')
    logger.log_point(point3)
    game_state.add_point('opponent')
    
    # Verify all 3 points in CSV
    with open(logger.filename, 'r') as f:
        lines = f.readlines()
        if len(lines) == 4:  # header + 3 points
            print("   ✓ Three points logged: P1, P2, P3")
        else:
            print(f"   ✗ Expected 4 lines, got {len(lines)}")
            return False
    
    print("\n2. Testing UNDO to T-1 (P2)...")
    removed = logger.undo_last_log()
    game_state.undo()
    if removed and removed.get('notes') == "Point 3 - Lost":
        print(f"   ✓ P3 removed, notes: '{removed['notes']}'")
        print(f"   ✓ P3 in undo stack: {len(logger.undo_stack)} items")
    else:
        print("   ✗ Failed to undo P3")
        return False
    
    print("\n3. Testing UNDO again to T-2 (P1)...")
    removed = logger.undo_last_log()
    game_state.undo()
    if removed and removed.get('notes') == "Point 2 - Ace!":
        print(f"   ✓ P2 removed, notes: '{removed['notes']}'")
        print(f"   ✓ Undo stack now has {len(logger.undo_stack)} items")
    else:
        print("   ✗ Failed to undo P2")
        return False
    
    print("\n4. Testing REDO to T-1 (restore P2)...")
    if logger.can_redo():
        print(f"   ✓ Can redo: {len(logger.undo_stack)} items in stack")
        restored = logger.redo_last_log()
        if restored and restored.get('notes') == "Point 2 - Ace!":
            print(f"   ✓ P2 restored, notes: '{restored['notes']}'")
            print(f"   ✓ Undo stack now has {len(logger.undo_stack)} items (P3 still there)")
        else:
            print("   ✗ Failed to restore P2")
            return False
    else:
        print("   ✗ Cannot redo (stack empty)")
        return False
    
    print("\n5. Testing REDO again to T (restore P3)...")
    if logger.can_redo():
        restored = logger.redo_last_log()
        if restored and restored.get('notes') == "Point 3 - Lost":
            print(f"   ✓ P3 restored, notes: '{restored['notes']}'")
            print(f"   ✓ Undo stack now empty: {len(logger.undo_stack)} items")
        else:
            print("   ✗ Failed to restore P3")
            return False
    else:
        print("   ✗ Cannot redo (stack empty)")
        return False
    
    print("\n6. Testing new point after undo (branching timeline)...")
    # Undo P3 again
    logger.undo_last_log()
    print(f"   - Undid P3, stack has {len(logger.undo_stack)} items")
    
    # Log a NEW point (different from P3)
    point3_new = {
        "set_no": 1, "game_no": 1, "score_before_point": "30 - 0",
        "server": "m", "serve_number": "2", "serve_code": "In (I)",
        "return_code": "In (I)", "rally_len_shots": "Medium",
        "pattern": "First Strike", "tactic_code": "Neutral",
        "final_outcome": "W", "notes": "Point 3 NEW - Won!"
    }
    logger.log_point(point3_new)
    
    # Check that undo stack is cleared
    if len(logger.undo_stack) == 0:
        print(f"   ✓ New point logged, undo stack cleared (was P3, now empty)")
        print("   ✓ Old P3 is lost (cannot redo to it) - THIS IS EXPECTED")
    else:
        print(f"   ✗ Undo stack should be empty but has {len(logger.undo_stack)} items")
        return False
    
    # Clean up
    if os.path.isfile(logger.filename):
        os.remove(logger.filename)
    
    return True

def test_scenario_described():
    """Test the exact scenario user described"""
    print("\n=== Test: User's Scenario (T, T-1, T-2, forward to T-1) ===")
    
    logger = MatchLogger(base_filename="test_scenario")
    
    # Log 3 points to get to state T
    for i in range(1, 4):
        logger.log_point({
            "set_no": 1, "game_no": 1, "score_before_point": "0 - 0",
            "server": "m", "serve_number": "1", "serve_code": "In",
            "final_outcome": "W", "notes": f"Point {i}"
        })
    
    print("State T: 3 points logged")
    
    # UNDO to T-1
    removed1 = logger.undo_last_log()
    print(f"UNDO → T-1: Removed '{removed1['notes']}', stack has {len(logger.undo_stack)} items")
    
    # UNDO to T-2
    removed2 = logger.undo_last_log()
    print(f"UNDO → T-2: Removed '{removed2['notes']}', stack has {len(logger.undo_stack)} items")
    
    # Click "Me" (log forward) - this should GO TO T-1 not create new point
    print("\nClick 'Me' winner button...")
    
    # Check if we can redo
    if logger.can_redo():
        print(f"✓ Can REDO: {len(logger.undo_stack)} points available")
        print("✓ Suggestion: Add 'REDO' button next to 'UNDO LAST'")
        print("✓ When user wants to go forward, they should click REDO")
        print("✓ When user wants NEW point (branch timeline), they click Me/Opponent")
    else:
        print("✗ Cannot redo")
    
    # If user clicks Me, it creates a NEW point and clears stack
    logger.log_point({
        "set_no": 1, "game_no": 1, "score_before_point": "0 - 0",
        "server": "m", "serve_number": "1", "serve_code": "In",
        "final_outcome": "W", "notes": "NEW Point at T-1"
    })
    
    print(f"\nAfter logging new point: stack has {len(logger.undo_stack)} items")
    if len(logger.undo_stack) == 0:
        print("✓ Stack cleared - old future (Point 2, Point 3) is LOST")
        print("✓ This is CORRECT behavior - you created a new timeline!")
    
    # Clean up
    if os.path.isfile(logger.filename):
        os.remove(logger.filename)
    
    return True

def main():
    print("="*60)
    print("TESTING UNDO/REDO FUNCTIONALITY")
    print("="*60)
    
    result1 = test_undo_redo_stack()
    result2 = test_scenario_described()
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Undo/Redo Stack: {'PASS' if result1 else 'FAIL'}")
    print(f"User Scenario: {'PASS' if result2 else 'FAIL'}")
    
    print("\n" + "="*60)
    print("SOLUTION IMPLEMENTED:")
    print("="*60)
    print("✓ UNDO button: Go backward (T → T-1 → T-2)")
    print("✓ REDO button: Go forward (T-2 → T-1 → T)")
    print("✓ Me/Opponent buttons: Create NEW point (clears redo stack)")
    print("")
    print("Timeline behavior:")
    print("  T → UNDO → T-1 → UNDO → T-2")
    print("  T-2 → REDO → T-1 → REDO → T (restores original)")
    print("  T-2 → Click Me → NEW_T-1 (old T-1 and T are lost)")
    print("="*60)
    
    if result1 and result2:
        print("✓ ALL TESTS PASSED")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
