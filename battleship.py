"""A."""


import random


def get_input() -> tuple:
    """A."""
    while 1:
        seed = input('Enter the seed: ')
        try:
            int(seed)
        except:
            continue
        seed = int(seed)
        break
    while 1:
        width = input('Enter the width of the board: ')
        try:
            int(width)
        except:
            continue
        width = int(width)
        if width > 0:
            break
    while 1:
        height = input('Enter the height of the board: ')
        try:
            int(height)
        except:
            continue
        height = int(height)
        if height > 0:
            break
    return seed, width, height


def get_data() -> list:
    """A."""
    seed, width, height = get_input()
    data = []
    data1 = []
    fname = input('Enter the name of the file containing your ship placements: ')
    with open('./UserShips/%s' % fname) as f:
        data = f.readlines()
    for i, s in enumerate(data):
        if i == len(data) - 1:
            s = s.split()
            for j in range(1, len(s)):
                s[j] = int(s[j])
            data1.append(s)
            continue
        s = s[:-1].split()
        for j in range(1, len(s)):
            s[j] = int(s[j])
        data1.append(s)
    while 1:
        print('Choose your AI.\n1. Random\n2. Smart\n3. Cheater')
        mode = input(' Your choice: ')
        try:
            int(mode)
        except:
            continue
        mode = int(mode)
        if mode == 1:
            # print(mode)
            break
        elif mode == 2:
            # print(mode, mode)
            break
        elif mode == 3:
            # print(mode, mode, mode)
            break
        else:
            continue
    checkship(data1, width, height)
    return [seed, width, height, data1, mode]


def checkship(data: list, width: int, height: int) -> None:
    """A."""
    symbol = ['x', 'X', 'o', 'O', '*']
    for i, x in enumerate(data):
        for j, y in enumerate(symbol):
            if x[0] == y:
                print('Error symbol %s is already in use. Terminating game' % x[0])
                exit(0)
        for k in range(i + 1, len(data)):
            if x[0] == data[k][0]:
                # print('shit %s' % data[k][0])
                print('Error symbol %s is already in use. Terminating game' % x[0])
                exit(0)
        on_board(x, width, height)
        diagonal(x)
    on_top(data, width, height)


def on_board(x: list, width: int, height: int) -> None:
    """A."""
    # print(x, width, height)
    if x[1] > height or x[3] > height or x[2] > width or x[4] > width\
    or x[1] < 0 or x[3] < 0 or x[2] < 0 or x[4] < 0:
        print('Error %s is placed outside of the board. Terminating game.' % x[0])
        exit(0)


def diagonal(x: list) -> None:
    """A."""
    if (x[1] != x[3]) and (x[2] != x[4]):
        print('Ships cannot be placed diagonally. Terminating game.')
        exit(0)


def on_top(data: list, width: int, height: int) -> None:
    """A."""
    arr = [[0 for i in range(width)] for j in range(height)]
    for i, x in enumerate(data):
        if x[1] == x[3]:
            j = max(x[2], x[4]) + 1
            k = min(x[2], x[4])
            for l in range(k, j):
                arr[x[1]][l] += 1
                if arr[x[1]][l] > 1:
                    print('There is already a ship at location %d, %d. Terminating game.' % (x[1], l))
                    exit(0)
        elif x[2] == x[4]:
            j = max(x[1], x[3]) + 1
            k = min(x[1], x[3])
            for l in range(k, j):
                arr[l][x[2]] += 1
                if arr[l][x[2]] > 1:
                    print('There is already a ship at location %d, %d. Terminating game.' % (l, x[2]))
                    exit(0)


def user_board(width: int, height: int, data: list) -> list:
    """A."""
    board = [["*" for j in range(width)] for i in range(height)]
    for i, x in enumerate(data):
        if x[1] == x[3]:
            j = max(x[2], x[4]) + 1
            k = min(x[2], x[4])
            temp = j - k
            data[i].append(temp)
            for l in range(k, j):
                board[x[1]][l] = x[0]
        elif x[2] == x[4]:
            j = max(x[1], x[3]) + 1
            k = min(x[1], x[3])
            temp = j - k
            data[i].append(temp)
            for l in range(k, j):
                board[l][x[2]] = x[0]
    return board, data


