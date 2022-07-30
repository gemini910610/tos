import random
from msvcrt import getch
import os

class Board:
    """版面"""
    __runestone_type = [
        '\033[37m■\033[0m', # 心符石
        '\033[34m■\033[0m', # 水符石
        '\033[31m■\033[0m', # 火符石
        '\033[32m■\033[0m', # 木符石
        '\033[33m■\033[0m', # 光符石
        '\033[35m■\033[0m', # 暗符石
        ' '                 # 沒有符石
    ]
    """符石字串"""

    __hand_on_type = [
        '\033[37m□\033[0m', # 心符石
        '\033[34m□\033[0m', # 水符石
        '\033[31m□\033[0m', # 火符石
        '\033[32m□\033[0m', # 木符石
        '\033[33m□\033[0m', # 光符石
        '\033[35m□\033[0m', # 暗符石
    ]
    """手持符石字串"""

    def __init__(self, runestones: list[list[int]] = None):
        if runestones is None:
            self.__runestones = []
            """版面符石"""
            for _ in range(5):
                row = []
                for _ in range(6):
                    row.append(random.randint(0, 5))
                self.__runestones.append(row)
        else:
            self.__runestones = runestones
    
    def copy(self):
        """複製版面"""
        runestones = []
        for i in range(5):
            runestones.append(self.__runestones[i].copy())
        return Board(runestones)
    
    def __swap(self, runestone1: tuple[int, int], runestone2: tuple[int, int]):
        """
        交換符石\n
        [參數]
        runestone1: 符石1座標
        runestone2: 符石2座標
        """
        y1, x1 = runestone1
        y2, x2 = runestone2
        runestone = self.__runestones[x1][y1]
        self.__runestones[x1][y1] = self.__runestones[x2][y2]
        self.__runestones[x2][y2] = runestone
    
    def move(self, start: tuple[int, int], operations: str) -> tuple[int, int]:
        """
        移動符石\n
        [參數]
        start: 起手符石座標
        operations: 移動路徑(r: 右, u: 上, l: 左, d: 下)\n
        [回傳]\n
        結束符石座標
        """
        hand_on = list(start)
        for operation in operations:
            next = hand_on.copy()
            match operation:
                case 'r':
                    next[0] += 1
                case 'u':
                    next[1] -= 1
                case 'l':
                    next[0] -= 1
                case 'd':
                    next[1] += 1
            self.__swap(tuple(hand_on), tuple(next))
            hand_on = next
        return tuple(hand_on)
    
    def __adjacent(self, runestone: tuple[int, int], target: int, adjacent: list[tuple[int, int]]):
        """
        將相鄰的符石加入陣列\n
        [參數]
        runestone: 符石座標
        target: 相鄰符石種類
        adjacent: 要加入的陣列
        """
        x, y = runestone
        if x < 5 and x >= 0 and y < 6 and y >= 0 and self.__runestones[x][y] == target and (x, y) not in adjacent:
            adjacent.append((x, y))
            self.__adjacent((x + 1, y), target, adjacent)
            self.__adjacent((x - 1, y), target, adjacent)
            self.__adjacent((x, y + 1), target, adjacent)
            self.__adjacent((x, y - 1), target, adjacent)
    
    def __can_dissolve(self, runestone: tuple[int, int], adjacent: list[tuple[int, int]]) -> bool: 
        """
        判斷符石是否可消除\n
        [參數]
        runestone: 符石座標
        adjacent: 存有相鄰符石座標的陣列\n
        [回傳]\n
        是否可消除
        """
        x, y = runestone
        if x + 2 < 5 and (x + 1, y) in adjacent and (x + 2, y) in adjacent:
            return True
        if y + 2 < 6 and (x, y + 1) in adjacent and (x, y + 2) in adjacent:
            return True
        if x + 1 < 5 and x - 1 >= 0 and (x + 1, y) in adjacent and (x - 1, y) in adjacent:
            return True
        if y + 1 < 6 and y - 1 >= 0 and (x, y + 1) in adjacent and (x, y - 1) in adjacent:
            return True
        if x - 2 >= 0 and (x - 1, y) in adjacent and (x - 2, y) in adjacent:
            return True
        if y - 2 >= 0 and (x, y - 1) in adjacent and (x, y - 2) in adjacent:
            return True
        return False
    
    def __dissolve(self, combo: int) -> int:
        """
        消除符石\n
        [參數]
        combo: 現有連擊數
        [回傳]\n
        連擊數
        """
        second_combo = 0
        for i in range(5):
            for j in range(6):
                if self.__runestones[i][j] != -1:
                    adjacent = [] # 相鄰
                    self.__adjacent((i, j), self.__runestones[i][j], adjacent)
                    can_dissolve = [] # 可消除
                    for runestone in adjacent:
                        if self.__can_dissolve(runestone, adjacent):
                            can_dissolve.append(runestone)
                    if len(can_dissolve) > 0:
                        second_combo += 1
                        for runestone in can_dissolve:
                            self.__runestones[runestone[0]][runestone[1]] = -1
                        self.show(f'dissolving... combo: {combo + second_combo}')
                        os.system('pause')
        return second_combo

    def dissolve(self) -> int:
        """
        消除符石並下落\n
        [回傳]\n
        連擊數
        """
        combo = 0
        while True:
            second_combo = self.__dissolve(combo)
            if second_combo == 0:
                break
            combo += second_combo
            if self.__fall():
                self.show(f'dissolving... combo: {combo}')
                os.system('pause')
            else:
                break
        return combo
    
    def __fall(self) -> bool:
        """
        符石下落\n
        [回傳]\n
        是否有符石下落
        """
        fall = False
        for i in range(6):
            empty = 0
            for j in range(4, -1, -1):
                if self.__runestones[j][i] == -1:
                    empty += 1
                else:
                    if empty > 0:
                        fall = True
                    self.__swap((i, j), (i, j + empty))
        return fall
    
    def show(self, title: str = 'Tower of Saviors', hand_on: tuple[int, int] = None, clear: bool = True):
        """
        顯示版面\n
        [參數]
        title: 標題
        hand_on: 移動中手持符石座標
        clear: 是否清除畫面
        """
        if clear:
            os.system('cls')
        print(title)
        for i in range(5):
            for j in range(6):
                runestone = self.__runestones[i][j]
                if (j, i) == hand_on:
                    print(self.__hand_on_type[runestone], end=' ')
                else:
                    print(self.__runestone_type[runestone], end=' ')
            print()

def keyboard_input() -> str:
    """
    取得鍵盤方向鍵輸入\n
    [回傳]\n
    方向(r: 右, u: 上, l: 左, d: 下)
    """
    key = getch()
    if key == b'\x00' or key == b'\xe0':
        match getch():
            case b'M':
                return 'r'
            case b'H':
                return 'u'
            case b'K':
                return 'l'
            case b'P':
                return 'd'
    else:
        return ''

board = Board()
board.show()
start = input('start > ').split(' ')
start = (int(start[0]), int(start[1]))
while True:
    board.show(f'hand on {start}', start)
    operation = keyboard_input()
    if operation == '':
        break
    start = board.move(start, [operation])
combo = board.dissolve()
board.show(f'combo: {combo}')