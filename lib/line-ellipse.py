""" SETTING """

SCREEN_NAME = "CG"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_COLOR = "black"
LINE_COLOR = "white"

SHELL_NAME = "slowCG"
"""  """
# library from https://mcsp.wartburg.edu/zelle/python/graphics.py
from graphics import GraphWin, Point, Rectangle

SCREEN = GraphWin(SCREEN_NAME, SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN.setBackground(SCREEN_COLOR)


# clear screen
def refresh() -> None:
    rec = Rectangle(Point(0, 0), Point(SCREEN_WIDTH, SCREEN_HEIGHT))
    rec.setFill(SCREEN_COLOR)
    rec.setOutline(SCREEN_COLOR)
    rec.draw(SCREEN)


def intArgs(*args: int) -> tuple[int, ...]:
    INTed = map(int, args)
    return tuple(INTed)


# FLIP SPACE UPSIDE DOWN
def flip(y: int) -> int:
    return SCREEN_HEIGHT - y


def drawPoint(x: int, y: int) -> None:
    SCREEN.plot(x, y, color=LINE_COLOR)


def drawPoints(pointsList: list[tuple[int, int]]) -> None:
    for x, y in pointsList:
        SCREEN.plot(x, y, color=LINE_COLOR)


def maskPoint(
    points: list[tuple[int, int]], mask: str
) -> tuple[list[tuple[int, int]], str, str]:
    newPoints = []
    maskSize = len(mask)
    for i in range(len(points)):
        point = points[i]
        isBright = mask[i % maskSize] == "1"
        if isBright:
            newPoints.append(point)
    maskedBit = mask[: (i + 1) % maskSize]
    unmaskBit = mask[(i + 1) % maskSize :]
    return newPoints, maskedBit, unmaskBit


def span(
    points: list[tuple[int, int]], width: int, verticleSpan: bool
) -> list[tuple[int, int]]:
    spanned = []
    width -= 1
    plusWidth = width // 2
    minusWidth = width - plusWidth
    for point in points:
        spanned.append(point)
        x, y = point
        for i in range(1, plusWidth + 1):
            if verticleSpan:
                spanned.append((x, y + i))
            else:
                spanned.append((x + i, y))

        for i in range(1, minusWidth + 1):
            if verticleSpan:
                spanned.append((x, y - i))
            else:
                spanned.append((x - i, y))
    return spanned


def translateTo(
    xC: int, yC: int, points: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    newPoints = []
    for x, y in points:
        newPoints.append((xC + x, yC + y))
    return newPoints


def quarterMirror(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    newPoints = []
    for x, y in points:
        newPoints.append((+x, +y))  # Q1
        newPoints.append((-x, +y))  # Q2
        newPoints.append((-x, -y))  # Q3
        newPoints.append((+x, -y))  # Q4
    return newPoints


def lineBresenham(x1: int, y1: int, x2: int, y2: int) -> list[tuple[int, int]]:
    # pre-process for general runner/follower and direction
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    isYRunner = dy > dx
    follwerStart = x1 if isYRunner else y1
    follwerEnd = x2 if isYRunner else y2
    runnerStart = y1 if isYRunner else x1
    runnerEnd = y2 if isYRunner else x2
    followerDirection = 1 if follwerStart < follwerEnd else -1
    runnerDirection = 1 if runnerStart < runnerEnd else -1

    # define init value/constant
    dRunner = max(dx, dy)
    dFollower = min(dx, dy)
    pk = 2 * dFollower - dRunner
    diffClause = 2 * (dFollower - dRunner)
    sameClause = 2 * dFollower

    # line render
    pointList = []
    if isYRunner:
        for runner in range(runnerStart, runnerEnd + runnerDirection, runnerDirection):
            if pk > 0:
                pk += diffClause
                follwerStart += followerDirection
            else:
                pk += sameClause
            pointList.append((follwerStart, runner))
    else:
        for runner in range(runnerStart, runnerEnd + runnerDirection, runnerDirection):
            if pk > 0:
                pk += diffClause
                follwerStart += followerDirection
            else:
                pk += sameClause
            pointList.append((runner, follwerStart))
    return pointList


def line(x1: int, y1: int, x2: int, y2: int, width: int = 1, mask: str = "1") -> None:
    x1, y1, x2, y2, width = intArgs(x1, y1, x2, y2, width)

    y1 = flip(y1)
    y2 = flip(y2)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    # calculate exact pixel for line
    pointList = lineBresenham(x1, y1, x2, y2)

    # mask line path
    pointList, masked, unmask = maskPoint(pointList, mask)

    # bolder the line
    pointList = span(pointList, width, verticleSpan=dx > dy)
    drawPoints(pointList)


def midpointEllipse(
    xRad: int, yRad: int
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    # init useful constant
    yRadSqr = yRad * yRad
    xRadSqr = xRad * xRad
    doubYRadSqr = 2 * yRadSqr
    doubXRadSqr = 2 * xRadSqr

    # run x cal y
    x = 0
    y = yRad
    xSqr = x * x
    ySqr = (y - 0.5) * (y - 0.5)
    pk = round(yRadSqr - xRadSqr * yRad + xRadSqr / 4)
    # pk = round(yRadSqr * xSqr + xRadSqr * ySqr - xRadSqr * yRadSqr)
    pointsByX = []
    while yRadSqr * x < xRadSqr * y:
        if pk < 0:
            pk += doubYRadSqr * x + yRadSqr
        else:
            pk += doubYRadSqr * x + doubYRadSqr - doubXRadSqr * y
            y -= 1
        pointsByX.append((x, y))
        x += 1

    # run y cal x
    xSqr = (x + 0.5) * (x + 0.5)
    ySqr = (y - 1) * (y - 1)
    pk = round(yRadSqr * xSqr + xRadSqr * ySqr - xRadSqr * yRadSqr)
    # pk = round(yRadSqr * xSqr + xRadSqr * ySqr - xRadSqr * yRadSqr)
    pointsByY = []
    while y >= 0:
        if pk > 0:
            pk += xRadSqr - doubXRadSqr * y
        else:
            pk += xRadSqr - doubXRadSqr * y + doubYRadSqr * x
            x += 1

        pointsByY.append((x, y))
        y -= 1
    return pointsByX, pointsByY


def ellipse(
    xC: int, yC: int, xRad: int, yRad: int, width: int = 1, mask: str = "1"
) -> None:
    xC, yC, xRad, yRad, width = intArgs(xC, yC, xRad, yRad, width)

    yC = flip(yC)
    # calculate exact pixel for ellipse
    pointsByX, pointsByY = midpointEllipse(xRad=xRad, yRad=yRad)

    # mask pixel path
    maskedByX, masked, unmask = maskPoint(pointsByX, mask)
    mask = unmask + masked
    maskedByY, masked, unmask = maskPoint(pointsByY, mask)

    # bolder the line
    spannedByX = span(maskedByX, width, verticleSpan=True)
    spannedByY = span(maskedByY, width, verticleSpan=False)

    # mirror quarter to full ellipse
    quarterEllipse = spannedByX + spannedByY
    fullEllipse = quarterMirror(quarterEllipse)

    # move center
    fullEllipse = translateTo(xC, yC, fullEllipse)
    drawPoints(fullEllipse)


def circle(xC: int, yC: int, rad: int, width: int = 1, mask: str = "1") -> None:
    xC, yC, rad, width = intArgs(xC, yC, rad, width)
    ellipse(xC, yC, xRad=rad, yRad=rad, width=width, mask=mask)


# library from https://github.com/n3bch4S/nebchell/blob/main/nebchell.py
from nebchell import Nebchell

sh = Nebchell(name=SHELL_NAME)
fns = {
    "help": sh.showHelp,
    "": sh.dummy,
    "line": line,
    "ellipse": ellipse,
    "circle": circle,
    "clear": refresh,
}
hlps = {
    "help": "help",
    "line": "line [x1] [y1] [x2] [y2] [?width] [?mask]",
    "ellipse": "ellipse [xC] [yC] [xRad] [yRad] [?width] [?mask]",
    "circle": "circle [xC] [yC] [rad] [?width] [?mask]",
    "clear": "clear",
}
sh.functions = fns
sh.helps = hlps
sh.startShell()
