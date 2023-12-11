def find_adj_cord(i, j, maze):
    adjacent_coordinates = [
        (i - 1, j),  # top
        (i, j - 1),  # left
        (i, j + 1),  # right
        (i + 1, j),  # bottom
    ]
    return adjacent_coordinates


def is_connected(s, ac, maze, maze_dist):
    orig_char = maze[s[0]][s[1]]
    target_char = maze[ac[0]][ac[1]]
    i, j = s[0], s[1]
    x, y = ac[0], ac[1]
    if x == i - 1 and y == j:
        # direction = "n"
        if orig_char in "|LJS" and target_char in "|7F":
            return True, "n"
        else:
            return False
    elif x == i + 1 and y == j:
        # direction = "s"
        if orig_char in "|F7S" and target_char in "|JL":
            return True, "s"
        else:
            return False
    elif x == i and y == j - 1:
        # direction = "w"
        if orig_char in "-7JS" and target_char in "-FL":
            return True, "w"
        else:
            return False
    elif x == i and y == j + 1:
        # direction = "e"
        if orig_char in "-FLS" and target_char in "-7J":
            return True, "e"
        else:
            return False


def solve_part_one(input_data):
    maze = []
    maze_dist = []
    rows = input_data.splitlines()
    for row in rows:
        maze.append(list(row))
        maze_dist.append(["." for _ in range(len(row))])
    for row in maze:
        if "S" in row:
            sublist_index = maze.index(row)
            char_index = row.index("S")
            s_pos = (sublist_index, char_index)
    adj_cord_s = find_adj_cord(sublist_index, char_index, maze)
    temp_cords = []
    for cord in adj_cord_s:
        if 0 <= cord[0] < len(maze) and 0 <= cord[1] < len(maze[1]):
            if is_connected(s_pos, cord, maze, maze_dist):
                maze_dist[cord[0]][cord[1]] = "1"
                temp_cords.append(cord)
    running = True
    counter = 2
    sum = 0
    while running:
        temp_cords2 = []
        for iy, cord in enumerate(temp_cords):
            adj_cord_s = find_adj_cord(cord[0], cord[1], maze)
            for ix, ac in enumerate(adj_cord_s):
                if 0 <= cord[0] < len(maze) and 0 <= cord[1] < len(maze[1]):
                    if 0 <= ac[0] < len(maze) and 0 <= ac[1] < len(maze[1]):
                        if 0 <= ac[0] < len(maze) and 0 <= ac[1] < len(maze[1]):
                            if is_connected(cord, ac, maze, maze_dist):
                                if maze_dist[ac[0]][ac[1]] == ".":
                                    maze_dist[ac[0]][ac[1]] = str(counter)
                                    sum = counter
                                    temp_cords2.append(ac)

        temp_cords = temp_cords2
        counter += 1
        if not temp_cords:
            running = False
    return sum


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_data = file.read()

    part_one_solution = solve_part_one(input_data)
    print(f"Part One Solution: {part_one_solution}")
