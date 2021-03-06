#!/usr/bin/env python3
import sys

def usage():
    print('Usage: iq <file>')
    sys.exit(1)


def transpose_reference(ref):
    # A = 65; O = 79
    if len(ref) == 3:
        try:
            # assume integer-integer-letter
            x = int(ref[0]) * 10 + int(ref[1])
            y = ref[2]
        except:
            # else, letter-integer-integer
            x = ref[0]
            y = int(ref[1]) * 10 + int(ref[2])
    else:
        x = ref[0]
        y = ref[1]

    try:
        first = ord(x) - ord('A') + 1
        second = chr(int(y)+ 64)
    except:
        first = chr(int(x)+ 64)
        second = ord(y) - ord('A') + 1

    return str(first) + str(second)


def prepare_move_string(data, score, name, rack, challenge=False):

    if challenge:
        move_array = data[3].split('_')
        position = transpose_reference(move_array[0])
        word = move_array[1].swapcase()
        points = int(move_array[2])
    else:
        # data[4], data[5] are discarded
        position = transpose_reference(data[1])
        word = data[2].swapcase()
        points = int(data[3])

    score = score + points
    move_string = f'>{name}: {rack} {position} {word} +{points} {score}'

    if challenge:
        score = score - points
        move_string = move_string + '\n' + f'>{name}: {rack} --  -{points} {score}'

    return move_string, score


def prepare_new_rack(data, rack, challenge=False):
    if challenge:
        new_rack = rack
    else:
        new_rack = data[6].upper()
    return new_rack


def parse_moves(meta, data):
    score = 0
    name = ""
    moves = []

    _meta = meta.split()
    name = _meta[0]
    rack = _meta[2].upper()

    data = data.split()

    while data:

        if data[0] == "MOVE":
            move_string, score = prepare_move_string(data, score, name, rack)
            new_rack = prepare_new_rack(data, rack)
            moves.append(move_string)
            rack = new_rack

        elif  data[0] == "PAS":
            if data[3] == '---':
                # actual pass scores nothing, but why not record it
                break
            # this pass is a correct challenge
            move_string, score = prepare_move_string(data, score, name, rack, True)
            new_rack = prepare_new_rack(data, rack)
            moves.append(move_string)
            rack = new_rack

        elif data[0] == "CHANGE":
            new_rack = data[1].upper()
            number = data[4]
            points = 0
            move = f'>{name}: {rack} -{number} +{points} {score}'
            moves.append(move)
            rack = new_rack

        # Nothing else really matters. Countback will be calculated by Quackle
        data = data[1:]

    return name, moves


def main():

    if len(sys.argv) != 2:
        usage()

    filename = sys.argv[1]
    try:
        f = open(filename, 'r')
        lines = f.read().splitlines()
    except:
        print('Could not read the file')
        sys.exit(1)


    meta = lines[3]
    data = lines[4]
    name_a, moves_a = parse_moves(meta, data)

    meta = lines[6]
    data = lines[7]
    name_b, moves_b = parse_moves(meta, data)

    # Quackle headers
    print("#character-encoding UTF-8")
    print(f'#player1 {name_a} {name_a}')
    print(f'#player2 {name_b} {name_b}')

    # Combine playerA, playerB, playerA
    combo = []
    while True:
        try:
            combo.append(moves_a.pop(0))
            combo.append(moves_b.pop(0))
        except IndexError:
            break
    for c in combo:
        print(c)


if __name__ == "__main__":
    main()

