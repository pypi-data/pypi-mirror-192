from typing import Iterator
from typing import List
import ghidra.program.model.address
import ghidra.program.model.reloc
import java.lang


class RelocationTable(object):
    """
    An interface for storing the relocations defined in a program.
     Table must preserve the order in which relocations are added such that
     the iterators return them in the same order.
    """

    RELOCATABLE_PROP_NAME: unicode = u'Relocatable'







    def add(self, addr: ghidra.program.model.address.Address, type: int, values: List[long], bytes: List[int], symbolName: unicode) -> ghidra.program.model.reloc.Relocation:
        """
        Creates and adds a new relocation with the specified
         address, type, and value.
        @param addr the address where the relocation is required
        @param type the type of relocation to perform
        @param values the values needed when performing the relocation.  Definition of values is
         specific to loader used and relocation type.
        @param bytes original instruction bytes affected by relocation.  A null value should be
         passed to rely on original underlying {@link FileBytes}.
        @param symbolName the name of the symbol being relocated; may be null
        @return the newly added relocation object
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getRelocationAddressAfter(self, addr: ghidra.program.model.address.Address) -> ghidra.program.model.address.Address:
        """
        Returns the next relocation address which follows the specified address.
        @param addr starting point
        @return next relocation address after addr or null if none
        """
        ...

    @overload
    def getRelocations(self) -> Iterator[ghidra.program.model.reloc.Relocation]:
        """
        Returns an iterator over all defined relocations (in ascending address order) located 
         within the program.
        @return ordered relocation iterator
        """
        ...

    @overload
    def getRelocations(self, addr: ghidra.program.model.address.Address) -> List[ghidra.program.model.reloc.Relocation]:
        """
        Returns the ordered list of relocations which have been defined for the specified address.
         In most cases there will be one or none, but in some cases multiple relocations may be
         applied to a single address.
        @param addr the address where the relocation(s) are defined
        @return the ordered list of relocations which have been defined for the specified address.
        """
        ...

    @overload
    def getRelocations(self, set: ghidra.program.model.address.AddressSetView) -> Iterator[ghidra.program.model.reloc.Relocation]:
        """
        Returns an iterator over all defined relocations (in ascending address order) located 
         within the program over the specified address set.
        @param set address set
        @return ordered relocation iterator
        """
        ...

    def getSize(self) -> int:
        """
        Returns the number of relocation in this table.
        @return the number of relocation in this table
        """
        ...

    def hasRelocation(self, addr: ghidra.program.model.address.Address) -> bool:
        """
        Determine if the specified address has a relocation defined.
        @param addr memory address within program
        @return true if relocation defined, otherwise false
        """
        ...

    def hashCode(self) -> int: ...

    def isRelocatable(self) -> bool:
        """
        Returns true if this relocation table contains relocations for a relocatable binary.
         Some binaries may contain relocations, but not actually be relocatable. For example, ELF executables.
        @return true if this relocation table contains relocations for a relocatable binary
        """
        ...

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
    def relocatable(self) -> bool: ...

    @property
    def relocations(self) -> java.util.Iterator: ...

    @property
    def size(self) -> int: ...