def ai_board(width: int, height: int, data1: list) -> list:
    """A."""
    board = [["*" for j in range(width)] for i in range(height)]
    data1 = sorted(data1)
    for i, x in enumerate(data1):
        length = x[5]
        while 1:
            choice = random.choice(['vert', 'horz'])
            if choice == 'horz':
                lenwidth = width - length
                if lenwidth < 0:
                    continue
                row = random.randint(0, height - 1)
                temp = random.randint(0, lenwidth)
                flag = 0
                for j in range(temp, temp + length):
                    if board[row][j] != '*':
                        flag = 1
                if flag == 1:
                    continue
                for j in range(temp, temp + length):
                    board[row][j] = x[0]
                print('Placing ship from %d,%d to %d,%d.' % (row, temp, row, temp + length - 1))
                break
            elif choice == 'vert':
                lenheight = height - length
                if lenheight < 0:
                    continue
                temp = random.randint(0, lenheight)
                column = random.randint(0, width - 1)
                flag = 0
                for j in range(temp, temp + length):
                    # print(j, column, board)
                    if board[j][column] != '*':
                        flag = 1
                if flag == 1:
                    continue
                for j in range(temp, temp + length):
                    board[j][column] = x[0]
                print('Placing ship from %d,%d to %d,%d.' % (temp, column, temp + length - 1, column))
                break
    return board


def set_game() -> list:
    """A."""
    info = get_data()
    random.seed(info[0])
    # print(info[1], info[2], info[3])
    user, data1 = user_board(info[1], info[2], info[3])
    # print_board(user)
    ai = ai_board(info[1], info[2], data1)
    # print_board(ai)
    turn = random.randint(0, 1)
    return user, ai, info[4], turn


def print_board(mat: list) -> None:
    """A."""
    width = len(mat[0])
    height = len(mat)
    print(" ", end="")
    for i in range(width):
        print(" %d" % i, end="")
    print()
    for i in range(height):
        print(i, end="")
        for j in range(width):
            print(" %s" % mat[i][j], end="")
        print()


def declear_winner(turn: int):
    """A."""
    if turn == 1:
        print('You win!')
    else:
        print('The AI wins.')


def getpair(mat: list) -> tuple:
    """A."""
    width = len(mat[0])
    height = len(mat)
    while 1:
        pair = input('Enter row and column to fire on separated by a space: ')
        pair = pair.split(' ')
        if len(pair) != 2:
            continue
        if pair[0].isdigit():
            pair[0] = int(pair[0])
            if 0 <= pair[0] <= height - 1:
                if pair[1].isdigit():
                    pair[1] = int(pair[1])
                    if 0 <= pair[1] <= width - 1:
                        if mat[pair[0]][pair[1]] != 'O' or 'X':
                            return pair[0], pair[1]


def judge(mat: list, row: int, column: int) -> str:
    """A."""
    if mat[row][column] == '*':
        print('Miss!')
        return 'O'
    elif mat[row][column] != '*':
        temp = mat[row][column]
        mat[row][column] = 'X'
        flag = 0
        for i, x in enumerate(mat):
            for j in range(len(x)):
                if x[j] == temp:
                    flag = 1
        if flag == 0:
            print('You sunk my %s' % temp)
            return 'X'
        else:
            print('Hit!')
            return 'X'


def disp(user: list, scan: list):
    """A."""
    print('Scanning Board')
    print_board(scan)
    print()
    print('My Board')
    print_board(user)
    print()


def one_turn(user: list, ai: list, scan: list, shoot: list, turn: int):
    """A."""
    if turn == 0:
        disp(user, scan)
        row, column = getpair(ai)
        char = judge(ai, row, column)
        scan[row][column] = char
        ai[row][column] = char
        turn = 1
        return user, ai, scan, shoot, turn
    elif turn == 1:
        row, column = random.choice(shoot)
        i = shoot.index((row, column))
        shoot.pop(i)
        print('The AI fires at location (%d, %d)' % (row, column))
        char = judge(user, row, column)
        user[row][column] = char
        turn = 0
        return user, ai, scan, shoot, turn


def one_turn2(user: list, ai: list, scan: list, shoot: list, turn: int):
    """A."""
    if turn == 0:
        disp(user, scan)
        row, column = getpair(ai)
        char = judge(ai, row, column)
        scan[row][column] = char
        ai[row][column] = char
        turn = 1
        return user, ai, scan, shoot, turn
    elif turn == 1:
        row, column = shoot.pop()
        print('The AI fires at location (%d, %d)' % (row, column))
        char = judge(user, row, column)
        user[row][column] = char
        turn = 0
        return user, ai, scan, shoot, turn


