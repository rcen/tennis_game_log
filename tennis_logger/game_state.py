class GameState:
    def __init__(self):
        self.reset_match()

    def reset_match(self):
        self.sets_me = 0
        self.sets_opponent = 0
        self.games_me = 0
        self.games_opponent = 0
        self.points_me = 0
        self.points_opponent = 0
        self.is_tiebreak = False
        self.current_set = 1
        self.match_history = [] # List of tuples/dicts for undo functionality

    def get_score_string(self, points):
        if self.is_tiebreak:
            return str(points)
        if points == 0: return "0"
        if points == 1: return "15"
        if points == 2: return "30"
        if points == 3: return "40"
        return "AD" # Simplified, logic handled in add_point

    def get_display_score(self):
        score_me = self.get_score_string(self.points_me)
        score_opponent = self.get_score_string(self.points_opponent)
        
        if self.is_tiebreak:
            return f"{score_me} - {score_opponent}"
        
        # Deuce handling
        if self.points_me >= 3 and self.points_opponent >= 3:
            if self.points_me == self.points_opponent:
                return "Deuce"
            elif self.points_me > self.points_opponent:
                return "Ad (Me)"
            else:
                return "Ad (Opp)"
                
        return f"{score_me} - {score_opponent}"

    def add_point(self, winner):
        """
        winner: 'me' or 'opponent'
        """
        # Save state for undo (deep copy or simple snapshot if primitives)
        self.match_history.append({
            'sets_me': self.sets_me,
            'sets_opponent': self.sets_opponent,
            'games_me': self.games_me,
            'games_opponent': self.games_opponent,
            'points_me': self.points_me,
            'points_opponent': self.points_opponent,
            'is_tiebreak': self.is_tiebreak,
            'current_set': self.current_set
        })

        if winner == 'me':
            self.points_me += 1
        else:
            self.points_opponent += 1

        self._check_game_end()

    def _check_game_end(self):
        # Tiebreak winning logic: 7 points and ahead by 2
        if self.is_tiebreak:
            if (self.points_me >= 7 or self.points_opponent >= 7) and \
               abs(self.points_me - self.points_opponent) >= 2:
                if self.points_me > self.points_opponent:
                    self.games_me += 1
                else:
                    self.games_opponent += 1
                
                self.points_me = 0
                self.points_opponent = 0
                self.is_tiebreak = False # Reset tiebreak flag after game ends
                self._check_set_end()
            return

        # Simple game winning logic
        # 4 points and ahead by 2
        if (self.points_me >= 4 or self.points_opponent >= 4) and \
           abs(self.points_me - self.points_opponent) >= 2:
            
            if self.points_me > self.points_opponent:
                self.games_me += 1
            else:
                self.games_opponent += 1
            
            self.points_me = 0
            self.points_opponent = 0
            self._check_set_end()

    def _check_set_end(self):
        # Simple set winning logic (6 games, ahead by 2, or 7-6 tiebreak - simplified for now to 6-X)
        # TODO: Implement Tiebreak logic properly if needed
        if (self.games_me >= 6 or self.games_opponent >= 6) and \
           abs(self.games_me - self.games_opponent) >= 2:
            
            if self.games_me > self.games_opponent:
                self.sets_me += 1
            else:
                self.sets_opponent += 1
            
            self.games_me = 0
            self.games_opponent = 0
            self.current_set += 1

    def undo(self):
        if self.match_history:
            state = self.match_history.pop()
            self.sets_me = state['sets_me']
            self.sets_opponent = state['sets_opponent']
            self.games_me = state['games_me']
            self.games_opponent = state['games_opponent']
            self.points_me = state['points_me']
            self.points_opponent = state['points_opponent']
            self.is_tiebreak = state.get('is_tiebreak', False)
            self.current_set = state['current_set']
