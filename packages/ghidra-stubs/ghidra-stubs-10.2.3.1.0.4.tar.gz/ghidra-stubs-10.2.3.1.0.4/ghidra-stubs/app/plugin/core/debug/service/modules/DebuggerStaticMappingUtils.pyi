from typing import List
import com.google.common.collect
import ghidra.app.plugin.core.debug.service.modules
import ghidra.app.services
import ghidra.framework.model
import ghidra.program.model.listing
import ghidra.program.util
import ghidra.trace.model
import ghidra.trace.model.modules
import ghidra.util.task
import java.lang
import java.util


class DebuggerStaticMappingUtils(java.lang.Enum):








    @staticmethod
    def addIdentityMapping(__a0: ghidra.trace.model.Trace, __a1: ghidra.program.model.listing.Program, __a2: com.google.common.collect.Range, __a3: bool) -> None: ...

    @overload
    @staticmethod
    def addMapping(__a0: ghidra.app.services.MapEntry, __a1: bool) -> None: ...

    @overload
    @staticmethod
    def addMapping(__a0: ghidra.trace.model.TraceLocation, __a1: ghidra.program.util.ProgramLocation, __a2: long, __a3: bool) -> None: ...

    @staticmethod
    def collectLibraries(__a0: ghidra.program.model.listing.Program, __a1: ghidra.util.task.TaskMonitor) -> java.util.Set: ...

    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def findProbableModulePrograms(__a0: ghidra.trace.model.modules.TraceModule, __a1: ghidra.framework.model.Project) -> java.util.Set: ...

    @staticmethod
    def findPrograms(__a0: unicode, __a1: ghidra.framework.model.DomainFolder) -> java.util.Set: ...

    @overload
    @staticmethod
    def findProgramsByPathOrName(__a0: unicode, __a1: ghidra.framework.model.DomainFolder) -> java.util.Set: ...

    @overload
    @staticmethod
    def findProgramsByPathOrName(__a0: unicode, __a1: ghidra.framework.model.Project) -> java.util.Set: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    @staticmethod
    def resolve(__a0: ghidra.framework.model.DomainFolder, __a1: unicode) -> ghidra.framework.model.DomainFile: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.plugin.core.debug.service.modules.DebuggerStaticMappingUtils: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.plugin.core.debug.service.modules.DebuggerStaticMappingUtils]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

