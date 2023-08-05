from typing import Iterator
from typing import List
import generic.jar
import ghidra.program.model.data
import ghidra.util
import ghidra.util.task
import java.io
import java.lang
import java.util


class FileDataTypeManager(ghidra.program.model.data.StandAloneDataTypeManager, ghidra.program.model.data.FileArchiveBasedDataTypeManager):
    """
    DataTypeManager for a file. Can import categories from a file, or export
     categories to a packed database.
    """

    EXTENSION: unicode = u'gdt'
    SUFFIX: unicode = u'.gdt'







    def addDataType(self, originalDataType: ghidra.program.model.data.DataType, handler: ghidra.program.model.data.DataTypeConflictHandler) -> ghidra.program.model.data.DataType: ...

    def addDataTypeManagerListener(self, l: ghidra.program.model.data.DataTypeManagerChangeListener) -> None: ...

    def addDataTypes(self, dataTypes: java.util.Collection, handler: ghidra.program.model.data.DataTypeConflictHandler, monitor: ghidra.util.task.TaskMonitor) -> None: ...

    def addInvalidatedListener(self, listener: ghidra.program.model.data.InvalidatedListener) -> None: ...

    def allowsDefaultBuiltInSettings(self) -> bool: ...

    def allowsDefaultComponentSettings(self) -> bool: ...

    def associateDataTypeWithArchive(self, datatype: ghidra.program.model.data.DataType, archive: ghidra.program.model.data.SourceArchive) -> None: ...

    def close(self) -> None: ...

    def contains(self, dataType: ghidra.program.model.data.DataType) -> bool: ...

    def containsCategory(self, path: ghidra.program.model.data.CategoryPath) -> bool: ...

    @staticmethod
    def convertFilename(file: java.io.File) -> java.io.File:
        """
        Convert the filename for the given file to have the packed database
         file extension.
        @param file file whose name is to be converted
        @return file if the filename already ends in the packed database
         file extension, or a new File object that has the packed database
         file extension
        """
        ...

    def createCategory(self, path: ghidra.program.model.data.CategoryPath) -> ghidra.program.model.data.Category: ...

    @staticmethod
    def createFileArchive(packedDbfile: java.io.File) -> ghidra.program.model.data.FileDataTypeManager:
        """
        Create a new data-type file archive using the default data organization
        @param packedDbfile archive file (filename must end with DataTypeFileManager.SUFFIX)
        @return data-type manager backed by specified packedDbFile
        @throws IOException
        """
        ...

    def dataTypeChanged(self, dt: ghidra.program.model.data.DataType, isAutoChange: bool) -> None:
        """
        Notification when data type is changed.
        @param dt data type that is changed
        @param isAutoChange true if change was an automatic change in response to
         another datatype's change (e.g., size, alignment).
        """
        ...

    def dataTypeSettingsChanged(self, dt: ghidra.program.model.data.DataType) -> None:
        """
        Notification when data type settings have changed.
        @param dt data type that is changed
        """
        ...

    def dbError(self, e: java.io.IOException) -> None:
        """
        Handles IOExceptions
        @param e the exception to handle
        """
        ...

    @overload
    def delete(self) -> None: ...

    @overload
    @staticmethod
    def delete(packedDbfile: java.io.File) -> None: ...

    def disassociate(self, dataType: ghidra.program.model.data.DataType) -> None: ...

    def dispose(self) -> None: ...

    def endTransaction(self, transactionID: int, commit: bool) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def finalize(self) -> None: ...

    def findDataType(self, dataTypePath: unicode) -> ghidra.program.model.data.DataType: ...

    def findDataTypeForID(self, datatypeID: ghidra.util.UniversalID) -> ghidra.program.model.data.DataType: ...

    @overload
    def findDataTypes(self, __a0: unicode, __a1: List[object]) -> None: ...

    @overload
    def findDataTypes(self, __a0: unicode, __a1: List[object], __a2: bool, __a3: ghidra.util.task.TaskMonitor) -> None: ...

    def findEnumValueNames(self, value: long, enumValueNames: java.util.Set) -> None: ...

    def fixupComposites(self, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Fixup all composites and thier components which may be affected by a data organization
         change include primitive type size changes and alignment changes.  It is highly recommended
         that this program be open with exclusive access before invoking this method to avoid 
         excessive merge conflicts with other users.
        @param monitor task monitor
        @throws CancelledException if operation is cancelled
        """
        ...

    def flushEvents(self) -> None: ...

    def getAllComposites(self) -> Iterator[ghidra.program.model.data.Composite]: ...

    @overload
    def getAllDataTypes(self) -> Iterator[ghidra.program.model.data.DataType]: ...

    @overload
    def getAllDataTypes(self, __a0: List[object]) -> None: ...

    def getAllStructures(self) -> Iterator[ghidra.program.model.data.Structure]: ...

    @overload
    def getCategory(self, id: long) -> ghidra.program.model.data.Category:
        """
        Get the category for the given ID.
        @return null if no category exists with the given ID.
        """
        ...

    @overload
    def getCategory(self, path: ghidra.program.model.data.CategoryPath) -> ghidra.program.model.data.Category: ...

    def getCategoryCount(self) -> int: ...

    def getClass(self) -> java.lang.Class: ...

    def getDataOrganization(self) -> ghidra.program.model.data.DataOrganization: ...

    @overload
    def getDataType(self, dataTypeID: long) -> ghidra.program.model.data.DataType: ...

    @overload
    def getDataType(self, dataTypePath: unicode) -> ghidra.program.model.data.DataType: ...

    @overload
    def getDataType(self, dataTypePath: ghidra.program.model.data.DataTypePath) -> ghidra.program.model.data.DataType: ...

    @overload
    def getDataType(self, path: ghidra.program.model.data.CategoryPath, name: unicode) -> ghidra.program.model.data.DataType: ...

    @overload
    def getDataType(self, sourceArchive: ghidra.program.model.data.SourceArchive, datatypeID: ghidra.util.UniversalID) -> ghidra.program.model.data.DataType: ...

    def getDataTypeCount(self, includePointersAndArrays: bool) -> int: ...

    @overload
    def getDataTypes(self, path: ghidra.program.model.data.CategoryPath) -> List[ghidra.program.model.data.DataType]:
        """
        Gets the datatypes in the given category path
        @param path the category path in which to look for datatypes
        @return array of datatypes contained with specified category
        """
        ...

    @overload
    def getDataTypes(self, sourceArchive: ghidra.program.model.data.SourceArchive) -> List[ghidra.program.model.data.DataType]: ...

    def getDataTypesContaining(self, dataType: ghidra.program.model.data.DataType) -> java.util.Set: ...

    def getFavorites(self) -> List[ghidra.program.model.data.DataType]: ...

    def getFilename(self) -> unicode:
        """
        Get the filename for the current file.
        @return String filename, or null if there is no current file.
        """
        ...

    def getID(self, dt: ghidra.program.model.data.DataType) -> long: ...

    def getLastChangeTimeForMyManager(self) -> long: ...

    def getLocalSourceArchive(self) -> ghidra.program.model.data.SourceArchive: ...

    def getName(self) -> unicode: ...

    def getPath(self) -> unicode: ...

    @overload
    def getPointer(self, dt: ghidra.program.model.data.DataType) -> ghidra.program.model.data.Pointer: ...

    @overload
    def getPointer(self, dt: ghidra.program.model.data.DataType, size: int) -> ghidra.program.model.data.Pointer: ...

    def getResolvedID(self, dt: ghidra.program.model.data.DataType) -> long: ...

    def getRootCategory(self) -> ghidra.program.model.data.Category: ...

    @overload
    def getSourceArchive(self, fileID: unicode) -> ghidra.program.model.data.SourceArchive: ...

    @overload
    def getSourceArchive(self, sourceID: ghidra.util.UniversalID) -> ghidra.program.model.data.SourceArchive: ...

    def getSourceArchives(self) -> List[ghidra.program.model.data.SourceArchive]: ...

    def getType(self) -> ghidra.program.model.data.ArchiveType: ...

    def getUniqueName(self, path: ghidra.program.model.data.CategoryPath, baseName: unicode) -> unicode: ...

    def getUniversalID(self) -> ghidra.util.UniversalID: ...

    def getUnusedConflictName(self, path: ghidra.program.model.data.CategoryPath, name: unicode) -> unicode:
        """
        This method gets a ".conflict" name that is not currently used by any data
         types in the indicated category of the data type manager.
        @param path the category path of the category where the new data type live in
                     the data type manager.
        @param name The name of the data type. This name may or may not contain
                     ".conflict" as part of it. If the name contains ".conflict", only
                     the part of the name that comes prior to the ".conflict" will be
                     used to determine a new unused conflict name.
        @return the unused conflict name
        """
        ...

    def hashCode(self) -> int: ...

    def invalidateCache(self) -> None:
        """
        Invalidates the cache.
        """
        ...

    def isChanged(self) -> bool: ...

    def isClosed(self) -> bool: ...

    def isFavorite(self, dataType: ghidra.program.model.data.DataType) -> bool: ...

    def isUpdatable(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    @staticmethod
    def openFileArchive(packedDbfile: generic.jar.ResourceFile, openForUpdate: bool) -> ghidra.program.model.data.FileDataTypeManager:
        """
        Open an existing data-type file archive using the default data organization
        @param packedDbfile archive file (filename must end with DataTypeFileManager.SUFFIX)
        @param openForUpdate if true archive will be open for update
        @return data-type manager backed by specified packedDbFile
        @throws IOException
        """
        ...

    @overload
    @staticmethod
    def openFileArchive(packedDbfile: java.io.File, openForUpdate: bool) -> ghidra.program.model.data.FileDataTypeManager:
        """
        Open an existing data-type file archive using the default data organization
        @param packedDbfile archive file (filename must end with DataTypeFileManager.SUFFIX)
        @param openForUpdate if true archive will be open for update
        @return data-type manager backed by specified packedDbFile
        @throws IOException
        """
        ...

    def remove(self, dataType: ghidra.program.model.data.DataType, monitor: ghidra.util.task.TaskMonitor) -> bool: ...

    def removeDataTypeManagerListener(self, l: ghidra.program.model.data.DataTypeManagerChangeListener) -> None: ...

    def removeInvalidatedListener(self, listener: ghidra.program.model.data.InvalidatedListener) -> None: ...

    def removeSourceArchive(self, sourceArchive: ghidra.program.model.data.SourceArchive) -> None: ...

    def replaceDataType(self, existingDt: ghidra.program.model.data.DataType, replacementDt: ghidra.program.model.data.DataType, updateCategoryPath: bool) -> ghidra.program.model.data.DataType: ...

    def replaceSourceArchive(self, oldSourceArchive: ghidra.program.model.data.SourceArchive, newSourceArchive: ghidra.program.model.data.SourceArchive) -> None:
        """
        Replace one source archive (oldDTM) with another (newDTM). Any data types
         whose source was the oldDTM will be changed to have a source that is the
         newDTM. The oldDTM will no longer be referenced as a source by this data type
         manager.
        @param oldSourceArchive data type manager for the old source archive
        @param newSourceArchive data type manager for the new source archive
        @throws IllegalArgumentException if the oldDTM isn't currently a source
                                          archive for this data type manager or if the
                                          old and new source archives already have the
                                          same unique ID.
        """
        ...

    def resolve(self, dataType: ghidra.program.model.data.DataType, handler: ghidra.program.model.data.DataTypeConflictHandler) -> ghidra.program.model.data.DataType: ...

    def resolveSourceArchive(self, sourceArchive: ghidra.program.model.data.SourceArchive) -> ghidra.program.model.data.SourceArchive: ...

    def save(self) -> None:
        """
        Save the category to source file.
        """
        ...

    @overload
    def saveAs(self, saveFile: java.io.File) -> None:
        """
        Saves the data type manager to the given file
        @param saveFile the file to save
        """
        ...

    @overload
    def saveAs(self, saveFile: java.io.File, newUniversalId: ghidra.util.UniversalID) -> None:
        """
        Saves the data type manager to the given file with a specific databaseId.
         NOTE: This method is intended for use in transforming one archive database to
         match another existing archive database.
        @param saveFile the file to save
        @param newUniversalId the new id to use
        @throws DuplicateFileException
        @throws IOException
        """
        ...

    def setFavorite(self, dataType: ghidra.program.model.data.DataType, isFavorite: bool) -> None: ...

    def setName(self, name: unicode) -> None: ...

    def sourceArchiveChanged(self, sourceArchiveID: ghidra.util.UniversalID) -> None: ...

    def startTransaction(self, description: unicode) -> int: ...

    def toString(self) -> unicode: ...

    def updateID(self) -> None: ...

    @overload
    def updateSourceArchiveName(self, archiveFileID: unicode, name: unicode) -> bool: ...

    @overload
    def updateSourceArchiveName(self, sourceID: ghidra.util.UniversalID, name: unicode) -> bool: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def closed(self) -> bool: ...

    @property
    def filename(self) -> unicode: ...

    @property
    def path(self) -> unicode: ...

    @property
    def type(self) -> ghidra.program.model.data.ArchiveType: ...