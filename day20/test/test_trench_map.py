from collections import defaultdict

from day20 import TrenchMap

ENHANCEMENT_STRING = \
"..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###.."\
"######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.#####"\
"#.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##"\
"..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#"\
".##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#"\
".##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#."\
"#.#...##..#.#..###..#####........#..####......#..#"

def test_pixels_to_ints():
    input_pixels = "#.###..#...."
    expected = [1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0]
    assert list(TrenchMap.pxls_to_ints(input_pixels)) == expected

def test_enhance_pixel():
    image = defaultdict(int)
    image[(1, 2)] = 1
    image[(2, 2)] = 1
    enhancement_table = defaultdict(int)
    enhancement_table[3] = 1
    trenches = TrenchMap(image, enhancement_table)
    assert image[(1, 1)] == 0
    assert trenches.enhance_state((1, 1)) == 1

def test_enhance_image():
    image = defaultdict(int)
    image.update({
        (0, 0) : 1,
        (3, 0) : 1,
        (0, 1) : 1,
        (0, 2) : 1,
        (1, 2) : 1,
        (4, 2) : 1,
        (2, 3) : 1,
        (2, 4) : 1,
        (3, 4) : 1,
        (4, 4) : 1
    })

    expected = {
        (0, -1) : 1,
        (1, -1) : 1,
        (3, -1) : 1,
        (4, -1) : 1,
        (-1, 0) : 1,
        (2, 0) : 1,
        (4, 0) : 1,
        (-1, 1) : 1,
        (0, 1) : 1,
        (2, 1) : 1,
        (5, 1) : 1,
        (-1, 2) : 1,
        (0, 2) : 1,
        (1, 2) : 1,
        (2, 2) : 1,
        (5, 2) : 1,
        (0, 3) : 1,
        (3, 3) : 1,
        (4, 3) : 1,
        (1, 4) : 1,
        (2, 4) : 1,
        (5, 4) : 1,
        (2, 5) : 1,
        (4, 5) : 1
}

    enhancement_table = list(TrenchMap.pxls_to_ints(ENHANCEMENT_STRING))
    trenches = TrenchMap(image, enhancement_table)
    print(trenches.enhance_state((4, 0)))
    trenches.enhance()
    assert trenches.pxls_lit == 24
    for coord, state in expected.items():
        assert trenches.image[coord] == state
