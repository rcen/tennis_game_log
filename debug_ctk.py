import customtkinter as ctk
import sys

print("Starting debug script...")
try:
    app = ctk.CTk()
    app.title("Debug Window")
    app.geometry("300x200")
    label = ctk.CTkLabel(app, text="If you see this, CTK works!")
    label.pack(pady=20)
    print("Window created, entering mainloop...")
    app.mainloop()
    print("Mainloop exited.")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
