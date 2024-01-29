""" SETTING """
SCREEN_NAME = "CG"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_COLOR = "black"
LINE_COLOR = "white"
"""  """
# library from https://mcsp.wartburg.edu/zelle/python/graphics.py
from graphics import GraphWin, Point, Rectangle

SCREEN = GraphWin(SCREEN_NAME, SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN.setBackground(SCREEN_COLOR)


# clear screen
def refresh():
    rec = Rectangle(Point(0, 0), Point(SCREEN_WIDTH, SCREEN_HEIGHT))
    rec.setFill(SCREEN_COLOR)
    rec.setOutline(SCREEN_COLOR)
    rec.draw(SCREEN)


# FLIP SPACE UPSIDE DOWN
def flip(y):
    return SCREEN_HEIGHT - y


def drawPoint(x, y):
    SCREEN.plot(x, y, color=LINE_COLOR)


def lineBreRunX(x1, y1, x2, y2):
    # define init value/constant
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    pk = 2 * dy - dx
    yDiffClause = 2 * (dy - dx)
    ySameClause = 2 * dy

    isX1up = x1 < x2
    isY1up = y1 < y2

    # line render
    xDirection = 1 if isX1up else -1
    yDirection = 1 if isY1up else -1
    y = y1
    for x in range(x1, x2 + xDirection, xDirection):
        if pk > 0:
            pk += yDiffClause
            y += yDirection
        else:
            pk += ySameClause

        drawPoint(x, y)


def lineBreRunY(x1, y1, x2, y2):
    # define init value/constant
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    pk = 2 * dx - dy
    xDiffClause = 2 * (dx - dy)
    xSameClause = 2 * dx

    isX1up = x1 < x2
    isY1up = y1 < y2

    # line render
    xDirection = 1 if isX1up else -1
    yDirection = 1 if isY1up else -1
    x = x1
    for y in range(y1, y2 + yDirection, yDirection):
        if pk > 0:
            pk += xDiffClause
            x += xDirection
        else:
            pk += xSameClause

        drawPoint(x, y)


def lineRender(x1, y1, x2, y2):
    y1 = flip(y1)
    y2 = flip(y2)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    if dy > dx:
        lineBreRunY(x1, y1, x2, y2)
    else:
        lineBreRunX(x1, y1, x2, y2)


def ellipsePlotPoint(xC, yC, x, y):
    drawPoint(xC + x, yC + y)  # Q1
    drawPoint(xC - x, yC + y)  # Q2
    drawPoint(xC - x, yC - y)  # Q3
    drawPoint(xC + x, yC - y)  # Q4


def ellipseRender(xC, yC, xRad, yRad):
    # init useful constant
    yC = flip(yC)
    yRadSqr = yRad * yRad
    xRadSqr = xRad * xRad
    doubYRadSqr = 2 * yRadSqr
    doubXRadSqr = 2 * xRadSqr
    trplYRadSqr = 3 * yRadSqr
    trplXRadSqr = 3 * xRadSqr

    # run x cal y
    x = 0
    y = yRad
    xSqr = x * x
    ySqr = (y - 0.5) * (y - 0.5)
    pk = round(yRadSqr * xSqr + xRadSqr * ySqr - xRadSqr * yRadSqr)
    while yRadSqr * x < xRadSqr * y:
        if pk < 0:
            pk += doubYRadSqr * x + trplYRadSqr
        else:
            pk += doubYRadSqr * x + trplYRadSqr - 2 * xRadSqr * y
            y -= 1

        ellipsePlotPoint(xC, yC, x, y)
        x += 1

    xSqr = (x + 0.5) * (x + 0.5)
    ySqr = y * y
    pk = round(yRadSqr * xSqr + xRadSqr * ySqr - xRadSqr * yRadSqr)
    while y >= 0:
        if pk > 0:
            pk += trplXRadSqr - doubXRadSqr * y
        else:
            pk += trplXRadSqr - doubXRadSqr * y + yRadSqr * (2 * x + 2)
            x += 1

        ellipsePlotPoint(xC, yC, x, y)
        y -= 1


def circleRender(xC, yC, rad):
    ellipseRender(xC, yC, xRad=rad, yRad=rad)


def main():
    prompt = input(
        "-> ---Slow CG by Thada.S---" + '\n-> type "help" for more info...' + "\nuCG > "
    )
    while prompt not in ["\\q", "quit", "bye"]:
        args = prompt.split()
        if len(args) > 1:
            cmd = args.pop(0)
            if cmd == "line":
                try:
                    x1, y1, x2, y2 = tuple(map(int, args))
                    lineRender(x1, y1, x2, y2)
                except:
                    print("-> Wrong argument for line")
            elif cmd == "circle":
                try:
                    xC, yC, rad = tuple(map(int, args))
                    circleRender(xC, yC, rad)
                except:
                    print("-> Wrong argument for circle")
            elif cmd == "ellipse":
                try:
                    xC, yC, xRad, yRad = tuple(map(int, args))
                    ellipseRender(xC, yC, xRad, yRad)
                except:
                    print("-> Wrong argument for ellipse")
            else:
                print("-> Command not found")

        elif len(args) == 1:
            cmd = args.pop(0)
            if cmd == "help":
                print(
                    "*Commands list*"
                    + "\n-> line [X Start] [Y Start] [X Stop] [Y Stop]"
                    + "\n-> circle [X Center] [Y Center] [Radius]"
                    + "\n-> ellipse [X Center] [Y Center] [X Radius] [Y Radius]"
                    + "\n-> refresh"
                )
            elif cmd == "line":
                print("-> line [X Start] [Y Start] [X Stop] [Y Stop]")
            elif cmd == "circle":
                print("-> circle [X Center] [Y Center] [Radius]")
            elif cmd == "ellipse":
                print("-> ellipse [X Center] [Y Center] [X Radius] [Y Radius]")
            elif cmd == "clear":
                print("-> clearing the screen")
                refresh()
            else:
                print("-> Command not found")

        prompt = input("uCG > ")
    print("-> bye")


main()
SCREEN.close()
