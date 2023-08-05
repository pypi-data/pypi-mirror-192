from typing import List
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf4
import java.lang


class LEB128(object):
    """
    Class to hold result of reading a LEB128 value, along with size and position metadata.
 
     Note: If a LEB128 value that would result in a native value longer than 64bits is attempted to
     be read, an IOException will be thrown, and the stream's position will be left at the last read byte.
 
     If this was a valid (but overly large) LEB128, the caller's stream will be left still pointing to LEB data.
 
    """









    def asInt32(self) -> int:
        """
        Returns the value as an signed int32.  If the actual value
         is outside the range of a java int (ie.  {@link Integer#MIN_VALUE}.. {@link Integer#MAX_VALUE}),
         an exception is thrown.
        @return int in the range of {@link Integer#MIN_VALUE} to  {@link Integer#MAX_VALUE}
        @throws IOException if value is outside range
        """
        ...

    def asLong(self) -> long:
        """
        Returns the value as a 64bit primitive long.  Interpreting the signed-ness of the
         value will depend on the way the value was read (ie. if {@link #readSignedValue(BinaryReader)}
         vs. {@link #readUnsignedValue(BinaryReader)} was used).
        @return long value.
        """
        ...

    def asUInt32(self) -> int:
        """
        Returns the value as an unsigned int32.  If the actual value
         is outside the positive range of a java int (ie. 0.. {@link Integer#MAX_VALUE}),
         an exception is thrown.
        @return int in the range of 0 to  {@link Integer#MAX_VALUE}
        @throws IOException if value is outside range
        """
        ...

    @overload
    @staticmethod
    def decode(bytes: List[int], isSigned: bool) -> long:
        """
        Decodes a LEB128 number from a byte array and returns it as a long.
         <p>
         See {@link #readAsLong(BinaryReader, boolean)}.
        @param bytes the bytes representing the LEB128 number
        @param isSigned true if the value is signed
        @return long integer value.  Caller must treat it as unsigned if isSigned parameter was
         set to false
        @throws IOException if error reading bytes or value is outside the
         range of a java 64 bit int
        """
        ...

    @overload
    @staticmethod
    def decode(bytes: List[int], offset: int, isSigned: bool) -> long:
        """
        Decodes a LEB128 number from a byte array and returns it as a long.
         <p>
         See {@link #readAsLong(BinaryReader, boolean)}.
        @param bytes the bytes representing the LEB128 number
        @param offset offset in byte array of where to start reading bytes
        @param isSigned true if the value is signed
        @return long integer value.  Caller must treat it as unsigned if isSigned parameter was
         set to false
        @throws IOException if error reading bytes or value is outside the
         range of a java 64 bit int
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getLength(self) -> int:
        """
        Returns the number of bytes that were used to store the LEB128 value in the stream
         it was read from.
        @return number of bytes used to store the read LEB128 value
        """
        ...

    def getOffset(self) -> long:
        """
        Returns the offset of the LEB128 value in the stream it was read from.
        @return stream offset of the LEB128 value
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def readAsInt32(reader: ghidra.app.util.bin.BinaryReader) -> int:
        """
        Reads a LEB128 signed number from the BinaryReader and returns it as a java 32 bit int.
         <p>
         If the value of the number can not fit in the int type, an {@link IOException} will
         be thrown.
        @param reader {@link BinaryReader} to read bytes from
        @return signed int32 value
        @throws IOException if error reading bytes or value is outside the
         range of a signed int32
        """
        ...

    @staticmethod
    def readAsLong(reader: ghidra.app.util.bin.BinaryReader, isSigned: bool) -> long:
        """
        Reads a LEB128 number from the BinaryReader and returns it as a java 64 bit long int.
         <p>
         Large unsigned integers that use all 64 bits are be returned in a java native
         'long' type, which is signed.  It is up to the caller to treat the value as unsigned.
         <p>
         Large integers that use more than 64 bits will cause an IOException to be thrown.
         <p>
        @param reader {@link BinaryReader} to read bytes from
        @param isSigned true if the value is signed
        @return long integer value.  Caller must treat it as unsigned if isSigned parameter was
         set to false
        @throws IOException if an I/O error occurs or value is outside the range of a java
         64 bit int
        """
        ...

    @staticmethod
    def readAsUInt32(reader: ghidra.app.util.bin.BinaryReader) -> int:
        """
        Reads a LEB128 unsigned number from the BinaryReader and returns it as a java 32 bit int.
         <p>
         If the value of the number can not fit in the positive range of the int type,
         an {@link IOException} will be thrown.
        @param reader {@link BinaryReader} to read bytes from
        @return unsigned int32 value 0..Integer.MAX_VALUE
        @throws IOException if error reading bytes or value is outside the
         positive range of a java 32 bit int (ie. 0..Integer.MAX_VALUE)
        """
        ...

    @staticmethod
    def readSignedValue(reader: ghidra.app.util.bin.BinaryReader) -> ghidra.app.util.bin.format.dwarf4.LEB128:
        """
        Reads an signed LEB128 value from the BinaryReader and returns a {@link LEB128} instance
         that contains the value along with size and position metadata.
         <p>
         See {@link #readAsLong(BinaryReader, boolean)}.
        @param reader {@link BinaryReader} to read bytes from
        @return a {@link LEB128} instance with the read LEB128 value with metadata
        @throws IOException if an I/O error occurs or value is outside the range of a java
         64 bit int
        """
        ...

    @staticmethod
    def readUnsignedValue(reader: ghidra.app.util.bin.BinaryReader) -> ghidra.app.util.bin.format.dwarf4.LEB128:
        """
        Reads an unsigned LEB128 value from the BinaryReader and returns a {@link LEB128} instance
         that contains the value along with size and position metadata.
         <p>
         See {@link #readAsLong(BinaryReader, boolean)}.
        @param reader {@link BinaryReader} to read bytes from
        @return a {@link LEB128} instance with the read LEB128 value with metadata
        @throws IOException if an I/O error occurs or value is outside the range of a java
         64 bit int
        """
        ...

    @staticmethod
    def readValue(reader: ghidra.app.util.bin.BinaryReader, isSigned: bool) -> ghidra.app.util.bin.format.dwarf4.LEB128:
        """
        Reads a LEB128 value from the BinaryReader and returns a {@link LEB128} instance
         that contains the value along with size and position metadata.
         <p>
         See {@link #readAsLong(BinaryReader, boolean)}.
        @param reader {@link BinaryReader} to read bytes from
        @param isSigned true if the value is signed
        @return a {@link LEB128} instance with the read LEB128 value with metadata
        @throws IOException if an I/O error occurs or value is outside the range of a java
         64 bit int
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def length(self) -> int: ...

    @property
    def offset(self) -> long: ...