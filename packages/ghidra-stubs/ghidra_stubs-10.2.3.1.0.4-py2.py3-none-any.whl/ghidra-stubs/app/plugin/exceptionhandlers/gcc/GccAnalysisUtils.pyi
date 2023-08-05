from typing import List
import ghidra.program.model.address
import ghidra.program.model.listing
import java.lang


class GccAnalysisUtils(object):
    """
    Utility methods for use by the gcc exception handling analysis.
    """





    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getSLEB128Length(program: ghidra.program.model.listing.Program, addr: ghidra.program.model.address.Address) -> int:
        """
        Gets the size of a signed little endian base 128 integer.
        @param program the program with memory to be read.
        @param addr the address in memory to begin reading the signed LEB128.
        @return the length of the signed LEB128 integer.
        """
        ...

    @staticmethod
    def getULEB128Length(program: ghidra.program.model.listing.Program, addr: ghidra.program.model.address.Address) -> int:
        """
        Gets the size of an unsigned little endian base 128 integer.
        @param program the program with memory to be read.
        @param addr the address in memory to begin reading the unsigned LEB128.
        @return the length of the unsigned LEB128 integer.
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def readByte(program: ghidra.program.model.listing.Program, addr: ghidra.program.model.address.Address) -> int:
        """
        Reads a byte from the program's memory at the indicated address.
        @param program the program containing the byte to read
        @param addr the address to start reading
        @return the byte
        @throws MemoryAccessException if the byte can't be read.
        """
        ...

    @staticmethod
    def readBytes(program: ghidra.program.model.listing.Program, addr: ghidra.program.model.address.Address, buffer: List[int]) -> None:
        """
        Reads buffer.length number of bytes from the program's memory starting at the indicated address.
        @param program the program containing the bytes to read
        @param addr the address to start reading
        @param buffer the array to save the bytes that were read.
        @throws MemoryAccessException if the expected number of bytes can't be read.
        """
        ...

    @staticmethod
    def readDWord(program: ghidra.program.model.listing.Program, addr: ghidra.program.model.address.Address) -> long:
        """
        Reads a double word from the program's memory starting at the indicated address.
        @param program the program containing the bytes to read
        @param addr the address to start reading
        @return the double word
        @throws MemoryAccessException if 4 bytes can't be read.
        """
        ...

    @staticmethod
    def readQWord(program: ghidra.program.model.listing.Program, addr: ghidra.program.model.address.Address) -> long:
        """
        Reads a quad word from the program's memory starting at the indicated address.
        @param program the program containing the bytes to read
        @param addr the address to start reading
        @return the quad word
        @throws MemoryAccessException if 8 bytes can't be read.
        """
        ...

    @staticmethod
    def readSLEB128(program: ghidra.program.model.listing.Program, addr: ghidra.program.model.address.Address) -> long:
        """
        Reads an signed little endian base 128 integer from memory.
        @param program the program with memory to be read.
        @param addr the address in memory to begin reading the signed LEB128.
        @return the signed LEB128 integer.
        """
        ...

    @staticmethod
    def readULEB128(program: ghidra.program.model.listing.Program, addr: ghidra.program.model.address.Address) -> long:
        """
        Reads an unsigned little endian base 128 integer from memory.
        @param program the program with memory to be read.
        @param addr the address in memory to begin reading the unsigned LEB128.
        @return the unsigned LEB128 integer.
        """
        ...

    @staticmethod
    def readWord(program: ghidra.program.model.listing.Program, addr: ghidra.program.model.address.Address) -> int:
        """
        Reads a word from the program's memory starting at the indicated address.
        @param program the program containing the bytes to read
        @param addr the address to start reading
        @return the word
        @throws MemoryAccessException if 2 bytes can't be read.
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

