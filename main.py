import numpy as np
import pyqtgraph as pg
from pyqtgraph import Qt, QtCore, QtGui
from pyqtgraph.Qt import QtWidgets

print("Hello world/Agnes")
print("Sup world/Daniel")
print("Yoyo world/Hanna")


class Environment(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor('black'))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 1))
        cells = [[QtGui.QPainterPath() for i in range(10)] for j in range(10)]  # Path är lätt att göra customizable
        dx=self.width()/len(cells)
        dy=self.height()/len(cells[0])
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                x0=j*dx
                y0=i*dy
                cells[i][j].moveTo(x0,y0)
                cells[i][j].lineTo(x0, y0+dy)
                cells[i][j].lineTo(x0 + dx, y0 + dy)
                cells[i][j].lineTo(x0 + dx, y0)
                cells[i][j].lineTo(x0, y0)
                brush.setColor(QtGui.QColor(int(255*np.random.rand()), int(255*np.random.rand()), int(255*np.random.rand())))
                painter.setBrush(brush)  # Sätter till en kopia av brush, har inte pointern till brush
                painter.drawPath(cells[i][j])


if __name__ == '__main__':
    app = pg.mkQApp("Cellular Automata Ecosystem")
    window = QtWidgets.QMainWindow()
    window.resize(1200, 700)
    window.show()
    ocean = Environment()
    window.setCentralWidget(ocean)

    pg.exec()
