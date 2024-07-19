from .system import System

class Map:
    
    @classmethod
    def New_Game_Init(cls, num_players: int):
        if num_players < 3 or num_players > 6:
            raise ValueError("Number of players must be between 3 and 6, inclusive.")

    def __init__(self, *, systems_arrays: tuple[list[System]] = None, ref_map: tuple[tuple] = None):
        if systems_arrays is not None:
            self.map = systems_arrays
        elif ref_map is not None:
            self.map = tuple(list(inner_tuple) for inner_tuple in ref_map)
        else:
            raise ValueError("One argument must be filled.")
    
    def place_system(self, system: System, coord: tuple):
        row, col = coord
        if self.map[row][col] is None:
            raise ValueError(f"Coordinates {coord} are not valid.")
        else:
            self.map[row][col] = system

    def get_neighbors(self, coord: tuple):
        
        neighbors = []
        row, col = coord

        has_top_neighbor = row >= 2
        has_bottom_neighbor = row < len(self.map) - 2
        has_upper_neighbors = row >= 1
        has_lower_neighbors = row < len(self.map) - 1
        has_right_neighbors = col < len(self.map[row]) - 1
        has_left_neighbors = col > len(self.map[row]) - 1

        # Top
        if has_top_neighbor and self.map[row - 2][col] is not None:
            neighbors.append(self.map[row - 2][col])
        # Up-Right
        if has_upper_neighbors and has_right_neighbors and self.map[row - 1][col + 1] is not None:
            neighbors.append(self.map[row - 1][col + 1])
        # Down-Right
        if has_lower_neighbors and has_right_neighbors and self.map[row + 1][col + 1] is not None:
            neighbors.append(self.map[row + 1][col + 1])
        # Bottom
        if has_bottom_neighbor and self.map[row + 2][col] is not None:
            neighbors.append(self.map[row + 2][col])
        # Down-Left
        if has_lower_neighbors and has_left_neighbors and self.map[row + 1][col - 1] is not None:
            neighbors.append(self.map[row + 1][col - 1])
        # Up-Left
        if has_upper_neighbors and has_left_neighbors and self.map[row - 1][col - 1] is not None:
            neighbors.append(self.map[row - 1][col - 1])

        return neighbors
       
