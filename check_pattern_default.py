import sys
from unittest.mock import MagicMock

# Define Mock classes
class MockCTk:
    def __init__(self, *args, **kwargs):
        pass
    def title(self, *args):
        pass
    def geometry(self, *args):
        pass
    def grid_columnconfigure(self, *args, **kwargs):
        pass
    def grid_rowconfigure(self, *args, **kwargs):
        pass
    def mainloop(self):
        pass

class MockWidget:
    def __init__(self, *args, **kwargs):
        pass
    def pack(self, *args, **kwargs):
        pass
    def grid(self, *args, **kwargs):
        pass
    def configure(self, *args, **kwargs):
        pass
    def insert(self, *args, **kwargs):
        pass
    def delete(self, *args, **kwargs):
        pass
    def get(self):
        return "" # Default return for entry.get()

class MockStringVar:
    def __init__(self, value="", *args, **kwargs):
        self._value = value
        # Store initialization value globally for verification
        if not hasattr(MockStringVar, 'initializations'):
            MockStringVar.initializations = []
        MockStringVar.initializations.append(value)
        
    def get(self):
        return self._value
    def set(self, value):
        self._value = value

class MockBooleanVar:
    def __init__(self, value=False, *args, **kwargs):
        self._value = value
    def get(self):
        return self._value
    def set(self, value):
        self._value = value

# Mock customtkinter module
mock_ctk = MagicMock()
mock_ctk.CTk = MockCTk
mock_ctk.CTkFrame = MockWidget
mock_ctk.CTkLabel = MockWidget
mock_ctk.CTkButton = MockWidget
mock_ctk.CTkEntry = MockWidget
mock_ctk.CTkSegmentedButton = MockWidget
mock_ctk.CTkComboBox = MockWidget
mock_ctk.CTkCheckBox = MockWidget
mock_ctk.CTkToplevel = MockCTk
mock_ctk.CTkScrollableFrame = MockWidget
mock_ctk.StringVar = MockStringVar
mock_ctk.BooleanVar = MockBooleanVar

sys.modules["customtkinter"] = mock_ctk

# Mock other dependencies
sys.modules["tennis_logger.game_state"] = MagicMock()
sys.modules["tennis_logger.logger"] = MagicMock()

# Now import the app
from tennis_logger.gui import TennisLoggerApp

def verify_pattern_default():
    # Reset mock tracking
    MockStringVar.initializations = []
    
    # Instantiate app
    app = TennisLoggerApp()
    
    # Check if "Unknown (UNK)" was used to initialize any StringVar
    # Note: "How?" also uses "Unknown (UNK)", so we expect at least 2 occurrences if both are defaulted
    count_unknown = MockStringVar.initializations.count("Unknown (UNK)")
    if count_unknown >= 2:
        print(f"SUCCESS: 'Unknown (UNK)' used {count_unknown} times (expected at least 2 for How and Pattern)")
    else:
        print(f"FAILURE: 'Unknown (UNK)' used {count_unknown} times (expected at least 2)")
        print("StringVar initializations:", MockStringVar.initializations)
        
    # Setup app state for log_point
    app.var_winner = MockStringVar("Me")
    app.var_server = MockStringVar("Me")
    app.var_serve_num = MockStringVar("1")
    app.var_serve_code = MockStringVar("I")
    app.var_how = MockStringVar("Unknown (UNK)")
    app.var_rally = MockStringVar("Medium")
    
    # Mock game state
    app.game_state = MagicMock()
    app.game_state.games_me = 0
    app.game_state.games_opponent = 0
    app.game_state.sets_me = 0
    app.game_state.sets_opponent = 0
    app.game_state.get_display_score.return_value = "0-0"
    
    # Mock logger
    app.logger = MagicMock()
    
    # Set var_pattern to something else to verify reset
    app.var_pattern.set("Rally (R)")
    
    # Call log_point
    app.log_point()
    
    # Verify reset
    if app.var_pattern.get() == "Unknown (UNK)":
        print("SUCCESS: var_pattern reset to 'Unknown (UNK)' in log_point")
    else:
        print(f"FAILURE: var_pattern is '{app.var_pattern.get()}', expected 'Unknown (UNK)'")

if __name__ == "__main__":
    verify_pattern_default()
