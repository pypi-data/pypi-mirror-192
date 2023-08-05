import db
import db.util
import ghidra.framework.model
import ghidra.program.model.data
import ghidra.program.model.listing
import ghidra.util.database
import java.lang


class UndoableTransaction(java.lang.AutoCloseable, object):





    class AbstractIntUndoableTransaction(ghidra.util.database.UndoableTransaction.AbstractUndoableTransaction):




        def __init__(self, __a0: int): ...



        def abort(self) -> None: ...

        def abortOnClose(self) -> None: ...

        def close(self) -> None: ...

        def commit(self) -> None: ...

        def commitOnClose(self) -> None: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.listing.ProgramUserData) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.data.DataTypeManager, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: db.DBHandle, __a1: db.util.ErrorHandler) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode, __a2: ghidra.framework.model.AbortedTransactionListener) -> ghidra.util.database.UndoableTransaction: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class DataTypeManagerUndoableTransaction(ghidra.util.database.UndoableTransaction.AbstractIntUndoableTransaction):








        def abort(self) -> None: ...

        def abortOnClose(self) -> None: ...

        def close(self) -> None: ...

        def commit(self) -> None: ...

        def commitOnClose(self) -> None: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.listing.ProgramUserData) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.data.DataTypeManager, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: db.DBHandle, __a1: db.util.ErrorHandler) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode, __a2: ghidra.framework.model.AbortedTransactionListener) -> ghidra.util.database.UndoableTransaction: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class DomainObjectUndoableTransaction(ghidra.util.database.UndoableTransaction.AbstractIntUndoableTransaction):








        def abort(self) -> None: ...

        def abortOnClose(self) -> None: ...

        def close(self) -> None: ...

        def commit(self) -> None: ...

        def commitOnClose(self) -> None: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.listing.ProgramUserData) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.data.DataTypeManager, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: db.DBHandle, __a1: db.util.ErrorHandler) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode, __a2: ghidra.framework.model.AbortedTransactionListener) -> ghidra.util.database.UndoableTransaction: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class DBHandleUndoableTransaction(ghidra.util.database.UndoableTransaction.AbstractLongUndoableTransaction):




        def __init__(self, __a0: db.DBHandle, __a1: long, __a2: db.util.ErrorHandler): ...



        def abort(self) -> None: ...

        def abortOnClose(self) -> None: ...

        def close(self) -> None: ...

        def commit(self) -> None: ...

        def commitOnClose(self) -> None: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.listing.ProgramUserData) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.data.DataTypeManager, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: db.DBHandle, __a1: db.util.ErrorHandler) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode, __a2: ghidra.framework.model.AbortedTransactionListener) -> ghidra.util.database.UndoableTransaction: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class AbstractUndoableTransaction(object, ghidra.util.database.UndoableTransaction):








        def abort(self) -> None: ...

        def abortOnClose(self) -> None: ...

        def close(self) -> None: ...

        def commit(self) -> None: ...

        def commitOnClose(self) -> None: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.listing.ProgramUserData) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.data.DataTypeManager, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: db.DBHandle, __a1: db.util.ErrorHandler) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode, __a2: ghidra.framework.model.AbortedTransactionListener) -> ghidra.util.database.UndoableTransaction: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class ProgramUserDataUndoableTransaction(ghidra.util.database.UndoableTransaction.AbstractIntUndoableTransaction):








        def abort(self) -> None: ...

        def abortOnClose(self) -> None: ...

        def close(self) -> None: ...

        def commit(self) -> None: ...

        def commitOnClose(self) -> None: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.listing.ProgramUserData) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.data.DataTypeManager, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: db.DBHandle, __a1: db.util.ErrorHandler) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode, __a2: ghidra.framework.model.AbortedTransactionListener) -> ghidra.util.database.UndoableTransaction: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class AbstractLongUndoableTransaction(ghidra.util.database.UndoableTransaction.AbstractUndoableTransaction):




        def __init__(self, __a0: long): ...



        def abort(self) -> None: ...

        def abortOnClose(self) -> None: ...

        def close(self) -> None: ...

        def commit(self) -> None: ...

        def commitOnClose(self) -> None: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.listing.ProgramUserData) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.program.model.data.DataTypeManager, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: db.DBHandle, __a1: db.util.ErrorHandler) -> ghidra.util.database.UndoableTransaction: ...

        @overload
        @staticmethod
        def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode, __a2: ghidra.framework.model.AbortedTransactionListener) -> ghidra.util.database.UndoableTransaction: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...







    def abort(self) -> None: ...

    def abortOnClose(self) -> None: ...

    def close(self) -> None: ...

    def commit(self) -> None: ...

    def commitOnClose(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    @staticmethod
    def start(__a0: ghidra.program.model.listing.ProgramUserData) -> ghidra.util.database.UndoableTransaction: ...

    @overload
    @staticmethod
    def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

    @overload
    @staticmethod
    def start(__a0: ghidra.program.model.data.DataTypeManager, __a1: unicode) -> ghidra.util.database.UndoableTransaction: ...

    @overload
    @staticmethod
    def start(__a0: db.DBHandle, __a1: db.util.ErrorHandler) -> ghidra.util.database.UndoableTransaction: ...

    @overload
    @staticmethod
    def start(__a0: ghidra.framework.model.UndoableDomainObject, __a1: unicode, __a2: ghidra.framework.model.AbortedTransactionListener) -> ghidra.util.database.UndoableTransaction: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

