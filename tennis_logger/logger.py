import csv
import os
from datetime import datetime

class MatchLogger:
    SCHEMA_COLUMNS = [
        "point_id", "set_no", "game_no", "score_before_point",
        "server", "serve_number", "serve_code",
        "return_code", "return_aggr",
        "rally_len_shots", "stroke_seq",
        "pattern", "tactic_code",
        "pressure_flags",
        "final_shot_type", "final_outcome",
        "court_pos_final", "notes"
    ]

    def __init__(self, filename="tennis_log.csv"):
        self.filename = filename
        self._init_csv()

    def _init_csv(self):
        file_exists = os.path.isfile(self.filename)
        if not file_exists:
            with open(self.filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.SCHEMA_COLUMNS)

    def log_point(self, data):
        """
        data: dict containing keys matching SCHEMA_COLUMNS
        """
        # Generate a unique point_id if not provided
        if 'point_id' not in data or not data['point_id']:
            data['point_id'] = datetime.now().strftime("%Y%m%d%H%M%S%f")

        row = []
        for col in self.SCHEMA_COLUMNS:
            row.append(data.get(col, ""))

        with open(self.filename, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
