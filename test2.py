import numpy as np

def flatten_dict(dictionary, parent_key='', separator='.'):
    flattened_dict = {}
    for key, value in dictionary.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            flattened_dict.update(flatten_dict(value, new_key, separator))
        else:
            flattened_dict[new_key] = value
    return flattened_dict

game_state = {"key1": 1, "key2": {"keysub1": 2, "keysub2": {"keysubsub1": 15}}}

var = np.array([list(flatten_dict(game_state).values())])
print(var)