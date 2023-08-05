import ghidra.framework.model
import ghidra.trace.model
import ghidra.trace.util
import java.lang


class TraceDomainObjectListener(object, ghidra.framework.model.DomainObjectListener):





    class AffectedAndValuesOnlyHandler(ghidra.trace.model.TraceDomainObjectListener.EventRecordHandler, object):








        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        @overload
        def handle(self, __a0: ghidra.trace.util.TraceChangeRecord) -> None: ...

        @overload
        def handle(self, __a0: object, __a1: object, __a2: object) -> None: ...

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






    class SpaceValuesHandler(ghidra.trace.model.TraceDomainObjectListener.EventRecordHandler, object):








        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        @overload
        def handle(self, __a0: ghidra.trace.util.TraceChangeRecord) -> None: ...

        @overload
        def handle(self, __a0: ghidra.trace.util.TraceAddressSpace, __a1: object, __a2: object) -> None: ...

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






    class AffectedObjectHandler(ghidra.trace.model.TraceDomainObjectListener.EventRecordHandler, object):








        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        @overload
        def handle(self, __a0: ghidra.trace.util.TraceChangeRecord) -> None: ...

        @overload
        def handle(self, __a0: ghidra.trace.util.TraceAddressSpace, __a1: object) -> None: ...

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






    class FullEventRecordHandler(ghidra.trace.model.TraceDomainObjectListener.EventRecordHandler, object):








        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        @overload
        def handle(self, __a0: ghidra.trace.util.TraceChangeRecord) -> None: ...

        @overload
        def handle(self, __a0: ghidra.trace.util.TraceAddressSpace, __a1: object, __a2: object, __a3: object) -> None: ...

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






    class AffectedObjectOnlyHandler(ghidra.trace.model.TraceDomainObjectListener.EventRecordHandler, object):








        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        @overload
        def handle(self, __a0: ghidra.trace.util.TraceChangeRecord) -> None: ...

        @overload
        def handle(self, __a0: object) -> None: ...

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






    class IgnoreAllHandler(ghidra.trace.model.TraceDomainObjectListener.EventRecordHandler, object):








        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        @overload
        def handle(self) -> None: ...

        @overload
        def handle(self, __a0: ghidra.trace.util.TraceChangeRecord) -> None: ...

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






    class EventRecordHandler(object):








        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def handle(self, __a0: ghidra.trace.util.TraceChangeRecord) -> None: ...

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






    class ValuesOnlyHandler(ghidra.trace.model.TraceDomainObjectListener.EventRecordHandler, object):








        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        @overload
        def handle(self, __a0: ghidra.trace.util.TraceChangeRecord) -> None: ...

        @overload
        def handle(self, __a0: object, __a1: object) -> None: ...

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






    class IgnoreValuesHandler(ghidra.trace.model.TraceDomainObjectListener.EventRecordHandler, object):








        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        @overload
        def handle(self, __a0: ghidra.trace.util.TraceAddressSpace) -> None: ...

        @overload
        def handle(self, __a0: ghidra.trace.util.TraceChangeRecord) -> None: ...

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



    def __init__(self): ...



    def domainObjectChanged(self, __a0: ghidra.framework.model.DomainObjectChangedEvent) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def handleTraceChangeRecord(self, __a0: ghidra.trace.util.TraceChangeRecord) -> None: ...

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

