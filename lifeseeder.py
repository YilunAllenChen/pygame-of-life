from construct import Construct
from app import Grid
import numpy as np




def find_stable_or_repeating_constucts(maxlen: int):
    count = 0

    estimated = 0
    for i in range(1, maxlen):
        estimated += 2 ** (maxlen ** 2)
    print(f"estimated: {estimated} possible states")

    for sidelen in range(2, maxlen + 1):
        max_integer = 2 ** (sidelen ** 2)
        for num in range(1, max_integer):
            digits = bin(num)[2:]
            serialized_construct = digits.rjust(sidelen ** 2, '0')


            construct = Construct(np.array([
                int(ele) for ele in serialized_construct
            ]).reshape(
                (sidelen, sidelen)
            ))

            spawning_pool = Grid(sidelen, sidelen)
            last_state = None
            known_states = set()
            spawning_pool.insert_construct(construct, (0, 0))
            while(
                last_state is None or (
                    np.all(last_state != spawning_pool.grid) and
                    np.all(construct.matrix != spawning_pool.grid) and
                    str(last_state) not in known_states
                )
            ):
                if serialized_construct == "000111000":
                    print(spawning_pool)
                last_state = spawning_pool.grid
                known_states.add(str(last_state))
                spawning_pool.step()
            if (str(last_state) in known_states) and np.all(construct.matrix):
                print("this construct seems to be cyclic")
                print(construct)
            elif np.all(construct.matrix == spawning_pool.grid):
                print("this following construct is stable")
                print(construct)
            count += 1



find_stable_or_repeating_constucts(4)
