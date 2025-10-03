import unittest

class TestAzulBoard(unittest.TestCase):
    def setUp(self):
        from core.board import Board  # replace with your actual import
        self.board = Board()

    def test_place_tiles_valid_row(self):
        # Place 2 tiles into row 2 (capacity 2)
        self.board.place_tiles(1, 1, 2)
        self.assertEqual(self.board.rows[1], [1, 1])
        self.assertEqual(self.board.floor, [])

    def test_place_tiles_overflow_to_floor(self):
        # Row 1 has capacity 1, place 3 tiles
        self.board.place_tiles(0, 2, 3)
        self.assertEqual(self.board.rows[0], [2])
        self.assertEqual(self.board.floor, [2, 2])

    def test_place_tiles_invalid_color(self):
        # Place a color in a row that already has different color
        self.board.place_tiles(2, 1, 1)
        self.board.place_tiles(2, 2, 1)  # should go to floor
        self.assertEqual(self.board.rows[2], [1])
        self.assertEqual(self.board.floor, [2])

    def test_end_round_score_tile(self):
        # Fill row 1 (capacity=1) with color 1
        self.board.place_tiles(0, 1, 1)
        self.board.end_round()
        # Row cleared, tile moved to wall
        self.assertEqual(self.board.rows[0], [])
        self.assertEqual(self.board.wall[0][self.board.pattern[0].index(1)], 1)
        # Score should be 1 (base, no adjacency)
        self.assertEqual(self.board.score, 1)

    def test_floor_penalty(self):
        # Place 8 tiles in floor (exceeding capacity)
        self.board._place_to_floor([1]*8)
        self.assertEqual(len(self.board.floor), 7)  # max 7
        self.board.end_round()
        # Penalty = -12 (-1,-1,-2,-2,-2,-3,-3)
        self.assertEqual(self.board.score, 0)  # can't go below 0

    def test_adjacent_scoring(self):
        # Place tiles to form adjacency
        for r in range(5):
            self.board.wall[r][2] = 1  # column 2
        # Place row 2, column 2 (already filled) → just test scoring logic
        self.board.wall[2][1] = 2
        points = self.board.score_tile(2, 1)
        self.assertEqual(points, 2)  # 2 adjacent vertically + base?

    def test_final_score(self):
        # Complete a row
        for c in range(5):
            self.board.wall[0][c] = c+1
        # Complete a column
        for r in range(5):
            self.board.wall[r][0] = self.board.pattern[r][0]
        # Complete color set (color 1)
        for r in range(5):
            c = self.board.pattern[r].index(1)
            self.board.wall[r][c] = 1
        bonus = self.board.final_score()
        self.assertEqual(bonus, 2 + 7 + 10)  # row + col + color set
        self.assertEqual(self.board.score, bonus)

    def test_cannot_place_color_already_in_wall_row(self):
        # Place color in row 0, column 1 of wall
        color = 2
        self.board.wall[0][self.board.pattern[0].index(color)] = color
        # Try to place color 2 in row 0 → should go to floor
        self.board.place_tiles(0, color, 1)
        self.assertEqual(self.board.rows[0], [])
        self.assertEqual(self.board.floor, [color])

    def test_overflow_discard_tiles_are_ignored(self):
        # Place 10 tiles in floor (capacity 7)
        self.board._place_to_floor([1]*10)
        self.assertEqual(len(self.board.floor), 7)  # only 7 are stored
