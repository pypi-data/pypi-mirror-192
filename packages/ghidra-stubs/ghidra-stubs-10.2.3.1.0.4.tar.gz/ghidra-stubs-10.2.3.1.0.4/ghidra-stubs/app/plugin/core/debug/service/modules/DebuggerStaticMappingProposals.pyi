from typing import List
import ghidra.app.plugin.core.debug.service.modules
import ghidra.app.services
import ghidra.program.model.listing
import ghidra.program.model.mem
import ghidra.trace.model.memory
import ghidra.trace.model.modules
import java.lang
import java.util
import java.util.function


class DebuggerStaticMappingProposals(java.lang.Enum):








    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    @staticmethod
    def groupByComponents(__a0: java.util.Collection, __a1: java.util.function.Function, __a2: java.util.function.BiPredicate) -> java.util.Set: ...

    @staticmethod
    def groupRegionsByLikelyModule(__a0: java.util.Collection) -> java.util.Set: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    @overload
    @staticmethod
    def proposeModuleMap(__a0: ghidra.trace.model.modules.TraceModule, __a1: ghidra.program.model.listing.Program) -> ghidra.app.services.ModuleMapProposal: ...

    @overload
    @staticmethod
    def proposeModuleMap(__a0: ghidra.trace.model.modules.TraceModule, __a1: java.util.Collection) -> ghidra.app.services.ModuleMapProposal: ...

    @staticmethod
    def proposeModuleMaps(__a0: java.util.Collection, __a1: java.util.Collection) -> java.util.Map: ...

    @overload
    @staticmethod
    def proposeRegionMap(__a0: java.util.Collection, __a1: ghidra.program.model.listing.Program) -> ghidra.app.services.RegionMapProposal: ...

    @overload
    @staticmethod
    def proposeRegionMap(__a0: java.util.Collection, __a1: java.util.Collection) -> ghidra.app.services.RegionMapProposal: ...

    @overload
    @staticmethod
    def proposeRegionMap(__a0: ghidra.trace.model.memory.TraceMemoryRegion, __a1: ghidra.program.model.listing.Program, __a2: ghidra.program.model.mem.MemoryBlock) -> ghidra.app.services.RegionMapProposal: ...

    @staticmethod
    def proposeRegionMaps(__a0: java.util.Collection, __a1: java.util.Collection) -> java.util.Map: ...

    @overload
    @staticmethod
    def proposeSectionMap(__a0: ghidra.trace.model.modules.TraceModule, __a1: ghidra.program.model.listing.Program) -> ghidra.app.services.SectionMapProposal: ...

    @overload
    @staticmethod
    def proposeSectionMap(__a0: ghidra.trace.model.modules.TraceModule, __a1: java.util.Collection) -> ghidra.app.services.SectionMapProposal: ...

    @overload
    @staticmethod
    def proposeSectionMap(__a0: ghidra.trace.model.modules.TraceSection, __a1: ghidra.program.model.listing.Program, __a2: ghidra.program.model.mem.MemoryBlock) -> ghidra.app.services.SectionMapProposal: ...

    @staticmethod
    def proposeSectionMaps(__a0: java.util.Collection, __a1: java.util.Collection) -> java.util.Map: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.plugin.core.debug.service.modules.DebuggerStaticMappingProposals: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.plugin.core.debug.service.modules.DebuggerStaticMappingProposals]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

