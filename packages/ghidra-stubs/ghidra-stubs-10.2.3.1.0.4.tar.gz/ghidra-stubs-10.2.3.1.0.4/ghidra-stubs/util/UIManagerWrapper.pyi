import java.awt
import java.lang
import javax.swing.border


class UIManagerWrapper(object):




    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def getBorder(__a0: unicode) -> javax.swing.border.Border: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getColor(__a0: unicode) -> java.awt.Color: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

