from collections import deque


backtrack_calls = 0
failures = 0


PEERS = {}
for _r in range(9):
    for _c in range(9):
        p = set()
        for i in range(9):
            if i != _c:
                p.add((_r, i))
            if i != _r:
                p.add((i, _c))
        br, bc = (_r // 3) * 3, (_c // 3) * 3
        for dr in range(3):
            for dc in range(3):
                nr, nc = br + dr, bc + dc
                if (nr, nc) != (_r, _c):
                    p.add((nr, nc))
        PEERS[(_r, _c)] = p


def read_board(filename):
    board = []
    with open(filename) as f:
        for line in f:
            board.append([int(ch) for ch in line.strip()])
    return board


def print_board(board):
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("------+-------+------")
        row_str = ""
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            row_str += str(val) + " "
        print(row_str.strip())


def make_domains(board):
    d = {}
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                d[(r, c)] = {board[r][c]}
            else:
                d[(r, c)] = set(range(1, 10))
    return d


def revise(domains, xi, xj):
    if len(domains[xj]) == 1:
        v = next(iter(domains[xj]))
        if v in domains[xi]:
            domains[xi].discard(v)
            return True
    return False


def ac3(domains):
    queue = deque()
    for cell in domains:
        for peer in PEERS[cell]:
            queue.append((cell, peer))

    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False
            for peer in PEERS[xi]:
                if peer != xj:
                    queue.append((peer, xi))
    return True


def select_cell(domains, board):
    best, best_len = None, 10
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                d = len(domains[(r, c)])
                if d < best_len:
                    best_len = d
                    best = (r, c)
    return best


def forward_check(domains, board, r, c, val):
    new_d = {k: set(v) for k, v in domains.items()}
    new_d[(r, c)] = {val}
    for pr, pc in PEERS[(r, c)]:
        if board[pr][pc] == 0:
            new_d[(pr, pc)].discard(val)
            if not new_d[(pr, pc)]:
                return None
    return new_d


def backtrack(board, domains):
    global backtrack_calls, failures
    backtrack_calls += 1

    cell = select_cell(domains, board)
    if cell is None:
        return True

    r, c = cell
    for val in sorted(domains[(r, c)]):
        board[r][c] = val
        new_domains = forward_check(domains, board, r, c, val)
        if new_domains is not None:
            if backtrack(board, new_domains):
                return True
        board[r][c] = 0

    failures += 1
    return False


def solve(filename):
    global backtrack_calls, failures
    backtrack_calls = 0
    failures = 0

    board = read_board(filename)
    domains = make_domains(board)

    if not ac3(domains):
        print(f"\n[{filename}] No solution — AC-3 found contradiction.")
        return

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0 and len(domains[(r, c)]) == 1:
                board[r][c] = next(iter(domains[(r, c)]))

    success = backtrack(board, domains)

    print(f"\n{'='*38}")
    print(f"  {filename}")
    print(f"{'='*38}")
    if success:
        print_board(board)
    else:
        print("No solution found.")

    print(f"\n  Backtrack calls : {backtrack_calls}")
    print(f"  Failures        : {failures}")


if __name__ == "__main__":
    for f in ["easy.txt", "medium.txt", "hard.txt", "veryhard.txt"]:
        solve(f)
