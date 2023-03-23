import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Построение графика функции')
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.button = QPushButton('Построить график')
        self.layout.addWidget(self.button)

        self.function_selector = QComboBox()
        self.function_selector.addItem('x**2', 'x**2')
        self.function_selector.addItem('sin(x)', 'np.sin(x)')
        self.function_selector.addItem('cos(x)', 'np.cos(x)')
        self.function_selector.addItem('exp(x)', 'np.exp(x)')
        self.function_selector.addItem('log(x)', 'np.log(x)')
        self.layout.addWidget(self.function_selector)

        self.button.clicked.connect(self.plot)

    def plot(self):
        self.figure.clear()

        expression = self.function_selector.currentData()
        x = np.linspace(-10, 10, 1000)

        try:
            y = eval(expression)
        except:
            print('Ошибка в выражении. Проверьте правильность введенной функции.')
            return

        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_title(expression)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
