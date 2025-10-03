import unittest
import random
from core.tile import Tile
from core.factory import Factory
from core.middle import Middle
from core.game_logic import AzulGame

class TestFactoryGame(unittest.TestCase):

    def setUp(self):
        # 2 dummy players
        self.players = ["Player1", "Player2"]
        self.game = AzulGame(self.players)

    def test_take_tiles_from_plate(self):
        # Fill factories from bag
        self.game.fill_factories()

        # Choose a random factory
        plate_index = random.randint(0, len(self.game.factories) - 1)
        plate = self.game.factories[plate_index]

        if not plate.tiles:
            self.skipTest("Randomly picked empty plate, skip")

        # Choose a color that exists on this plate
        chosen_color = random.choice([t.color for t in plate.tiles])

        # Copy initial plate tiles
        initial_tiles = plate.tiles[:]

        # Perform the action: player takes tiles from the factory
        chosen_tiles = self.game.player_select_from_factory(factory_index=plate_index, color=chosen_color)

        # All tiles of chosen color taken
        expected_chosen = [t for t in initial_tiles if t.color == chosen_color]
        self.assertEqual(sorted(t.color for t in chosen_tiles),
                         sorted(t.color for t in expected_chosen),
                         "Player did not take all tiles of the chosen color")

        # Remaining tiles go to middle (existing Tile(-1) stays)
        expected_remaining = [t for t in initial_tiles if t.color != chosen_color]
        middle_colors = [t.color for t in self.game.middle.tiles]

        # There should be Tile(-1) plus remaining tiles
        self.assertIn(-1, middle_colors, "Tile(-1) should still be in the middle")
        for t in expected_remaining:
            self.assertIn(t.color, middle_colors, "Remaining tiles not correctly moved to middle")

        # Plate should be empty
        self.assertEqual(plate.tiles, [], "Factory plate was not emptied")
        
    
    
    def test_take_from_factory_then_middle(self):
        # Fill factories
        self.game.fill_factories()

        # Step 1: take tiles from a random factory
        plate_index = random.randint(0, len(self.game.factories) - 1)
        plate = self.game.factories[plate_index]

        if not plate.tiles:
            self.skipTest("Randomly picked empty plate, skip")

        chosen_color_factory = random.choice([t.color for t in plate.tiles])
        chosen_from_factory = self.game.player_select_from_factory(factory_index=plate_index,
                                                                color=chosen_color_factory)

        # Step 2: take tiles from middle
        middle_available_colors = [t.color for t in self.game.middle.tiles if t.color != -1]
        if not middle_available_colors:
            self.skipTest("No tiles other than -1 in middle to take")

        chosen_color_middle = random.choice(middle_available_colors)
        chosen_from_middle = self.game.game_logic.middle.take_tiles(chosen_color_middle) \
            if hasattr(self.game, "game_logic") else self.game.middle.take_tiles(chosen_color_middle)

        # Assertions
        # All tiles of chosen color taken
        self.assertTrue(all(t.color == chosen_color_middle or t.color == -1 for t in chosen_from_middle),
                        "Did not take correct tiles from middle")

        # Tile(-1) should now be marked taken
        self.assertTrue(self.game.middle.tile_first_taken, "Tile(-1) was not marked as taken")

        # Middle should no longer have any tiles of the chosen color
        remaining_colors = [t.color for t in self.game.middle.tiles]
        self.assertNotIn(chosen_color_middle, remaining_colors,
                        "Chosen color still present in middle after taking")


    def test_draw_from_all_factories_then_middle(self):
        # Fill all factories
        self.game.fill_factories()

        # --- Step 1: Draw from every plate ---
        for i, plate in enumerate(self.game.factories):
            if not plate.tiles:
                continue
            chosen_color = random.choice([t.color for t in plate.tiles])
            chosen_tiles = self.game.player_select_from_factory(factory_index=i, color=chosen_color)
            # Plate should be empty after taking
            self.assertEqual(plate.tiles, [], f"Factory {i} not empty after taking tiles")

        # --- Step 2: Check middle after all factories drawn ---
        middle_colors = [t.color for t in self.game.middle.tiles]
        self.assertIn(-1, middle_colors, "Tile(-1) must be in middle after all factories drawn")
        self.assertGreaterEqual(len(middle_colors), 1, "Middle should contain remaining tiles")

        # --- Step 3: Draw 3 times from middle ---
        for draw_idx in range(3):
            # Pick a random color from middle (excluding -1 if already taken)
            available_colors = [t.color for t in self.game.middle.tiles if t.color != -1]
            if not available_colors:
                break
            chosen_color = random.choice(available_colors)
            tiles_taken = self.game.middle.take_tiles(chosen_color)

            # First time drawing from middle should include -1 tile
            if draw_idx == 0:
                self.assertIn(-1, [t.color for t in tiles_taken], "Tile(-1) not included on first middle draw")
            else:
                self.assertNotIn(-1, [t.color for t in tiles_taken], "Tile(-1) included after first draw")

            # None of the drawn color should remain in middle
            remaining_colors = [t.color for t in self.game.middle.tiles]
            self.assertNotIn(chosen_color, remaining_colors,
                             f"Color {chosen_color} still in middle after drawing")

        # --- Step 4: Final middle state ---
        # Tile(-1) should be marked as taken
        self.assertTrue(self.game.middle.tile_first_taken, "Tile(-1) not marked as taken")
        # Middle should only contain colors that were not drawn in the 3 draws
        remaining_colors = [t.color for t in self.game.middle.tiles]
        for t in remaining_colors:
            self.assertNotEqual(t, -1, "Tile(-1) should no longer be in middle")
