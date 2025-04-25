import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QMessageBox)
from PyQt6.QtGui import QIntValidator
from datetime import datetime

class CarImportApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Расчет таможенных платежей')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.namecar = QLineEdit(self)
        layout.addWidget(QLabel('Введите марку и модель машины:'))
        layout.addWidget(self.namecar)

        self.obem = QLineEdit(self)
        layout.addWidget(QLabel('Введите объем двигателя в мл: (Если автомобиль электрический вводите 0)'))
        layout.addWidget(self.obem)
        self.obem.setValidator(QIntValidator(0, 99999999))
        self.celm = QComboBox(self)
        self.celm.addItems(['Физическое лицо (для личного использования)',
                           'Физическое лицо (для перепродажи)',
                           'Юридическое лицо'])
        layout.addWidget(QLabel('Автомобиль ввозит:'))
        layout.addWidget(self.celm)

        self.dvigat = QComboBox(self)
        self.dvigat.addItems(['Бензиновый', 'Дизельный', 'Гибридный', 'Электрический'])
        layout.addWidget(QLabel('Тип двигателя:'))
        layout.addWidget(self.dvigat)

        self.mosh = QLineEdit(self)
        layout.addWidget(QLabel('Введите мощность двигателя в лс:'))
        layout.addWidget(self.mosh)
        self.mosh.setValidator(QIntValidator(0, 999999))

        self.god = QLineEdit(self)
        layout.addWidget(QLabel('Введите год производства:'))
        layout.addWidget(self.god)
        self.god.setValidator(QIntValidator(1900, datetime.now().year))

        self.zena = QLineEdit(self)
        layout.addWidget(QLabel('Введите стоимость автомобиля в рублях:'))
        layout.addWidget(self.zena)
        self.zena.setValidator(QIntValidator(0, 99999999))

        self.calculateButton = QPushButton('Рассчитать', self)
        self.calculateButton.clicked.connect(self.calculate)
        layout.addWidget(self.calculateButton)

        self.setLayout(layout)

    def calculate(self):
        try:
            obem = int(self.obem.text())
            celm = self.celm.currentIndex() + 1
            dvigat = self.dvigat.currentIndex() + 1
            mosh = int(self.mosh.text())
            god = int(self.god.text())
            zena = int(self.zena.text())

            if mosh == 0 or god == 0 or (dvigat != 4 and obem == 0) or god > datetime.now().year:
                raise ValueError("Некоректные данные") # datetime.now() = 2025-04-24 23:53:сек.милисек


            utilsbor = 0
            tamozhsbor = 1067
            akzi = 0
            NDS = 0

            def calculate_age(go):
                current_year = datetime.now().year
                age = current_year - go
                return age

            ag = calculate_age(god)
            if dvigat != 4 and celm == 1:
                if ag < 3:
                    utilsbor += 3400
                elif ag > 3:
                    utilsbor += 5200
            elif dvigat == 4 and celm == 1:
                if ag < 3:
                    utilsbor += 3400
                if ag > 3:
                    utilsbor += 5200

            if dvigat != 4 and celm == 2:
                if ag < 3:
                    utilsbor += 180200
                elif ag > 3:
                    utilsbor += 460000
            elif dvigat == 4 and celm == 2:
                if ag < 3:
                    utilsbor += 667400
                elif ag > 3:
                    utilsbor += 1174000

            if dvigat != 4 and celm == 3:
                if ag < 3:
                    utilsbor += 180200
                elif ag > 3:
                    utilsbor += 460000
            elif dvigat == 4 and celm == 3:
                if ag < 3:
                    utilsbor += 667400
                elif ag > 3:
                    utilsbor += 1174000

            if dvigat != 4:
                if celm == 1 or celm == 2:
                    if ag < 3:
                        tmposh = obem * 230
                    elif ag > 3 and ag < 5:
                        tmposh = obem * 143
                    elif ag > 5:
                        tmposh = obem * 285
                elif celm == 3:
                    tmposh = zena * 0.15
                    akzi = mosh * 61
                    NDS = (zena + akzi + tmposh) * 0.2
            elif dvigat == 4:
                tmposh = zena * 0.15
                akzi = mosh * 61
                NDS = (zena + akzi + tmposh) * 0.2

            itog = tamozhsbor + tmposh + utilsbor + NDS + akzi + zena

            QMessageBox.information(
                self,
                'Результат',
                f'Таможенный сбор составляет: {tamozhsbor}\n'
                f'Таможенная пошлина составляет: {tmposh}\n'
                f'Утилизационный сбор составляет: {utilsbor}\n'
                f'НДС: {NDS}\n'
                f'Акциз: {akzi}\n'
                f'Итого (с учетом стоимости автомобиля): {itog}'
            )
        except ValueError as e:
            QMessageBox.warning(self, 'Ошибка', str(e) if str(e) else 'Пожалуйста, введите корректные данные.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CarImportApp()
    ex.show()
    sys.exit(app.exec())
