# Importuj niezbędne biblioteki i moduły
import matplotlib
import matplotlib.pyplot as plt
from PySide6.QtGui import QCloseEvent, Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLineEdit, QLabel

# Ustaw backend dla matplotlib, aby używał Qt5Agg
matplotlib.use('Qt5Agg')


# Utwórz klasę opartą na QWidget dla programu
class Geometry(QWidget):
    def __init__(self):
        super().__init__()

        # Zainicjuj zmienne dla okna wykresu, rysunku i elementów interfejsu użytkownika
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
        self.setup()  # Wywołaj metodę setup, aby skonfigurować interfejs użytkownika

    def setup(self):

        # Utwórz główne okno programu
        self.setFixedSize(420, 300)
        self.setWindowTitle("Geometria")

        # Utwórz przycisk „Wykonaj” i połącz go z metodą data
        do_btn = QPushButton("Wykonaj", self)
        do_btn.move(20, 270)
        do_btn.clicked.connect(self.data)

        # Utwórz przycisk „Wyjście” i połącz go z metodą quit
        quit_btn = QPushButton("Wyjście", self)
        quit_btn.move(320, 270)
        quit_btn.clicked.connect(QApplication.instance().quit)

        # Twórz etykiety do wyświetlania komunikatów o błędach
        self.error = QLabel(
            "Wprowadzone dane muszą być liczbami z zakresu (-50,50),\n jeśli występuje ułamek należy użyć: ,, . '' ",
            self)
        self.error.move(20, 170)
        self.error.hide()

        self.W_neg = QLabel("Podane punkty się nie przecinają", self)
        self.W_neg.move(20, 170)
        self.W_neg.hide()

        self.W_pos = QLabel("Punkt przecięcia odcinków to: ", self)
        self.W_pos.move(20, 170)
        self.W_pos.hide()

        self.W_zaw = QLabel("Odcinek posiadają część wspólną ", self)
        self.W_zaw.move(20, 170)
        self.W_zaw.hide()

        # Twórz etykiety i pola do wprowadzania współrzędnych
        p_odc = QLabel(
            "Podaj współrzędne dla pierwszego odcinka, zakres to (-50,50) :", self)
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

        p_odc = QLabel(
            "Podaj współrzędne dla drugiego odcinka, zakres to (-50,50) :", self)
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

        self.show()  # Pokaż główne okno

        self.figure = None
        self.plot_window = None

    # Metoda obsługi wprowadzania danych i wyświetlania wykresu
    def data(self):
        try:
            # Pobierz dane wprowadzone przez użytkownika
            x1 = float(self.x1_line.text())
            y1 = float(self.y1_line.text())
            x2 = float(self.x2_line.text())
            y2 = float(self.y2_line.text())
            x3 = float(self.x3_line.text())
            y3 = float(self.y3_line.text())
            x4 = float(self.x4_line.text())
            y4 = float(self.y4_line.text())

            # Sprawdź, czy wartości wejściowe mieszczą się w określonym zakresie
            if not (-50 <= x1 <= 50) or not (-50 <= y1 <= 50) or not (-50 <= x2 <= 50) or not (-50 <= y2 <= 50) or not (
                    -50 <= x3 <= 50) or not (-50 <= y3 <= 50) or not (-50 <= x4 <= 50) or not (-50 <= y4 <= 50):
                raise ValueError

            intersection_point = self.calculateIntersection(
                x1, y1, x2, y2, x3, y3, x4, y4)  # Oblicz punkt przecięcia

            # Create or close the figure
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

            # Sprawdź, czy istnieje punkt przecięcia i zaokrąglij wynik
            if isinstance(intersection_point, tuple):
                intersection_x, intersection_y = intersection_point
                intersection_x = round(intersection_x, 2)
                intersection_y = round(intersection_y, 2)

                # Wyświetl wynik w programie i odcinki linii z punktem przecięcia na wykresie
                plt.title(f"Wykres dla odcinków przecinających się")
                plt.plot([x1, x2], [y1, y2], 'b-', label='Linia 1')
                plt.plot([x3, x4], [y3, y4], 'r-', label='Linia 2')
                plt.plot(intersection_x, intersection_y,
                         'go', label='Przecięcie')
                self.W_pos.setText(
                    f"Punkt przecięcia odcinków to: ({intersection_x}, {intersection_y})")
                self.W_pos.show()
                self.W_neg.hide()
                self.error.hide()
                self.W_zaw.hide()

            # Wyświetl wynik w programie i wyświetl nachodzące na siebie odcinki
            elif (x1 <= x3 <= x2 or x1 <= x4 <= x2 or x3 <= x1 <= x4 or x3 <= x2 <= x4) and \
                    (y1 <= y3 <= y2 or y1 <= y4 <= y2 or y3 <= y1 <= y4 or y3 <= y2 <= y4):
                plt.title('Wykres odcinków nakładających się')
                plt.plot([x1, x2], [y1, y2], 'b-', label='Linia 1')
                plt.plot([x3, x4], [y3, y4], 'r-', label='Linia 2')
                self.W_zaw.show()
                self.W_pos.hide()
                self.W_neg.hide()
                self.error.hide()

            else:
                # Wyświetl informację o braku punktu przecięcia i wyświetl odcinki linii
                plt.title('Wykres odcinków nieprzecinających się')
                plt.plot([x1, x2], [y1, y2], 'b-', label='Linia 1')
                plt.plot([x3, x4], [y3, y4], 'r-', label='Linia 2')
                self.W_neg.setText("Odcinki nie przecinają się")
                self.W_neg.show()
                self.W_pos.hide()
                self.error.hide()
                self.W_zaw.hide()

            plt.xlabel('X')
            plt.ylabel('Y', rotation='horizontal')
            plt.legend(loc='best')
            plt.grid(True)
            plt.show()

        # Wyświetl komunikaty o błędach
        except ValueError:
            self.W_neg.hide()
            self.W_pos.hide()
            self.error.show()

        # Wyczyść pola wprowadzania
        self.x1_line.clear()
        self.y1_line.clear()
        self.x2_line.clear()
        self.y2_line.clear()
        self.x3_line.clear()
        self.y3_line.clear()
        self.x4_line.clear()
        self.y4_line.clear()

    # Oblicz punkt przecięcia dwóch odcinków
    @staticmethod
    def calculateIntersection(x1, y1, x2, y2, x3, y3, x4, y4):
        # Oblicz mianownik równań użytych do określenia, czy dwa odcinki linii się przecinają
        denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)

        # Sprawdź, czy odcinki są równoległe
        if denom == 0:
            return None

        # Oblicz parametr „ua”, aby określić punkt przecięcia
        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom

        # Sprawdź, czy punkt przecięcia leży poza zasięgiem pierwszego odcinka
        if ua < 0 or ua > 1:
            return None

        # Oblicz parametr „ub”, aby określić punkt przecięcia na drugim odcinku
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

        # Sprawdź, czy punkt przecięcia leży poza zasięgiem drugiego odcinka
        if ub < 0 or ub > 1:
            return None

        # Sprawdź, czy punkt przecięcia pokrywa się z jednym z punktów końcowych dowolnego odcinka
        if ua == 0 or ua == 1 or ub == 0 or ub == 1:
            if (x1, y1) == (x3, y3) or (x1, y1) == (x4, y4):
                return x1, y1
            if (x2, y2) == (x3, y3) or (x2, y2) == (x4, y4):
                return x2, y2
            return None

        # Oblicz współrzędne punktu przecięcia
        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)

        return x, y

    # Obsłuż zdarzenie „Zamknij” okna programu
    def closeEvent(self, event: QCloseEvent):
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