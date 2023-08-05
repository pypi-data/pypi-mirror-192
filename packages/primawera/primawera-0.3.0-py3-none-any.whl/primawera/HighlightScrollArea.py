from PyQt5.QtWidgets import QScrollArea


class HighlightScrollArea(QScrollArea):
    """
    QScrollArea with borders indicating focus.
    """

    def __init__(self):
        super(HighlightScrollArea, self).__init__()
        if self.hasFocus():
            self.setStyleSheet("border: 1px solid yellow;")
        else:
            self.setStyleSheet("border: 1px solid gray;")
        self.setMouseTracking(True)

    def focusInEvent(self, event):
        self.setStyleSheet("border: 1px solid yellow;")
        event.accept()

    def focusOutEvent(self, event):
        self.setStyleSheet("border: 1px solid gray;")
        event.accept()

    def in_focus(self) -> bool:
        return self.hasFocus()
