from tennis_logger.game_state import GameState

def verify_no_ad():
    game = GameState()
    
    # Test Standard Scoring (Ad)
    print("Testing Standard Scoring (Ad)...")
    game.no_ad_mode = False
    game.points_me = 3 # 40
    game.points_opponent = 3 # 40 (Deuce)
    
    game.add_point('me') # Ad Me
    if game.games_me == 0:
        print("SUCCESS: Game did NOT end at Ad (Standard)")
    else:
        print("FAILURE: Game ended at Ad (Standard)")
        
    game.add_point('opponent') # Deuce
    game.add_point('opponent') # Ad Opp
    game.add_point('opponent') # Game Opp
    
    if game.games_opponent == 1:
        print("SUCCESS: Game ended after winning from Ad (Standard)")
    else:
        print("FAILURE: Game did NOT end after winning from Ad (Standard)")

    # Test No Ad Scoring
    print("\nTesting No Ad Scoring...")
    game.reset_match()
    game.no_ad_mode = True
    
    game.points_me = 3 # 40
    game.points_opponent = 3 # 40 (Deuce)
    
    # Next point should win the game
    game.add_point('me') 
    
    if game.games_me == 1:
        print("SUCCESS: Game ended immediately after Deuce point (No Ad)")
    else:
        print(f"FAILURE: Game did NOT end after Deuce point (No Ad). Score: {game.points_me}-{game.points_opponent}")

if __name__ == "__main__":
    verify_no_ad()
