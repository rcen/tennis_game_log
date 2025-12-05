# Undo/Redo Implementation & Database Considerations

## Problem Statement

**Issue Identified:**
- Current state T has points: P1, P2, P3
- User clicks UNDO → removes P3, shows P2 (state T-1)
- User clicks UNDO again → removes P2, shows P1 (state T-2)
- User clicks "Me" → logs NEW point P2' **BUT original P2 and P3 are lost forever**

## Solution Implemented: In-Memory Undo/Redo Stack

### How It Works

1. **UNDO Stack**: When you undo a point, it's removed from CSV but saved in memory
2. **REDO Button**: New button that restores points from the undo stack
3. **Timeline Branching**: When you log a NEW point, the undo stack is cleared (you create a new timeline)

### User Workflow

```
Current State (T): [P1, P2, P3]
         ↓ Click UNDO
State T-1: [P1, P2]    (P3 in undo stack)
         ↓ Click UNDO
State T-2: [P1]        (P2, P3 in undo stack)

NOW YOU HAVE TWO CHOICES:

Option A: REDO (restore old timeline)
    ↓ Click REDO
State T-1: [P1, P2]    (P3 still in undo stack)
    ↓ Click REDO
State T: [P1, P2, P3]  (back to original)

Option B: NEW POINT (create new timeline)
    ↓ Click "Me" or "Opponent"
State T-1': [P1, P2']  (P2 and P3 LOST, undo stack cleared)
```

### GUI Changes

**Before:**
```
[UNDO LAST]  (single button)
```

**After:**
```
[UNDO LAST]  [REDO]  (two buttons side by side)
```

- **UNDO LAST**: Navigate backward through history
- **REDO**: Navigate forward through previously undone points
- **Me/Opponent/Unknown**: Log a NEW point (starts fresh timeline)

## Indexing Strategy

### Current Approach: Point ID
```
point_id = timestamp (YYYYMMDDHHMMSSffffff)
Example: 20251205163732123456
```

**Pros:**
- ✓ Globally unique
- ✓ Sortable chronologically
- ✓ No conflicts across days/sessions

**Cons:**
- ✗ Not sequential (if you undo/redo, IDs are out of order)
- ✗ Hard to reference ("point 12" vs "point 20251205163732123456")

### Alternative: Sequential Index
If you want easier referencing, we could add a `point_number` column:
```
point_number,point_id,timestamp,...
1,20251205163732123456,2025-12-05 16:37:32,...
2,20251205163745789012,2025-12-05 16:37:45,...
3,20251205163801234567,2025-12-05 16:38:01,...
```

**Implementation consideration:** Point numbers would need to be per-session or per-day.

## Database Question: SQLite vs CSV

### Current: CSV Files
```
✓ Simple, human-readable
✓ Easy to open in Excel/Google Sheets
✓ No dependencies
✓ Works perfectly for your use case
✗ Slow for large datasets (360+ rows is still fine)
✗ No complex queries
✗ Undo/redo requires reading entire file
```

### Alternative: SQLite Database

**When to switch to SQLite:**

1. **You have LOTS of undo/redo operations** (current solution handles this fine)
2. **You want complex analytics** (e.g., "Show all serves where I was down 0-30")
3. **You have 10,000+ points** (CSV gets slow)
4. **You want full transaction history** (every edit, not just current state)

**SQLite Implementation:**
```sql
-- Main points table
CREATE TABLE points (
    point_id TEXT PRIMARY KEY,
    timestamp DATETIME,
    set_no INTEGER,
    game_no INTEGER,
    -- ... all other columns ...
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL  -- Soft delete for undo/redo
);

-- History table for full audit trail
CREATE TABLE point_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    point_id TEXT,
    action TEXT,  -- 'INSERT', 'UPDATE', 'DELETE', 'UNDO', 'REDO'
    timestamp DATETIME,
    data TEXT  -- JSON snapshot
);
```

### Recommendation: **STICK WITH CSV FOR NOW**

**Why CSV is sufficient:**
1. ✓ Your undo/redo stack (in-memory) handles navigation perfectly
2. ✓ 300-400 points per session is small (CSV handles thousands efficiently)
3. ✓ Daily files keep individual files manageable
4. ✓ You can analyze in Excel/Jupyter without extra tools
5. ✓ Simple backup (just copy files)

**When to switch to SQLite:**
- You're doing 50+ undo/redo operations per session
- You want to query across multiple sessions/days
- You need advanced analytics (aggregations, joins)
- You have 10,000+ total points across all sessions

## Technical Implementation Details

### Files Modified

**tennis_logger/logger.py:**
- Added `self.undo_stack` to store undone points
- Modified `log_point()` to clear undo stack on new points
- Modified `undo_last_log()` to push removed points to stack
- Added `redo_last_log()` to restore from stack
- Added `can_redo()` to check if redo is possible

**tennis_logger/gui.py:**
- Added REDO button next to UNDO button
- Added `redo_point()` method to handle redo clicks
- Both undo and redo restore full UI state (notes, serve code, etc.)

### Stack Behavior

```python
# Initially empty
undo_stack = []

# After UNDO P3
undo_stack = [P3]

# After UNDO P2
undo_stack = [P3, P2]  # Stack grows (LIFO)

# After REDO
undo_stack = [P3]  # P2 popped and re-logged

# After NEW point
undo_stack = []  # Cleared! Old future lost
```

## Testing Results

✅ **All tests passed:**
- Undo removes point and stores in stack
- Redo restores point from stack
- Multiple undo/redo operations work correctly
- New point clears undo stack (timeline branching)
- UI fields restore correctly on both undo and redo

## Future Enhancements (Optional)

If you find you need more sophisticated history management:

1. **Persistent Undo Stack**: Save undo stack to a file so it survives app restart
2. **Undo History Limit**: Keep only last N undos to save memory
3. **Visual Timeline**: Show a tree of undo/redo states
4. **SQLite Migration**: If you need complex queries or 10,000+ points

---

**Current Status:** ✅ **Fully Implemented & Tested**

The in-memory undo/redo stack is the right solution for your use case. It's simple, fast, and doesn't require a database. You can undo/redo as much as you want within a session, and the CSV files remain clean and human-readable.
