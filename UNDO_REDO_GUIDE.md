# Quick Guide: Using UNDO and REDO

## The Buttons

```
┌─────────────────────────────────────────┐
│  [Me]  [Unknown]  [Opponent]           │  ← Log NEW points
│                                          │
│  [UNDO LAST]  [REDO]                    │  ← Navigate history
└─────────────────────────────────────────┘
```

## When to Use Each Button

### LOG NEW POINTS: Me / Unknown / Opponent
✓ Use when: You want to log what just happened
⚠️ Warning: This CLEARS any points you've undone

**Example:**
```
You have: [P1, P2, P3]
Click UNDO twice → [P1] (P2, P3 saved)
Click "Me" → [P1, P4] (P2, P3 LOST forever!)
```

### NAVIGATE BACKWARD: UNDO LAST
✓ Use when: You made a mistake or want to review previous points
✓ Safe: Points are saved, you can REDO back to them

**Example:**
```
You have: [P1, P2, P3]
Click UNDO → [P1, P2] (can redo P3)
Click UNDO → [P1] (can redo P2, P3)
```

### NAVIGATE FORWARD: REDO
✓ Use when: You undid too many points and want to restore them
✓ Restores: The exact point data (notes, serve code, everything)

**Example:**
```
After UNDO twice: [P1] (can redo P2, P3)
Click REDO → [P1, P2] (can still redo P3)
Click REDO → [P1, P2, P3] (back to original!)
```

## Common Scenarios

### Scenario 1: Made a Mistake (Simple Fix)
```
1. Log point with wrong winner
2. Click UNDO LAST
3. UI shows previous point's data
4. Click correct winner (Me or Opponent)
   → Creates NEW point, old one is replaced
```

### Scenario 2: Want to Review Previous Points
```
1. Playing, at point 10
2. Click UNDO several times to review points 9, 8, 7...
3. Click REDO several times to get back to point 10
   → No data lost!
```

### Scenario 3: Accidentally Undid Too Much
```
1. At point 10, clicked UNDO 3 times
2. Now at point 7, but you didn't mean to!
3. Click REDO 3 times
4. Back at point 10
   → Everything restored!
```

### Scenario 4: Want to Re-record a Sequence
```
1. At point 10, you realize points 8-10 were wrong
2. Click UNDO 3 times → back to point 7
3. Click "Me" or "Opponent" to log NEW point 8
   → Old points 8-10 are now GONE (new timeline)
4. Continue logging points 9, 10 with correct data
```

## Visual Timeline Example

```
INITIAL STATE
═══════════════════════════════════════
[P1] [P2] [P3] [P4] [P5]  ← Current: P5
                      ↑
                   You are here


AFTER UNDO, UNDO, UNDO
═══════════════════════════════════════
[P1] [P2] (P3) (P4) (P5)  ← Current: P2
      ↑     └─────────┘
   You are  In undo stack
    here    (can REDO)


OPTION A: Click REDO
═══════════════════════════════════════
[P1] [P2] [P3] (P4) (P5)  ← Current: P3
            ↑   └────┘
         You are  Can still
          here    REDO more


OPTION B: Click "Me" (NEW point)
═══════════════════════════════════════
[P1] [P2] [P3'] [P4'] [P5']  ← New timeline!
            ↑
         New P3
         (old P3, P4, P5 LOST)
```

## Pro Tips

1. **UNDO is safe**: You can always REDO back
2. **NEW POINT is destructive**: Clears undo stack
3. **Review without risk**: Use UNDO/REDO to browse history
4. **Think before logging**: Once you click Me/Opponent after UNDO, old points are gone

## Button Color Guide

- 🟢 **Green (Me/Opponent)**: Logs new point
- 🟠 **Orange (REDO)**: Restores undone point
- 🔴 **Red (UNDO)**: Removes last point (saved for redo)

---

**Remember:** 
- UNDO/REDO = Navigate (safe, reversible)
- Me/Opponent = Create new (clears redo stack)
