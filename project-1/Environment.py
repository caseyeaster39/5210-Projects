Cord_Dict = {
    'A': [1, 1],
    'B': [2, 2],
    'C': [1, 3],
    'D': [2, 0],
    'E': [0, 2],
    'F': [2, 4],
    'G': [4, 1],
    'H': [5, 4],
    'J': [3, 5],
    'I': [4, 2]
}

empty_arr = [['*' for i in range(6)] for j in range(6)]
for letter, (x_pos, y_pos) in Cord_Dict.items():    # "letter" represents key of dictionary. Each time loop runs "letter is
                                                    # different key from dict.
    empty_arr[y_pos][x_pos] = letter                # Key Value which is "letter is placed into empty_arr using x and y

for line in empty_arr:
    print(line)