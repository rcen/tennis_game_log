## This is a vibe coding for recording a tennis match.
Features:
- log some basic event for each play, such as actions, strategies, major strikes from observation, and outcome. 
- the logging machenism tries to be simple and efficient, there is only short break between each play. 
- GUI is for laptop for now. 
- the log (.csv file)can be used for later analysis, using AI to generate a summary and training plan for the future.


## Current Status
✅ Popup button selections  
✅ Multi-select for Point Type and Tactic  
✅ Expanded tactics list (13 options)  
✅ Expanded point types (11 options)  
✅ Categorical Rally Length (Short/Medium/Long)  
✅ Unknown options for Winner and How  
✅ Score editing feature    
✅ Notes field for additional details    
✅ Specific winner types in How? dialog    
✅ Yellow highlighting for errors  
✅ Taller main buttons (height=40)  
✅ Hints/descriptions on all options  

The data is saved to tennis_log.csv with the following columns:
CSV Schema:
- point_id - Unique timestamp ID  
- set_no - Current set number  
- game_no - Current game number  
- score_before_point - Score like "15 - 30" or "Deuce"  
- server - "n" (Me) or "o" (Opponent)  
- serve_number - "1" or "2"  

- serve_code - e.g., "In (I)", "Ace (A)", "Fault (SF)"  
- return_code - e.g., "In (I)", "Net (N)", "Long (L)"  
- return_aggr - (currently empty - not filled by UI)  
- rally_len_shots - "Short", "Medium", or "Long"  
- stroke_seq - (currently empty - not filled by UI)  
- pattern - Point types like "Rally (R)|Approach (A)"  
- tactic_code - Tactics like "Depth (D)|Weak Wing (W)"  
- pressure_flags - (currently empty - not filled by UI)  
- final_shot_type - e.g., "Forehand (F)", "Volley (V)"  
- final_outcome - e.g., "PtWon|W", "PtLost|UE"  
- court_pos_final - (currently empty - not filled by UI)  
- notes - Your custom notes text  
