import ghidra.app.plugin.core.debug.service.emulation
import ghidra.trace.model
import ghidra.trace.model.guest
import ghidra.trace.model.time.schedule
import ghidra.util.task
import java.lang
import java.util
import java.util.concurrent


class DebuggerEmulationService(object):








    def backgroundEmulate(self, __a0: ghidra.trace.model.guest.TracePlatform, __a1: ghidra.trace.model.time.schedule.TraceSchedule) -> java.util.concurrent.CompletableFuture: ...

    @overload
    def emulate(self, __a0: ghidra.trace.model.Trace, __a1: ghidra.trace.model.time.schedule.TraceSchedule, __a2: ghidra.util.task.TaskMonitor) -> long: ...

    @overload
    def emulate(self, __a0: ghidra.trace.model.guest.TracePlatform, __a1: ghidra.trace.model.time.schedule.TraceSchedule, __a2: ghidra.util.task.TaskMonitor) -> long: ...

    def equals(self, __a0: object) -> bool: ...

    def getCachedEmulator(self, __a0: ghidra.trace.model.Trace, __a1: ghidra.trace.model.time.schedule.TraceSchedule) -> ghidra.app.plugin.core.debug.service.emulation.DebuggerPcodeMachine: ...

    def getClass(self) -> java.lang.Class: ...

    def getEmulatorFactories(self) -> java.util.Collection: ...

    def getEmulatorFactory(self) -> ghidra.app.plugin.core.debug.service.emulation.DebuggerPcodeEmulatorFactory: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setEmulatorFactory(self, __a0: ghidra.app.plugin.core.debug.service.emulation.DebuggerPcodeEmulatorFactory) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def emulatorFactories(self) -> java.util.Collection: ...

    @property
    def emulatorFactory(self) -> ghidra.app.plugin.core.debug.service.emulation.DebuggerPcodeEmulatorFactory: ...

    @emulatorFactory.setter
    def emulatorFactory(self, value: ghidra.app.plugin.core.debug.service.emulation.DebuggerPcodeEmulatorFactory) -> None: ...