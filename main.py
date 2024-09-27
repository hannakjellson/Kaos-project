import numpy as np
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore, QtWidgets


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
        dx = self.width() / len(cells)
        dy = self.height() / len(cells[0])
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                x0 = j * dx
                y0 = i * dy
                cells[i][j].moveTo(x0, y0)
                cells[i][j].lineTo(x0, y0 + dy)
                cells[i][j].lineTo(x0 + dx, y0 + dy)
                cells[i][j].lineTo(x0 + dx, y0)
                cells[i][j].lineTo(x0, y0)
                brush.setColor(QtGui.QColor(int(255 * np.random.rand()), int(255 * np.random.rand()), int(255 * np.random.rand())))
                painter.setBrush(brush)  # Sätter till en kopia av brush, har inte pointern till brush
                painter.drawPath(cells[i][j])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main widget and layout
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        # Create the grid area (the 'ocean')
        ocean = Environment()

        # Create the right menu with labels
        menu_layout = QtWidgets.QVBoxLayout()

        #set side menu width 
        menu_width = 150

        menu_label = QtWidgets.QLabel("Initial values: (temporary)", self)
        menu_label.setFixedWidth(menu_width)
        menu_layout.addWidget(menu_label)

        rabbits_label = QtWidgets.QLabel("Rabbits (yellow): 2", self)
        rabbits_label.setFixedWidth(menu_width)
        menu_layout.addWidget(rabbits_label)

        wolves_label = QtWidgets.QLabel("Wolves (green): 6", self)
        wolves_label.setFixedWidth(menu_width)
        menu_layout.addWidget(wolves_label)

        apples_label = QtWidgets.QLabel("Apples (blue): 3", self)
        apples_label.setFixedWidth(menu_width)
        menu_layout.addWidget(apples_label)

        # Spacer to push the labels up
        menu_layout.addStretch()

        # Layout for main window (grid + menu)
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(ocean)  # Add the grid (left side)
        main_layout.addLayout(menu_layout)  # Add the menu (right side)

        # Set the layout to the central widget
        central_widget.setLayout(main_layout)


if __name__ == '__main__':
    app = pg.mkQApp("Cellular Automata Ecosystem")
    window = MainWindow()
    window.resize(1200, 600)
    window.show()

    pg.exec()
