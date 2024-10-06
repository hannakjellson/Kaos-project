import copy
import numpy as np
import pyqtgraph as pg
from pyqtgraph.dockarea.DockArea import DockArea
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph import QtGui, QtCore, QtWidgets

import TestPopulation

timestep=200  # Tid mellan steg i millisekunder (lägre ger högre framerate)
seed=1

def torusloop(pos, size):
    return np.mod(pos + size, size)  # Fixa torus geometri


class Environment(QtWidgets.QWidget):
    def __init__(self, populationArray):
        super().__init__()
        self.xsize = np.shape(populationArray)[0]
        self.ysize = np.shape(populationArray)[1]

        self.population = copy.deepcopy(populationArray)
        self.requestedPopulation = copy.deepcopy(populationArray)

        self.speciesList = []
        for i in range(self.xsize):
            for j in range(self.ysize):
                if not self.speciesList.__contains__(type(populationArray[i][j])):
                    self.speciesList.append(type(populationArray[i][j]))
        print(self.speciesList)
        self.species = np.zeros(np.shape(self.speciesList)[0])
        self.speciesHistory = [[] for i in range(np.shape(self.species)[0])]
        self.measurePopulations()

        self.day = QtCore.QTimer()
        self.day.timeout.connect(self.develop)
        self.day.start(timestep)

    def develop(self):
        for row in self.population:
            for individual in row:
                x, y = individual.getpos()
                neighbors = [self.population[torusloop(x - 1, self.xsize)][torusloop(y - 1, self.ysize)],
                             self.population[torusloop(x - 1, self.xsize)][torusloop(y, self.ysize)],
                             self.population[torusloop(x - 1, self.xsize)][torusloop(y + 1, self.ysize)],
                             self.population[torusloop(x, self.xsize)][torusloop(y + 1, self.ysize)],
                             self.population[torusloop(x + 1, self.xsize)][torusloop(y + 1, self.ysize)],
                             self.population[torusloop(x + 1, self.xsize)][torusloop(y, self.ysize)],
                             self.population[torusloop(x + 1, self.xsize)][torusloop(y - 1, self.ysize)],
                             self.population[torusloop(x, self.xsize)][torusloop(y - 1, self.ysize)]]
                self.requestedPopulation[x][y] = individual.behavior(neighbors)
        self.population = copy.deepcopy(self.requestedPopulation)
        self.measurePopulations()
        self.repaint()

    def measurePopulations(self):
        self.species = np.zeros(np.shape(self.speciesList)[0])
        for i in range(np.shape(self.speciesList)[0]):
            for row in self.population:
                for individual in row:
                    if isinstance(individual, self.speciesList[i]): self.species[i] += 1
            self.speciesHistory[i].append(self.species[i])

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
                color = self.population[i][j].getColor()
                brush.setColor(QtGui.QColor(color[0], color[1], color[2]))
                painter.setBrush(brush)  # Sätter till en kopia av brush, har inte pointern till brush
                painter.drawPath(cells[i][j])


class CellularAutomataSimulator(QtWidgets.QWidget):
    def __init__(self, skew):
        super().__init__()

        xsize = 50
        ysize = 50
        initpop = [[TestPopulation.Individual for j in range(ysize)] for i in range(xsize)]
        #  Start population
        np.random.seed(seed)
        """
        for i in range(self.xsize):
            for j in range(self.ysize):
                if (i==4 and j==4) or (i==5 and j==4) or (i==5 and j==5) or (i==6 and j==5) or (i==4 and j==6):
                    self.population[i][j] = TestPopulation.Alive(i,j)
                else:
                    self.population[i][j] = TestPopulation.Dead(i, j)
        """

        """
        for i in range(xsize):
            for j in range(ysize):
                element = int(4 * np.random.rand())
                match element:
                    case 0:
                        initpop[i][j] = TestPopulation.FireElemental(i, j)
                    case 1:
                        initpop[i][j] = TestPopulation.AirElemental(i, j)
                    case 2:
                        initpop[i][j] = TestPopulation.WaterElemental(i, j)
                    case 3:
                        initpop[i][j] = TestPopulation.EarthElemental(i, j)
        """

        for i in range(xsize):
            for j in range(ysize):
                element = int(4 * np.random.rand())
                if i == xsize/2 and j == ysize/2: element = torusloop(element+skew, 4)
                match element:
                    case 0:
                        initpop[i][j] = TestPopulation.Agar(i, j)
                    case 1:
                        initpop[i][j] = TestPopulation.Bacteria(i, j)
                    case 2:
                        initpop[i][j] = TestPopulation.Waste(i, j)
                    case 3:
                        initpop[i][j] = TestPopulation.Amoeba(i, j)

        self.environment = Environment(initpop)
        self.environment.setMinimumSize(400, 200)

        self.historyWidget = pg.PlotWidget()
        self.historyWidget.setMinimumSize(200, 200)
        self.updatePlot()

        # Layout for main window
        main_layout = QtWidgets.QGridLayout()
        main_layout.addWidget(self.environment, 0, 0)
        main_layout.addWidget(self.historyWidget, 0, 1)

        # Set the layout to the central widget
        self.setLayout(main_layout)

        self.plotUpdater=QtCore.QTimer()
        self.plotUpdater.timeout.connect(self.updatePlot)
        self.plotUpdater.start(timestep)

    def updatePlot(self):
        self.historyWidget.clear()
        for i in range(np.shape(self.environment.speciesHistory)[0]):
            self.historyWidget.plot(range(np.shape(self.environment.speciesHistory)[1]), self.environment.speciesHistory[i][:],
                                    pen=pg.mkPen(color=self.environment.speciesList[i].color, width=2))

if __name__ == '__main__':
    app = pg.mkQApp("Cellular Automata Ecosystem")
    window = QtWidgets.QMainWindow()
    window.resize(1200, 600)
    dockarea=DockArea()
    window.setCentralWidget(dockarea)

    dock1=Dock("Run 1", size=(1,1))
    dockarea.addDock(dock1, 'top')
    sim1=CellularAutomataSimulator(0)
    dock1.addWidget(sim1)

    dock2=Dock("Run 2", size=(1,1))
    dockarea.addDock(dock2, 'bottom', dock1)
    sim2=CellularAutomataSimulator(1)
    dock2.addWidget(sim2)


    window.show()

    pg.exec()
