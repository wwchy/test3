from PyQt5.QtCore import QPoint, QRect, QSize, Qt,pyqtSignal
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
  QApplication, QLayout, QPushButton, QSizePolicy, QWidget, QSpacerItem)
import sys
class Window(QWidget):
  def resizeEvent(self, a0 ) -> None:
    self.qscrollarea.resize(self.size())
    return super().resizeEvent(a0)
  def __init__(self):
    self.imageheight = 100
    super(Window, self).__init__()
    self.resize(800, 600)
  
    highlight_dir = r"./"
    self.files_it = iter([os.path.join(highlight_dir, file)
               for file in os.listdir(highlight_dir)])
 
    # self.centralwidget = QtWidgets.QWidget(MainWindow)
    # self.gongzuomoshi = QtWidgets.QGroupBox(self.centralwidget)
    self.listWidget = QtWidgets.QListWidget(self)
    #self.listWidget.setFixedWidth(600) 
    
    l = FlowLayout() 
    
    for file in iter(self.files_it):
      pixmap = QtGui.QPixmap(file)
      if not pixmap.isNull():
        autoWidth = pixmap.width()*self.imageheight/pixmap.height()
        label = QtWidgets.QLabel(pixmap=pixmap)
        label.setScaledContents(True)
        label.setFixedHeight(self.imageheight)
        label.setFixedWidth(autoWidth)
        l.addWidget(label)
  
    self.listWidget.setLayout(l)
 
    self.qscrollarea = QtWidgets.QScrollArea(self) 
    self.qscrollarea.setWidgetResizable(True)
    self.qscrollarea.setWidget(self.listWidget)
    self.setWindowTitle("Flow Layout Scroll")
 
class FlowLayout(QLayout):
  """流式布局,使用说明
  1.声明流式布局 layout = FlowLayout
  2.将元素放入流式布局中
  3.将QGroupBox应用流式布局
  4.如果期望水平流式,将QGroupBox放入到QHBoxLayout,如果期望垂直布局,将QGroupBox放入到QVBoxLayout
  """
  heightChanged = pyqtSignal(int)
 
  def __init__(self, parent=None, margin=0, spacing=-1):
    super().__init__(parent)
    if parent is not None:
      self.setContentsMargins(margin, margin, margin, margin)
    self.setSpacing(spacing)
 
    self._item_list = []
 
  def __del__(self):
    while self.count():
      self.takeAt(0)
 
  def addItem(self, item): # pylint: disable=invalid-name
    self._item_list.append(item)
 
  def addSpacing(self, size): # pylint: disable=invalid-name
    self.addItem(QSpacerItem(size, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
 
  def count(self):
    return len(self._item_list)
 
  def itemAt(self, index): # pylint: disable=invalid-name
    if 0 <= index < len(self._item_list):
      return self._item_list[index]
    return None
 
  def takeAt(self, index): # pylint: disable=invalid-name
    if 0 <= index < len(self._item_list):
      return self._item_list.pop(index)
    return None
 
  def expandingDirections(self): # pylint: disable=invalid-name,no-self-use
    return Qt.Orientations(Qt.Orientation(0))
 
  def hasHeightForWidth(self): # pylint: disable=invalid-name,no-self-use
    return True
 
  def heightForWidth(self, width): # pylint: disable=invalid-name
    height = self._do_layout(QRect(0, 0, width, 0), True)
    return height
 
  def setGeometry(self, rect): # pylint: disable=invalid-name
    super().setGeometry(rect)
    self._do_layout(rect, False)
 
  def sizeHint(self): # pylint: disable=invalid-name
    return self.minimumSize()
 
  def minimumSize(self): # pylint: disable=invalid-name
    size = QSize()
 
    for item in self._item_list:
      minsize = item.minimumSize()
      extent = item.geometry().bottomRight()
      size = size.expandedTo(QSize(minsize.width(), extent.y()))
 
    margin = self.contentsMargins().left()
    size += QSize(2 * margin, 2 * margin)
    return size
 
  def _do_layout(self, rect, test_only=False):
    m = self.contentsMargins()
    effective_rect = rect.adjusted(+m.left(), +m.top(), -m.right(), -m.bottom())
    x = effective_rect.x()
    y = effective_rect.y()
    line_height = 0
 
    for item in self._item_list:
      wid = item.widget()
 
      space_x = self.spacing()
      space_y = self.spacing()
      if wid is not None:
        space_x += wid.style().layoutSpacing(
          QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
        space_y += wid.style().layoutSpacing(
          QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
 
      next_x = x + item.sizeHint().width() + space_x
      if next_x - space_x > effective_rect.right() and line_height > 0:
        x = effective_rect.x()
        y = y + line_height + space_y
        next_x = x + item.sizeHint().width() + space_x
        line_height = 0
 
      if not test_only:
        item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
 
      x = next_x
      line_height = max(line_height, item.sizeHint().height())
 
    new_height = y + line_height - rect.y()
    self.heightChanged.emit(new_height)
    return new_height
 
if __name__ == '__main__':
  app = QApplication(sys.argv)
  mainWin = Window()
 
  mainWin.show()
  sys.exit(app.exec_())