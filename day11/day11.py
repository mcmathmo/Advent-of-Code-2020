from time import perf_counter


def adjacents(seats, x, y, n, m):
    checkseats = ((x-1, y-1), (x-1, y), (x-1, y+1),
                  (x, y-1),             (x, y+1),
                  (x+1, y-1), (x+1, y), (x+1, y+1))
    # Count adjacent occupied seats
    seen_occupied = 0
    for i, j in checkseats:
        if 0 <= i < n and 0 <= j < m:
            seen_occupied += seats[i][j] == 2
        if seen_occupied > 3:
            return True
    return False


def adjempt(seats, x, y, n, m):
    checkseats = ((x-1, y-1), (x-1, y), (x-1, y+1),
                  (x, y-1),             (x, y+1),
                  (x+1, y-1), (x+1, y), (x+1, y+1))
    # Count adjacent occupied seats)
    return not any((seats[i][j] == 2 for i, j in checkseats
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
                if seen_occupied > 4:
                    return True
                break
            xrg += vec[0]
            yrg += vec[1]

    return False


def adj_view_empty(seats, x, y, n, m):
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
                if seats[xrg][yrg] == 2:
                    return False
                break
            xrg += vec[0]
            yrg += vec[1]
    return True


def one_step_seating(seat_plan, n, m):
    new_seat_plan = [line.copy() for line in seat_plan]
    for x in range(n):
        for y in range(m):
            state = seat_plan[x][y]
            # if empty and nobody adjacent, turn to occupied
            if state == 1 and adjempt(seat_plan, x, y, n, m):
                new_seat_plan[x][y] = 2
            # elif occupied and > 3 adjacent, turn to empty
            elif state == 2 and adjacents(seat_plan, x, y, n, m):
                new_seat_plan[x][y] = 1
    return new_seat_plan


def two_step_seating(seat_plan, n, m):
    new_seat_plan = [line.copy() for line in seat_plan]
    for x in range(n):
        for y in range(m):
            state = seat_plan[x][y]
            # if empty and nobody adjacent, turn to occupied
            if state == 1 and adj_view_empty(seat_plan, x, y, n, m):
                new_seat_plan[x][y] = 2
            # elif occupied and > 3 adjacent, turn to empty
            elif state == 2 and adj_view(seat_plan, x, y, n, m):
                new_seat_plan[x][y] = 1
    return new_seat_plan


def get_result(line_list, part):
    n = len(line_list)
    m = len(line_list[0])
    old_seating = []
    new_seating = [[char == 'L' for char in line] for line in line_list]
    # 0 is floor, 1 is not occupied, 2 is occupied
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
