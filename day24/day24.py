from time import perf_counter

cardinal_map = {'e': (1, -1, 0), 'ne': (1, 0, -1), 'se': (0, -1, 1),
                'w': (-1, 1, 0), 'sw': (-1, 0, 1), 'nw': (0, 1, -1)}


class Hexagon:
    def __init__(self):
        self.isblack = False

    def flip(self):
        self.isblack = not self.isblack

    def __repr__(self):
        return 'Black' if self.isblack else 'White'


class Hexgrid:
    def __init__(self):
        self.hexagon_locs = dict()

    def fliphex(self, pos):
        gon = self.hexagon_locs.setdefault(pos, Hexagon())
        gon.flip()

    def tot_black(self):
        return sum((gon.isblack for gon in self.hexagon_locs.values()))

    def adj_black(self, pos):
        adj_positions = {tuple(sum(direction) for direction in zip(pos, card))
                         for card in cardinal_map.values()}
        black_sum = 0
        for newpos in adj_positions:
            gon = self.hexagon_locs.setdefault(newpos, Hexagon())
            black_sum += gon.isblack
        return black_sum

    def prep_tiles(self):
        for gon in set(self.hexagon_locs.keys()):
            self.adj_black(gon)

    def step(self):
        toflip = set()
        cur_positions = set(self.hexagon_locs.keys())
        for pos in cur_positions:
            if self.hexagon_locs[pos].isblack:
                if not self.adj_black(pos) in {1, 2}:
                    toflip.add(pos)
            else:
                if self.adj_black(pos) == 2:
                    toflip.add(pos)
        for pos in toflip:
            self.hexagon_locs[pos].flip()


def translate_cardinal(string):
    i = 0
    moves = []
    while i < len(string):
        if string[i] in {'n', 's'}:
            moves.append(cardinal_map[string[i:i+2]])
            i += 2
        else:
            moves.append(cardinal_map[string[i]])
            i += 1
    return tuple(sum(direction) for direction in zip(*moves))


def lobby_layout(line_list):
    grid = Hexgrid()
    for line in line_list:
        pos = translate_cardinal(line)
        grid.fliphex(pos)
    return grid.tot_black(), grid


def hex_conway(line_list):
    grid = lobby_layout(line_list)[1]
    grid.prep_tiles()
    for _ in range(100):
        grid.step()
    return grid.tot_black()


def get_result(line_list, part):
    if part == 1:
        return lobby_layout(line_list)[0]
    elif part == 2:
        return hex_conway(line_list)


def test(day, targetvals):
    # Open test data, split by line
    with open("day" + str(day) + "_test.txt") as input_file:
        read_data = input_file.read()
        line_list = read_data.split('\n')
    resultvals = [0 for _ in range(len(targetvals))]
    for i, _ in enumerate(targetvals):
        resultvals[i] = get_result(line_list, i + 1)
        if resultvals[i] != testvals[i]:
            print(f'Test part {i+1} fails: expected '
                  f'{testvals[i]} but got {resultvals[i]}')
    return resultvals == testvals


def main():
    # Only run functions on the input if tests pass
    if test(day, testvals):
        # Open input data, split by line
        with open("day" + str(day) + "_input.txt") as input_file:
            read_data = input_file.read()
            line_list = read_data.split('\n')
        for i, _ in enumerate(testvals):
            tic = perf_counter()
            output = get_result(line_list, i + 1)
            toc = perf_counter()
            print(f'Part {i+1}: {output}')
            print(f'This took {toc-tic:0.7f} seconds')


if __name__ == "__main__":
    day = 24
    testvals = [10, 2208]
    main()
