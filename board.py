# board.py

import random
from tile import Tile


class Board:
    SIZE = 4
    GATES = ["AND", "OR", "XOR"]

    def __init__(self):
        self.grid = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self):
        empty = [(r, c) for r in range(self.SIZE)
                 for c in range(self.SIZE)
                 if self.grid[r][c] is None]

        if not empty:
            return

        r, c = random.choice(empty)
        gate = random.choice(self.GATES)
        self.grid[r][c] = Tile(gate)

    def move(self, direction):
        moved = False

        if direction == "left":
            for row in range(self.SIZE):
                if self._merge(self.grid[row]):
                    moved = True

        elif direction == "right":
            for row in range(self.SIZE):
                reversed_row = list(reversed(self.grid[row]))
                if self._merge(reversed_row):
                    moved = True
                self.grid[row] = list(reversed(reversed_row))

        elif direction == "up":
            for col in range(self.SIZE):
                column = [self.grid[row][col] for row in range(self.SIZE)]
                if self._merge(column):
                    moved = True
                for row in range(self.SIZE):
                    self.grid[row][col] = column[row]

        elif direction == "down":
            for col in range(self.SIZE):
                column = [self.grid[row][col] for row in range(self.SIZE)]
                column.reverse()
                if self._merge(column):
                    moved = True
                column.reverse()
                for row in range(self.SIZE):
                    self.grid[row][col] = column[row]

        if moved:
            self.spawn_tile()

        return moved

    def _merge(self, tiles):
        original = list(tiles)
        new_tiles = [t for t in tiles if t is not None]

        merged = []
        skip = False

        for i in range(len(new_tiles)):
            if skip:
                skip = False
                continue

            if (i + 1 < len(new_tiles)
                and new_tiles[i].gate_type == new_tiles[i + 1].gate_type
                and new_tiles[i].level == new_tiles[i + 1].level):

                new_tiles[i].upgrade()
                merged.append(new_tiles[i])
                skip = True
            else:
                merged.append(new_tiles[i])

        while len(merged) < self.SIZE:
            merged.append(None)

        for i in range(self.SIZE):
            tiles[i] = merged[i]

        return original != tiles

    def check_win(self):
        for row in self.grid:
            for tile in row:
                if tile and tile.level == 5:
                    return True
        return False

    def check_game_over(self):
        for row in self.grid:
            if None in row:
                return False

        for r in range(self.SIZE):
            for c in range(self.SIZE):
                current = self.grid[r][c]

                if c + 1 < self.SIZE:
                    neighbor = self.grid[r][c + 1]
                    if neighbor and current.gate_type == neighbor.gate_type and current.level == neighbor.level:
                        return False

                if r + 1 < self.SIZE:
                    neighbor = self.grid[r + 1][c]
                    if neighbor and current.gate_type == neighbor.gate_type and current.level == neighbor.level:
                        return False

        return True

    def to_list(self):
        """
        Convert grid to serializable format for HTML.
        """
        return [
            [tile.to_dict() if tile else None for tile in row]
            for row in self.grid
        ]