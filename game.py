from unicodedata import name
import pygame as pg
import random as r
from utility import Array
from timeit import Timer


WIN_WIDTH  = 360
WIN_HEIGHT = 480
BOARD_SIZE = 4
PADDING = 8

#   COLOURS
COLORS = {"bg": "#FBF8EF", "board": "#C5B497", 0: "#CCC0B3", 2: "#EEE4DA", 4: "#EDE0C8", 8: "#F2B179", 16: "#F59563", 32: "#F67C5F", 64: "#F65E3B", 128: "#EED177", 256: "#EDCD63", 512: "#EDC850", 1024: "#F0C638", 2048: "#F1C222", -1: "#3E3933"}


class Tile:
    size = (WIN_WIDTH-64 - PADDING * 2 -(PADDING * (BOARD_SIZE - 1))) / BOARD_SIZE
    
    def __init__(self, num=0, pos=None) -> None:
        self.number = num
        self.pos = pos if pos else (0, 0)


class Board:
    size = (WIN_WIDTH-64, WIN_WIDTH-64)
    
    def __init__(self) -> None:
        self._tiles = [[Tile() for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        self.position = (32, WIN_HEIGHT - self.size[1] - 64)

    def __getitem__(self, coords) -> Tile:
        assert len(coords) == 2, "Invalid index"
        assert BOARD_SIZE > coords[0] >= 0, "Row out of bounds"
        assert BOARD_SIZE > coords[1] >= 0, "Column out of bounds"

        row = coords[0]
        col = coords[1]

        return self._tiles[row][col]

    def __setitem__(self, key, value) -> None:
        assert len(key) == 2, "Invalid index"
        assert BOARD_SIZE > key[0] >= 0, "Row out of bounds"
        assert BOARD_SIZE > key[1] >= 0, "Column out of bounds"

        row = key[0]
        col = key[1]

        self._tiles[row][col] = value

    def GetEmpty(self):
        empty = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self[i, j].number != 0:
                    continue
                empty.append((i, j))
        return empty
    
    def MoveUp(self):
        moves = 0
        for col in range(BOARD_SIZE):
            notDone = True
            startRow = 0
            curRow = startRow
            while notDone:
                if self[curRow, col].number == 0 or curRow == startRow:
                    curRow += 1
                    if curRow == BOARD_SIZE:
                        notDone = False
                    continue

                i = curRow - 1
                while (i != startRow) and (self[i, col].number == 0):
                    i -= 1
                
                if self[i, col].number == 0:
                    self[i, col].number = self[curRow, col].number
                    self[curRow, col].number = 0
                    moves += 1
                    continue
                
                if self[i, col].number != self[curRow, col].number:
                    if i != curRow - 1:
                        self[i + 1, col].number = self[curRow, col].number
                        self[curRow, col].number = 0
                        moves += 1
                    startRow = i + 1
                    continue

                if self[i, col].number == self[curRow, col].number:
                    self[i, col].number *= 2
                    self[curRow, col].number = 0
                    startRow = i + 1
                    moves += 1
                    continue
        
        if moves != 0:
            self.SpawnNew()

    def MoveLeft(self):
        moves = 0
        for row in range(BOARD_SIZE):
            notDone = True
            startCol = 0
            curCol = startCol
            while notDone:
                if self[row, curCol].number == 0 or curCol == startCol:
                    curCol += 1
                    if curCol == BOARD_SIZE:
                        notDone = False
                    continue

                i = curCol - 1
                while (i != startCol) and (self[row, i].number == 0):
                    i -= 1
                
                if self[row, i].number == 0:
                    self[row, i].number = self[row, curCol].number
                    self[row, curCol].number = 0
                    moves += 1
                    continue
                
                if self[row, i].number != self[row, curCol].number:
                    if i != curCol - 1:
                        self[row, i + 1].number = self[row, curCol].number
                        self[row, curCol].number = 0
                        moves += 1
                    startCol = i + 1
                    continue

                if self[row, i].number == self[row, curCol].number:
                    self[row, i].number *= 2
                    self[row, curCol].number = 0
                    startCol = i + 1
                    moves += 1
                    continue
        
        if moves != 0:
            self.SpawnNew()
        
    def MoveDown(self):
        moves = 0
        for col in range(BOARD_SIZE):
            notDone = True
            startRow = BOARD_SIZE-1
            curRow = startRow
            while notDone:
                if self[curRow, col].number == 0 or curRow == startRow:
                    curRow -= 1
                    if curRow < 0:
                        notDone = False
                    continue

                i = curRow + 1
                while (i != startRow) and (self[i, col].number == 0):
                    i += 1
                
                if self[i, col].number == 0:
                    self[i, col].number = self[curRow, col].number
                    self[curRow, col].number = 0
                    moves += 1
                    continue
                
                if self[i, col].number != self[curRow, col].number:
                    if i != curRow + 1:
                        self[i - 1, col].number = self[curRow, col].number
                        self[curRow, col].number = 0
                        moves += 1
                    startRow = i - 1
                    continue

                if self[i, col].number == self[curRow, col].number:
                    self[i, col].number *= 2
                    self[curRow, col].number = 0
                    startRow = i - 1
                    moves += 1
                    continue
        
        if moves != 0:
            self.SpawnNew()

    def MoveRight(self):
        moves = 0
        for row in range(BOARD_SIZE):
            notDone = True
            startCol = BOARD_SIZE - 1
            curCol = startCol
            while notDone:
                if self[row, curCol].number == 0 or curCol == startCol:
                    curCol -= 1
                    if curCol < 0:
                        notDone = False
                    continue

                i = curCol + 1
                while (i != startCol) and (self[row, i].number == 0):
                    i += 1
                
                if self[row, i].number == 0:
                    self[row, i].number = self[row, curCol].number
                    self[row, curCol].number = 0
                    moves += 1
                    continue
                
                if self[row, i].number != self[row, curCol].number:
                    if i != curCol + 1:
                        self[row, i - 1].number = self[row, curCol].number
                        self[row, curCol].number = 0
                        moves += 1
                    startCol = i - 1
                    continue

                if self[row, i].number == self[row, curCol].number:
                    self[row, i].number *= 2
                    self[row, curCol].number = 0
                    startCol = i - 1
                    moves += 1
                    continue
        
        if moves != 0:
            self.SpawnNew()

    def __str__(self):
        res = ""
        for row in self._tiles:
            for element in row:
                res += str(element.number) + " "
            res += "\n"
        return res

    def draw(self):
        pg.draw.rect(screen, COLORS["board"], (self.position[0], self.position[1], self.size[0], self.size[1]), border_radius=4)

    def drawTiles(self):
        
        tileSize = (self.size[0]- PADDING * 2 -(PADDING * (BOARD_SIZE - 1))) / BOARD_SIZE
        rOffset = PADDING

        for row in self._tiles:
            cOffset = PADDING
            for col in row:
                tilePosX = self.position[0] + cOffset
                tilePosY = self.position[1] + rOffset
                
                cOffset += tileSize + PADDING

                if col.number == 0:
                    num = TILE_FONT.render(str(), True, COLORS[-1])
                else:
                    num = TILE_FONT.render(str(col.number), True, COLORS[-1] if col.number <= 4 else COLORS["bg"])
                
                tileColor = COLORS[col.number] if col.number <= 2048 else COLORS[-1]

                pg.draw.rect(screen, tileColor, (tilePosX, tilePosY, tileSize, tileSize), border_radius=4)
                
                numRect = num.get_rect()
                numRect.centerx, numRect.centery = tilePosX + tileSize / 2, tilePosY + tileSize / 2
                screen.blit(num, numRect)
            
            
            rOffset += tileSize + PADDING

    def SpawnNew(self):
        empties = gameBoard.GetEmpty()
        if empties:
            randIdx  = r.choice(empties)
            gameBoard[randIdx].number = r.choices([2, 4], [0.9, 0.1])[0]

def InitBoard():
    global gameBoard
    gameBoard = Board()
    gameBoard.SpawnNew()
    gameBoard.SpawnNew()
    # gameBoard[0, 0] = Tile(2)
    # gameBoard[1, 1] = Tile(2)


def main():
    global screen, TILE_FONT
    pg.init()
    screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    screen.fill(COLORS["bg"])
    pg.display.set_caption("2048")
    
    clock = pg.time.Clock()
    TILE_FONT = pg.font.SysFont("Ariel.ttf", 40)

    InitBoard()
    gameBoard.draw()

    running = True
    while running:
        dt = clock.tick(60)
        # EVENT HANDLER
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    gameBoard.MoveLeft()
                elif event.key == pg.K_w:
                    gameBoard.MoveUp()
                elif event.key == pg.K_d:
                    gameBoard.MoveRight()
                elif event.key == pg.K_s:
                    gameBoard.MoveDown()
                
        gameBoard.drawTiles()
    
        pg.display.flip()

    pg.quit()
    quit()


if __name__ == "__main__":
    main()
