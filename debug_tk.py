import tkinter as tk
import sys

print("Starting TK debug script...")
try:
    root = tk.Tk()
    root.title("TK Debug Window")
    root.geometry("300x200")
    label = tk.Label(root, text="If you see this, TK works!")
    label.pack(pady=20)
    print("Window created, entering mainloop...")
    root.mainloop()
    print("Mainloop exited.")
except Exception as e:
    print(f"Error: {e}")
