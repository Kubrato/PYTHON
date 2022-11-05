import random
import os
import json
from datetime import datetime

EMPTY = 'E'
TREASURE = 'T'
MONSTER = 'M'
SWORD = 'S'
POTION = 'P'
VENOM = 'V'

FILE_PATH = "gamelog.json"

startTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

whatToAddInGrid = (TREASURE, TREASURE, TREASURE, TREASURE, TREASURE, MONSTER,
                   MONSTER, MONSTER, MONSTER, MONSTER, SWORD, SWORD, POTION,
                   POTION, POTION, VENOM, VENOM, VENOM)
score = 0
posion_count = 0
sword_count = 0

moveList = []

NROWS_IN_GRID = 6
NCOLS_IN_GRID = 7
grid = []
hidden_grid = []
for r in range(0, NROWS_IN_GRID):  #0-5
    aRow = []
    hidden_row = []
    for c in range(0, NCOLS_IN_GRID):  #0-6
        aRow.append(EMPTY)
        hidden_row.append(' ')
    grid.append(aRow)
    hidden_grid.append(hidden_row)


def findEmptyCell(aGrid, nRows, nCols):
    while True:
        row = random.randrange(nRows)
        col = random.randrange(nCols)
        if (aGrid[row][col] == EMPTY):
            return row, col


def print_grid(grid):
    for row in grid:
        print(row)


def fileExists(filePath):
    exists = os.path.exists(filePath)
    return exists


def writeFile(filePath, textToWrite):
    fileHandle = open(filePath, 'w')
    fileHandle.write(textToWrite)
    fileHandle.close()


def readFile(filePath):
    if not fileExists(filePath):
        print('The file, ' + filePath + ' does not exist - cannot read it.')
        return ""
    fileHandle = open(filePath, 'r')
    data = fileHandle.read()
    fileHandle.close()
    return data


for item in whatToAddInGrid:
    rowRandom, colRandom = findEmptyCell(grid, NROWS_IN_GRID, NCOLS_IN_GRID)
    grid[rowRandom][colRandom] = item

startRow, startCol = findEmptyCell(grid, NROWS_IN_GRID, NCOLS_IN_GRID)
prev_row = startRow
prev_col = startCol
hidden_grid[startRow][startCol] = grid[startRow][startCol]

print_grid(hidden_grid)
print()
print('Starting at row:', startRow + 1, 'col:', startCol + 1)

userDict = {}
userData = {}
while True:
    #move the user around
    direction = input('Press L, U, R, D to move: ').lower()
    print()

    moveList.append(str(direction))
    if (direction == 'l' or direction == 'L'):
        if (startCol == 0):
            startCol = NCOLS_IN_GRID - 1
        else:
            startCol -= 1
    elif (direction == 'r'):
        if (startCol == NCOLS_IN_GRID - 1):
            startCol = 0
        else:
            startCol += 1
    elif (direction == 'u'):
        if (startRow == 0):
            startRow = NROWS_IN_GRID - 1
        else:
            startRow -= 1
    elif (direction == 'd'):
        if (startRow == NROWS_IN_GRID - 1):
            startRow = 0
        else:
            startRow += 1
    else:
        print('Invalid move. Quitting the game.')
        break

    if hidden_grid[startRow][startCol] != ' ':
      startCol = prev_col
      startRow = prev_row
      print('You cannot pass same cell. Try again.')
      continue

    prev_col = startCol
    prev_row = startRow
    
    foundInCell = grid[startRow][startCol]
    print('Now at row', startRow + 1, ' col:', startCol + 1, ' cell contains:',
          foundInCell)

    hidden_grid[startRow][startCol] = grid[startRow][startCol]
    print("\033[H\033[J", end="")
    print_grid(hidden_grid)
    print()
    print("----------------------------------")
    print()

    if foundInCell == 'T':
        score += 1
        print('+TREASURE')
        print()
    elif foundInCell == 'S':
        sword_count += 1
        print('+SWORD')
        print()

    elif foundInCell == 'P':
        posion_count += 1
        print('+POTION')
        print()

    elif foundInCell == 'M':
        if sword_count > 0:
            sword_count -= 1
            print('Oh No! Monster')
            print('SWORD is used.')
            print()
        else:
            print('Oh No! Monster')
            print('You die.')
            print('Score [' + str(score) + ']' + ' Sword:[' +
                  str(sword_count) + ']' + ' Positon:[' + str(posion_count) +
                  ']')
            print()
            print('The game ends.')
            break

    elif foundInCell == 'V':
        if posion_count > 0:
            posion_count -= 1
            print('Oh No! Venom')
            print('POTION is used.')
            print()
        else:
            print('Oh No! Venom')
            print('You died.')
            print('Score [' + str(score) + ']' + ' Sword:[' +
                  str(sword_count) + ']' + ' Positon:[' + str(posion_count) +
                  ']')
            print()
            print('The game ends.')
            break

    score += 1
    print("----------------------------------")
    print()
    print('Score [' + str(score) + ']' + ' Sword:[' + str(sword_count) + ']' +
          ' Positon:[' + str(posion_count) + ']')

if fileExists(FILE_PATH):
    content = readFile(FILE_PATH)
    userDict = json.loads(content)

endTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
userData["moves"] = moveList
userData["score"] = score
userDict[startTime] = userData
dict_str = str(userDict)
dict_str = dict_str.replace("\'", "\"")

writeFile(FILE_PATH, dict_str)

print()