"""Simple Graphics Library made by n3bch4S."""

# Thank for Graphic Library from https://mcsp.wartburg.edu/zelle/python/graphics.py
import graphics as gr
import nebmetry as gm
from typing import Callable


class KnotVector:
    def __init__(self, *unitRange: float) -> None:
        self.vector: list[float] = list(unitRange)

    def getUnitRange(self, startIdx: int, endIdx: int, frequency: int) -> list[float]:
        if startIdx < 0:
            raise ValueError("Start index must be greater than 0")
        if endIdx < 0:
            raise ValueError("End index must be greater than 0")
        if startIdx > endIdx:
            raise ValueError("Start index must be less than end index")
        if frequency < 1:
            raise ValueError("Frequency must be greater than 0")
        firstUnit: float = self.vector[startIdx]
        endUnit: float = self.vector[endIdx]
        length: float = endUnit - firstUnit
        unitRange: list[float] = [
            firstUnit + (i + 1) * length / (frequency + 1) for i in range(frequency)
        ]
        return unitRange

    def __getitem__(self, index: int) -> float:
        return self.vector[index]

    def __setitem__(self, index: int, value: float) -> None:
        self.vector[index] = value


class BlendingB:
    """experimental class"""

    def __init__(self, degree: int, controlNum: int, knotVector: KnotVector) -> None:
        preferKnotNum: int = degree + controlNum
        gotKnotNum: int = len(knotVector.vector)
        if preferKnotNum != gotKnotNum:
            raise ValueError(
                f"Knot vector length must be {preferKnotNum} but got {gotKnotNum}"
            )
        self.knotVector: KnotVector = knotVector
        self.blendingMatrix: list[list[Callable[[float], float] | None]] = []
        rowLength: int = gotKnotNum - 1
        for i in range(degree):
            row: list[Callable | None] = [None for x in range(rowLength)]
            self.blendingMatrix.append(row)

    def getFunction(self, degreePoly: int, controlNow: int) -> Callable[[float], float]:
        if degreePoly < 0:
            raise ValueError("Degree must not be negative")
        checkpoint: list[list[Callable[[float], float] | None]] = self.blendingMatrix
        lookup: Callable[[float], float] | None = checkpoint[degreePoly][controlNow]
        knot: KnotVector = self.knotVector
        if lookup is None and degreePoly == 0:
            bottom: float = knot[controlNow]
            top: float = knot[controlNow + 1]

            def func(u: float) -> float:
                if bottom <= u <= top:
                    return 1.0
                return 0.0

            lookup = func
            checkpoint[degreePoly][controlNow] = lookup

        elif lookup is None:
            degree: int = degreePoly + 1

            def func(u: float) -> float:
                for i in range(degree):
                    bottom: float = knot[controlNow + i]
                    top: float = knot[controlNow + i + 1]
                    if bottom <= u < top:
                        uk: float = knot[controlNow]
                        ukd1: float = knot[controlNow + degree - 1]
                        ukd: float = knot[controlNow + degree]
                        uk1: float = knot[controlNow + 1]
                        d1Result: float = self.getFunction(degreePoly - 1, controlNow)(
                            u
                        )
                        k1d1Result: float = self.getFunction(
                            degreePoly - 1, controlNow + 1
                        )(u)
                        firstPoly: float = (
                            (u - uk) / (ukd1 - uk) * d1Result if ukd1 - uk != 0 else 0
                        )
                        secondPoly: float = (
                            (ukd - u) / (ukd - uk1) * k1d1Result
                            if ukd - uk1 != 0
                            else 0
                        )
                        return firstPoly + secondPoly
                return 0.0

            lookup = func
            checkpoint[degreePoly][controlNow] = lookup

        return lookup


