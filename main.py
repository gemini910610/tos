import random
from msvcrt import getch
import os

class DissolvedRunestone:
    """消除的符石"""
    def __init__(self, weights: list[int] = [1, 1, 1, 1, 1, 1]):
        self.__runestones = []
        self.__weights = weights
    
    @property
    def runestones(self) -> list[tuple[int, int]]:
        """消除的符石"""
        return self.__runestones
    
    @property
    def score(self) -> int:
        """消除評分"""
        sum = 0
        for runestone in self.__runestones:
            sum += runestone[1] * self.__weights[runestone[0]]
        return sum
    
    @property
    def combo(self) -> int:
        """連擊數"""
        return len(self.__runestones)
    
    def add(self, runestone_type: int, amount: int):
        """
        將符石加入陣列\n
        [參數]
        runestone_type: 符石種類
        amount: 數量
        """
        self.__runestones.append((runestone_type, amount))
    
    def show(self):
        """顯示消除的符石"""
        color = ['\033[47m', '\033[44m', '\033[41m', '\033[42m', '\033[43m', '\033[45m']
        for runestone in self.__runestones:
            print(f'{color[runestone[0]]} {runestone[1]} \033[0m', end=' ')
        print()

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

    def __init__(self, runestones: list[list[int]] = None, weight: list[int] = [1, 1, 1, 1, 1, 1]):
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
        self.__weight = weight
        """符石權重"""
    
    def copy(self):
        """複製版面"""
        runestones = []
        for i in range(5):
            runestones.append(self.__runestones[i].copy())
        return Board(runestones, self.__weight.copy())
    
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
    
    def __dissolve(self, dissolved_runestone: DissolvedRunestone) -> bool:
        """
        消除符石\n
        [參數]
        dissolved_runestone: 消除的符石
        [回傳]\n
        是否有符石被消除
        """
        dissolve = False
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
                        dissolve = True
                        dissolved_runestone.add(self.__runestones[i][j], len(can_dissolve))
                        for runestone in can_dissolve:
                            self.__runestones[runestone[0]][runestone[1]] = -1
                        self.show(f'dissolving... combo: {dissolved_runestone.combo}')
                        os.system('pause')
        return dissolve

    def dissolve(self) -> DissolvedRunestone:
        """
        消除符石並下落\n
        [回傳]\n
        消除的符石
        """
        dissolved_runestone = DissolvedRunestone(self.__weight)
        while True:
            if not self.__dissolve(dissolved_runestone):
                break
            if self.__fall():
                self.show(f'dissolving... combo: {dissolved_runestone.combo}')
                os.system('pause')
            else:
                break
        return dissolved_runestone
    
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
dissolved_runestone = board.dissolve()
board.show(f'combo: {dissolved_runestone.combo}')
dissolved_runestone.show()
print(f'score: {dissolved_runestone.score}')