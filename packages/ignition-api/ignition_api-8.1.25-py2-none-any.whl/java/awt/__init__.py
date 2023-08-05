from __future__ import print_function

__all__ = [
    "AWTEvent",
    "Color",
    "Component",
    "Container",
    "Frame",
    "Graphics",
    "Image",
    "Point",
    "Toolkit",
    "Window",
]

from typing import Any, Optional

from java.awt.geom import Point2D
from java.lang import Object, String
from java.util import EventObject


class AWTEvent(EventObject):
    _id = None  # type: int

    def __init__(self, source, id):
        # type: (Object, int) -> None
        super(AWTEvent, self).__init__(source)
        self._id = id

    def getID(self):
        # type: () -> int
        return self._id

    def paramString(self):
        # type: () -> String
        pass

    def setSource(self, newSource):
        # type: (Object) -> None
        pass


class Color(Object):
    def __init__(self, *args):
        # type: (*Any) -> None
        print(args)


class Component(Object):
    def imageUpdate(
        self,
        img,  # type: Image
        infoflags,  # type: int
        x,  # type: int
        y,  # type: int
        width,  # type: int
        height,  # type: int
    ):
        # type: (...) -> bool
        return True


class Container(Component):
    def add(self, *args):
        # type: (*Any) -> Optional[Component]
        pass


class Image(Object):
    def flush(self):
        # type: () -> None
        pass

    def getAccelerationPriority(self):
        # type: () -> float
        pass

    def setAccelerationPriority(self, priority):
        # type: (float) -> None
        pass


class Point(Point2D):
    x = 0
    y = 0

    def __init__(self, *args):
        # type: (*Any) -> None
        pass

    def getLocation(self):
        # type: () -> Point
        pass

    def getX(self):
        # type: () -> float
        pass

    def getY(self):
        # type: () -> float
        pass

    def move(self, x, y):
        # type: (int, int) -> None
        pass

    def setLocation(self, *args):
        # type: (*Any) -> None
        pass

    def translate(self, dx, dy):
        # type: (int, int) -> None
        pass


class Toolkit(Object):
    def __init__(self):
        # type: () -> None
        pass

    def beep(self):
        # type: () -> None
        print(self, "Beep!")

    @staticmethod
    def getDefaultToolkit():
        # type: () -> Toolkit
        return Toolkit()


class Window(Container):
    def __init__(self, *args):
        # type: (*Any) -> None
        pass


class Frame(Window):
    def __init__(self, *args):
        # type: (*Any) -> None
        super(Frame, self).__init__(*args)


class Graphics(Object):
    def create(self):
        # type: () -> Graphics
        raise NotImplementedError
