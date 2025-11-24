class GameState:
    def __init__(self):
        self.reset_match()

    def reset_match(self):
        self.sets_server = 0
        self.sets_receiver = 0
        self.games_server = 0
        self.games_receiver = 0
        self.points_server = 0
        self.points_receiver = 0
        self.current_set = 1
        self.match_history = [] # List of tuples/dicts for undo functionality

    def get_score_string(self, points):
        if points == 0: return "0"
        if points == 1: return "15"
        if points == 2: return "30"
        if points == 3: return "40"
        return "AD" # Simplified, logic handled in add_point

    def get_display_score(self):
        server_score = self.get_score_string(self.points_server)
        receiver_score = self.get_score_string(self.points_receiver)
        
        # Deuce handling
        if self.points_server >= 3 and self.points_receiver >= 3:
            if self.points_server == self.points_receiver:
                return "Deuce"
            elif self.points_server > self.points_receiver:
                return "Ad-In"
            else:
                return "Ad-Out"
                
        return f"{server_score} - {receiver_score}"

    def add_point(self, winner):
        """
        winner: 'server' or 'receiver'
        """
        # Save state for undo (deep copy or simple snapshot if primitives)
        self.match_history.append({
            'sets_server': self.sets_server,
            'sets_receiver': self.sets_receiver,
            'games_server': self.games_server,
            'games_receiver': self.games_receiver,
            'points_server': self.points_server,
            'points_receiver': self.points_receiver,
            'current_set': self.current_set
        })

        if winner == 'server':
            self.points_server += 1
        else:
            self.points_receiver += 1

        self._check_game_end()

    def _check_game_end(self):
        # Simple game winning logic
        # 4 points and ahead by 2
        if (self.points_server >= 4 or self.points_receiver >= 4) and \
           abs(self.points_server - self.points_receiver) >= 2:
            
            if self.points_server > self.points_receiver:
                self.games_server += 1
            else:
                self.games_receiver += 1
            
            self.points_server = 0
            self.points_receiver = 0
            self._check_set_end()

    def _check_set_end(self):
        # Simple set winning logic (6 games, ahead by 2, or 7-6 tiebreak - simplified for now to 6-X)
        # TODO: Implement Tiebreak logic properly if needed
        if (self.games_server >= 6 or self.games_receiver >= 6) and \
           abs(self.games_server - self.games_receiver) >= 2:
            
            if self.games_server > self.games_receiver:
                self.sets_server += 1
            else:
                self.sets_receiver += 1
            
            self.games_server = 0
            self.games_receiver = 0
            self.current_set += 1

    def undo(self):
        if self.match_history:
            state = self.match_history.pop()
            self.sets_server = state['sets_server']
            self.sets_receiver = state['sets_receiver']
            self.games_server = state['games_server']
            self.games_receiver = state['games_receiver']
            self.points_server = state['points_server']
            self.points_receiver = state['points_receiver']
            self.current_set = state['current_set']
