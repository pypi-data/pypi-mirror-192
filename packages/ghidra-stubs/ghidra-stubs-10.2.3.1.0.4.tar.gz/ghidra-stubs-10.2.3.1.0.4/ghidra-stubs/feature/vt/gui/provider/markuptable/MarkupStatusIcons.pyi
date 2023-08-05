import java.lang


class MarkupStatusIcons(object):
    APPLIED_ADDED_ICON: javax.swing.Icon = MultiIcon[images/checkmark_green.gif, TranslateIcon[images/Plus.png]]
    APPLIED_ICON: javax.swing.Icon = images/checkmark_green.gif
    APPLIED_REPLACED_ICON: javax.swing.Icon = MultiIcon[images/checkmark_green.gif, TranslateIcon[images/sync_enabled.png]]
    APPLY_ADD_MENU_ICON: javax.swing.Icon = images/Plus.png
    APPLY_REPLACE_MENU_ICON: javax.swing.Icon = images/sync_enabled.png
    CONFLICT_ICON: javax.swing.Icon = images/cache.png
    DONT_CARE_ICON: javax.swing.Icon = images/asterisk_orange.png
    DONT_KNOW_ICON: javax.swing.Icon = images/unknown.gif
    FAILED_ICON: javax.swing.Icon = images/edit-delete.png
    REJECTED_ICON: javax.swing.Icon = images/dialog-cancel.png
    SAME_ICON: javax.swing.Icon = MultiIcon[images/checkmark_green.gif, TranslateIcon[images/checkmark_green.gif]]



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

