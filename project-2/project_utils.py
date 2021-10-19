import math


# PATH UTILITIES
def path_trace(node, reverse=True):
    level = math.floor(math.log2(node))
    root_path = [node]
    next_node = node
    for i in range(level):
        next_node = next_node // 2
        root_path.append(next_node)
    if reverse:
        root_path.reverse()
    return root_path


def path_merge(var1, var2, method='node'):
    path1, path2, common = find_common(var1, var2, method=method)
    path1.reverse()

    path1_merge_point = path1.index(common)
    path2_merge_point = path2.index(common)

    new_path = path1[0:path1_merge_point] + path2[path2_merge_point:]

    return new_path


def find_common(var1, var2, method='node'):
    if method == 'node':
        path1 = path_trace(var1)
        path2 = path_trace(var2)
    else:
        path1 = var1
        path2 = var2
    rng = min(len(path1), len(path2))

    common_node = 1
    for i in range(rng):
        if path1[i] == path2[i]:
            common_node = path1[i]
        else:
            break

    return path1, path2, common_node


def path_forger(targets, agent_path):
    target_paths = []
    for target in targets:
        target_paths.append(
            path_merge(
                agent_path,
                targets[f'{target}'].root_path,
                method='path')
        )
    target_paths.sort(key=len)
    return target_paths
