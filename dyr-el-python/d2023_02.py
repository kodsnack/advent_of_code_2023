from aoc_prepare import PrepareAoc

def parse(inp):
    return [(int(game_no.split(' ')[1]), 
             [[(int(round[0]), round[1]) 
               for round in map(lambda x: x.split(), game.split(', '))]
              for game in game_rest.split('; ')])
            for game_no, _, game_rest in map(lambda x: x.partition(': '),
                                             inp.splitlines())]

def part1(inp):
    games = parse(inp)
    result = 0
    limit = {"red": 12, "green": 13, "blue":14}
    for game in games:
        game_number = game[0]
        possible_game = True
        for round in game[1]:
            for part in round:
                if part[0] > limit[part[1]]:
                    possible_game = False
                    break
            if possible_game == False:
                break
        if possible_game:
            result += game_number
    return result


def part2(inp):
    games = parse(inp)
    result = 0
    for game in games:
        max_cubes = dict()
        for round in game[1]:
            for part in round:
                max_cubes[part[1]] = max(max_cubes.get(part[1], 0), part[0])
        assert len(max_cubes) >= 3
        result += (max_cubes['green'] * max_cubes['blue'] * max_cubes['red'])
    return result    


def test_1_1():
    assert 8 == part1("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""")


def test_2_1():
    assert 2286 == part2("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""")


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 2)
    main(prep.get_content())