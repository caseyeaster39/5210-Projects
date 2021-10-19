import math


# PATH UTILITIES
def path_trace(node, reverse=True):                                             # Root traceback
    level = math.floor(math.log2(node))                                         # Current depth
    root_path = [node]                                                          # Start from this node
    next_node = node
    for i in range(level):
        next_node = next_node // 2                                              # Step back to parent,
        root_path.append(next_node)                                             # add it to the path list
    if reverse:
        root_path.reverse()                                                     # reverse the order so root is first
    return root_path


def path_merge(var1, var2, method='node'):                                      # Path merging utility
    path1, path2, common = find_common(var1, var2, method=method)               # Find common node
    path1.reverse()                                                             # Because the agent is backtracking

    path1_merge_point = path1.index(common)                                     # Find index of common node
    path2_merge_point = path2.index(common)                                     # Find index of common node

    new_path = path1[0:path1_merge_point] + path2[path2_merge_point:]           # Merge the two at the common node

    return new_path                                                             # Return merged path


def find_common(var1, var2, method='node'):                                     # Utility to find common node
    if method == 'node':                                                        # If passed two nodes,
        path1 = path_trace(var1)                                                # run path trace on each
        path2 = path_trace(var2)                                                # to get their root paths.
    else:
        path1 = var1                                                            # Otherwise, use the paths passed in
        path2 = var2
    rng = min(len(path1), len(path2))                                           # Use shorter path length

    common_node = 1                                                             # Root
    for i in range(rng):
        if path1[i] == path2[i]:                                                # Change common if they are the same
            common_node = path1[i]
        else:                                                                   # Otherwise, the paths have diverged
            break

    return path1, path2, common_node                                            # Return the paths and their common node


def path_forger(targets, agent_path):                                           # Creates priority queue based on
    target_paths = []                                                           # step length
    for target in targets:
        target_paths.append(
            path_merge(                                                         # Create paths from
                agent_path,                                                     # current agent location
                targets[f'{target}'].root_path,                                 # and targets
                method='path')
        )
    target_paths.sort(key=len)                                                  # Sort ascending by length and return
    return target_paths
