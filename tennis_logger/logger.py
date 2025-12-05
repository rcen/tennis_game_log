import csv
import os
from datetime import datetime

class MatchLogger:
    SCHEMA_COLUMNS = [
        "point_id", "timestamp", "set_no", "game_no", "score_before_point",
        "server", "serve_number", "serve_code",
        "return_code", "return_aggr",
        "rally_len_shots", "stroke_seq",
        "pattern", "tactic_code",
        "pressure_flags",
        "final_shot_type", "final_outcome",
        "court_pos_final", "notes"
    ]

    def __init__(self, base_filename="tennis_log"):
        self.base_filename = base_filename
        self.last_logged_point_id = None  # Track last point for undo
        self.undo_stack = []  # Stack of undone points that can be redone
        self._get_today_filename()

    def _get_today_filename(self):
        """Get filename for today's date: tennis_log_YYYYMMDD.csv"""
        today = datetime.now().strftime("%Y%m%d")
        self.filename = f"{self.base_filename}_{today}.csv"
        self._init_csv()

    def _init_csv(self):
        """Initialize CSV file with headers if it doesn't exist"""
        file_exists = os.path.isfile(self.filename)
        if not file_exists:
            with open(self.filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.SCHEMA_COLUMNS)

    def log_point(self, data):
        """
        data: dict containing keys matching SCHEMA_COLUMNS (except point_id and timestamp)
        """
        # Clear undo stack when a new point is logged (forward action)
        # This means we can't redo to lost futures
        if self.undo_stack:
            self.undo_stack.clear()
        
        # Check if date has changed, rotate file if needed
        current_filename = self._get_expected_filename()
        if current_filename != self.filename:
            self.filename = current_filename
            self._init_csv()

        # Generate a unique point_id if not provided
        if 'point_id' not in data or not data['point_id']:
            point_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
            data['point_id'] = point_id
            self.last_logged_point_id = point_id

        # Generate readable timestamp
        if 'timestamp' not in data or not data['timestamp']:
            data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = []
        for col in self.SCHEMA_COLUMNS:
            row.append(data.get(col, ""))

        with open(self.filename, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def _get_expected_filename(self):
        """Get the expected filename for today"""
        today = datetime.now().strftime("%Y%m%d")
        return f"{self.base_filename}_{today}.csv"

    def undo_last_log(self):
        """Remove the last logged row from the current log file and return it"""
        if not os.path.isfile(self.filename):
            return None

        lines = []
        with open(self.filename, mode='r', newline='') as f:
            lines = list(csv.reader(f))

        if len(lines) > 1:  # Keep header
            last_row = lines.pop()
            
            with open(self.filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(lines)
            
            # Return the removed row as a dict for potential restoration
            header = lines[0] if lines else self.SCHEMA_COLUMNS
            removed_data = dict(zip(header, last_row))
            
            # Push to undo stack so we can restore it later
            self.undo_stack.append(removed_data)
            
            return removed_data
        
        return None
    
    def redo_last_log(self):
        """Restore the last undone point from the undo stack"""
        if not self.undo_stack:
            return None
        
        # Pop the last undone point
        point_data = self.undo_stack.pop()
        
        # Re-log it without clearing the undo stack
        # We need to append directly to CSV without clearing undo_stack
        row = []
        for col in self.SCHEMA_COLUMNS:
            row.append(point_data.get(col, ""))
        
        with open(self.filename, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        
        return point_data
    
    def can_redo(self):
        """Check if there are points in the undo stack to redo"""
        return len(self.undo_stack) > 0
    
    def get_last_point_data(self):
        """Retrieve the data from the last point in the current log file"""
        if not os.path.isfile(self.filename):
            return None

        lines = []
        with open(self.filename, mode='r', newline='') as f:
            lines = list(csv.reader(f))

        if len(lines) > 1:  # More than just header
            last_row = lines[-1]
            header = lines[0] if lines else self.SCHEMA_COLUMNS
            return dict(zip(header, last_row))
        
        return None
