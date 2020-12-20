from time import perf_counter


def get_side(tile, direction):
    if direction == 'U':
        return tile[0]
    elif direction == 'D':
        return tile[-1]
    elif direction == 'L':
        return ''.join([line[0] for line in tile])
    elif direction == 'R':
        return ''.join([line[-1] for line in tile])


def empty_sides(used_coords, check_coord):
    side_list = []
    if (check_coord[0], check_coord[1]+1) not in used_coords:
        side_list.append('U')
    if (check_coord[0], check_coord[1]-1) not in used_coords:
        side_list.append('D')
    if (check_coord[0]+1, check_coord[1]) not in used_coords:
        side_list.append('R')
    if (check_coord[0]-1, check_coord[1]) not in used_coords:
        side_list.append('L')
    return side_list


def adjacent(coord):
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return [tuple(coord[i] + vec[i] for i in range(2)) for vec in dirs]


class Tile:
    def __init__(self,  tile):
        self.side = dict()
        for direction in ['U', 'D', 'L', 'R']:
            self.side[direction] = get_side(tile, direction)
        self.fix_orient = False
        self.tile = tile
        self.internal = [line[1:-1] for line in self.tile[1:-1]]

    # sides are read up to down, left to right
    def rot(self):
        if not self.fix_orient:
            # anticlockwise rotation
            temp = dict()
            temp['U'] = self.side['R']
            temp['D'] = self.side['L']
            temp['L'] = self.side['U'][::-1]
            temp['R'] = self.side['D'][::-1]
            self.side = temp.copy()
            self.tile = [''.join(j)
                         for j in reversed([i for i in zip(*self.tile)])]

    def xflip(self):
        if not self.fix_orient:
            self.side['L'], self.side['R'] = self.side['R'], self.side['L']
            self.side['U'] = self.side['U'][::-1]
            self.side['D'] = self.side['D'][::-1]
            self.tile = [''.join(j[::-1]) for j in self.tile]

    def find_match(self, match_side, direction):
        if self.fix_orient:
            return self.side[direction] == match_side

        for i in range(2):
            if i:
                self.xflip()
            if self.side[direction] == match_side:
                self.fix_orient = True
                self.internal = [line[1:-1] for line in self.tile[1:-1]]
                return True
            for i in range(3):
                self.rot()
                if self.side[direction] == match_side:
                    self.fix_orient = True
                    self.internal = [line[1:-1] for line in self.tile[1:-1]]
                    return True
        return False

    def __repr__(self):
        return '\n'.join(self.internal)

    def __str__(self):
        return '\n'.join(self.tile)


class Tileimage:
    def __init__(self, tile_init):
        self.id_array = dict()
        # key = coords, val = id - this is our image
        self.id_array[(0, 0)] = tile_init
        # start with a random tile in the middle, doesn't matter which
        self.perimeter = set([(0, 0)])
        # only try to match tiles to the perimeter of the image

    def add_tile(self, unplaced_ids, tile_dict):
        # choose a coord on the perimeter to add a new tile to
        opp_dir = {'D': 'U', 'U': 'D', 'L': 'R', 'R': 'L'}
        dirvec = {'D': (0, -1), 'U': (0, 1), 'R': (1, 0), 'L': (-1, 0)}
        coord = self.perimeter.pop()
        # print(coord, self.perimeter)
        side_list = empty_sides(self.id_array.keys(), coord)
        # find empty sides which we can attach a tile to
        check_set = set()
        for direction in side_list:
            match_side = tile_dict[self.id_array[coord]].side[direction]
            # this is the border we are aiming to match
            for t_id in unplaced_ids:
                # iterate through unplaced ids
                if tile_dict[t_id].find_match(match_side, opp_dir[direction]):
                    # match found! update id_array with new id
                    new_coords = tuple(coord[i] + dirvec[direction][i]
                                       for i in range(2))
                    self.id_array[new_coords] = t_id
                    check_set.add(new_coords)
                    break
            # remove from unplaced ids
            for disc_coord in check_set:
                unplaced_ids.discard(self.id_array[disc_coord])

        # fix perimeter
        for new_coord in check_set:
            if empty_sides(self.id_array.keys(), new_coord):
                # new coord is on the perimeter
                self.perimeter.add(new_coord)
            for check_coord in adjacent(new_coord):
                if not empty_sides(self.id_array.keys(), check_coord):
                    # if new tile encloses an old tile, remove from perimeter
                    self.perimeter.discard(check_coord)
        return unplaced_ids

    def multiply_corners(self):
        xs = [coord[0] for coord in self.id_array.keys()]
        ys = [coord[1] for coord in self.id_array.keys()]
        maxx, minx = max(xs), min(xs)
        maxy, miny = max(ys), min(ys)
        return (self.id_array[(maxx, maxy)] *
                self.id_array[(maxx, miny)] *
                self.id_array[(minx, maxy)] *
                self.id_array[(minx, miny)])

    def stitch_image(self, tile_dict):
        xs = [coord[0] for coord in self.id_array.keys()]
        ys = [coord[1] for coord in self.id_array.keys()]
        maxx, minx = max(xs), min(xs)
        maxy, miny = max(ys), min(ys)
        stitched_image = []
        for y in range(maxy, miny-1, -1):
            zippd = zip(*[tile_dict[self.id_array[(x, y)]].internal
                          for x in range(minx, maxx+1)])
            xstitched = [''.join(st) for st in zippd]
            stitched_image.extend(xstitched)
        return Tile(stitched_image)


