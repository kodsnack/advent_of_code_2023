import itertools


def get_galaxies(image, koef=1):
    galaxies = {}

    row_dots_indices = [
        i for i, row in enumerate(image) if all(element == "." for element in row)
    ]
    col_dots_indices = [
        i for i, col in enumerate(zip(*image)) if all(element == "." for element in col)
    ]

    for i, row in enumerate(image):
        for j, col in enumerate(row):
            if col.isdigit():
                i_galaxy, j_galaxy = i, j
                for idx, row_idx in enumerate(row_dots_indices[::-1]):
                    if i_galaxy > row_idx:
                        i_galaxy += (len(row_dots_indices) - idx) * (koef - 1)
                        break
                for idx, col_idx in enumerate(col_dots_indices[::-1]):
                    if j_galaxy > col_idx:
                        j_galaxy += (len(col_dots_indices) - idx) * (koef - 1)
                        break
                galaxies[col] = (i_galaxy, j_galaxy)

    print(galaxies)
    return galaxies


def get_dist(first_coord, second_coord):
    x1, y1 = first_coord
    x2, y2 = second_coord
    return abs(x1 - x2) + abs(y1 - y2)


def part1(path, koef=1):
    with open(path, "r") as f:
        image = f.read().split("\n")
        counter = itertools.count(1)
        image = [
            list(
                str(next(counter)) if symbol == "#" else symbol for symbol in list(line)
            )
            for line in image
        ]

        galaxies = get_galaxies(image, koef)

        total = 0
        for k1, v1 in galaxies.items():
            for k2, v2 in galaxies.items():
                if k1 < k2:
                    total += get_dist(v1, v2)

        return total


if __name__ == "__main__":
    # print(part1('test.txt'))
    print(part1("input.txt"))
    # print(part1('test.txt', 10))
    # print(part1('test.txt', 100))
    print(part1("input.txt", 1000000))
