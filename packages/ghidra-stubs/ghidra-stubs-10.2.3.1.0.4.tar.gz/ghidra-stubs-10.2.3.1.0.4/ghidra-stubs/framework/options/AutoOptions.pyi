from typing import List
import generic
import ghidra.framework.options
import ghidra.framework.options.annotation
import ghidra.framework.plugintool
import ghidra.util
import java.lang
import java.lang.annotation


class AutoOptions(object):





    class OldValue(java.lang.annotation.Annotation, object):








        def annotationType(self) -> java.lang.Class: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

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






    class Wiring(object):








        def dispose(self) -> None: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

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






    class WiringImpl(object, ghidra.framework.options.AutoOptions.Wiring):




        def __init__(self, __a0: ghidra.framework.options.AutoOptionsListener): ...



        def dispose(self) -> None: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

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






    class NewValue(java.lang.annotation.Annotation, object):








        def annotationType(self) -> java.lang.Class: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

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






    class CategoryAndName(object, generic.ComparableTupleRecord):
        ACCESSORS: List[object] = [ghidra.framework.options.AutoOptions$CategoryAndName$$Lambda$481/0x00000001017557e8@70f280e0, ghidra.framework.options.AutoOptions$CategoryAndName$$Lambda$482/0x0000000101755a28@409b1007]



        @overload
        def __init__(self, __a0: unicode, __a1: unicode): ...

        @overload
        def __init__(self, __a0: ghidra.framework.options.annotation.AutoOptionConsumed, __a1: ghidra.framework.plugintool.Plugin): ...

        @overload
        def __init__(self, __a0: ghidra.framework.options.annotation.AutoOptionDefined, __a1: ghidra.framework.plugintool.Plugin): ...



        @overload
        def compareTo(self, __a0: generic.ComparableTupleRecord) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def doEquals(self, __a0: object) -> bool: ...

        def doHashCode(self) -> int: ...

        def equals(self, __a0: object) -> bool: ...

        def getCategory(self) -> unicode: ...

        def getClass(self) -> java.lang.Class: ...

        def getComparableFieldAccessors(self) -> List[object]: ...

        def getFieldAccessors(self) -> List[object]: ...

        def getName(self) -> unicode: ...

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

        @property
        def category(self) -> unicode: ...

        @property
        def comparableFieldAccessors(self) -> List[object]: ...

        @property
        def fieldAccessors(self) -> List[object]: ...

        @property
        def name(self) -> unicode: ...





    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getHelpLocation(__a0: unicode, __a1: ghidra.framework.options.annotation.HelpInfo) -> ghidra.util.HelpLocation: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def registerOptionsDefined(__a0: ghidra.framework.plugintool.Plugin, __a1: java.lang.Class, __a2: object) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @overload
    @staticmethod
    def wireOptions(__a0: ghidra.framework.plugintool.Plugin) -> ghidra.framework.options.AutoOptions.Wiring: ...

    @overload
    @staticmethod
    def wireOptions(__a0: ghidra.framework.plugintool.Plugin, __a1: object) -> ghidra.framework.options.AutoOptions.Wiring: ...

    @staticmethod
    def wireOptionsConsumed(__a0: ghidra.framework.plugintool.Plugin, __a1: object) -> ghidra.framework.options.AutoOptions.Wiring: ...

