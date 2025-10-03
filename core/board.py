class Board:
    SIZE = 5
    FLOOR_CAPACITY = 7
    FLOOR_PENALTIES = [-1, -1, -2, -2, -2, -3, -3]

    def __init__(self):
        self.rows = [[] for _ in range(self.SIZE)]
        self.floor = []
        self.wall = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.pattern = [
            [1, 2, 3, 4, 5],
            [5, 1, 2, 3, 4],
            [4, 5, 1, 2, 3],
            [3, 4, 5, 1, 2],
            [2, 3, 4, 5, 1],
        ]
        self.score = 0

    def can_place(self, row_idx, color):
        if self.rows[row_idx] and self.rows[row_idx][0] != color:
            return False
        if color in self.pattern[row_idx]:
            col_idx = self.pattern[row_idx].index(color)
            if self.wall[row_idx][col_idx] == color:
                return False
        return True

    def place_tiles(self, row_idx, color, count):
        if row_idx == -1 or not self.can_place(row_idx, color):
            self._place_to_floor([color] * count)
            return

        capacity = row_idx + 1
        free_slots = capacity - len(self.rows[row_idx])
        to_place = min(count, free_slots)
        overflow = count - to_place

        self.rows[row_idx].extend([color] * to_place)
        if overflow > 0:
            self._place_to_floor([color] * overflow)

    def _place_to_floor(self, tiles):
        free_slots = self.FLOOR_CAPACITY - len(self.floor)
        self.floor.extend(tiles[:free_slots])

    def end_round(self):
        for r, row in enumerate(self.rows):
            if len(row) == r + 1:
                color = row[0]
                col = self.pattern[r].index(color)
                self.wall[r][col] = color
                self.score += self.score_tile(r, col)
                self.rows[r] = []

        penalty = sum(self.FLOOR_PENALTIES[:len(self.floor)])
        self.score += penalty
        if self.score < 0:
            self.score = 0
        self.floor = []

    def score_tile(self, row, col):
        base = 1
        row_count = self._count_adj(row, col, axis="row")
        col_count = self._count_adj(row, col, axis="col")

        if row_count > 1 and col_count > 1:
            return row_count + col_count - 1
        elif row_count > 1:
            return row_count
        elif col_count > 1:
            return col_count
        return base

    def _count_adj(self, row, col, axis="row"):
        count = 1
        if axis == "row":
            c = col - 1
            while c >= 0 and self.wall[row][c] is not None:
                count += 1
                c -= 1
            c = col + 1
            while c < self.SIZE and self.wall[row][c] is not None:
                count += 1
                c += 1
        else:
            r = row - 1
            while r >= 0 and self.wall[r][col] is not None:
                count += 1
                r -= 1
            r = row + 1
            while r < self.SIZE and self.wall[r][col] is not None:
                count += 1
                r += 1
        return count

    # ----------------------------
    # End Game Scoring
    # ----------------------------
    def final_score(self):
        bonus = 0

        # Completed rows = +2 each
        for r in range(self.SIZE):
            if all(self.wall[r][c] is not None for c in range(self.SIZE)):
                bonus += 2

        # Completed columns = +7 each
        for c in range(self.SIZE):
            if all(self.wall[r][c] is not None for r in range(self.SIZE)):
                bonus += 7

        # Completed color sets = +10 each
        colors = {1, 2, 3, 4, 5}
        for color in colors:
            count = sum(
                1 for r in range(self.SIZE) for c in range(self.SIZE)
                if self.wall[r][c] == color
            )
            if count == self.SIZE:
                bonus += 10

        self.score += bonus
        return bonus