def one_turn3(user: list, ai: list, scan: list, shoot: list, turn: int, shoot1: list, aimode: int):
    """A."""
    width = len(user[0])
    height = len(user)
    if turn == 0:
        disp(user, scan)
        row, column = getpair(ai)
        char = judge(ai, row, column)
        scan[row][column] = char
        ai[row][column] = char
        turn = 1
        return user, ai, scan, shoot, turn, shoot1, aimode
    elif turn == 1:
        # print(shoot1)
        if aimode == 0:
            row, column = random.choice(shoot)
            i = shoot.index((row, column))
            shoot.pop(i)
            print('The AI fires at location (%d, %d)' % (row, column))
            char = judge(user, row, column)
            user[row][column] = char
            if char == 'X':
                aimode = 1
                if row - 1 > -1:
                    if user[row - 1][column] != "X":
                        if user[row - 1][column] != "O":
                            if (row - 1, column) not in shoot1:
                                shoot1.append((row - 1, column))
                                try:
                                    shoot.remove((row - 1, column))
                                except:
                                    pass
                if row + 1 < height:
                    if user[row + 1][column] != "X":
                        if user[row + 1][column] != "O":
                            if (row + 1, column) not in shoot1:
                                shoot1.append((row + 1, column))
                                try:
                                    shoot.remove((row + 1, column))
                                except:
                                    pass
                if column - 1 > -1:
                    if user[row][column - 1] != "X":
                        if user[row][column - 1] != "O":
                            if (row, column - 1) not in shoot1:
                                shoot1.append((row, column - 1))
                                try:
                                    shoot.remove((row, column - 1))
                                except:
                                    pass
                if column + 1 < width:
                    if user[row][column + 1] != "X":
                        if user[row][column + 1] != "O":
                            if (row, column + 1) not in shoot1:
                                shoot1.append((row, column + 1))
                                try:
                                    shoot.remove((row, column + 1))
                                except:
                                    pass
                aimode = 1
            turn = 0
        elif aimode == 1:
            row, column = shoot1.pop(0)
            print('The AI fires at location (%d, %d)' % (row, column))
            char = judge(user, row, column)
            user[row][column] = char
            if char == 'X':
                aimode = 1
                if row - 1 > -1:
                    if user[row - 1][column] != "X":
                        if user[row - 1][column] != "O":
                            if (row - 1, column) not in shoot1:
                                shoot1.append((row - 1, column))
                                try:
                                    shoot.remove((row - 1, column))
                                except:
                                    pass
                if row + 1 < height:
                    if user[row + 1][column] != "X":
                        if user[row + 1][column] != "O":
                            if (row + 1, column) not in shoot1:
                                shoot1.append((row + 1, column))
                                try:
                                    shoot.remove((row + 1, column))
                                except:
                                    pass
                if column - 1 > -1:
                    if user[row][column - 1] != "X":
                        if user[row][column - 1] != "O":
                            if (row, column - 1) not in shoot1:
                                shoot1.append((row, column - 1))
                                try:
                                    shoot.remove((row, column - 1))
                                except:
                                    pass
                if column + 1 < width:
                    if user[row][column + 1] != "X":
                        if user[row][column + 1] != "O":
                            if (row, column + 1) not in shoot1:
                                shoot1.append((row, column + 1))
                                try:
                                    shoot.remove((row, column + 1))
                                except:
                                    pass
            turn = 0
            if len(shoot1) == 0:
                aimode = 0
        return user, ai, scan, shoot, turn, shoot1, aimode


def is_game_over(user: list, ai: list, turn: int, scan: list):
    """A."""
    if turn == 1:
        mat = ai
    else:
        mat = user
    flag = 0
    for i, x in enumerate(mat):
        for j in range(len(x)):
            # print(x[j])
            if x[j] != '*':
                if x[j] != 'X':
                    if x[j] != 'O':
                        flag = 1
    if flag == 1:
        return False
    else:
        disp(user, scan)
        return True


def randomai(user: list, ai: list, turn: int, width: int, height: int):
    """A."""
    shoot = []
    scan = [["*" for j in range(width)] for i in range(height)]
    for i in range(height):
        for j in range(width):
            shoot.append((i, j))
    while 1:
        user, ai, scan, shoot, turn = one_turn(user, ai, scan, shoot, turn)
        if is_game_over(user, ai, turn, scan):
            break
    declear_winner(turn)


def smartai(user: list, ai: list, turn: int, width: int, height: int):
    """A."""
    aimode = 0
    shoot = []
    shoot1 = []
    scan = [["*" for j in range(width)] for i in range(height)]
    for i in range(height):
        for j in range(width):
            shoot.append((i, j))
    while 1:
        user, ai, scan, shoot, turn, shoot1, aimode = one_turn3(user, ai, scan, shoot, turn, shoot1, aimode)
        if is_game_over(user, ai, turn, scan):
            break
    declear_winner(turn)


def cheatai(user: list, ai: list, turn: list, width: int, height: int):
    """A."""
    # print_board(user)
    shoot = []
    scan = [["*" for j in range(width)] for i in range(height)]
    for i, x in enumerate(user):
        for j, y in enumerate(x):
            if y != '*':
                # print((i, j))
                shoot.append((i, j))
    shoot = sorted(shoot, reverse=True)
    while 1:
        user, ai, scan, shoot, turn = one_turn2(user, ai, scan, shoot, turn)
        if is_game_over(user, ai, turn, scan):
            break
    declear_winner(turn)


def play() -> None:
    """A."""
    user, ai, mode, turn = set_game()
    width = len(user[0])
    height = len(user)
    if mode == 1:
        randomai(user, ai, turn, width, height)
    elif mode == 2:
        smartai(user, ai, turn, width, height)
    else:
        cheatai(user, ai, turn, width, height)


play()
