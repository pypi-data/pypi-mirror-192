import ghidra.pcode.floatformat
import java.lang
import java.math


class BigFloat(object, java.lang.Comparable):
    """
    An IEEE 754 floating point class.

     Values represented:
 
          QUIET_NAN, SIGNALED_NAN
          -INF, +INF
          value = sign * unscaled * 2 ^ (scale-fracbits)
 
     sign = -1 or +1, unscaled has at most fracbits+1 bits, and scale is at most expbits bits.
      
     Operations compute exact result then round to nearest even.
    """









    @overload
    def abs(self) -> None:
        """
        {@code this=abs(this)}
        """
        ...

    @overload
    @staticmethod
    def abs(a: ghidra.pcode.floatformat.BigFloat) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param a a BigFloat
        @return {@code abs(a)}
        """
        ...

    @overload
    def add(self, other: ghidra.pcode.floatformat.BigFloat) -> None:
        """
        {@code this+=other}
        @param other a BigFloat
        """
        ...

    @overload
    @staticmethod
    def add(a: ghidra.pcode.floatformat.BigFloat, b: ghidra.pcode.floatformat.BigFloat) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param a a BigFloat
        @param b a BigFloat
        @return {@code a+b}
        """
        ...

    @overload
    def ceil(self) -> None:
        """
        {@code this=ceil(this)}
        """
        ...

    @overload
    @staticmethod
    def ceil(a: ghidra.pcode.floatformat.BigFloat) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param a a BigFloat
        @return {@code ceil(a)}
        """
        ...

    @overload
    def compareTo(self, other: ghidra.pcode.floatformat.BigFloat) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def copy(self) -> ghidra.pcode.floatformat.BigFloat:
        """
        @return a copy of this BigFloat
        """
        ...

    @overload
    def div(self, other: ghidra.pcode.floatformat.BigFloat) -> None:
        """
        {@code this/=other}
        @param other a BigFloat
        """
        ...

    @overload
    @staticmethod
    def div(a: ghidra.pcode.floatformat.BigFloat, b: ghidra.pcode.floatformat.BigFloat) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param a a BigFloat
        @param b a BigFloat
        @return {@code a/b}
        """
        ...

    def equals(self, obj: object) -> bool: ...

    @overload
    def floor(self) -> None:
        """
        {@code this=floor(this)}
        """
        ...

    @overload
    @staticmethod
    def floor(a: ghidra.pcode.floatformat.BigFloat) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param a a BigFloat
        @return {@code floor(a)}
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    @staticmethod
    def infinity(fracbits: int, expbits: int, sign: int) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param fracbits number of fractional bits
        @param expbits number of bits in the exponent
        @param sign +1 or -1
        @return +inf or -inf
        """
        ...

    def isDenormal(self) -> bool:
        """
        Determine if the state of this BigFloat reflects a subnormal/denormal value.
         <p>NOTE: This method relies on the manner of construction and
         only checks for {@link FloatKind#FINITE} and that the non-zero
         unscaled valued does not use all fractional bits.
        @return {@code true} if this BigFloat is FINITE and denormal
        """
        ...

    def isInfinite(self) -> bool:
        """
        @return {@code true} if this BigFloat is infinite
        """
        ...

    def isNaN(self) -> bool:
        """
        @return {@code true} if this BigFloat is NaN
        """
        ...

    def isNormal(self) -> bool:
        """
        Determine if the state of this BigFloat reflects a normalized value.
         <p>NOTE: This method relies on the manner of construction and
         only checks for {@link FloatKind#FINITE} and that full size of the
         fractional bits is used for the unscaled value.
        @return {@code true} if this BigFloat is FINITE and normal.
        """
        ...

    def isZero(self) -> bool:
        """
        @return {@code true} if this BigFloat is zero
        """
        ...

    @overload
    def mul(self, other: ghidra.pcode.floatformat.BigFloat) -> None:
        """
        {@code this*=other}
        @param other a BigFloat
        """
        ...

    @overload
    @staticmethod
    def mul(a: ghidra.pcode.floatformat.BigFloat, b: ghidra.pcode.floatformat.BigFloat) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param a a BigFloat
        @param b a BigFloat
        @return {@code a*b}
        """
        ...

    @overload
    def negate(self) -> None:
        """
        {@code this*=-1}
        """
        ...

    @overload
    @staticmethod
    def negate(a: ghidra.pcode.floatformat.BigFloat) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param a a BigFloat
        @return {@code -a}
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def quietNaN(fracbits: int, expbits: int, sign: int) -> ghidra.pcode.floatformat.BigFloat:
        """
        Return the BigFloat with the given number of bits representing (quiet) NaN.
        @param fracbits number of fractional bits
        @param expbits number of bits in the exponent
        @param sign +1 or -1
        @return a BigFloat representing (quiet) NaN
        """
        ...

    @overload
    def round(self) -> None:
        """
        Round this value to the nearest whole number
        """
        ...

    @overload
    @staticmethod
    def round(a: ghidra.pcode.floatformat.BigFloat) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param a a BigFloat
        @return {@code round(a)}
        """
        ...

    @overload
    def sqrt(self) -> None:
        """
        {@code this=sqrt(this)}
 
        	<p>Square root by abacus algorithm, Martin Guy @ UKC, June 1985.
        	From a book on programming abaci by Mr C. Woo.
        	Argument is a positive integer, as is result.

          <p>adapted from http://medialab.freaknet.org/martin/src/sqrt/sqrt.c
        """
        ...

    @overload
    @staticmethod
    def sqrt(a: ghidra.pcode.floatformat.BigFloat) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param a a BigFloat
        @return the square root of {@code a}
        """
        ...

    @overload
    def sub(self, other: ghidra.pcode.floatformat.BigFloat) -> None:
        """
        {@code this-=other}
        @param other a BigFloat
        """
        ...

    @overload
    @staticmethod
    def sub(a: ghidra.pcode.floatformat.BigFloat, b: ghidra.pcode.floatformat.BigFloat) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param a a BigFloat
        @param b a BigFloat
        @return {@code a-b}
        """
        ...

    def toBigDecimal(self) -> java.math.BigDecimal:
        """
        If finite, the returned BigDecimal is exactly equal to this.  If not finite, one of the
         FloatFormat.BIG_* constants is returned.
        @return a BigDecimal
        """
        ...

    def toBigInteger(self) -> long:
        """
        @return the truncated integer form of this BigFloat
        """
        ...

    def toBinaryString(self) -> unicode: ...

    def toString(self) -> unicode: ...

    @overload
    def trunc(self) -> None:
        """
        {@code this=trunc(this)} (round toward zero)
        """
        ...

    @overload
    @staticmethod
    def trunc(a: ghidra.pcode.floatformat.BigFloat) -> ghidra.pcode.floatformat.BigFloat:
        """
        @param a a BigFloat
        @return {@code trunc(a)} (round toward zero)
        """
        ...

    @staticmethod
    def valueOf(fracbits: int, expbits: int, i: long) -> ghidra.pcode.floatformat.BigFloat:
        """
        Return the BigFloat with the given number of bits representing the given BigInteger.
        @param fracbits number of fractional bits
        @param expbits number of bits in the exponent
        @param i an integer
        @return a BigFloat representing i
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @overload
    @staticmethod
    def zero(fracbits: int, expbits: int) -> ghidra.pcode.floatformat.BigFloat:
        """
        Return the BigFloat with the given number of bits representing (positive) zero.
        @param fracbits number of fractional bits
        @param expbits number of bits in the exponent
        @return a BigFloat representing +zero
        """
        ...

    @overload
    @staticmethod
    def zero(fracbits: int, expbits: int, sign: int) -> ghidra.pcode.floatformat.BigFloat:
        """
        Return the BigFloat with the given number of bits representing zero.
        @param fracbits number of fractional bits
        @param expbits number of bits in the exponent
        @param sign +1 or -1
        @return a BigFloat representing +zero or -zero
        """
        ...

    @property
    def denormal(self) -> bool: ...

    @property
    def infinite(self) -> bool: ...

    @property
    def naN(self) -> bool: ...

    @property
    def normal(self) -> bool: ...