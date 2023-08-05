import java.lang


class ImageManager(object):
    """
    Static helper to register and load Icons for the file system browser plugin and its
     child windows.
 
     Visible to just this package.
    """

    CLOSE: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/door.png
    COLLAPSE_ALL: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/arrow_in.png
    COMPRESS: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/compress.png
    COPY: javax.swing.ImageIcon = images/page_copy.png
    CREATE_FIRMWARE: javax.swing.ImageIcon = images/media-flash.png
    CUT: javax.swing.ImageIcon = images/edit-cut.png
    DELETE: javax.swing.ImageIcon = images/page_delete.png
    ECLIPSE: javax.swing.ImageIcon = images/eclipse.png
    EXPAND_ALL: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/arrow_inout.png
    EXTRACT: javax.swing.ImageIcon = images/package_green.png
    FONT: javax.swing.ImageIcon = images/text_lowercase.png
    IMPORT: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/application_get.png
    INFO: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/information.png
    IPOD: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/ipod.png
    IPOD_48: javax.swing.ImageIcon = images/oxygen/48x48/multimedia-player-apple-ipod.png
    JAR: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/page_white_cup.png
    KEY: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/application_key.png
    LIST_MOUNTED: javax.swing.ImageIcon = images/downArrow.png
    LOCKED: javax.swing.ImageIcon = images/lock.gif
    NEW: javax.swing.ImageIcon = images/page_add.png
    OPEN: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/door_open.png
    OPEN_ALL: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/application_cascade.png
    OPEN_AS_BINARY: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/controller.png
    OPEN_FILE_SYSTEM: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/folder_brick.png
    OPEN_IN_LISTING: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/folder_table.png
    PASTE: javax.swing.ImageIcon = images/page_paste.png
    PHOTO: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/photo.png
    REDO: javax.swing.ImageIcon = images/redo.png
    REFRESH: javax.swing.ImageIcon = images/reload3.png
    RENAME: javax.swing.ImageIcon = images/textfield_rename.png
    SAVE: javax.swing.ImageIcon = images/disk.png
    SAVE_AS: javax.swing.ImageIcon = images/disk_save_as.png
    UNDO: javax.swing.ImageIcon = images/undo.png
    UNKNOWN: javax.swing.ImageIcon = images/help-browser.png
    UNLOCKED: javax.swing.ImageIcon = images/unlock.gif
    VIEW_AS_IMAGE: javax.swing.ImageIcon = images/oxygen/16x16/games-config-background.png
    VIEW_AS_TEXT: javax.swing.ImageIcon = images/format-text-bold.png
    iOS: javax.swing.ImageIcon = images/famfamfam_silk_icons_v013/phone.png



    def __init__(self): ...



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

