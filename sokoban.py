import os

# 定义地图：'#' 墙，' ' 地面，'.' 目标，'$' 箱子，'@' 玩家
level = [
    "#####",
    "# . #",
    "# $ #",
    "# @ #",
    "#####"
]

def find_player(map_data):
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == '@':
                return x, y
    return None, None

def print_map(map_data):
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in map_data:
        print(''.join(row))

def move(map_data, dx, dy):
    px, py = find_player(map_data)
    tx, ty = px + dx, py + dy
    nx, ny = px + dx*2, py + dy*2
    target_cell = map_data[ty][tx]
    beyond_cell = map_data[ny][nx] if 0 <= nx < len(map_data[0]) and 0 <= ny < len(map_data) else '#'

    # 玩家能否移动？
    if target_cell in ' .$':
        if target_cell == '$':
            if beyond_cell in ' .':
                # 推箱子
                map_data[ny] = map_data[ny][:nx] + '$' + map_data[ny][nx+1:]
                map_data[ty] = map_data[ty][:tx] + '@' + map_data[ty][tx+1:]
                map_data[py] = map_data[py][:px] + (' ' if level[py][px] == ' ' else '.') + map_data[py][px+1:]
        else:
            map_data[ty] = map_data[ty][:tx] + '@' + map_data[ty][tx+1:]
            map_data[py] = map_data[py][:px] + (' ' if level[py][px] == ' ' else '.') + map_data[py][px+1:]
    return map_data

def is_win(map_data):
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if level[y][x] == '.' and map_data[y][x] != '$':
                return False
    return True

def main():
    cur_map = [list(row) for row in level]
    while True:
        print_map(cur_map)
        if is_win(cur_map):
            print("恭喜通关！")
            break
        key = input('输入 w 上  s 下  a 左  d 右，q 退出：').lower()
        if key == 'w':
            cur_map = move(cur_map, 0, -1)
        elif key == 's':
            cur_map = move(cur_map, 0, 1)
        elif key == 'a':
            cur_map = move(cur_map, -1, 0)
        elif key == 'd':
            cur_map = move(cur_map, 1, 0)
        elif key == 'q':
            break

if __name__ == "__main__":
    main()