# tile.py

class Tile:
    def __init__(self, gate_type, level=1):
        self.gate_type = gate_type
        self.level = level

    def upgrade(self):
        self.level += 1

    def to_dict(self):
        return {
            "gate_type": self.gate_type,
            "level": self.level
        }