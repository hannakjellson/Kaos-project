import copy
import numpy as np
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore, QtWidgets

import TestPopulation

print("Hello world/Agnes")
print("Sup world/Daniel")
print("Yoyo world/Hanna")

def torusloop(pos, size):
    return np.mod(pos+size, size)  # Fixa torus geometri

class Environment(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.xsize = 100
        self.ysize = 100

        self.population = [[TestPopulation.Individual for j in range(self.ysize)] for i in range(self.xsize)]
        self.requestedPopulation = [[TestPopulation.Individual for j in range(self.ysize)] for i in range(self.xsize)]

        #  Start population
        """
        for i in range(self.xsize):
            for j in range(self.ysize):
                if (i==4 and j==4) or (i==5 and j==4) or (i==5 and j==5) or (i==6 and j==5) or (i==4 and j==6):
                    self.population[i][j] = TestPopulation.Alive(i,j)
                else:
                    self.population[i][j] = TestPopulation.Dead(i, j)
        """
        for i in range(self.xsize):
            for j in range(self.ysize):
                element=int(4*np.random.rand())
                match element:
                    case 0:
                        self.population[i][j] = TestPopulation.FireElemental(i, j)
                    case 1:
                        self.population[i][j] = TestPopulation.AirElemental(i, j)
                    case 2:
                        self.population[i][j] = TestPopulation.WaterElemental(i, j)
                    case 3:
                        self.population[i][j] = TestPopulation.EarthElemental(i, j)


        self.day=QtCore.QTimer()
        self.day.timeout.connect(self.develop)
        self.day.start(100)  #  Tid mellan steg i millisekunder (lägre ger högre framerate)

    def develop(self):
        for row in self.population:
            for individual in row:
                x,y = individual.getpos()
                neighbors=[self.population[torusloop(x-1, self.xsize)][torusloop(y-1, self.ysize)],
                           self.population[torusloop(x-1, self.xsize)][torusloop(y, self.ysize)],
                           self.population[torusloop(x-1, self.xsize)][torusloop(y+1, self.ysize)],
                           self.population[torusloop(x, self.xsize)][torusloop(y+1, self.ysize)],
                           self.population[torusloop(x+1, self.xsize)][torusloop(y+1, self.ysize)],
                           self.population[torusloop(x+1, self.xsize)][torusloop(y, self.ysize)],
                           self.population[torusloop(x+1, self.xsize)][torusloop(y-1, self.ysize)],
                           self.population[torusloop(x, self.xsize)][torusloop(y-1, self.ysize)]]
                individual.behavior(neighbors, self.requestedPopulation)
        self.population=copy.deepcopy(self.requestedPopulation)
        self.repaint()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor('black'))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)
        painter.setPen(QtGui.QPen(QtGui.QColor(150, 150, 150), 1))
        cells = [[QtGui.QPainterPath() for j in range(self.ysize)] for i in
                 range(self.xsize)]  # Path är lätt att göra customizable
        dx = self.width() / len(cells)
        dy = self.height() / len(cells[0])
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                x0 = i * dx
                y0 = j * dy
                cells[i][j].moveTo(x0, y0)
                cells[i][j].lineTo(x0, y0 + dy)
                cells[i][j].lineTo(x0 + dx, y0 + dy)
                cells[i][j].lineTo(x0 + dx, y0)
                cells[i][j].lineTo(x0, y0)
                color=self.population[i][j].getColor()
                brush.setColor(QtGui.QColor(color[0], color[1], color[2]))
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
