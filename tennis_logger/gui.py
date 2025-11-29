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
        ctk.CTkLabel(self, text="Sets (Me - Opponent)", font=("Arial", 14, "bold")).pack(pady=10)
        frame_sets = ctk.CTkFrame(self)
        frame_sets.pack(pady=5)
        self.entry_sets_me = ctk.CTkEntry(frame_sets, width=50)
        self.entry_sets_me.insert(0, str(self.game_state.sets_me))
        self.entry_sets_me.pack(side="left", padx=5)
        ctk.CTkLabel(frame_sets, text="-").pack(side="left")
        self.entry_sets_opp = ctk.CTkEntry(frame_sets, width=50)
        self.entry_sets_opp.insert(0, str(self.game_state.sets_opponent))
        self.entry_sets_opp.pack(side="left", padx=5)

        # Games
        ctk.CTkLabel(self, text="Games (Me - Opponent)", font=("Arial", 14, "bold")).pack(pady=10)
        frame_games = ctk.CTkFrame(self)
        frame_games.pack(pady=5)
        self.entry_games_me = ctk.CTkEntry(frame_games, width=50)
        self.entry_games_me.insert(0, str(self.game_state.games_me))
        self.entry_games_me.pack(side="left", padx=5)
        ctk.CTkLabel(frame_games, text="-").pack(side="left")
        self.entry_games_opp = ctk.CTkEntry(frame_games, width=50)
        self.entry_games_opp.insert(0, str(self.game_state.games_opponent))
        self.entry_games_opp.pack(side="left", padx=5)
        
        # Points
        frame_points_header = ctk.CTkFrame(self, fg_color="transparent")
        frame_points_header.pack(pady=(10, 0))
        ctk.CTkLabel(frame_points_header, text="Points (Me - Opponent)", font=("Arial", 14, "bold")).pack(side="left", padx=10)
        
        self.var_is_tiebreak = ctk.BooleanVar(value=self.game_state.is_tiebreak)
        self.chk_tiebreak = ctk.CTkCheckBox(frame_points_header, text="Tie Breaker Mode", variable=self.var_is_tiebreak, command=self._update_point_options)
        self.chk_tiebreak.pack(side="left", padx=10)
        
        frame_points = ctk.CTkFrame(self)
        frame_points.pack(pady=5)
        
        self.combo_points_me = ctk.CTkComboBox(frame_points, width=70)
        self.combo_points_me.pack(side="left", padx=5)
        
        ctk.CTkLabel(frame_points, text="-").pack(side="left")
        
        self.combo_points_opp = ctk.CTkComboBox(frame_points, width=70)
        self.combo_points_opp.pack(side="left", padx=5)

        # Initialize options
        self._update_point_options()
        
        # Set current values
        self.combo_points_me.set(self.game_state.get_score_string(self.game_state.points_me))
        self.combo_points_opp.set(self.game_state.get_score_string(self.game_state.points_opponent))

        # Save
        ctk.CTkButton(self, text="Save & Update", command=self.save, fg_color="green").pack(pady=30)
    
    def _update_point_options(self):
        if self.var_is_tiebreak.get():
            options = [str(i) for i in range(21)] # 0 to 20
        else:
            options = ["0", "15", "30", "40", "AD"]
            
        self.combo_points_me.configure(values=options)
        self.combo_points_opp.configure(values=options)

    def save(self):
        try:
            self.game_state.sets_me = int(self.entry_sets_me.get())
            self.game_state.sets_opponent = int(self.entry_sets_opp.get())
            self.game_state.games_me = int(self.entry_games_me.get())
            self.game_state.games_opponent = int(self.entry_games_opp.get())
            self.game_state.is_tiebreak = self.var_is_tiebreak.get()
            
            if self.game_state.is_tiebreak:
                # Direct integer conversion for tiebreak
                self.game_state.points_me = int(self.combo_points_me.get())
                self.game_state.points_opponent = int(self.combo_points_opp.get())
            else:
                # Map points string back to int for standard scoring
                pmap = {"0": 0, "15": 1, "30": 2, "40": 3, "AD": 4}
                self.game_state.points_me = pmap.get(self.combo_points_me.get(), 0)
                self.game_state.points_opponent = pmap.get(self.combo_points_opp.get(), 0)
            
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
        # Main Layout: Left (Input), Right (Outcome/Log), Top (Score)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top Score Frame
        self.top_frame = ctk.CTkFrame(self, height=100)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        self.lbl_score = ctk.CTkLabel(self.top_frame, text="Score (Me - Opponent): 0 - 0", font=("Arial", 24, "bold"))
        self.lbl_score.pack(pady=10)
        
        self.lbl_games = ctk.CTkLabel(self.top_frame, text="Games: 0 - 0 | Sets: 0 - 0", font=("Arial", 16))
        self.lbl_games.pack(pady=5)
        
        self.btn_edit_score = ctk.CTkButton(self.top_frame, text="Edit Score", command=self._open_score_edit, width=100)
        self.btn_edit_score.pack(pady=5)

        # Left Frame - Point Details
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.left_frame, text="Point Details", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Server
        self.lbl_server = ctk.CTkLabel(self.left_frame, text="Server")
        self.lbl_server.pack(anchor="w")
        self.var_server = ctk.StringVar(value="Me")
        self.seg_server = ctk.CTkSegmentedButton(self.left_frame, values=["Me", "Opponent"], variable=self.var_server)
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


        # Right Frame - Outcome & Log
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.right_frame, text="Point Outcome", font=("Arial", 16, "bold")).pack(pady=10)

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
        
        self.var_winner = ctk.StringVar(value="Me") # Keep variable for log_point logic
        
        frame_winner_btns = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        frame_winner_btns.pack(fill="x", pady=5)
        
        self.btn_win_me = ctk.CTkButton(frame_winner_btns, text="Me", 
                                        command=lambda: self._on_winner_click("Me"),
                                        fg_color="green", hover_color="darkgreen", width=80)
        self.btn_win_me.pack(side="left", padx=2, expand=True, fill="x")
        
        self.btn_win_unk = ctk.CTkButton(frame_winner_btns, text="Unknown", 
                                         command=lambda: self._on_winner_click("Unknown"),
                                         fg_color="gray", hover_color="darkgray", width=80)
        self.btn_win_unk.pack(side="left", padx=2, expand=True, fill="x")

        self.btn_win_opp = ctk.CTkButton(frame_winner_btns, text="Opponent", 
                                         command=lambda: self._on_winner_click("Opponent"),
                                         fg_color="green", hover_color="darkgreen", width=80)
        self.btn_win_opp.pack(side="left", padx=2, expand=True, fill="x")

        # Undo Button
        self.btn_undo = ctk.CTkButton(self.right_frame, text="UNDO LAST", command=self.undo_point, fg_color="red", hover_color="darkred")
        self.btn_undo.pack(side="bottom", fill="x", pady=20)

    def _open_popup(self, title, options, variable):
        SelectionPopup(self, title, options, lambda val: variable.set(val))
        
    def _open_multi_popup(self, title, options, variable):
        MultiSelectionPopup(self, title, options, lambda val: variable.set(val))

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

    def _open_score_edit(self):
        ScoreEditPopup(self, self.game_state, self._update_score_display)

    def _update_score_display(self):
        self.lbl_score.configure(text=f"Score (Me - Opponent): {self.game_state.get_display_score()}")
        self.lbl_games.configure(text=f"Games: {self.game_state.games_me} - {self.game_state.games_opponent} | Sets: {self.game_state.sets_me} - {self.game_state.sets_opponent}")

    def _on_winner_click(self, winner):
        self.var_winner.set(winner)
        self.log_point()

    def log_point(self):
        winner = self.var_winner.get()
        
        # Determine who won based on "Me" / "Opponent" / "Unknown"
        winner_is_me = (winner == "Me")
        server_val = "n" # n=Me (server), o=Opponent (server)
        if self.var_server.get() == "Me": server_val = "m"
        else: server_val = "o"

        if winner == "Unknown":
            pass
        else:
            # Add point to 'me' or 'opponent' directly
            self.game_state.add_point('me' if winner_is_me else 'opponent')
        
        self._update_score_display()
        
        # Prepare data for CSV
        # Map winner to code
        outcome_code = "U"
        if winner == "Me": outcome_code = "W"
        elif winner == "Opponent": outcome_code = "L"
        
        data = {
            "set_no": self.game_state.current_set,
            "game_no": self.game_state.games_me + self.game_state.games_opponent + 1,
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
        
        self.logger.log_point(data)
        
        # Reset some fields for next point
        self.var_rally.set("Short")
        self.var_serve_num.set("1") # Reset to 1st serve usually
        self.entry_notes.delete(0, 'end') # Clear notes

    def undo_point(self):
        self.game_state.undo()
        self._update_score_display()
        self.logger.undo_last_log()
