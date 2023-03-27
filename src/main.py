import sys

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QAction, QApplication, QCheckBox, QComboBox,
    QDialog, QFileDialog, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QMessageBox, QPushButton, QTextEdit, QVBoxLayout,
    QWidget
)


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Построение графика функции')
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        self.create_central_widget()
        self.create_canvas()
        self.create_button()
        self.create_function_selector()
        self.create_custom_function_input()
        self.create_settings_layout()
        self.create_menu()
        self.connect_signals()

    def create_central_widget(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

    def create_canvas(self):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def create_button(self):
        self.button = QPushButton('Построить график')
        self.layout.addWidget(self.button)

    def create_function_selector(self):
        self.function_selector = QComboBox()
        self.function_selector.addItem('x**2', 'x**2')
        self.function_selector.addItem('sin(x)', 'np.sin(x)')
        self.function_selector.addItem('cos(x)', 'np.cos(x)')
        self.function_selector.addItem('exp(x)', 'np.exp(x)')
        self.function_selector.addItem('log(x)', 'np.log(x)')
        self.function_selector.addItem('Свой вариант', 'custom')
        self.layout.addWidget(self.function_selector)

    def create_grid_checkbox(self):
        self.grid_checkbox = QCheckBox('Показать сетку')
        self.grid_checkbox.setChecked(True)
        self.layout.addWidget(self.grid_checkbox)

    def create_custom_function_input(self):
        self.custom_function_input = QLineEdit()
        self.custom_function_input.setPlaceholderText(
            'Введите свою функцию. Пример: np.sin(x) + np.cos(x)')
        self.layout.addWidget(self.custom_function_input)
        self.custom_function_input.setVisible(False)

    def on_function_selector_change(self):
        if self.function_selector.currentData() == 'custom':
            self.custom_function_input.setVisible(True)
        else:
            self.custom_function_input.setVisible(False)

    def show_examples_dialog(self):
        examples_dialog = QDialog(self)
        examples_dialog.setWindowTitle("Примеры пользовательских функций")

        examples_layout = QVBoxLayout(examples_dialog)

        examples_text = QTextEdit(examples_dialog)
        examples_text.setReadOnly(True)
        examples_text.setPlainText("Примеры пользовательских функций:\n\n"
                                   "1. np.sin(x) + x**2\n"
                                   "2. np.exp(-x**2)\n"
                                   "3. x * np.cos(x)\n"
                                   "4. np.log10(x) + x**0.5\n\n"
                                   "При вводе своих функций используйте синтаксис Python и библиотеку NumPy.")
        examples_layout.addWidget(examples_text)

        examples_dialog.exec_()

    def create_menu(self):
        self.menu = QMenuBar(self)
        self.setMenuBar(self.menu)

        self.file_menu = QMenu('Файл', self)
        self.menu.addMenu(self.file_menu)

        self.file_action = QAction("Сохранить график", self)
        self.file_menu.addAction(self.file_action)

        self.help_menu = QMenu("Помощь", self)
        self.menu.addMenu(self.help_menu)

        self.help_action = QAction("Инструкции", self)
        self.help_menu.addAction(self.help_action)

        self.examples_action = QAction("Примеры пользовательских функций", self)
        self.help_menu.addAction(self.examples_action)

        self.file_action.triggered.connect(self.save_plot)

        self.examples_action.triggered.connect(self.show_examples_dialog)

        self.help_action.triggered.connect(self.show_help_dialog)

    def save_plot(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить график', '',
                                                   'Изображения (*.png *.jpg *.bmp);;Все файлы (*)')

        if file_name:
            self.figure.savefig(file_name)

    def create_settings_layout(self):
        self.settings_layout = QHBoxLayout()
        self.layout.addLayout(self.settings_layout)

        self.x_start_label = QLabel('Начальное значение X:')
        self.settings_layout.addWidget(self.x_start_label)

        self.x_start_input = QLineEdit('-10')
        self.settings_layout.addWidget(self.x_start_input)

        self.x_end_label = QLabel('Конечное значение X:')
        self.settings_layout.addWidget(self.x_end_label)

        self.x_end_input = QLineEdit('10')
        self.settings_layout.addWidget(self.x_end_input)

        self.dot_count_label = QLabel('Точек для построения: ')
        self.settings_layout.addWidget(self.dot_count_label)

        self.dot_count_input = QLineEdit('1000')
        self.settings_layout.addWidget(self.dot_count_input)

        self.grid_checkbox = QCheckBox('Показать сетку')
        self.grid_checkbox.setChecked(True)
        self.settings_layout.addWidget(self.grid_checkbox)

    def connect_signals(self):
        self.button.clicked.connect(self.plot)
        self.function_selector.currentIndexChanged.connect(self.on_function_selector_change)

    def show_help_dialog(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Инструкции по использованию")

        help_layout = QVBoxLayout(help_dialog)

        help_text = QTextEdit(help_dialog)
        help_text.setReadOnly(True)
        help_text.setPlainText("1. Выберите функцию из списка или введите свою функцию.\n"
                               "2. Введите начальное и конечное значения X.\n"
                               "3. Отметьте галочку 'Показать сетку', если хотите отобразить сетку на графике.\n"
                               "4. Нажмите кнопку 'Построить график' для построения графика функции.\n\n"
                               "Для ввода своей функции используйте синтаксис Python и библиотеку NumPy. "
                               "Например, введите 'np.sin(x) + x**2' для построения графика синусоиды с квадратичной функцией.")
        help_layout.addWidget(help_text)

        help_dialog.exec_()

    def plot(self):
        self.figure.clear()

        if self.function_selector.currentData() == 'custom':
            expression = self.custom_function_input.text()
        else:
            expression = self.function_selector.currentData()

        x_start = float(self.x_start_input.text())
        x_end = float(self.x_end_input.text())
        dot_count = int(self.dot_count_input.text())

        if "log" in expression:
            x_start = max(x_start, 1e-10)

        x = np.linspace(x_start, x_end, dot_count)

        try:
            y = eval(expression)
        except Exception as ex:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowTitle("Ошибка")
            error_msg.setText(
                "Ошибка в выражении. Проверьте правильность введенной функции. \n"
                "Возможно вы указали не правильно название функции, проверьте правильность \n"
                "ПРИМЕР: np.sin(x) + np.cos(x)\n"
            )
            error_msg.exec_()
            return

        ax = self.figure.add_subplot()
        ax.plot(x, y)

        if self.grid_checkbox.isChecked():
            ax.grid(True, linestyle='-', linewidth=0.5)
        else:
            ax.grid(False)

        ax.annotate(
            '',
            xy=(0, np.max(y)),
            xytext=(0, np.min(y)),
            arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=0.8),
            annotation_clip=False
        )
        ax.text(0.05 * x_end, np.max(y), 'у', fontsize=12, ha='center', va='center')

        ax.annotate(
            '',
            xy=(x_end, 0),
            xytext=(x_start, 0),
            arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=0.8),
            annotation_clip=False
        )
        ax.text(x_end, 0.05 * np.max(y), 'х', fontsize=12, ha='center', va='center')

        ax.yaxis.set_tick_params(direction='inout', length=6, width=0.5, colors='black')

        self.annotation = ax.annotate(
            '',
            xy=(0, 0),
            xytext=(-20, 20),
            textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='white'),
            arrowprops=dict(arrowstyle='->', lw=1.5)
        )
        self.annotation.set_visible(False)

        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('axes_leave_event', self.on_mouse_leave)

        ax.set_title(expression)
        self.canvas.draw()

    def on_mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        self.annotation.xy = (x, y)
        self.annotation.set_text(f'x = {x:.2f}, y = {y:.2f}')
        self.annotation.set_visible(True)
        self.canvas.draw_idle()

    def on_mouse_leave(self, event):
        self.annotation.set_visible(False)
        self.canvas.draw_idle()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
