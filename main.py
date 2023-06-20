# Importuje potrzebne biblioteki oraz moduły
import matplotlib
import matplotlib.pyplot as plt
from PySide6.QtGui import QCloseEvent, Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLineEdit, QLabel

matplotlib.use('Qt5Agg')


class Geometry(QWidget):
    def __init__(self):
        super().__init__()

        self.plot_window = None
        self.figure = None
        self.label_y4 = None
        self.y4_line = None
        self.label_x4 = None
        self.x4_line = None
        self.label_y3 = None
        self.y3_line = None
        self.label_x3 = None
        self.x3_line = None
        self.label_y2 = None
        self.y2_line = None
        self.label_x2 = None
        self.x2_line = None
        self.label_y1 = None
        self.y1_line = None
        self.label_x1 = None
        self.W_pos = None
        self.W_neg = None
        self.error = None
        self.x1_line = None
        self.setup()

    def setup(self):

        # Odpowiada za wygląd okna służącego do obsługi programu
        self.setFixedSize(420, 300)
        self.setWindowTitle("Geometria")

        do_btn = QPushButton("Wykonaj", self)
        do_btn.move(20, 270)
        do_btn.clicked.connect(self.data)

        quit_btn = QPushButton("Wyjście", self)
        quit_btn.move(320, 270)
        quit_btn.clicked.connect(QApplication.instance().quit)

        self.error = QLabel(
            "Wprowadzone dane muszą być liczbami z zakresu (-50,50),\n jeśli występuje ułamek należy użyć: ,, . '' ",
            self)
        self.error.move(20, 170)
        self.error.hide()

        self.W_neg = QLabel("Podane punkty się nie przecinają", self)
        self.W_neg.move(20, 170)
        self.W_neg.hide()

        self.W_pos = QLabel("Punkt przecięcia lini to: ", self)
        self.W_pos.move(20, 170)
        self.W_pos.hide()

        p_odc = QLabel("Podaj współrzędne dla pierwszego odcinka, zakres to (-50,50) :", self)
        p_odc.move(20, 10)

        self.x1_line = QLineEdit("", self)
        self.x1_line.setFixedWidth(75)
        self.x1_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x1_line.move(40, 30)

        self.label_x1 = QLabel("x1:", self)
        self.label_x1.move(20, 31)

        self.y1_line = QLineEdit("", self)
        self.y1_line.setFixedWidth(75)
        self.y1_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y1_line.move(160, 30)

        self.label_y1 = QLabel("y1:", self)
        self.label_y1.move(140, 31)

        self.x2_line = QLineEdit("", self)
        self.x2_line.setFixedWidth(75)
        self.x2_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x2_line.move(40, 60)

        self.label_x2 = QLabel("x2:", self)
        self.label_x2.move(20, 61)

        self.y2_line = QLineEdit("", self)
        self.y2_line.setFixedWidth(75)
        self.y2_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y2_line.move(160, 60)

        self.label_y2 = QLabel("y2:", self)
        self.label_y2.move(140, 61)

        p_odc = QLabel("Podaj współrzędne dla drugiego odcinka, zakres to (-50,50) :", self)
        p_odc.move(20, 90)

        self.x3_line = QLineEdit("", self)
        self.x3_line.setFixedWidth(75)
        self.x3_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x3_line.move(40, 110)

        self.label_x3 = QLabel("x3:", self)
        self.label_x3.move(20, 111)

        self.y3_line = QLineEdit("", self)
        self.y3_line.setFixedWidth(75)
        self.y3_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y3_line.move(160, 110)

        self.label_y3 = QLabel("y3:", self)
        self.label_y3.move(140, 111)

        self.x4_line = QLineEdit("", self)
        self.x4_line.setFixedWidth(75)
        self.x4_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x4_line.move(40, 140)

        self.label_x4 = QLabel("x4:", self)
        self.label_x4.move(20, 141)

        self.y4_line = QLineEdit("", self)
        self.y4_line.setFixedWidth(75)
        self.y4_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y4_line.move(160, 140)

        self.label_y4 = QLabel("y4:", self)
        self.label_y4.move(140, 141)

        self.show()

        self.figure = None
        self.plot_window = None

    def data(self):  # Obsługuje wprowadzone dane oraz wyświetla wynik
        try:  # Pobiera dane od użytkownika wprowadzone w polach
            x1 = float(self.x1_line.text())
            y1 = float(self.y1_line.text())
            x2 = float(self.x2_line.text())
            y2 = float(self.y2_line.text())
            x3 = float(self.x3_line.text())
            y3 = float(self.y3_line.text())
            x4 = float(self.x4_line.text())
            y4 = float(self.y4_line.text())

            if not (-50 <= x1 <= 50) or not (-50 <= y1 <= 50) or not (-50 <= x2 <= 50) or not (-50 <= y2 <= 50) or not (
                    -50 <= x3 <= 50) or not (-50 <= y3 <= 50) or not (-50 <= x4 <= 50) or not (-50 <= y4 <= 50):
                raise ValueError  # Tworzy zakres jaki można wprowadzić

            intersection_point = self.calculateIntersection(x1, y1, x2, y2, x3, y3, x4, y4)  # definuje punkt przecięcia

            # Obsługuję okna wykresu
            if self.plot_window is None:
                self.plot_window = QWidget()
            else:
                self.plot_window.close()

            self.plot_window.setWindowTitle("Wykres")
            self.plot_window.setFixedSize(400, 300)

            if self.figure is None:
                self.figure = plt.figure()
            else:
                plt.close(self.figure)

            # Generuje odcinki na wykresie:
            plt.plot([x1, x2], [y1, y2], 'b-', label='Linia 1')
            plt.plot([x3, x4], [y3, y4], 'r-', label='Linia 2')

            if isinstance(intersection_point, tuple):  # Sprawdza czy istnieje punkt przecięcia oraz zaokrągla wynik
                intersection_x, intersection_y = intersection_point
                intersection_x = round(intersection_x, 2)
                intersection_y = round(intersection_y, 2)

                # Wyświetla wynik obliczeń w programie oraz na wykresie:
                plt.plot(intersection_x, intersection_y, 'go', label='Przecięcie')
                plt.title(f"Punkt przecięcia odcinków to: ({intersection_x}, {intersection_y})")
                self.W_pos.setText(f"Punkt przecięcia odcinków to: ({intersection_x}, {intersection_y})")
                self.W_pos.show()
                self.W_neg.hide()
                self.error.hide()
            else:
                # Wyświetla informację o braku przecięcia w programie oraz na wykresie:
                plt.title('Wykres odcinków nieprzecinających się')
                self.W_neg.setText("Odcinki nie przecinają się")
                self.W_neg.show()
                self.W_pos.hide()
                self.error.hide()

            # Wyświetlenie wykresu
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.legend(loc='best')
            plt.grid(True)
            plt.show()

        except ValueError:  # Odpowiada za wyświetlanie komunikatu w przypadku błędu
            self.W_neg.hide()
            self.W_pos.hide()
            self.error.show()

        # Czyści pola do wpisywania współżędnych po każdym użyciu
        self.x1_line.clear()
        self.y1_line.clear()
        self.x2_line.clear()
        self.y2_line.clear()
        self.x3_line.clear()
        self.y3_line.clear()
        self.x4_line.clear()
        self.y4_line.clear()

    @staticmethod
    def calculateIntersection(x1, y1, x2, y2, x3, y3, x4, y4):
        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        a1 = y2 - y1
        b1 = x1 - x2
        c1 = det([x1, y1], [x2, y2])

        a2 = y4 - y3
        b2 = x3 - x4
        c2 = det([x3, y3], [x4, y4])

        det_ = det([a1, b1], [a2, b2])
        if det_ == 0:
            return False

        x = det([c1, b1], [c2, b2]) / det_
        y = det([a1, c1], [a2, c2]) / det_

        return x, y

    def closeEvent(self, event: QCloseEvent):  # Obsługuga okno dialogowe
        should_close = QMessageBox.question(self, "Zamknij aplikację", "Czy chcesz zamknąć aplikację?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                            QMessageBox.StandardButton.No)

        if should_close == QMessageBox.StandardButton.Yes:
            if self.plot_window is not None:
                self.plot_window.close()
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication([])
    login = Geometry()
    app.exec()