def create_image(line_list):
    tile_dict = dict()
    # key = id, val = Tile - this is the dict of our tiles
    for tilelst in line_list:
        tilelst = tilelst.split('\n')
        tile_id = int(tilelst[0].split()[1][:-1])
        tile_dict[tile_id] = Tile(tilelst[1:])

    unplaced_ids = set(tile_dict.keys())
    # keep track of tiles yet to place
    init_tile = min(tile_dict.keys())
    image = Tileimage(init_tile)
    unplaced_ids.discard(init_tile)
    while unplaced_ids:
        # i.e. while there are still tiles we haven't yet placed in the image
        unplaced_ids = image.add_tile(unplaced_ids, tile_dict)

    combined_tile = image.stitch_image(tile_dict)
    return image, combined_tile


def count_monsters(combined_tile):
    with open("seamonster.txt") as monster_input:
        monster = monster_input.read().split('\n')
    monster_coords = set()
    for i in range(3):
        for j in range(len(monster[0])):
            if monster[i][j] == '#':
                monster_coords.add((i, j))
    monsters_found = 0
    for x in range(len(combined_tile.tile[0])-18):
        for y in range(len(combined_tile.tile)-2):
            if all((combined_tile.tile[y+coord[0]][x+coord[1]] == '#'
                   for coord in monster_coords)):
                monsters_found += 1
    return monsters_found


def rough_water(combined_tile):
    tothash = sum(char == '#' for char in ''.join(combined_tile.tile))
    monsters_found = 0
    monsters_found += count_monsters(combined_tile)
    for i in range(2):
        if i:
            combined_tile.xflip()
        monsters_found += count_monsters(combined_tile)
        if monsters_found:
            break
        for _ in range(3):
            combined_tile.rot()
            monsters_found += count_monsters(combined_tile)
            if monsters_found:
                break
    return tothash - monsters_found*15


def get_result(line_list, part):
    if part == 1:
        return create_image(line_list)[0].multiply_corners()
    elif part == 2:
        return rough_water(create_image(line_list)[1])


def test(day, targetvals):
    # Open test data, split by eq
    with open("day" + str(day) + "_test.txt") as input_file:
        read_data = input_file.read()
        line_list = read_data.split('\n\n')
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
        # Open input data, split by eq
        with open("day" + str(day) + "_input.txt") as input_file:
            read_data = input_file.read()
            line_list = read_data.split('\n\n')
        for i, _ in enumerate(testvals):
            tic = perf_counter()
            output = get_result(line_list, i + 1)
            toc = perf_counter()
            print(f'Part {i+1}: {output}')
            print(f'This took {toc-tic:0.7f} seconds')


if __name__ == "__main__":
    day = 20
    testvals = [20899048083289, 273]
    main()
