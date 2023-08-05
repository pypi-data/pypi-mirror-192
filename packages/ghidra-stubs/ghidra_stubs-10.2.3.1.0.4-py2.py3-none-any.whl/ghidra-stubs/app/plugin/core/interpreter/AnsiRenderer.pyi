import java.lang
import javax.swing.text


class AnsiRenderer(object):
    BLACK: java.awt.Color = java.awt.Color[r=0,g=0,b=0]
    BLUE: java.awt.Color = java.awt.Color[r=73,g=46,b=225]
    CYAN: java.awt.Color = java.awt.Color[r=51,g=187,b=200]
    GREEN: java.awt.Color = java.awt.Color[r=37,g=188,b=36]
    HI_BLACK: java.awt.Color = java.awt.Color[r=129,g=131,b=131]
    HI_BLUE: java.awt.Color = java.awt.Color[r=88,g=51,b=255]
    HI_CYAN: java.awt.Color = java.awt.Color[r=20,g=240,b=240]
    HI_GREEN: java.awt.Color = java.awt.Color[r=49,g=231,b=34]
    HI_MAGENTA: java.awt.Color = java.awt.Color[r=249,g=53,b=248]
    HI_RED: java.awt.Color = java.awt.Color[r=252,g=57,b=31]
    HI_WHITE: java.awt.Color = java.awt.Color[r=233,g=235,b=235]
    HI_YELLOW: java.awt.Color = java.awt.Color[r=234,g=236,b=35]
    MAGENTA: java.awt.Color = java.awt.Color[r=211,g=56,b=211]
    RED: java.awt.Color = java.awt.Color[r=194,g=54,b=33]
    WHITE: java.awt.Color = java.awt.Color[r=203,g=204,b=205]
    YELLOW: java.awt.Color = java.awt.Color[r=173,g=173,b=39]



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def renderString(self, __a0: javax.swing.text.StyledDocument, __a1: unicode, __a2: javax.swing.text.MutableAttributeSet) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

