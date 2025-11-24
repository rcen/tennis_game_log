import customtkinter as ctk
from .game_state import GameState
from .logger import MatchLogger

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class SelectionPopup(ctk.CTkToplevel):
    def __init__(self, parent, title, options, callback):
        super().__init__(parent)
        self.title(title)
        # Center the window roughly
        self.geometry("500x400")
        self.callback = callback
        
        # Make it modal-like
        self.attributes("-topmost", True)
        self.grab_set()
        
        self.grid_columnconfigure((0, 1, 2), weight=1)
        
        for i, option in enumerate(options):
            btn = ctk.CTkButton(self, text=option, command=lambda opt=option: self.on_select(opt),
                                width=120, height=80, font=("Arial", 14, "bold"))
            btn.grid(row=i//3, column=i%3, padx=10, pady=10)
            
    def on_select(self, option):
        self.callback(option)
        self.destroy()


class TennisLoggerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tennis Game Logger")
        self.geometry("1000x800")

        self.game_state = GameState()
        self.logger = MatchLogger()

        self._init_ui()
        self._update_score_display()

    def _init_ui(self):
        # Main Layout: 2 Columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0) # Scoreboard
        self.grid_rowconfigure(1, weight=1) # Controls

        # --- Scoreboard ---
        self.score_frame = ctk.CTkFrame(self)
        self.score_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        self.lbl_score = ctk.CTkLabel(self.score_frame, text="0 - 0", font=("Arial", 40, "bold"))
        self.lbl_score.pack(pady=20)
        
        self.lbl_games = ctk.CTkLabel(self.score_frame, text="Games: 0 - 0 | Sets: 0 - 0", font=("Arial", 16))
        self.lbl_games.pack(pady=5)

        # --- Input Controls (Left Column) ---
        self.left_frame = ctk.CTkScrollableFrame(self, label_text="Point Details")
        self.left_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Server
        self.lbl_server = ctk.CTkLabel(self.left_frame, text="Server")
        self.lbl_server.pack(anchor="w")
        self.var_server = ctk.StringVar(value="n")
        self.seg_server = ctk.CTkSegmentedButton(self.left_frame, values=["Me (n)", "Opponent (o)"], variable=self.var_server)
        self.seg_server.pack(fill="x", pady=5)

        # Serve Number
        self.lbl_serve_num = ctk.CTkLabel(self.left_frame, text="Serve Number")
        self.lbl_serve_num.pack(anchor="w")
        self.var_serve_num = ctk.StringVar(value="1")
        self.seg_serve_num = ctk.CTkSegmentedButton(self.left_frame, values=["1", "2"], variable=self.var_serve_num)
        self.seg_serve_num.pack(fill="x", pady=5)

        # Serve Code
        self.lbl_serve_code = ctk.CTkLabel(self.left_frame, text="Serve Code")
        self.lbl_serve_code.pack(anchor="w")
        self.var_serve_code = ctk.StringVar(value="IN")
        self.btn_serve_code = ctk.CTkButton(self.left_frame, textvariable=self.var_serve_code, 
                                            command=lambda: self._open_popup("Serve Code", ["IN", "A", "W", "SF", "DF", "WB"], self.var_serve_code))
        self.btn_serve_code.pack(fill="x", pady=5)

        # Return Code
        self.lbl_return_code = ctk.CTkLabel(self.left_frame, text="Return Code")
        self.lbl_return_code.pack(anchor="w")
        self.var_return_code = ctk.StringVar(value="IN")
        self.btn_return_code = ctk.CTkButton(self.left_frame, textvariable=self.var_return_code,
                                             command=lambda: self._open_popup("Return Code", ["IN", "NET", "LONG", "WIDE", "UE", "FE"], self.var_return_code))
        self.btn_return_code.pack(fill="x", pady=5)

        # Rally Length
        self.lbl_rally = ctk.CTkLabel(self.left_frame, text="Rally Length")
        self.lbl_rally.pack(anchor="w")
        self.entry_rally = ctk.CTkEntry(self.left_frame, placeholder_text="0")
        self.entry_rally.pack(fill="x", pady=5)

        # Pattern
        self.lbl_pattern = ctk.CTkLabel(self.left_frame, text="Pattern")
        self.lbl_pattern.pack(anchor="w")
        self.var_pattern = ctk.StringVar(value="RALLY")
        self.btn_pattern = ctk.CTkButton(self.left_frame, textvariable=self.var_pattern,
                                         command=lambda: self._open_popup("Pattern", ["RALLY", "FIRST", "APPROACH", "NET", "LOB_DEF", "MOON_BALL"], self.var_pattern))
        self.btn_pattern.pack(fill="x", pady=5)

        # Tactic
        self.lbl_tactic = ctk.CTkLabel(self.left_frame, text="Tactic")
        self.lbl_tactic.pack(anchor="w")
        self.var_tactic = ctk.StringVar(value="NEUTRAL")
        self.btn_tactic = ctk.CTkButton(self.left_frame, textvariable=self.var_tactic,
                                        command=lambda: self._open_popup("Tactic", ["NEUTRAL", "MOVE_OP", "DEPTH", "CHANGE_DIR", "TO_WEAK_WING", "BODY", "PACE"], self.var_tactic))
        self.btn_tactic.pack(fill="x", pady=5)

        # --- Outcome Controls (Right Column) ---
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.lbl_outcome = ctk.CTkLabel(self.right_frame, text="Point Outcome", font=("Arial", 20))
        self.lbl_outcome.pack(pady=10)

        # Who Won?
        self.lbl_winner = ctk.CTkLabel(self.right_frame, text="Winner")
        self.lbl_winner.pack(anchor="w")
        self.var_winner = ctk.StringVar(value="Me")
        self.seg_winner = ctk.CTkSegmentedButton(self.right_frame, values=["Me", "Opponent"], variable=self.var_winner)
        self.seg_winner.pack(fill="x", pady=5)

        # How?
        self.lbl_how = ctk.CTkLabel(self.right_frame, text="How?")
        self.lbl_how.pack(anchor="w")
        self.var_how = ctk.StringVar(value="Winner (W)")
        self.btn_how = ctk.CTkButton(self.right_frame, textvariable=self.var_how,
                                     command=lambda: self._open_popup("How?", ["Winner (W)", "Forced Error (FE)", "Unforced Error (UE)", "Double Fault (DF)"], self.var_how))
        self.btn_how.pack(fill="x", pady=5)

        # Final Shot
        self.lbl_final_shot = ctk.CTkLabel(self.right_frame, text="Final Shot Type")
        self.lbl_final_shot.pack(anchor="w")
        self.var_final_shot = ctk.StringVar(value="F")
        self.btn_final_shot = ctk.CTkButton(self.right_frame, textvariable=self.var_final_shot,
                                            command=lambda: self._open_popup("Final Shot Type", ["F", "B", "V", "O", "D", "L", "SLICE"], self.var_final_shot))
        self.btn_final_shot.pack(fill="x", pady=5)

        # Save Button
        self.btn_save = ctk.CTkButton(self.right_frame, text="LOG POINT", command=self.log_point, height=50, fg_color="green")
        self.btn_save.pack(fill="x", pady=20)

        # Undo Button
        self.btn_undo = ctk.CTkButton(self.right_frame, text="UNDO LAST", command=self.undo_point, fg_color="red")
        self.btn_undo.pack(fill="x", pady=5)

    def _open_popup(self, title, options, string_var):
        SelectionPopup(self, title, options, lambda val: string_var.set(val))


    def _update_score_display(self):
        self.lbl_score.configure(text=self.game_state.get_display_score())
        self.lbl_games.configure(text=f"Games: {self.game_state.games_server} - {self.game_state.games_receiver} | Sets: {self.game_state.sets_server} - {self.game_state.sets_receiver}")

    def log_point(self):
        # Gather data
        server_val = "n" if "Me" in self.var_server.get() else "o"
        winner_is_me = self.var_winner.get() == "Me"
        winner_code = "server" if (server_val == "n" and winner_is_me) or (server_val == "o" and not winner_is_me) else "receiver"
        
        # Construct final_outcome string
        how = self.var_how.get()
        outcome_code = "PtWon" if winner_is_me else "PtLost" # Simplified, user can adjust logic
        if "Winner" in how: outcome_code += "|W"
        elif "Unforced" in how: outcome_code += "|UE"
        elif "Forced" in how: outcome_code += "|FE"
        
        data = {
            "set_no": self.game_state.current_set,
            "game_no": self.game_state.games_server + self.game_state.games_receiver + 1,
            "score_before_point": self.game_state.get_display_score(),
            "server": server_val,
            "serve_number": self.var_serve_num.get(),
            "serve_code": self.var_serve_code.get(),
            "return_code": self.var_return_code.get(),
            "rally_len_shots": self.entry_rally.get(),
            "pattern": self.var_pattern.get(),
            "tactic_code": self.var_tactic.get(),
            "final_shot_type": self.var_final_shot.get(),
            "final_outcome": outcome_code,
        }


        # Log to CSV
        self.logger.log_point(data)

        # Update Game State
        self.game_state.add_point('server' if winner_code == 'server' else 'receiver')
        self._update_score_display()
        
        # Reset some fields for next point
        self.entry_rally.delete(0, 'end')
        self.var_serve_num.set("1") # Reset to 1st serve usually

    def undo_point(self):
        self.game_state.undo()
        self._update_score_display()
