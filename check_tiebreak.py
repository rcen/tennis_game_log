from tennis_logger.game_state import GameState

def verify_tiebreak_target():
    game = GameState()
    game.is_tiebreak = True
    game.tiebreak_target = 10 # Set to 10-point tiebreak
    
    print(f"Testing tiebreak with target: {game.tiebreak_target}")
    
    # Simulate 7-0
    game.points_me = 7
    game.points_opponent = 0
    game._check_game_end()
    
    if game.games_me == 0 and game.games_opponent == 0:
        print("SUCCESS: Game did NOT end at 7-0")
    else:
        print(f"FAILURE: Game ended at 7-0. Games: {game.games_me}-{game.games_opponent}")
        
    # Simulate 9-9
    game.points_me = 9
    game.points_opponent = 9
    game._check_game_end()
    
    # Simulate 10-9 (should not end)
    game.add_point('me') # 10-9
    if game.games_me == 0:
        print("SUCCESS: Game did NOT end at 10-9")
    else:
        print("FAILURE: Game ended at 10-9")
        
    # Simulate 11-9 (should end)
    game.add_point('me') # 11-9
    if game.games_me == 1:
        print("SUCCESS: Game ended at 11-9")
    else:
        print("FAILURE: Game did NOT end at 11-9")

    # Test 7-point tiebreak (default)
    game.reset_match()
    game.is_tiebreak = True
    game.tiebreak_target = 7
    print(f"\nTesting tiebreak with target: {game.tiebreak_target}")
    
    game.points_me = 6
    game.points_opponent = 0
    game.add_point('me') # 7-0
    
    if game.games_me == 1:
        print("SUCCESS: Game ended at 7-0")
    else:
        print("FAILURE: Game did NOT end at 7-0")

if __name__ == "__main__":
    verify_tiebreak_target()