class BSpline(gm.Geometry):
    FREQUENCY: int = 1024

    def __init__(
        self, controls: list[gm.Point], degreePoly: int, knot: KnotVector
    ) -> None:
        controlNum: int = len(controls)
        degree: int = degreePoly + 1
        preferKnot: int = controlNum + degree
        gotKnot: int = len(knot.vector)
        if preferKnot != gotKnot:
            raise ValueError(
                f"The number of knots should be {preferKnot}, but got {gotKnot}"
            )
        self.degreePoly: int = degreePoly
        self.controlNum: int = controlNum
        self.controls: list[gm.Point] = controls
        self.knot: KnotVector = knot
        self.blending: BlendingB = BlendingB(degree, controlNum, knot)

    """
    sandbox zone
    knot = [5, 6, 7, 9]
    p(u) = p0B0 + p1B1 + p2B2
    """

    def pointAt(self, unit: float) -> gm.Point:
        startUnit: float = self.knot[0]
        endUnit: float = self.knot[-1]
        if unit < startUnit or unit > endUnit:
            raise ValueError(
                f"The unit is {unit}, so not in range [{startUnit}, {endUnit}]"
            )

        pointAt: gm.Point = gm.Point(0, 0)
        for pointIdx in range(self.controlNum):
            point: gm.Point = self.controls[pointIdx]
            blendingFunction: Callable[[float], float] = self.blending.getFunction(
                self.degreePoly, pointIdx
            )
            gravitationalForce: float = blendingFunction(unit)
            pointAt += point * gravitationalForce
        return pointAt

    def toPoints(self) -> list[gm.Point]:
        points: list[gm.Point] = []
        unitRange: list[float] = self.knot.getUnitRange(
            self.degreePoly, self.controlNum, self.FREQUENCY
        )
        for unit in unitRange:
            point: gm.Point = self.pointAt(unit)
            points.append(point)
        polyline: gm.PolyLine = gm.PolyLine(*points)
        return polyline.toPoints()


class RGB:
    """Contain color as a RGB value(R, G, B)

    Usage example: construct 'black' color

    - `black: RGB = RGB(0, 0, 0)`
    - `black: RGB = RGB(*RGB.BLACK)`

    """

    WHITE: tuple[int, int, int] = (255, 255, 255)
    LIGHT_GREY: tuple[int, int, int] = (191, 191, 191)
    GREY: tuple[int, int, int] = (127, 127, 127)
    DARK_GREY: tuple[int, int, int] = (63, 63, 63)
    BLACK: tuple[int, int, int] = (0, 0, 0)
    ORANGE_PANTONE: tuple[int, int, int] = (251, 97, 7)
    CITRINE: tuple[int, int, int] = (243, 222, 44)
    APPLE_GREEN: tuple[int, int, int] = (124, 181, 24)
    AVOCAADO: tuple[int, int, int] = (92, 128, 1)
    XANTHOUS: tuple[int, int, int] = (251, 176, 45)

    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red: int = red
        self.green: int = green
        self.blue: int = blue

    def getColorTuple(self) -> tuple[int, int, int]:
        return self.red, self.green, self.blue

    def setColor(self, red: int, green: int, blue: int) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self) -> str:
        return f"({self.red}, {self.green}, {self.blue})"

    def __repr__(self) -> str:
        return f"Color{self}\n"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(f"{type(self)} != {type(other)}")

        isSameRed: bool = self.red == other.red
        isSameGreen: bool = self.green == other.green
        isSameBlue: bool = self.blue == other.blue
        return isSameRed and isSameGreen and isSameBlue

    def __ne__(self, other: object) -> bool:
        return not self == other


class Pixel:
    """A pixel in the image with a color and position.

    # Usage example

    construct "black pixel at 0, 0".

    ```python
    black: RGB = RGB(*RGB.BLACK)
    pixel: Pixel = Pixel(0, 0, black)
    ```

    """

    DEFAULT_COLOR: tuple[int, int, int] = RGB.WHITE

    def __init__(self, point: gm.Point, color: RGB | None = None) -> None:
        if color is None:
            color = RGB(*self.DEFAULT_COLOR)
        self.x: float = point.x
        self.y: float = point.y
        self.color: RGB = color


