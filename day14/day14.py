from time import perf_counter


def mask(value, bitmask):
    # Set masked bits to 0
    value &= ~bitmask[0]
    # Enter masked 1s
    value |= bitmask[1]
    return value


def keymask(ikey, bitmask, keys, lasti=0):
    # value as binary string
    for i in range(lasti+1, 38):
        if bitmask[i] == '1':
            ikey |= 1 << 37-i
        elif bitmask[i] == 'X':
            keys = keymask(ikey | 1 << 37-i, bitmask, keys, i)
            keys = keymask(ikey & ~(1 << 37-i), bitmask, keys, i)
    keys.add(ikey)
    return keys


class Decoder:
    def __init__(self, bitmask):
        andmask = int(''.join((str(int(char != 'X')) for char in bitmask)), 2)
        ormask = int(''.join((str(int(char == '1')) for char in bitmask)), 2)
        self.mask = (andmask, ormask)
        self.memory = dict()

    def update_mem(self, key, value):
        self.memory[key] = mask(value, self.mask)

    def update_mask(self, bitmask):
        andmask = int(''.join((str(int(char != 'X')) for char in bitmask)), 2)
        ormask = int(''.join((str(int(char == '1')) for char in bitmask)), 2)
        self.mask = (andmask, ormask)

    def total_memory(self):
        return sum((self.memory[key] for key in self.memory))


class Addr_decoder:
    def __init__(self, bitmask):
        self.mask = bitmask
        self.memory = dict()

    def update_mem(self, ikey, value):
        for key in keymask(ikey, self.mask, set()):
            self.memory[key] = value

    def update_mask(self, bitmask):
        self.mask = bitmask

    def total_memory(self):
        return sum((self.memory[key] for key in self.memory))


def decode(line_list):
    emulator = Decoder(line_list[0].split()[-1])
    for line in line_list[1:]:
        line = line.split()
        if line[0] == 'mask':
            emulator.update_mask(line[-1])
        else:
            key = line[0][4:-1]
            emulator.update_mem(key, int(line[-1]))
    return emulator.total_memory()


def decode_addr(line_list):
    emulator = Addr_decoder('0b' + line_list[0].split()[-1])
    for line in line_list[1:]:
        line = line.split()
        if line[0] == 'mask':
            emulator.update_mask('0b' + line[-1])
        else:
            ikey = int(line[0][4:-1])
            value = int(line[-1])
            emulator.update_mem(ikey, value)
    return emulator.total_memory()


def get_result(line_list, part):
    if part == 1:
        return decode(line_list)
    elif part == 2:
        return decode_addr(line_list)


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
    day = 14
    testvals = [51, 208]
    main()
