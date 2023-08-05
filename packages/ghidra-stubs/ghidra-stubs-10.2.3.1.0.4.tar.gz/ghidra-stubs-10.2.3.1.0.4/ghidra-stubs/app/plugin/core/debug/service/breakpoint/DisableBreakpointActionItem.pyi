import ghidra.app.plugin.core.debug.service.breakpoint
import java.lang
import java.util.concurrent


class DisableBreakpointActionItem(object, ghidra.app.plugin.core.debug.service.breakpoint.BreakpointActionItem):




    def __init__(self, __a0: ghidra.dbg.target.TargetTogglable): ...



    def equals(self, __a0: object) -> bool: ...

    def execute(self) -> java.util.concurrent.CompletableFuture: ...

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

