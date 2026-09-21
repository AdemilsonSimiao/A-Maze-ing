from collections.abc import Callable, Iterator
import random


def dfs_edges(
    cells: list[tuple[int, int]],
    start: tuple[int, int],
    neighbors: Callable[[tuple[int, int]], list[tuple[int, int]]],
    rng: random.Random,
) -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
    visited = {start}
    stack = [start]
    while stack:
        current = stack[-1]
        options = [
            position
            for position in neighbors(current)
            if position not in visited
        ]
        if not options:
            stack.pop()
            continue
        chosen = rng.choice(options)
        yield current, chosen
        visited.add(chosen)
        stack.append(chosen)


def prim_edges(
    cells: list[tuple[int, int]],
    start: tuple[int, int],
    neighbors: Callable[[tuple[int, int]], list[tuple[int, int]]],
    rng: random.Random,
) -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
    """Randomized Prim: grows from a random border, many short dead-ends."""
    visited = {start}
    frontier = [(start, position) for position in neighbors(start)]
    while frontier:
        index = rng.randrange(len(frontier))
        frontier[index], frontier[-1] = frontier[-1], frontier[index]
        origin, target = frontier.pop()
        if target in visited:
            continue
        yield origin, target
        visited.add(target)
        for position in neighbors(target):
            if position not in visited:
                frontier.append((target, position))


def _find_root(
    parents: dict[tuple[int, int], tuple[int, int]],
    position: tuple[int, int],
) -> tuple[int, int]:
    while parents[position] != position:
        parents[position] = parents[parents[position]]
        position = parents[position]
    return position


def kruskal_edges(
    cells: list[tuple[int, int]],
    start: tuple[int, int],
    neighbors: Callable[[tuple[int, int]], list[tuple[int, int]]],
    rng: random.Random,
) -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
    """Randomized Kruskal: shuffles every wall and joins separate sets."""
    parents = {position: position for position in cells}
    edges = [
        ((x, y), (nx, ny))
        for x, y in cells
        for nx, ny in neighbors((x, y))
        if nx > x or ny > y
    ]
    rng.shuffle(edges)
    for first, second in edges:
        first_root = _find_root(parents, first)
        second_root = _find_root(parents, second)
        if first_root != second_root:
            parents[first_root] = second_root
            yield first, second


def wilson_edges(
    cells: list[tuple[int, int]],
    start: tuple[int, int],
    neighbors: Callable[[tuple[int, int]], list[tuple[int, int]]],
    rng: random.Random,
) -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
    """Wilson: loop-erased random walks, every possible maze equally likely."""
    in_tree = {start}
    starts = list(cells)
    rng.shuffle(starts)
    for first in starts:
        if first in in_tree:
            continue
        next_step: dict[tuple[int, int], tuple[int, int]] = {}
        current = first
        while current not in in_tree:
            following = rng.choice(neighbors(current))
            next_step[current] = following
            current = following
        current = first
        while current not in in_tree:
            target = next_step[current]
            yield current, target
            in_tree.add(current)
            current = target


def algorithm_names() -> tuple[str, ...]:
    return tuple(_algorithms())


def _algorithms() -> dict[
    str,
    Callable[
        [
            list[tuple[int, int]],
            tuple[int, int],
            Callable[[tuple[int, int]], list[tuple[int, int]]],
            random.Random,
        ],
        Iterator[tuple[tuple[int, int], tuple[int, int]]],
    ],
]:
    return {
        "dfs": dfs_edges,
        "prim": prim_edges,
        "kruskal": kruskal_edges,
        "wilson": wilson_edges,
    }


def generate_edges(
    algorithm: str,
    cells: list[tuple[int, int]],
    start: tuple[int, int],
    neighbors: Callable[[tuple[int, int]], list[tuple[int, int]]],
    rng: random.Random,
) -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
    algorithms = _algorithms()
    if algorithm not in algorithms:
        raise ValueError(
            f"Unknown algorithm '{algorithm}'. "
            f"Choose one of: {', '.join(algorithms)}."
        )
    return algorithms[algorithm](cells, start, neighbors, rng)
