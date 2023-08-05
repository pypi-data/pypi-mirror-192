import docking.action
import ghidra.app.plugin.core.debug
import ghidra.pcode.exec
import ghidra.program.model.address
import ghidra.trace.model.guest
import java.lang
import java.util.concurrent


class DebuggerGoToTrait(object):




    def __init__(self, __a0: ghidra.framework.plugintool.PluginTool, __a1: ghidra.framework.plugintool.Plugin, __a2: docking.ComponentProvider): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def goToCoordinates(self, __a0: ghidra.app.plugin.core.debug.DebuggerCoordinates) -> None: ...

    @overload
    def goToSleigh(self, __a0: unicode, __a1: unicode) -> java.util.concurrent.CompletableFuture: ...

    @overload
    def goToSleigh(self, __a0: ghidra.trace.model.guest.TracePlatform, __a1: ghidra.program.model.address.AddressSpace, __a2: ghidra.pcode.exec.PcodeExpression) -> java.util.concurrent.CompletableFuture: ...

    def hashCode(self) -> int: ...

    def installAction(self) -> docking.action.DockingAction: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

