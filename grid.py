import numpy as np
from construct import cube, Construct, glider
from typing import List, Tuple

class Grid:
    """
    Implementation of the universe, in form of a grid.
    """

    def __init__(self, width: int, height: int):
        self.height = height
        self.width = width
        self.grid = np.zeros((width, height))

        # fixed size allocation, used to store intermediate states in neighbor counting
        self.intermediate_states = [np.zeros((width, height)) for i in range(8)]

        # spawning pool for automated life creation
        # self.spawning_pool_location = [(100, 40)]
        # self.spawning_pool_size = [(30, 30)]

    def step(self) -> np.ndarray:
        """
        Function steps forward in time by one tick,
            - recalculates states of cells
            - assigns back into self.grid
            - also return the new state

        :return: the updated state of the Grid.
        """

        next_state = self.grid.copy()
        max_row, max_col = self.grid.shape

        # create neighbor matrix
        # optimized with dynamic programming & vectorized operations
        for state in range(len(self.intermediate_states)):
            self.intermediate_states[state].fill(0)
        self.intermediate_states[0][:-1, :-1] = self.grid[1:, 1:]
        self.intermediate_states[1][:, :-1] = self.grid[:, 1:]
        self.intermediate_states[2][1:, :-1] = self.grid[:-1, 1:]
        self.intermediate_states[3][1:, :] = self.grid[:-1, :]
        self.intermediate_states[4][1:, 1:] = self.grid[:-1, :-1]
        self.intermediate_states[5][:, 1:] = self.grid[:, :-1]
        self.intermediate_states[6][:-1, 1:] = self.grid[1:, :-1]
        self.intermediate_states[7][:-1, :] = self.grid[1:, :]
        neighbor_matrix = np.sum(self.intermediate_states, axis=0)

        # determine state deltas
        next_state[(self.grid == 0) & (neighbor_matrix == 3)] = 1

        next_state[
            (self.grid == 1) & ((neighbor_matrix > 3) | (neighbor_matrix < 2))
        ] = 0

        # # spawning pool
        # for pool_idx in range(len(self.spawning_pool_size)):
        #     loc = self.spawning_pool_location[pool_idx]
        #     size = self.spawning_pool_size[pool_idx]
        #     if np.random.random() < 0.01:
        #         next_state[
        #             loc[0] : loc[0] + size[0], loc[1] : loc[1] + size[1]
        #         ] = np.round(np.random.random(size))

        # # this also works, but very slow
        # for row in range(max_row):
        #     for col in range(max_col):
        #
        #         num_neighbors = int(np.sum(self.grid[
        #             (row - 1) % max_row : (row + 2) % max_row,
        #             (col - 1) % max_col : (col + 2) % max_col,
        #         ]) - self.grid[row, col])
        #
        #         # birth
        #         if (num_neighbors == 3 and self.grid[row, col] == 0):
        #             next_state[row, col] = 1
        #
        #         # dead
        #         if (
        #             self.grid[row, col] == 1 and
        #             (
        #                 num_neighbors > 3
        #                 or
        #                 num_neighbors < 2
        #             )
        #         ):
        #             next_state[row, col] = 0

        self.grid = next_state
        return next_state

    def get_ones(self) -> np.ndarray:
        """
        get the list of coordinates where the Grid holds value 1

        :return: a list of coordinates where the Grid holds value 1, in form of np.array ([(1,1), (3,5)]) as an example.
        """
        return np.argwhere(self.grid == 1)

    def insert_construct(self, construct: Construct, target: Tuple[int, int]) -> None:
        """
        Insert a construct into the Grid.

        :param construct: A Construct
        :param target: target coordinates. Example: (10, 40)
        """
        width, height = construct.shape
        top, left = target
        self.grid[top : top + height, left : left + width] = construct.matrix

    def randomize(self, target: Tuple[int, int]):
        width, height = (20, 20)
        max_row, max_col = self.grid.shape
        row, col = target
        for r in range(row % max_row, (row + width) % max_row):
            for c in range(col % max_col, (col + width) % max_col):
                self.grid[r, c] = 1 if np.random.random() >= 0.5 else 0

    def __repr__(self) -> str:
        res = "Grid: \n\n\t"
        for row in self.grid:
            for col in row:
                res += "???" if col == 1 else "???"
            res += "\n\t"
        return res
