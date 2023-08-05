import ghidra.pcode.floatformat
import java.lang
import java.math


class FloatFormat(object):
    BIG_NEGATIVE_INFINITY: java.math.BigDecimal = -1E+65536
    BIG_NaN: java.math.BigDecimal = None
    BIG_POSITIVE_INFINITY: java.math.BigDecimal = 1E+65536
    maxValue: ghidra.pcode.floatformat.BigFloat
    minValue: ghidra.pcode.floatformat.BigFloat







    def equals(self, __a0: object) -> bool: ...

    @overload
    def getBigFloat(self, encoding: long) -> ghidra.pcode.floatformat.BigFloat:
        """
        Decode {@code encoding} to a BigFloat using this format.
 
         NB: this method should not be used if {@link #size}&gt;8
        @param encoding the encoding
        @return the decoded value as a BigFloat
        """
        ...

    @overload
    def getBigFloat(self, f: float) -> ghidra.pcode.floatformat.BigFloat: ...

    @overload
    def getBigFloat(self, f: float) -> ghidra.pcode.floatformat.BigFloat: ...

    def getBigInfinity(self, sgn: bool) -> ghidra.pcode.floatformat.BigFloat: ...

    def getBigInfinityEncoding(self, sgn: bool) -> long: ...

    def getBigNaN(self, sgn: bool) -> ghidra.pcode.floatformat.BigFloat: ...

    def getBigNaNEncoding(self, sgn: bool) -> long: ...

    def getBigZero(self, sgn: bool) -> ghidra.pcode.floatformat.BigFloat: ...

    def getBigZeroEncoding(self, sgn: bool) -> long: ...

    def getClass(self) -> java.lang.Class: ...

    @overload
    def getEncoding(self, host: float) -> long: ...

    @overload
    def getEncoding(self, value: ghidra.pcode.floatformat.BigFloat) -> long: ...

    @overload
    def getHostFloat(self, encoding: long) -> float: ...

    @overload
    def getHostFloat(self, encoding: long) -> float: ...

    def getInfinityEncoding(self, sgn: bool) -> long: ...

    def getNaNEncoding(self, sgn: bool) -> long: ...

    def getSize(self) -> int: ...

    def getZeroEncoding(self, sgn: bool) -> long: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def opAbs(self, a: long) -> long: ...

    @overload
    def opAbs(self, a: long) -> long: ...

    @overload
    def opAdd(self, a: long, b: long) -> long: ...

    @overload
    def opAdd(self, a: long, b: long) -> long: ...

    @overload
    def opCeil(self, a: long) -> long: ...

    @overload
    def opCeil(self, a: long) -> long: ...

    @overload
    def opDiv(self, a: long, b: long) -> long: ...

    @overload
    def opDiv(self, a: long, b: long) -> long: ...

    @overload
    def opEqual(self, a: long, b: long) -> long: ...

    @overload
    def opEqual(self, a: long, b: long) -> long: ...

    @overload
    def opFloat2Float(self, a: long, outformat: ghidra.pcode.floatformat.FloatFormat) -> long: ...

    @overload
    def opFloat2Float(self, a: long, outformat: ghidra.pcode.floatformat.FloatFormat) -> long: ...

    @overload
    def opFloor(self, a: long) -> long: ...

    @overload
    def opFloor(self, a: long) -> long: ...

    @overload
    def opInt2Float(self, a: long, sizein: int) -> long: ...

    @overload
    def opInt2Float(self, a: long, sizein: int, signed: bool) -> long: ...

    @overload
    def opLess(self, a: long, b: long) -> long: ...

    @overload
    def opLess(self, a: long, b: long) -> long: ...

    @overload
    def opLessEqual(self, a: long, b: long) -> long: ...

    @overload
    def opLessEqual(self, a: long, b: long) -> long: ...

    @overload
    def opMult(self, a: long, b: long) -> long: ...

    @overload
    def opMult(self, a: long, b: long) -> long: ...

    @overload
    def opNan(self, a: long) -> long: ...

    @overload
    def opNan(self, a: long) -> long: ...

    @overload
    def opNeg(self, a: long) -> long: ...

    @overload
    def opNeg(self, a: long) -> long: ...

    @overload
    def opNotEqual(self, a: long, b: long) -> long: ...

    @overload
    def opNotEqual(self, a: long, b: long) -> long: ...

    @overload
    def opRound(self, a: long) -> long: ...

    @overload
    def opRound(self, a: long) -> long: ...

    @overload
    def opSqrt(self, a: long) -> long: ...

    @overload
    def opSqrt(self, a: long) -> long: ...

    @overload
    def opSub(self, a: long, b: long) -> long: ...

    @overload
    def opSub(self, a: long, b: long) -> long: ...

    @overload
    def opTrunc(self, a: long, sizeout: int) -> long: ...

    @overload
    def opTrunc(self, a: long, sizeout: int) -> long: ...

    def round(self, bigFloat: ghidra.pcode.floatformat.BigFloat) -> java.math.BigDecimal:
        """
        Round {@code bigFloat} using this format's displayContext.
        @param bigFloat any BigFloat
        @return a BigDecimal rounded according to this format's displayContext
        """
        ...

    @overload
    @staticmethod
    def toBigFloat(f: float) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param f a float
        @return BigFloat equal to {@code f}
        """
        ...

    @overload
    @staticmethod
    def toBigFloat(f: float) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param f a float
        @return BigFloat equal to {@code f}
        """
        ...

    @overload
    def toBinaryString(self, encoding: long) -> unicode:
        """
        Convert an encoded value to a binary floating point representation.
 
         NB: this method should not be used if {@link #size}&gt;8
        @param encoding the encoding of a floating point value in this format
        @return a binary string representation of the encoded floating point {@code encoding}
        """
        ...

    @overload
    @staticmethod
    def toBinaryString(f: float) -> unicode:
        """
        @param f a float
        @return binary representation of {@code f}
        """
        ...

    @overload
    @staticmethod
    def toBinaryString(f: float) -> unicode:
        """
        @param f a float
        @return binary representation of {@code f}
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
    def size(self) -> int: ...