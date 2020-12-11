from time import perf_counter


def adjacents(seats, x, y, n, m):
    checkseats = ((x-1, y-1), (x-1, y), (x-1, y+1),
                  (x, y-1),             (x, y+1),
                  (x+1, y-1), (x+1, y), (x+1, y+1))
    # Count adjacent occupied seats
    return sum((seats[i][j] == 2 for i, j in checkseats
                if 0 <= i < n and 0 <= j < m))


def adj_view(seats, x, y, n, m):
    seen_occupied = 0
    vectors = ((-1, -1), (-1, 0), (-1, 1),
               (0, -1),           (0, 1),
               (1, -1),  (1, 0),  (1, 1))
    for vec in vectors:
        xrg, yrg = x, y
        # Move in each direction until find another seat or hit wall
        xrg += vec[0]
        yrg += vec[1]
        while 0 <= xrg < n and 0 <= yrg < m:
            if seats[xrg][yrg] != 0 and (xrg, yrg) != (x, y):
                seen_occupied += seats[xrg][yrg] == 2
                break
            xrg += vec[0]
            yrg += vec[1]
    return seen_occupied


def one_step_seating(seat_plan, n, m):
    new_seat_plan = [line.copy() for line in seat_plan]
    for x in range(n):
        for y in range(m):
            state = seat_plan[x][y]
            if state != 0:
                adj = adjacents(seat_plan, x, y, n, m)
            # if empty and nobody adjacent, turn to occupied
            if state == 1 and adj == 0:
                new_seat_plan[x][y] = 2
            # elif occupied and > 3 adjacent, turn to empty
            elif state == 2 and adj > 3:
                new_seat_plan[x][y] = 1
    return new_seat_plan


def two_step_seating(seat_plan, n, m):
    new_seat_plan = [line.copy() for line in seat_plan]
    for x in range(n):
        for y in range(m):
            state = seat_plan[x][y]
            if state != 0:
                adj = adj_view(seat_plan, x, y, n, m)
            # if empty and nobody adjacent, turn to occupied
            if state == 1 and adj == 0:
                new_seat_plan[x][y] = 2
            # elif occupied and > 3 adjacent, turn to empty
            elif state == 2 and adj > 4:
                new_seat_plan[x][y] = 1
    return new_seat_plan


def get_result(line_list, part):
    n = len(line_list)
    m = len(line_list[0])
    old_seating = []
    new_seating = [[0]*m for _ in range(n)]
    # 0 is floor, 1 is not occupied, 2 is occupied
    for x in range(n):
        for y in range(m):
            if line_list[x][y] == 'L':
                new_seating[x][y] = 1
    while old_seating != new_seating:
        old_seating = [line.copy() for line in new_seating]
        if part == 1:
            new_seating = one_step_seating(old_seating, n, m)
        elif part == 2:
            new_seating = two_step_seating(old_seating, n, m)

    return sum([line.count(2) for line in new_seating])


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
    day = 11
    testvals = [37, 26]
    main()
