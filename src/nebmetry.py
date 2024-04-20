from __future__ import annotations
import math
from abc import ABC, abstractmethod


class Geometry(ABC):
    @abstractmethod
    def toPoints(self) -> list: ...


class Point(Geometry):

    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

    def setPoint(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def toPoints(self) -> list:
        return [self]

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Point{self}"

    def __eq__(self, other: Point) -> bool:
        isXSame: bool = self.x == other.x
        isYSame: bool = self.y == other.y
        return isXSame and isYSame

    def __ne__(self, other: Point) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)  # type: ignore

    # def __iadd__(self, other: object) -> Geometry:
    #     return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other: float) -> Point:
        newX: float = self.x * other
        newY: float = self.y * other
        return Point(newX, newY)


class LineSegment(Geometry):
    def __init__(self, point1: Point, point2: Point) -> None:
        self.point1: Point = point1
        self.point2: Point = point2

    def getLength(self) -> float:
        dX: float = self.point1.x - self.point2.x
        dY: float = self.point1.y - self.point2.y
        squareX: float = dX * dX
        squareY: float = dY * dY
        return math.sqrt(squareX + squareY)

    def getRateOfChange(self) -> float | None:
        dX: float = self.point2.x - self.point1.x
        dY: float = self.point2.y - self.point1.y
        if dX == 0:
            return None
        return dY / dX

    def getYIntercept(self) -> float | None:
        x: float = self.point1.x
        y: float = self.point1.y
        m: float | None = self.getRateOfChange()
        if m is None:
            return None
        return y - m * x

    def getXIntercept(self) -> float | None:
        m: float | None = self.getRateOfChange()
        b: float | None = self.getYIntercept()
        if m is None or b is None:
            return self.point1.x
        if m == 0:
            return None
        return -b / m

    def toPoints(self) -> list[Point]:
        x1: int = round(self.point1.x)
        y1: int = round(self.point1.y)
        x2: int = round(self.point2.x)
        y2: int = round(self.point2.y)
        # pre-process for general runner/follower and direction
        dx: int = abs(x2 - x1)
        dy: int = abs(y2 - y1)
        isYRunner: bool = dy > dx
        follwerStart: int = x1 if isYRunner else y1
        follwerEnd: int = x2 if isYRunner else y2
        runnerStart: int = y1 if isYRunner else x1
        runnerEnd: int = y2 if isYRunner else x2
        followerDirection: int = 1 if follwerStart < follwerEnd else -1
        runnerDirection: int = 1 if runnerStart < runnerEnd else -1

        # define init value/constant
        dRunner: int = max(dx, dy)
        dFollower: int = min(dx, dy)
        pk: int = 2 * dFollower - dRunner
        diffClause: int = 2 * (dFollower - dRunner)
        sameClause: int = 2 * dFollower

        # line render
        points: list[Point] = []
        if isYRunner:
            for runner in range(
                runnerStart, runnerEnd + runnerDirection, runnerDirection
            ):
                if pk > 0:
                    pk += diffClause
                    follwerStart += followerDirection
                else:
                    pk += sameClause
                point: Point = Point(follwerStart, runner)
                points.append(point)
        else:
            for runner in range(
                runnerStart, runnerEnd + runnerDirection, runnerDirection
            ):
                if pk > 0:
                    pk += diffClause
                    follwerStart += followerDirection
                else:
                    pk += sameClause
                point: Point = Point(runner, follwerStart)
                points.append(point)
        return points

    def __str__(self) -> str:
        return f"{self.point1}->{self.point2}"

    def __repr__(self) -> str:
        txt: str = (
            f"LineSegment({self})\n"
            f"- Line Length: {self.getLength()}\n"
            f"- Rate of Change: {self.getRateOfChange()}\n"
            f"- X-Intercept: {self.getXIntercept()}\n"
            f"- Y-Intercept: {self.getYIntercept()}\n"
        )
        return txt

    def __eq__(self, other: LineSegment) -> bool:
        isPoint1Same: bool = self.point1 == other.point1
        isPoint2Same: bool = self.point2 == other.point2
        return isPoint1Same and isPoint2Same

    def __ne__(self, other: LineSegment) -> bool:
        return not self.__eq__(other)


class Polygon(Geometry):
    def __init__(self, *points: Point) -> None:
        self.points: list[Point] = list(points)

    def getLineSegments(self) -> list[LineSegment]:
        segments: list[LineSegment] = []
        pointNum: int = len(self.points)
        for i in range(pointNum):
            pointNow: Point = self.points[i]
            pointNext: Point = self.points[(i + 1) % pointNum]
            segment: LineSegment = LineSegment(pointNow, pointNext)
            segments.append(segment)
        return segments

    def toPoints(self) -> list[Point]:
        pointNum: int = len(self.points)
        segments: list[LineSegment] = self.getLineSegments()
        points: list[Point] = []
        for segment in segments:
            points += segment.toPoints()
        return points

    def __str__(self) -> str:
        pointNum: int = len(self.points)
        txt: str = ""
        if pointNum > 0:
            txt += str(self.points[0])
        if pointNum > 1:
            for i in range(1, pointNum):
                point: Point = self.points[i]
                txt += f"->{point}"
        return txt

    def __repr__(self) -> str:
        pointNum: int = len(self.points)
        txt: str = f"Polygon({self})\n" f"- Point Number: {pointNum}\n"
        return txt

    # TODO
    def __eq__(self, other: Polygon) -> bool: ...

    # TODO
    def __ne__(self, other: Polygon) -> bool: ...


class PolyLine(Polygon):
    def getLineSegments(self) -> list[LineSegment]:
        segments: list[LineSegment] = []
        pointNum: int = len(self.points)
        for i in range(pointNum - 1):
            pointNow: Point = self.points[i]
            pointNext: Point = self.points[i + 1]
            segment: LineSegment = LineSegment(pointNow, pointNext)
            segments.append(segment)
        return segments


if __name__ == "__main__":
    p1: Point = Point(4.5, 3.67)
    p2: Point = Point(1, 2)
    p2 += p1
    p3: Point = Point(2, 3)
    pl1: Polygon = PolyLine(p1, p2, p3)
    l1: LineSegment = LineSegment(p1, p2)
    l2: LineSegment = LineSegment(p2, p1)
    print(f"\n{pl1}\n\n{repr(pl1)}")

    print(p2)
