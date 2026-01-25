from tennis_logger.logger import MatchLogger
import os
import csv

def verify_undo():
    test_file = "test_log_check.csv"
    result_file = "verification_result.txt"
    
    if os.path.exists(test_file):
        os.remove(test_file)
    if os.path.exists(result_file):
        os.remove(result_file)
        
    try:
        logger = MatchLogger(test_file)
        
        # Log a point
        data = {
            "point_id": "1",
            "set_no": 1,
            "game_no": 1,
            "score_before_point": "0-0",
            "server": "m",
            "serve_number": "1",
            "serve_code": "I",
            "return_code": "N/A",
            "rally_len_shots": "Short",
            "pattern": "Rally",
            "tactic_code": "Rally",
            "final_shot_type": "N/A",
            "final_outcome": "W",
            "notes": "Test point"
        }
        logger.log_point(data)
        
        # Verify point logged
        with open(test_file, 'r') as f:
            lines = list(csv.reader(f))
            if len(lines) != 2:
                raise Exception(f"Expected 2 lines (header + 1 point), got {len(lines)}")
            
        # Undo
        logger.undo_last_log()
        
        # Verify point removed
        with open(test_file, 'r') as f:
            lines = list(csv.reader(f))
            if len(lines) != 1:
                raise Exception(f"Expected 1 line (header only), got {len(lines)}")
            
        with open(result_file, "w") as f:
            f.write("Verification passed!")
            
    except Exception as e:
        with open(result_file, "w") as f:
            f.write(f"Verification failed: {str(e)}")
            
    # No cleanup of test_file to allow inspection

if __name__ == "__main__":
    verify_undo()
