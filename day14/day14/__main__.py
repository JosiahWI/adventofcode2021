from more_itertools import pairwise

from collections import Counter, defaultdict
import sys

# strip is important here because the newline would become template[-1]
polymer = list(sys.stdin.readline().strip())

# empty line between the input blocks
sys.stdin.readline()

insertion_pairs = dict(line.strip().split(" -> ") for line in sys.stdin)
counts = {pair : c for pair, c in Counter(pairwise(polymer)).most_common()}
element_counts = {element : c for element, c in Counter(polymer).most_common()}

for _ in range(40):
    new_counts = defaultdict(int)
    for pair, count in counts.items():
        a, c = pair
        b = insertion_pairs.get(f"{a}{c}")
        if b is None:
            continue
        element_counts[b] = element_counts.get(b, 0) + count
        new_counts[(a, c)] = new_counts[(a, c)] - count
        new_counts[(a, b)] = new_counts[(a, b)] + count
        new_counts[(b, c)] = new_counts[(b, c)] + count
    for pair, count in new_counts.items():
        counts[pair] = counts.get(pair, 0) + count

print(f"{max(element_counts.values()) - min(element_counts.values())}")
