from typing import List
import ghidra.app.util.pcode
import ghidra.program.model.address
import ghidra.program.model.lang
import java.awt
import java.lang


class AttributedStringPcodeFormatter(ghidra.app.util.pcode.AbstractPcodeFormatter):




    def __init__(self):
        """
        Constructor
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    @overload
    def formatOps(self, __a0: ghidra.program.model.lang.Language, __a1: List[object]) -> object: ...

    @overload
    def formatOps(self, __a0: ghidra.program.model.lang.Language, __a1: ghidra.program.model.address.AddressFactory, __a2: List[object]) -> object: ...

    def formatTemplates(self, __a0: ghidra.program.model.lang.Language, __a1: List[object]) -> object: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getPcodeOpTemplates(__a0: ghidra.program.model.address.AddressFactory, __a1: List[object]) -> List[object]: ...

    def hashCode(self) -> int: ...

    def isFormatRaw(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setAddressColor(self, addressColor: java.awt.Color) -> None:
        """
        Set the color for addresses
        @param addressColor
        """
        ...

    def setFontMetrics(self, metrics: java.awt.FontMetrics) -> None:
        """
        Set font metrics for AttributedString objects
        @param metrics
        """
        ...

    def setLineLabelColor(self, lineLabelColor: java.awt.Color) -> None:
        """
        Set the color for labels referring to p-code ops
        @param lineLabelColor
        """
        ...

    def setLocalColor(self, localColor: java.awt.Color) -> None:
        """
        Set the color for labels referring to addresses
        @param localColor
        """
        ...

    def setMnemonicColor(self, mnemonicColor: java.awt.Color) -> None:
        """
        Set the color for op mnemonics
        @param mnemonicColor
        """
        ...

    def setOptions(self, maxDisplayLines: int, displayRawPcode: bool) -> None:
        """
        Set general formatting options
        @param maxDisplayLines
        @param displayRawPcode
        """
        ...

    def setRawColor(self, rawColor: java.awt.Color) -> None:
        """
        Set the color for raw varnodes
        @param rawColor
        """
        ...

    def setRegisterColor(self, registerColor: java.awt.Color) -> None:
        """
        Set the color for register names
        @param registerColor
        """
        ...

    def setScalarColor(self, scalarColor: java.awt.Color) -> None:
        """
        Set the color for scalars and non-address constants
        @param scalarColor
        """
        ...

    def setSeparatorColor(self, separatorColor: java.awt.Color) -> None:
        """
        Set the color for punctuation
        @param separatorColor
        """
        ...

    def setSpaceColor(self, spaceColor: java.awt.Color) -> None:
        """
        Set the color for address space names
        @param spaceColor
        """
        ...

    def setUnimplColor(self, unimplColor: java.awt.Color) -> None:
        """
        Set the color for the {@code unimpl} op mnemonic
        @param unimplColor
        """
        ...

    def setUseropColor(self, useropColor: java.awt.Color) -> None:
        """
        Set the color for userop ({@code CALLOTHER}) names
        @param useropColor
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
    def addressColor(self) -> None: ...  # No getter available.

    @addressColor.setter
    def addressColor(self, value: java.awt.Color) -> None: ...

    @property
    def fontMetrics(self) -> None: ...  # No getter available.

    @fontMetrics.setter
    def fontMetrics(self, value: java.awt.FontMetrics) -> None: ...

    @property
    def formatRaw(self) -> bool: ...

    @property
    def lineLabelColor(self) -> None: ...  # No getter available.

    @lineLabelColor.setter
    def lineLabelColor(self, value: java.awt.Color) -> None: ...

    @property
    def localColor(self) -> None: ...  # No getter available.

    @localColor.setter
    def localColor(self, value: java.awt.Color) -> None: ...

    @property
    def mnemonicColor(self) -> None: ...  # No getter available.

    @mnemonicColor.setter
    def mnemonicColor(self, value: java.awt.Color) -> None: ...

    @property
    def rawColor(self) -> None: ...  # No getter available.

    @rawColor.setter
    def rawColor(self, value: java.awt.Color) -> None: ...

    @property
    def registerColor(self) -> None: ...  # No getter available.

    @registerColor.setter
    def registerColor(self, value: java.awt.Color) -> None: ...

    @property
    def scalarColor(self) -> None: ...  # No getter available.

    @scalarColor.setter
    def scalarColor(self, value: java.awt.Color) -> None: ...

    @property
    def separatorColor(self) -> None: ...  # No getter available.

    @separatorColor.setter
    def separatorColor(self, value: java.awt.Color) -> None: ...

    @property
    def spaceColor(self) -> None: ...  # No getter available.

    @spaceColor.setter
    def spaceColor(self, value: java.awt.Color) -> None: ...

    @property
    def unimplColor(self) -> None: ...  # No getter available.

    @unimplColor.setter
    def unimplColor(self, value: java.awt.Color) -> None: ...

    @property
    def useropColor(self) -> None: ...  # No getter available.

    @useropColor.setter
    def useropColor(self, value: java.awt.Color) -> None: ...