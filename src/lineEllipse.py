from graphics import GraphWin, Image, Point, Text, color_rgb

""" SETTING """

SCREEN_NAME = "CG"
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 512
SCREEN_COLOR = color_rgb(0, 0, 0)  # BLACK
LINE_COLOR = color_rgb(255, 255, 255)  # White
DRAW_RATE = 1024  # Frequency of point using unit time step
SHELL_NAME = "slowCG"
"""  """
# library from https://mcsp.wartburg.edu/zelle/python/graphics.py
import math

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


def isInteger(x: float):
    x = float(x)

    return x % 1 == 0


# FLIP SPACE UPSIDE DOWN
def flip(y: int) -> int:
    return SCREEN_HEIGHT - y


def drawPoint(x: int, y: int, color: str = LINE_COLOR) -> None:
    SCREEN.plot(x, y, color=color)


def drawPoints(pointsList: list[tuple[int, int]], color: str = LINE_COLOR) -> None:
    for x, y in pointsList:
        SCREEN.plot(x, y, color=color)


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


def line(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    width: int = 1,
    color: str = LINE_COLOR,
    mask: str = "1",
) -> None:
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
    xC: int,
    yC: int,
    xRad: int,
    yRad: int,
    width: int = 1,
    color: str = LINE_COLOR,
    mask: str = "1",
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


def circle(
    xC: int, yC: int, rad: int, width: int = 1, color: str = LINE_COLOR, mask: str = "1"
) -> None:
    xC, yC, rad, width = intArgs(xC, yC, rad, width)
    ellipse(xC, yC, xRad=rad, yRad=rad, width=width, color=color, mask=mask)


def stepEpitrochoid(a: int, b: int, k: int) -> list[tuple[int, int]]:
    pointList = []

    # CONSTANT
    aPlusB = a + b
    aDivB = a / b
    doubPi = math.pi * 2
    innerK = doubPi * aPlusB / b

    stepT = 1 / DRAW_RATE
    t = 0
    oldPoint = ("", "")
    while not (
        isInteger(t * aDivB) and isInteger(t) and t != 0
    ):  # recurrence properties of ocillation from sin, cos
        x = aPlusB * math.cos(doubPi * t) - k * math.cos(innerK * t)
        y = aPlusB * math.sin(doubPi * t) - k * math.sin(innerK * t)
        x = round(x)
        y = round(y)
        point = x, y

        """only keep new point relate to previous point for faster rendering(a bit)"""
        if oldPoint != point:
            pointList.append(point)
        oldPoint = point

        t += stepT

    return pointList


def stepHypotrochoid(a: int, b: int, k: int) -> list[tuple[int, int]]:
    pointList = []

    # CONSTANT
    aMinusB = a - b
    aDivB = a / b
    doubPi = math.pi * 2
    innerK = doubPi * aMinusB / b

    stepT = 1 / DRAW_RATE
    t = 0
    oldPoint = ("", "")
    while not (
        isInteger(t * aDivB) and isInteger(t) and t != 0
    ):  # recurrence properties of ocillation from sin, cos
        x = aMinusB * math.cos(doubPi * t) + k * math.cos(innerK * t)
        y = aMinusB * math.sin(doubPi * t) - k * math.sin(innerK * t)
        x = round(x)
        y = round(y)
        point = x, y

        """only keep new point relate to previous point for faster rendering(a bit)"""
        if oldPoint != point:
            pointList.append(point)
        oldPoint = point

        t += stepT

    return pointList


def epitrochoid(
    xC: int,
    yC: int,
    a: int,
    b: int,
    k: int,
    thickness: int = 1,
    color: str = LINE_COLOR,
) -> None:
    xC, yC, a, b, k, thickness = intArgs(xC, yC, a, b, k, thickness)
    yC = flip(yC)

    # Get base line
    pointList = stepEpitrochoid(a, b, k)

    # Bolding
    i = 0
    while thickness > 1:
        sign = pow(-1, i)
        bold = i // 2 * sign + 1 * sign
        pointList += stepEpitrochoid(a, b, k + bold)
        thickness -= 1
        i += 1

    pointList = translateTo(xC, yC, pointList)
    drawPoints(pointList, color)


def hypotrochoid(
    xC: int,
    yC: int,
    a: int,
    b: int,
    k: int,
    thickness: int = 1,
    color: str = LINE_COLOR,
) -> None:
    xC, yC, a, b, k, thickness = intArgs(xC, yC, a, b, k, thickness)
    yC = flip(yC)

    # Get base line
    pointList = stepHypotrochoid(a, b, k)

    # Bolding
    i = 0
    while thickness > 1:
        sign = pow(-1, i)
        bold = i // 2 * sign + 1 * sign
        pointList += stepHypotrochoid(a, b, k + bold)
        thickness -= 1
        i += 1

    pointList = translateTo(xC, yC, pointList)
    drawPoints(pointList, color)


# TODO assignment 3
# (a) a = 20, b = 15, k = 30 with red color and 1-pixel thick
epitrochoid(128, 384, 20, 15, 30, thickness=1, color=color_rgb(255, 64, 64))
hypotrochoid(128, 128, 20, 15, 30, thickness=1, color=color_rgb(255, 64, 64))
textA = Text(Point(128, 256), "a=20 b=15 k=30 red 1thick")
textA.setTextColor(LINE_COLOR)
textA.draw(SCREEN)

# (b) a = 30, b = 45, k = 20 with green color and 3-pixel thick
epitrochoid(320, 384, 30, 45, 20, thickness=3, color=color_rgb(64, 255, 64))
hypotrochoid(320, 128, 30, 45, 20, thickness=3, color=color_rgb(64, 255, 64))
textB = Text(Point(320, 256), "a=30 b=45 k=20 green 3thick")
textB.setTextColor(LINE_COLOR)
textB.draw(SCREEN)

# (c) a = 50, b = 35, k = 15 with blue color and 2-pixel thick
epitrochoid(576, 384, 50, 35, 15, thickness=2, color=color_rgb(64, 64, 255))
hypotrochoid(576, 128, 50, 35, 15, thickness=2, color=color_rgb(64, 64, 255))
textC = Text(Point(576, 256), "a=50 b=35 k=15 blue 2thick")
textC.setTextColor(LINE_COLOR)
textC.draw(SCREEN)

# (d) a = 15, b = 55, k = 35 with purple color and 3-pixel thick
epitrochoid(832, 384, 15, 55, 35, thickness=3, color=color_rgb(255, 64, 255))
hypotrochoid(832, 128, 15, 55, 35, thickness=3, color=color_rgb(255, 64, 255))
textD = Text(Point(832, 256), "a=15 b=55 k=35 purple 3thick")
textD.setTextColor(LINE_COLOR)
textD.draw(SCREEN)


"""Holly area don't touch"""
# library from https://github.com/n3bch4S/nebchell/blob/main/lib/nebchell.py
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
