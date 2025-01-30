from cmu_graphics import *
import math
maze=[[0, 0, 0, 0, 3, 3, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 3, 0, 0, 3, 0],
      [0, 3, 3, 0, 0, 0, 0, 3, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 3, 3, 3, 0, 0],
      [0, 0, 0, 3, 0, 0, 0, 0, 3], [0, 1, 0, 0, 0, 3, 0, 0, 3], [0, 0, 0, 3, 3, 3, 3, 0, 0]];
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0  # g值（起点到当前节点的实际代价）
        self.h = 0  # h值（当前节点到目标节点的估计代价）
        self.f = 0  # f值（g值加上h值）
    def __eq__(self, other):
        return self.position == other.position
    def __str__(self):
        return f'{self.position},{self.parent}';



def onAppStart(app):
    app.rows = 9
    app.cols = 9
    app.boardLeft = 65
    app.boardTop = 65
    app.boardWidth = 270
    app.boardHeight = 270
    app.cellBorderWidth = 1
    app.width=700;
    app.selection = (0, 0)
    app.hover =(0,0);
    app.start=(7,1);


def redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
def onMouseMove(app, mouseX, mouseY):
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
        app.hover = selectedCell
def onMousePress(app,mouseX,mouseY):
    for row in range(len(maze)):
        for col in range(len(maze)):
            if maze[row][col]==2:
                maze[row][col]=0;
    if getCell(app,mouseX,mouseY)!=None:
        r,c=getCell(app,mouseX,mouseY)
    Path=astar(maze,(7,1),(r,c))
    #prevpath=Path
    if Path != None:
        for elem in Path:
            maze[elem[0]][elem[1]]=2;
    print(Path)
    if(maze[r][c]!=1):
        app.selection=r,c;
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)
            #print(app.numbers[row][col])
def drawBoardBorder(app):
    # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill=None, border='black',
             borderWidth=2 * app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if (row, col) == app.hover:
        color = 'cyan'
    elif (row, col) == app.selection and maze[row][col]!=1 and maze[row][col]!=3:
        color = 'yellow'
    elif  maze[row][col]==3:
        color = 'green'
    elif (row,col)==app.start:
        color= 'blue'
    elif maze[row][col]==2 and (row,col)!=app.start:
        color= 'red'
    else:
        color = 'white'
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)


def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
        return (row, col)

    else:
        return None

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)
def drawnumberatcell(app,number,r,c):
    n=str(number);
    x,y=getCellSize(app);
    if(number!=0):
        drawLabel(n,r*x+app.boardLeft+0.5*x,c*y+app.boardTop+0.5*y);
def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
def astar(maze, start, end):
    # 创建起点和目标节点
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # 初始化开放和关闭节点集合
    open_list = []
    closed_list = []

    # 将起点加入开放节点集合
    open_list.append(start_node)

    while len(open_list) > 0:
        # 从开放节点集合中选择f值最小的节点作为当前节点
        current_node = open_list[0]
        current_index = 0
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        # 将当前节点从开放节点集合中移除，并加入到关闭节点集合中
        open_list.pop(current_index)
        closed_list.append(current_node)

        # 如果当前节点是目标节点，返回路径
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        # 生成当前节点的相邻节点
        neighbors = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # 确保节点在迷宫范围内
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # 确保节点不是墙
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # 创建新节点
            new_node = Node(current_node, node_position)

            # 加入相邻节点集合
            neighbors.append(new_node)

        # 处理相邻节点
        for neighbor in neighbors:
            # 如果相邻节点已在关闭节点集合中，忽略
            if neighbor in closed_list:
                continue

            # 计算相邻节点的g值、h值和f值
            neighbor.g = current_node.g + 1
            neighbor.h = ((neighbor.position[0] - end_node.position[0]) ** 2) + (
                        (neighbor.position[1] - end_node.position[1]) ** 2)
            neighbor.f = neighbor.g + neighbor.h

            # 如果相邻节点已在开放节点集合中且g值更大，忽略
            if any((neighbor == node and neighbor.g >= node.g) for node in open_list):
                continue

            # 将相邻节点加入开放节点集合
            open_list.append(neighbor)

    # 如果找不到路径，返回空
    return None


def main():
    runApp()

# inspired by USC professor Quan Nyugen and CMU Professor David Cosbie
main()