class PixelMap:
    """PixelMap is 2d array contain color value(as a tuple) represent  each pixel's RGB values.

    # Usage example

    construct blank black pixel map the size of 256x256.

    - `pixmap: PixelMap = PixelMap()` default constructer usually get a default background color and size.
    - `pixmap: PixelMap = PixelMap(256, 256, (0, 0, 0))` can be custom value of size and background color.
    - `PixelMap(256, 256, *Color(Color.BLACK))` alternative way for input color like this.

    """

    DEFAULT_WIDTH: int = 800
    DEFAULT_HEIGHT: int = 600
    DEFAULT_BACKGROUND_COLOR: tuple[int, int, int] = RGB.BLACK
    DEFAULT_DRAW_COLOR: tuple[int, int, int] = RGB.WHITE

    def __init__(
        self,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        backgroundColor: RGB | None = None,
        drawColor: RGB | None = None,
    ) -> None:
        if backgroundColor is None:
            backgroundColor = RGB(*self.DEFAULT_BACKGROUND_COLOR)
        if drawColor is None:
            drawColor = RGB(*self.DEFAULT_DRAW_COLOR)
        self.width: int = width
        self.height: int = height
        self.backgroundColor: RGB = backgroundColor
        self.drawColor: RGB = drawColor

        self.pixelMap: list[list[RGB]] = []
        for i in range(width):
            newRow = []
            for j in range(height):
                newRow.append(backgroundColor)
            self.pixelMap.append(newRow)

    def __flipX(self, x: int) -> int:
        return self.width - x - 1

    def __flipY(self, y: int) -> int:
        return self.height - y - 1

    def getTotalPixel(self) -> int:
        return self.width * self.height

    def __str__(self) -> str:
        return f"[{self.width} x {self.height}]"

    def __repr__(self) -> str:
        totalPixel: int = self.getTotalPixel()
        txt: str = f"PixelMap({self})\n" f"- Total Pixel: {totalPixel}\n"
        return txt

    def __eq__(self, value: object) -> bool: ...
    def __ne__(self, value: object) -> bool: ...

    def __getitem__(self, index: int) -> list[RGB]:
        return self.pixelMap[index]

    def __setitem__(self, index: int, colorRow: list[RGB]) -> None:
        self.pixelMap[index] = colorRow


# class Window:
#     DEFAULT_WIDTH = 8
#     DEFAULT_HEIGHT = 8
#     DEFAULT_BACKGROUND_COLOR = Color(*Color.BLACK)
#     DEFAULT_PIXEL_COLOR = Color(*Color.WHITE)
#     DEFAULT_PIXEL_MAP = PixelMap(DEFAULT_WIDTH, DEFAULT_HEIGHT)

#     WINDOW_SCALE = 2
#     WINDOW_WIDTH = round(DEFAULT_WIDTH * math.sqrt(WINDOW_SCALE))
#     WINDOW_HEIGHT = round(DEFAULT_HEIGHT * math.sqrt(WINDOW_SCALE))

#     def __init__(
#         self,
#         width: int = DEFAULT_WIDTH,
#         height: int = DEFAULT_HEIGHT,
#         backgroundColor: Color = DEFAULT_BACKGROUND_COLOR,
#         pixelMap: PixelMap = DEFAULT_PIXEL_MAP,
#     ) -> None:
#         self.__width = width
#         self.__height = height
#         self.__backgroundColor = backgroundColor
#         self.__pixelMap = pixelMap

#         self.__app = pg.mkQApp("ImageItem Example")
#         self.__win = pg.GraphicsLayoutWidget()
#         self.__win.show()
#         self.__win.setWindowTitle("pyqtgraph example: ImageItem")
#         self.__view = self.__win.addViewBox()

#         self.__img = pg.ImageItem()
#         self.__img.setImage(pixelMap.getNpPixelMap())
#         self.__view.addItem(self.__img)

#     def start(self) -> None:
#         pg.exec()
#         pass

#     def stop(self) -> None:
#         pg.exit()
#         pass

#     def update(self) -> None:
#         # self.stop()
#         self.__img.setImage(self.__pixelMap.getNpPixelMap())
#         # self.start()
#         pass

#     def plotMap(self, pixelMap: PixelMap) -> None:
#         self.__pixelMap = pixelMap
#         self.update()

#     def setPixel(self, pixel: Pixel) -> None:
#         self.__pixelMap.setPixel(*pixel.getPixelTuple())
#         self.update()


