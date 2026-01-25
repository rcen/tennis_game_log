import os
import time

files = ["verify_ui.py", "debug_ctk.py", "debug_tk.py"]

for f in files:
    try:
        if os.path.exists(f):
            os.remove(f)
            print(f"Removed {f}")
        else:
            print(f"{f} not found")
    except Exception as e:
        print(f"Error removing {f}: {e}")
