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
        self.geometry("600x700") # Increased height to fit all options
        self.callback = callback
        
        # Make it modal-like
        self.attributes("-topmost", True)
        self.grab_set()
        
        self.grid_columnconfigure((0, 1, 2), weight=1)
        
        for i, option in enumerate(options):
            if isinstance(option, tuple):
                if len(option) == 3:
                    display_text, value, color = option
                elif len(option) == 2:
                    display_text, value = option
                    color = None
                else:
                    display_text = value = option[0]
                    color = None
            else:
                display_text, value = option, option
                color = None
                
            btn_kwargs = {
                "text": display_text,
                "command": lambda val=value: self.on_select(val),
                "width": 180,
                "height": 100,
                "font": ("Arial", 12, "bold")
            }
            if color:
                btn_kwargs["fg_color"] = color
                
            btn = ctk.CTkButton(self, **btn_kwargs)
            btn.grid(row=i//3, column=i%3, padx=10, pady=10)
            
    def on_select(self, option):
        self.callback(option)
        self.destroy()

class MultiSelectionPopup(ctk.CTkToplevel):
    def __init__(self, parent, title, options, callback, current_selection=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("800x700") # Increased size
        self.callback = callback
        self.options = options
        self.selected_values = set()
        
        # Parse current selection if string
        if current_selection and isinstance(current_selection, str):
            self.selected_values = set(current_selection.split("|"))
        
        self.attributes("-topmost", True)
        self.grab_set()
        
        self._init_ui()
        
    def _init_ui(self):
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=1) # Scrollable area
        
        # Scrollable frame for buttons
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        self.scroll_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.buttons = {}
        
        for i, option in enumerate(self.options):
            if isinstance(option, tuple):
                display_text, value = option
            else:
                display_text, value = option, option
            
            # Check if selected
            fg_color = "green" if value in self.selected_values else "blue"
            
            btn = ctk.CTkButton(self.scroll_frame, text=display_text, 
                                command=lambda v=value: self.toggle_selection(v),
                                width=220, height=60, font=("Arial", 12, "bold"), # Smaller height, wider
                                fg_color=fg_color)
            btn.grid(row=i//3, column=i%3, padx=10, pady=10)
            self.buttons[value] = btn

        # Done Button
        self.btn_done = ctk.CTkButton(self, text="DONE", command=self.finish, height=50, fg_color="darkgreen")
        self.btn_done.grid(row=1, column=0, columnspan=3, sticky="ew", padx=20, pady=20)

    def toggle_selection(self, value):
        if value in self.selected_values:
            self.selected_values.remove(value)
            self.buttons[value].configure(fg_color="blue")
        else:
            self.selected_values.add(value)
            self.buttons[value].configure(fg_color="green")

    def finish(self):
        # Sort for consistency
        sorted_vals = sorted(list(self.selected_values))
        result_str = "|".join(sorted_vals)
        self.callback(result_str)
        self.destroy()

class ScoreEditPopup(ctk.CTkToplevel):
    def __init__(self, parent, game_state, callback):
        super().__init__(parent)
        self.title("Edit Score")
        self.geometry("400x550")
        self.game_state = game_state
        self.callback = callback
        self.attributes("-topmost", True)
        self.grab_set()
        
        self._init_ui()
        
    def _init_ui(self):
        self.grid_columnconfigure(1, weight=1)
        


        # Sets
        ctk.CTkLabel(self, text="Sets (Server - Receiver)", font=("Arial", 14, "bold")).pack(pady=10)
        frame_sets = ctk.CTkFrame(self)
        frame_sets.pack(pady=5)
        self.entry_sets_s = ctk.CTkEntry(frame_sets, width=50)
        self.entry_sets_s.insert(0, str(self.game_state.sets_server))
        self.entry_sets_s.pack(side="left", padx=5)
        ctk.CTkLabel(frame_sets, text="-").pack(side="left")
        self.entry_sets_r = ctk.CTkEntry(frame_sets, width=50)
        self.entry_sets_r.insert(0, str(self.game_state.sets_receiver))
        self.entry_sets_r.pack(side="left", padx=5)

        # Games
        ctk.CTkLabel(self, text="Games (Server - Receiver)", font=("Arial", 14, "bold")).pack(pady=10)
        frame_games = ctk.CTkFrame(self)
        frame_games.pack(pady=5)
        self.entry_games_s = ctk.CTkEntry(frame_games, width=50)
        self.entry_games_s.insert(0, str(self.game_state.games_server))
        self.entry_games_s.pack(side="left", padx=5)
        ctk.CTkLabel(frame_games, text="-").pack(side="left")
        self.entry_games_r = ctk.CTkEntry(frame_games, width=50)
        self.entry_games_r.insert(0, str(self.game_state.games_receiver))
        self.entry_games_r.pack(side="left", padx=5)
        
        # Points
        frame_points_header = ctk.CTkFrame(self, fg_color="transparent")
        frame_points_header.pack(pady=(10, 0))
        ctk.CTkLabel(frame_points_header, text="Points (Server - Receiver)", font=("Arial", 14, "bold")).pack(side="left", padx=10)
        
        self.var_is_tiebreak = ctk.BooleanVar(value=self.game_state.is_tiebreak)
        self.chk_tiebreak = ctk.CTkCheckBox(frame_points_header, text="Tie Breaker Mode", variable=self.var_is_tiebreak, command=self._update_point_options)
        self.chk_tiebreak.pack(side="left", padx=10)
        frame_points = ctk.CTkFrame(self)
        frame_points.pack(pady=5)
        
        self.combo_points_s = ctk.CTkComboBox(frame_points, width=70)
        self.combo_points_s.pack(side="left", padx=5)
        
        ctk.CTkLabel(frame_points, text="-").pack(side="left")
        
        self.combo_points_r = ctk.CTkComboBox(frame_points, width=70)
        self.combo_points_r.pack(side="left", padx=5)

        # Initialize options
        self._update_point_options()
        
        # Set current values
        self.combo_points_s.set(self.game_state.get_score_string(self.game_state.points_server))
        self.combo_points_r.set(self.game_state.get_score_string(self.game_state.points_receiver))

        # Save
        ctk.CTkButton(self, text="Save & Update", command=self.save, fg_color="green").pack(pady=30)
    
    def _update_point_options(self):
        if self.var_is_tiebreak.get():
            options = [str(i) for i in range(21)] # 0 to 20
        else:
            options = ["0", "15", "30", "40", "AD"]
            
        self.combo_points_s.configure(values=options)
        self.combo_points_r.configure(values=options)

    def save(self):
        try:
            self.game_state.sets_server = int(self.entry_sets_s.get())
            self.game_state.sets_receiver = int(self.entry_sets_r.get())
            self.game_state.games_server = int(self.entry_games_s.get())
            self.game_state.games_receiver = int(self.entry_games_r.get())
            self.game_state.is_tiebreak = self.var_is_tiebreak.get()
            
            if self.game_state.is_tiebreak:
                # Direct integer conversion for tiebreak
                self.game_state.points_server = int(self.combo_points_s.get())
                self.game_state.points_receiver = int(self.combo_points_r.get())
            else:
                # Map points string back to int for standard scoring
                pmap = {"0": 0, "15": 1, "30": 2, "40": 3, "AD": 4}
                # Handle case where user switches from tiebreak (e.g. "5") back to standard
                # Default to 0 if not in map
                self.game_state.points_server = pmap.get(self.combo_points_s.get(), 0)
                self.game_state.points_receiver = pmap.get(self.combo_points_r.get(), 0)
            
            self.callback()
            self.destroy()
        except ValueError:
            pass # Ignore invalid input

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
        
        self.btn_edit_score = ctk.CTkButton(self.score_frame, text="Edit Score", command=self._open_score_edit, width=100, height=24, font=("Arial", 12))
        self.btn_edit_score.pack(pady=5)

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
        self.var_serve_code = ctk.StringVar(value="In (I) [6]")
        self.btn_serve_code = ctk.CTkButton(self.left_frame, textvariable=self.var_serve_code, 
                                            command=lambda: self._open_serve_code_popup(),
                                            height=40)
        self.btn_serve_code.pack(fill="x", pady=5)



        # Rally Length
        self.lbl_rally = ctk.CTkLabel(self.left_frame, text="Rally Length")
        self.lbl_rally.pack(anchor="w")
        self.var_rally = ctk.StringVar(value="Short")
        self.seg_rally = ctk.CTkSegmentedButton(self.left_frame, values=["Short", "Medium", "Long"], variable=self.var_rally)
        self.seg_rally.pack(fill="x", pady=5)

        # Point Type & Tactic (merged)
        self.lbl_pattern = ctk.CTkLabel(self.left_frame, text="Point Type & Tactic")
        self.lbl_pattern.pack(anchor="w")
        self.var_pattern = ctk.StringVar(value="Rally (R) [18]")
        
        # Merged options - removed duplicates and combined similar tactics
        point_type_options = [
            ("Rally (R)\nBaseline exchange", "Rally (R)"),
            ("Serve + 1 (S1)\nServe then attack", "Serve + 1 (S1)"),
            ("Return + 1 (R1)\nReturn then attack", "Return + 1 (R1)"),
            ("First Strike (F)\nShort point < 4 shots", "First Strike (F)"),
            ("Approach (A)\nTransition to net", "Approach (A)"),
            ("Net Play (N)\nVolleys & Overheads", "Net Play (N)"),
            ("Passing Shot (P)\nPass net player", "Passing Shot (P)"),
            ("Lob/Deep Ball (L)\nHigh or deep shot", "Lob/Deep Ball (L)"),
            ("Defense (D)\nScrambling", "Defense (D)"),
            ("Move Opponent (M)\nAngles / Change Dir / Run", "Move Opponent (M)"),
            ("Consistency (C)\nHigh % shot", "Consistency (C)"),
            ("Body (B)\nJam the opponent", "Body (B)"),
            ("Pace (PC)\nOverwhelm with speed", "Pace (PC)"),
            ("Serve & Volley (SV)\nServe -> Net", "Serve & Volley (SV)"),
            ("Chip & Charge (CC)\nSlice return -> Net", "Chip & Charge (CC)"),
            ("Drop Shot (DS)\nDraw them in", "Drop Shot (DS)"),
            ("Backhand Slice (BS)\nSlice defense/neutral", "Backhand Slice (BS)"),
            ("Inside-Out (IO)\nRun around BH", "Inside-Out (IO)")
        ]
        
        self.btn_pattern = ctk.CTkButton(self.left_frame, textvariable=self.var_pattern,
                                         command=lambda: self._open_multi_popup("Point Type & Tactic", point_type_options, self.var_pattern),
                                         height=40)
        self.btn_pattern.pack(fill="x", pady=5)

        # --- Outcome Controls (Right Column) ---
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.lbl_outcome = ctk.CTkLabel(self.right_frame, text="Point Outcome", font=("Arial", 20))
        self.lbl_outcome.pack(pady=10)


        # How?
        self.lbl_how = ctk.CTkLabel(self.right_frame, text="How?")
        self.lbl_how.pack(anchor="w")
        self.var_how = ctk.StringVar(value="Forehand Winner (FW) [15]")
        how_options = [
            # Errors first (yellow background)
            ("Forced Error (FE)", "Forced Error (FE)", "#DAA520"),
            ("Unforced Error (UE)", "Unforced Error (UE)", "#DAA520"),
            ("Double Fault (DF)", "Double Fault (DF)", "#DAA520"),
            # Winners (alphabetical, default blue)
            "Ace (A)", 
            "Backhand Winner (BW)", 
            "Cross Court Winner (CC)",
            "Down the Line Winner (DTL)",
            "Drop Shot Winner (DW)", 
            "Forehand Winner (FW)", 
            "Lob Winner (LW)",
            "Overhead Winner (OW)", 
            "Passing Shot Winner (PW)", 
            "Service Winner (SW)", 
            "Unknown (UNK)",
            "Volley Winner (VW)"
        ]
        
        self.btn_how = ctk.CTkButton(self.right_frame, textvariable=self.var_how,
                                     command=lambda: self._open_popup("How?", how_options, self.var_how),
                                     height=40)
        self.btn_how.pack(fill="x", pady=5)

        # Notes
        self.lbl_notes = ctk.CTkLabel(self.right_frame, text="Notes")
        self.lbl_notes.pack(anchor="w")
        self.entry_notes = ctk.CTkEntry(self.right_frame, placeholder_text="How opponent defeated me...")
        self.entry_notes.pack(fill="x", pady=5)



        # Who Won? (Moved to bottom - clicking auto-logs the point)
        self.lbl_winner = ctk.CTkLabel(self.right_frame, text="Winner (Click to Log Point)", font=("Arial", 14, "bold"))
        self.lbl_winner.pack(anchor="w", pady=(20, 0))
        self.var_winner = ctk.StringVar(value="Me")
        self.seg_winner = ctk.CTkSegmentedButton(self.right_frame, values=["Me", "Opponent", "Unknown"], 
                                                  variable=self.var_winner, command=self._on_winner_selected,
                                                  selected_color="green", selected_hover_color="darkgreen")
        self.seg_winner.pack(fill="x", pady=5)

        # Undo Button
        self.btn_undo = ctk.CTkButton(self.right_frame, text="UNDO LAST", command=self.undo_point, fg_color="red")
        self.btn_undo.pack(fill="x", pady=5)

    def _open_popup(self, title, options, string_var):
        def callback_with_count(val):
            # Add count to the selected value
            string_var.set(f"{val} [{len(options)}]")
        SelectionPopup(self, title, options, callback_with_count)

    def _open_serve_code_popup(self):
        """Special popup for serve code that auto-logs on Ace or Winner"""
        # Reordered: regular serves first, then point-ending serves at bottom
        serve_options = ["In (I)", "Fault (SF)", "Double Fault (DF)", "Wide (WB)", "Ace (A)", "Winner (W)"]
        
        def callback_with_auto_log(val):
            # Add count to the selected value
            self.var_serve_code.set(f"{val} [6]")
            # Auto-log if Ace or Winner
            if val in ["Ace (A)", "Winner (W)"]:
                self.log_point()
        
        SelectionPopup(self, "Serve Code", serve_options, callback_with_auto_log)

    def _open_multi_popup(self, title, options, string_var):
        def callback_with_count(val):
            # Add count to the selected value (could be multi-value with |)
            if val:
                string_var.set(f"{val} [{len(options)}]")
            else:
                # If nothing selected, use the first option with count
                first_val = options[0][1] if isinstance(options[0], tuple) else options[0]
                string_var.set(f"{first_val} [{len(options)}]")
        # Remove count from current selection before passing to popup
        current = string_var.get()
        if ' [' in current:
            current = current[:current.rfind(' [')]
        MultiSelectionPopup(self, title, options, callback_with_count, current_selection=current)

    def _open_score_edit(self):
        ScoreEditPopup(self, self.game_state, self._update_score_display)

    def _on_winner_selected(self, value):
        """Called when a winner is selected - automatically logs the point"""
        # The value parameter is passed by CTkSegmentedButton when selection changes
        self.log_point()

    def _update_score_display(self):
        self.lbl_score.configure(text=self.game_state.get_display_score())
        self.lbl_games.configure(text=f"Games: {self.game_state.games_server} - {self.game_state.games_receiver} | Sets: {self.game_state.sets_server} - {self.game_state.sets_receiver}")

    def log_point(self):
        # Gather data
        server_val = "n" if "Me" in self.var_server.get() else "o"
        winner_val = self.var_winner.get()
        
        winner_is_me = winner_val == "Me"
        winner_is_unknown = winner_val == "Unknown"
        
        # Determine outcome code
        if winner_is_unknown:
            outcome_code = "PtUnknown"
        else:
            outcome_code = "PtWon" if winner_is_me else "PtLost"
            
        # Append 'How' details
        how = self.var_how.get()
        if "Winner" in how: outcome_code += "|W"
        elif "Unforced" in how: outcome_code += "|UE"
        elif "Forced" in how: outcome_code += "|FE"
        elif "Unknown" in how: outcome_code += "|UNK"
        
        data = {
            "set_no": self.game_state.current_set,
            "game_no": self.game_state.games_server + self.game_state.games_receiver + 1,
            "score_before_point": self.game_state.get_display_score(),
            "server": server_val,
            "serve_number": self.var_serve_num.get(),
            "serve_code": self.var_serve_code.get(),
            "return_code": "N/A",  # Return code field removed from UI
            "rally_len_shots": self.var_rally.get(),
            "pattern": self.var_pattern.get(),
            "tactic_code": self.var_pattern.get(),  # Same as pattern now (merged)
            "final_shot_type": "N/A",  # Final shot type field removed from UI
            "final_outcome": outcome_code,
            "notes": self.entry_notes.get(),
        }

        # Log to CSV
        self.logger.log_point(data)

        # Update Game State ONLY if winner is known
        if not winner_is_unknown:
            # Determine if server or receiver won
            # If server is Me (n) and Me won -> server won
            # If server is Opponent (o) and Opponent won -> server won
            # Otherwise receiver won
            server_won = (server_val == "n" and winner_is_me) or (server_val == "o" and not winner_is_me)
            self.game_state.add_point('server' if server_won else 'receiver')
            self._update_score_display()
        
        # Reset some fields for next point
        self.var_rally.set("Short")
        self.var_serve_num.set("1") # Reset to 1st serve usually
        self.entry_notes.delete(0, 'end') # Clear notes

    def undo_point(self):
        self.game_state.undo()
        self._update_score_display()
