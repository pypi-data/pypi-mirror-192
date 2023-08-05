from typing import List
import java.lang


class MultipleProgramsStrategy(object):
    ALL_PROGRAMS: ghidra.app.util.importer.MultipleProgramsStrategy = ghidra.app.util.importer.MultipleProgramsStrategy$1@40c20adc
    ONE_PROGRAM_OR_EXCEPTION: ghidra.app.util.importer.MultipleProgramsStrategy = ghidra.app.util.importer.MultipleProgramsStrategy$2@18e98f7f
    ONE_PROGRAM_OR_NULL: ghidra.app.util.importer.MultipleProgramsStrategy = ghidra.app.util.importer.MultipleProgramsStrategy$3@225159fb







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def handlePrograms(self, __a0: List[object], __a1: object) -> List[object]: ...

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

