import numpy as np

class Construct:
    def __init__(self, structure: np.ndarray):
        self.structure = structure

    @property
    def shape(self):
        return self.structure.shape

    @property
    def matrix(self):
        return self.structure

    def __repr__(self) -> str:
        res = "Construct: \n\n\t"
        for row in self.structure:
            for col in row:
                res += "■" if col == 1 else "□"
            res += "\n\t"
        return res

cube = Construct(np.array([
    [1, 1],
    [1, 1]
]))


glider = Construct(np.array([
    [1, 1, 1],
    [0, 0, 1],
    [0, 1, 0]
]))
