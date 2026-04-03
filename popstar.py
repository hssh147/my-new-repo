import random
import os
import sys

ROWS = 10
COLS = 10
COLORS = ['R', 'G', 'B', 'Y', 'P']  # 红、绿、蓝、黄、紫

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def random_board():
    return [[random.choice(COLORS) for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board, score):
    clear_screen()
    print(f"分数: {score}")
    print("   " + " ".join(str(i) for i in range(COLS)))
    for i, row in enumerate(board):
        print(f"{i:2} " + " ".join(c if c else '.' for c in row))
    print("输入格式：行 列，如 2 3，q 退出")

def neighbors(board, x, y):
    color = board[x][y]
    nbs = []
    for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
        nx, ny = x+dx, y+dy
        if 0<=nx<ROWS and 0<=ny<COLS and board[nx][ny]==color:
            nbs.append((nx, ny))
    return nbs

def flood(board, x, y, visited):
    color = board[x][y]
    blocks = [(x, y)]
    visited.add((x, y))
    for nx, ny in neighbors(board, x, y):
        if (nx, ny) not in visited:
            blocks += flood(board, nx, ny, visited)
    return blocks

def drop_down(board):
    for col in range(COLS):
        stack = [board[row][col] for row in range(ROWS) if board[row][col]]
        empties = ROWS - len(stack)
        for row in range(ROWS):
            board[row][col] = None
        for i in range(len(stack)):
            board[ROWS-1-i][col] = stack[-1-i]
    # 左移（清空整列）
    shift = 0
    for col in range(COLS):
        if all(board[row][col] is None for row in range(ROWS)):
            shift += 1
        elif shift:
            for row in range(ROWS):
                board[row][col-shift], board[row][col] = board[row][col], None

def has_moves(board):
    for x in range(ROWS):
        for y in range(COLS):
            if board[x][y]:
                for nx, ny in neighbors(board, x, y):
                    if board[nx][ny]:
                        return True
    return False

def main():
    board = random_board()
    score = 0

    while True:
        print_board(board, score)
        if not has_moves(board):
            print("游戏结束！最终得分：", score)
            break
        inp = input('你的操作:').strip()
        if inp.lower() == 'q':
            print("退出游戏.")
            break
        try:
            x, y = map(int, inp.split())
            if not (0 <= x < ROWS and 0 <= y < COLS):
                raise ValueError
            if not board[x][y]:
                print("空格子，换一个。")
                continue
            group = flood(board, x, y, set())
            if len(group) < 2:
                print("必须选择相连的两个及以上同色方块！")
                continue
            for gx, gy in group:
                board[gx][gy] = None
            score += len(group) ** 2
            drop_down(board)
        except Exception:
            print("输入格式错误，请输入 行 列，比如 2 3")

if __name__ == '__main__':
    main()
