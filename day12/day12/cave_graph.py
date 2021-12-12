from collections import defaultdict
from typing import Dict, Iterable, List, Sequence

Edge = Sequence[str]

def bidirectional(edges: Iterable[Edge]) -> Iterable[Edge]:
    """
    Take a list of two string tuples and return them with their inverses.
    """
    for cave1, cave2 in edges:
        yield cave1, cave2
        yield cave2, cave1

class CaveGraph:
    """Advent of Code 2021 day 12 cave representation."""

    def __init__(self, edges: Iterable[Edge]) -> None:
        """
        Construct a CaveGraph.
        
        The graph is bidirectional, except for edges from start or to end.

        :param edges: All ("from", "to") pairs of edges. Example: [("A", "b")]
        """
        # The internal graph is represented as a mapping of source edges
        # to all their destination edges. This means each edge should appear
        # twice in the graph, once for each direction (from - to and to - from).
        self._graph: Dict[str, List[str]] = defaultdict(list)
        for cave1, cave2 in bidirectional(edges):
            if cave1 == "end" or cave2 == "start":
                continue
            curr_dests = self._graph[cave1]
            if cave2 in curr_dests:
                raise ValueError(f"Edge ({cave1}, {cave2}) found twice.")
            curr_dests.append(cave2)

    def __str__(self) -> str:
        """String representation of the graph."""
        edges = []
        for cave1, dests in self._graph.items():
            for cave2 in dests:
                edges.append(f"{cave1}-{cave2}")
        # extra line after the edges for convenience
        res = "\n".join(sorted(edges))
        return f"{res}\n"

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "CaveGraph":
        """
        Construct the graph from lines of input.
        
        :param lines: An iterable of strings as problem input.
        :return: A new graph.
        """
        return cls(line.strip().split("-") for line in lines)

    def all_paths(self, extra_visit: bool = False) -> Iterable[str]:
        """
        Get all the paths through the graph from start to end.
        
        Small caves (lowercase letters) must all be traversed at most once.
        
        :param extra_visit: If True, allows visiting one small cave twice.
        
        :return: An iterable of the paths in the format e.g. "start,a,B,end"
        """
        in_progress: List[List[str]] = [["start"]]
        paths = []

        def extra_visit_allowed(path: List[str]) -> bool:
            if not extra_visit:
                return False
            # whether we can visit a small cave again in this path
            been_there_done_that = set()
            for dark_musty_stop in path:
                # we are only interested in small caves
                if not dark_musty_stop.islower():
                    continue
                elif dark_musty_stop in been_there_done_that:
                    # already visited twice, not going back there again!
                    return False
                else:
                    been_there_done_that.add(dark_musty_stop)
            return True

        # as long as we have unfinished paths
        while in_progress:
            next_progress = []
            for path in in_progress:
                # if there are none (dead end) the path is conveniently dropped
                for next_cave in self._graph[path[-1]]:
                    # we look at each cave up ahead and generate new paths
                    if not extra_visit_allowed(path) and next_cave.islower() \
                            and next_cave in path:
                        # we already visited this small cave
                        continue
                    elif next_cave == "end":
                        paths.append(path + [next_cave])
                    else:
                        next_progress.append(path + [next_cave])
            in_progress = next_progress
        return (",".join(path) for path in paths)
