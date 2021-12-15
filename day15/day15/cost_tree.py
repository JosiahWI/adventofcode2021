def make_cost_tree(grid, pos):
    cost_tree = {pos : (None, 0)}
    from_positions = {pos}
    while from_positions:
        to_positions = set()
        for from_pos in from_positions:
            for to_pos in grid.adjacent(from_pos):
                from_cost = cost_tree[from_pos][1]
                to_cost = grid[to_pos]
                cost = from_cost + to_cost
                current = cost_tree.get(to_pos)
                if current is None or cost < current[1]:
                    cost_tree[to_pos] = (from_pos, cost)
                    to_positions.add(to_pos)
        from_positions = to_positions
    return cost_tree