class Graphics:
    DEFAULT_WINDOW_NAME: str = "Graphic"
    DEFAULT_WIDTH: int = 800
    DEFAULT_HEIGHT: int = 600
    DEFAULT_BACKGROUND_COLOR: tuple[int, int, int] = RGB.BLACK
    DEFAULT_DRAW_COLOR: tuple[int, int, int] = RGB.WHITE

    def __init__(
        self,
        windowName: str | None = None,
        width: int | None = None,
        height: int | None = None,
        backgroundColor: RGB | None = None,
        drawColor: RGB | None = None,
    ) -> None:
        if windowName is None:
            windowName = self.DEFAULT_WINDOW_NAME
        if width is None:
            width = self.DEFAULT_WIDTH
        if height is None:
            height = self.DEFAULT_HEIGHT
        if backgroundColor is None:
            backgroundColor = RGB(*self.DEFAULT_BACKGROUND_COLOR)
        if drawColor is None:
            drawColor = RGB(*self.DEFAULT_DRAW_COLOR)
        halfWidth: int = width // 2
        halfHeight: int = height // 2

        self.win: gr.GraphWin = gr.GraphWin(windowName, width, height)
        self.pixmap: PixelMap = PixelMap(width, height, backgroundColor, drawColor)
        center: gr.Point = gr.Point(halfWidth, halfHeight)
        self.image: gr.Image = gr.Image(center, width, height)
        self.objectLayer: list[tuple[gm.Geometry, RGB]] = []

    def isIn(self, point: gm.Point) -> bool:
        width: float = self.win.getWidth()
        height: float = self.win.getHeight()
        inWidth: bool = 0 <= point.x < width
        inHeight: bool = 0 <= point.y < height
        return inWidth and inHeight

    def fillBackground(self, backgroundColor: RGB | None = None) -> None:
        if backgroundColor is None:
            backgroundColor = RGB(*self.DEFAULT_BACKGROUND_COLOR)
        width: int = self.image.getWidth()
        height: int = self.image.getHeight()
        color: str = gr.color_rgb(*backgroundColor.getColorTuple())
        for y in range(height):
            for x in range(width):
                self.image.setPixel(x, y, color)

    def drawObject(self, object: gm.Geometry, drawColor: RGB | None = None) -> None:
        if drawColor is None:
            drawColor = RGB(*self.DEFAULT_DRAW_COLOR)
        points: list[gm.Point] = object.toPoints()
        flipY: int = self.image.getHeight() - 1
        color: str = gr.color_rgb(*drawColor.getColorTuple())
        for point in points:
            if self.isIn(point):
                self.image.setPixel(point.x, flipY - point.y, color)

    def drawObjects(self, objects: list[tuple[gm.Geometry, RGB]]) -> None:
        for object in objects:
            self.drawObject(object[0], object[1])

    def refresh(self) -> None:
        self.image.undraw()
        self.fillBackground()
        self.drawObjects(self.objectLayer)
        self.image.draw(self.win)
        self.win.getMouse()

    def __getitem__(self, index: int) -> tuple[gm.Geometry, RGB]:
        return self.objectLayer[index]

    def __setitem__(self, index: int, value: tuple[gm.Geometry, RGB]) -> None:
        self.objectLayer[index] = value
        self.refresh()


if __name__ == "__main__":
    graphics: Graphics = Graphics()
    width: float = graphics.win.getWidth()
    height: float = graphics.win.getHeight()
    halfWidth: float = width // 2
    halfHeight: float = height // 2
    horizonBorder: gm.LineSegment = gm.LineSegment(
        gm.Point(0, halfHeight), gm.Point(width - 1, halfHeight)
    )
    verticalBorder: gm.LineSegment = gm.LineSegment(
        gm.Point(halfWidth, 0), gm.Point(halfWidth, height - 1)
    )
    graphics.objectLayer.append((horizonBorder, RGB(*RGB.WHITE)))
    graphics.objectLayer.append((verticalBorder, RGB(*RGB.WHITE)))

    degreePoly: int = 3
    knot: KnotVector = KnotVector(0, 0, 0, 0, 1, 1, 1, 1)

    p1: gm.Point = gm.Point(30, 550)
    p2: gm.Point = gm.Point(150, 530)
    p3: gm.Point = gm.Point(-70, 430)
    p4: gm.Point = gm.Point(50, 350)
    controls: list[gm.Point] = [p1, p2, p3, p4]
    baseLine: gm.PolyLine = gm.PolyLine(*controls)
    spline: BSpline = BSpline(controls, degreePoly, knot)
    graphics.objectLayer.append((baseLine, RGB(*RGB.DARK_GREY)))
    graphics.objectLayer.append((spline, RGB(*RGB.CITRINE)))

    p1: gm.Point = gm.Point(50, 350)
    p2: gm.Point = gm.Point(75, 340)
    p3: gm.Point = gm.Point(100, 340)
    p4: gm.Point = gm.Point(125, 350)
    controls: list[gm.Point] = [p1, p2, p3, p4]
    baseLine: gm.PolyLine = gm.PolyLine(*controls)
    spline: BSpline = BSpline(controls, degreePoly, knot)
    graphics.objectLayer.append((baseLine, RGB(*RGB.DARK_GREY)))
    graphics.objectLayer.append((spline, RGB(*RGB.CITRINE)))

    graphics.refresh()
