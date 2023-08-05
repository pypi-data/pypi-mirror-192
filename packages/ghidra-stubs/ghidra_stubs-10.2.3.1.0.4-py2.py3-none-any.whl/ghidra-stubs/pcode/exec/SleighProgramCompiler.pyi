from typing import List
import ghidra.app.plugin.processors.sleigh
import ghidra.app.plugin.processors.sleigh.template
import ghidra.pcode.exec
import ghidra.pcodeCPort.sleighbase
import ghidra.pcodeCPort.slghsymbol
import ghidra.program.model.lang
import ghidra.program.model.pcode
import java.lang
import java.util


class SleighProgramCompiler(object):
    NIL_SYMBOL_NAME: unicode = u'__nil'




    class PcodeProgramConstructor(object):








        def construct(self, __a0: ghidra.app.plugin.processors.sleigh.SleighLanguage, __a1: List[object], __a2: java.util.Map) -> ghidra.pcode.exec.PcodeProgram: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

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



    @staticmethod
    def buildOps(__a0: ghidra.program.model.lang.Language, __a1: ghidra.app.plugin.processors.sleigh.template.ConstructTpl) -> List[object]: ...

    @staticmethod
    def compileExpression(__a0: ghidra.app.plugin.processors.sleigh.SleighLanguage, __a1: unicode) -> ghidra.pcode.exec.PcodeExpression: ...

    @staticmethod
    def compileProgram(__a0: ghidra.app.plugin.processors.sleigh.SleighLanguage, __a1: unicode, __a2: unicode, __a3: ghidra.pcode.exec.PcodeUseropLibrary) -> ghidra.pcode.exec.PcodeProgram: ...

    @staticmethod
    def compileTemplate(__a0: ghidra.program.model.lang.Language, __a1: ghidra.program.model.lang.PcodeParser, __a2: unicode, __a3: unicode) -> ghidra.app.plugin.processors.sleigh.template.ConstructTpl: ...

    @staticmethod
    def compileUserop(__a0: ghidra.app.plugin.processors.sleigh.SleighLanguage, __a1: unicode, __a2: List[object], __a3: unicode, __a4: ghidra.pcode.exec.PcodeUseropLibrary, __a5: List[object]) -> ghidra.pcode.exec.PcodeProgram: ...

    @staticmethod
    def constructProgram(__a0: ghidra.pcode.exec.SleighProgramCompiler.PcodeProgramConstructor, __a1: ghidra.app.plugin.processors.sleigh.SleighLanguage, __a2: ghidra.app.plugin.processors.sleigh.template.ConstructTpl, __a3: java.util.Map) -> ghidra.pcode.exec.PcodeProgram: ...

    @staticmethod
    def createParser(__a0: ghidra.app.plugin.processors.sleigh.SleighLanguage) -> ghidra.program.model.lang.PcodeParser: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def paramSym(__a0: ghidra.program.model.lang.Language, __a1: ghidra.pcodeCPort.sleighbase.SleighBase, __a2: unicode, __a3: unicode, __a4: ghidra.program.model.pcode.Varnode) -> ghidra.pcodeCPort.slghsymbol.VarnodeSymbol: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

