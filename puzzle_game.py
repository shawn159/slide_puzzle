from bangtal import *
import random
import time
import os

setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)

FROZ = 0
MOAN = 1

CURR_GAME = FROZ

U = 0
D = 1
R = 2
L = 3

start_scene = Scene('즐거운 퍼즐 놀이~', 'puzzle_images/start_scene.png')
frozen_scene = Scene('Frozen2', 'puzzle_images/frozen/frozen_background.png')
moana_scene = Scene('Moana', 'puzzle_images/moana/moana_background.png')

frozen = Object('puzzle_images/frozen/frozen.jpg')
frozen_end = Object('puzzle_images/frozen/frozen.jpg')
moana = Object('puzzle_images/moana/moana.png')
moana_end = Object('puzzle_images/moana/moana.png')
screen = Object('puzzle_images/transparent_screen.png')


frozen.setScale(0.4)
frozen.locate(start_scene, 50, 50)
frozen.show()
moana.setScale(0.8)
moana.locate(start_scene, 600, 50)
moana.show()
frozen_end.setScale(0.59)
moana_end.setScale(1.31)

cwd = os.getcwd()
file_frozen = os.path.join(cwd, 'records_frozen.txt')
if not os.path.exists(file_frozen):
    with open(file_frozen, 'w') as f:
        f.write('9999.9999')

file_moana = os.path.join(cwd, 'records_moana.txt')
if not os.path.exists(file_moana):
    with open(file_moana, 'w') as f:
        f.write('9999.9999')

game_scene = [frozen_scene, moana_scene]
complete_img = [frozen_end, moana_end]
record_file = [file_frozen, file_moana]

start_time = time.time()

class Controller:
    def __init__(self):
        self.parts = []
        self.data = list(range(16))
        self.base_x = 0
        self.base_y = 0
        self.len = 119

    def mix_puzzle(self):
        for i in range(1000):
            move = random.randrange(0, 4)
            empty = self.data.index(15)
            x = empty % 4
            y = empty // 4
            if move == 0 and y != 0:
                temp = self.data[empty - 4]
                self.data[empty - 4] = 15
                self.data[empty] = temp
            elif move == 1 and y != 3:
                temp = self.data[empty + 4]
                self.data[empty + 4] = 15
                self.data[empty] = temp
            elif move == 2 and x != 3:
                temp = self.data[empty + 1]
                self.data[empty + 1] = 15
                self.data[empty] = temp
            elif move == 3 and x != 0:
                temp = self.data[empty - 1]
                self.data[empty - 1] = 15
                self.data[empty] = temp
            else:
                pass

    def init_game_data(self):
        file_name = 'puzzle_images/'
        if CURR_GAME == FROZ:
            file_name += '/frozen/frozen_part_'
        elif CURR_GAME == MOAN:
            file_name += '/moana/moana_part_'
        else:
            pass

        for i in range(1, 17):
            full_name = file_name + str(i) + '.jpg'
            part = Object(full_name)
            self.parts.append(part)

        #base location for puzzle parts
        self.base_x = 400
        self.base_y = 476
        self.len = 119

        scale_num = 0

        if CURR_GAME == FROZ:
            scale_num = 1.59
        elif CURR_GAME == MOAN:
            scale_num = 2.12
        else:
            pass

        self.mix_puzzle()

        for i in range(16):
            x = i % 4
            y = i // 4
            if self.data[i] != 15:
                self.parts[self.data[i]].setScale(scale_num)
                self.parts[self.data[i]].locate(game_scene[CURR_GAME], self.base_x + self.len * x, self.base_y - self.len * y)
                self.parts[self.data[i]].show()

        screen.locate(game_scene[CURR_GAME], 400, 119)
        screen.show()

    def move_control(self, x, y, direction):
        idx = x + y * 4
        if direction == U:
            if y != 0 and self.data[idx - 4] == 15:
                self.parts[self.data[idx]].locate(game_scene[CURR_GAME], self.base_x + self.len * x, self.base_y - self.len * (y - 1))
                self.data[idx - 4] = self.data[idx]
                self.data[idx] = 15
        elif direction == D:
            if y != 3 and self.data[idx + 4] == 15:
                self.parts[self.data[idx]].locate(game_scene[CURR_GAME], self.base_x + self.len * x, self.base_y - self.len * (y + 1))
                self.data[idx + 4] = self.data[idx]
                self.data[idx] = 15
        elif direction == R:
            if x != 3 and self.data[idx + 1] == 15:
                self.parts[self.data[idx]].locate(game_scene[CURR_GAME], self.base_x + self.len * (x + 1), self.base_y - self.len * y)
                self.data[idx + 1] = self.data[idx]
                self.data[idx] = 15
        elif direction == L:
            if x != 0 and self.data[idx - 1] == 15:
                self.parts[self.data[idx]].locate(game_scene[CURR_GAME], self.base_x + self.len * (x - 1), self.base_y - self.len * y)
                self.data[idx - 1] = self.data[idx]
                self.data[idx] = 15
        else:
            pass

        if self.end_check():
            self.finish_game()

    def end_check(self):
        for i in range(16):
            if self.data[i] != i:
                return False
        return True

    def finish_game(self):
        if CURR_GAME == FROZ:
            frozen_end.locate(game_scene[CURR_GAME], 285, 6)
        elif CURR_GAME == MOAN:
            moana_end.locate(game_scene[CURR_GAME], 115, 6)
        complete_img[CURR_GAME].show()
        end_time = time.time()
        current_record = end_time - start_time

        f = open(record_file[CURR_GAME], 'r')
        top_record = float(f.read())
        f.close()

        if current_record < top_record:
            with open(record_file[CURR_GAME], 'w') as f:
                f.write(str(current_record))
            showMessage('새로운 기록 갱신!! ' + str(current_record) + ' 초')
        else:
            showMessage('기록 갱신 실패.. ' + str(current_record) + ' 초')

game_data = Controller()

def screen_on_click(x, y, action):
    global game_data
    idx_x = x // 119
    idx_y = 3 - (y // 119)
    if action == MouseAction.DRAG_UP:
        game_data.move_control(idx_x, idx_y, U)
    elif action == MouseAction.DRAG_DOWN:
        game_data.move_control(idx_x, idx_y, D)
    elif action == MouseAction.DRAG_RIGHT:
        game_data.move_control(idx_x, idx_y, R)
    elif action == MouseAction.DRAG_LEFT:
        game_data.move_control(idx_x, idx_y, L)
    else:
        pass

screen.onMouseAction = screen_on_click

def control_game():
    global game_data
    game_data = Controller()
    game_data.init_game_data()

def frozen_on_click(x, y, action):
    global CURR_GAME
    global start_time
    CURR_GAME = FROZ
    control_game()
    game_scene[CURR_GAME].enter()
    start_time = time.time()

def moana_on_click(x, y, action):
    global CURR_GAME
    global start_time
    CURR_GAME = MOAN
    control_game()
    game_scene[CURR_GAME].enter()
    start_time = time.time()

def end_screen_on_click(x, y, action):
    if CURR_GAME == FROZ:
        game_scene[CURR_GAME] = Scene('Frozen2', 'puzzle_images/frozen/frozen_background.png')
    elif CURR_GAME == MOAN:
        game_scene[CURR_GAME] = Scene('Moana', 'puzzle_images/moana/moana_background.png')
    start_scene.enter()

frozen.onMouseAction = frozen_on_click
moana.onMouseAction = moana_on_click

frozen_end.onMouseAction = end_screen_on_click
moana_end.onMouseAction = end_screen_on_click

startGame(start_scene)