from math import floor


class Score:
    MAX_SCORE = 1_501_067

    time_played: float
    surrendered: bool = False
    lost_game: bool = False

    def __init__(self, time: float, lost_game: bool = False, surrendered: bool = False) -> None:
        self.time_played = time
        self.lost_game = lost_game
        self.surrendered = surrendered

    def calculate_score(self) -> int:
        if self.surrendered:
            return 0

        score =  max(self.MAX_SCORE - floor(self.time_played * 101.64), 0)
        if self.lost_game:
            return score // 6845
        return score
