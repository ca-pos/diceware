from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QSpinBox, QListWidget

import secrets

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Diceware")
        self.setFixedSize(300, 350)

        main_layout = QVBoxLayout(self)

        label1 = QLabel("Nombre de mots de la « Pass Phrase »")
        label2 = QLabel("4 : faible, à éviter")
        label3 = QLabel("5 à 8 : selon le degré de sécurité souhaité")
        label4 = QLabel("9 et plus : paranoiaque")

        button = QPushButton("Générer la « Pass Phrase »")
        button.clicked.connect(self.button_clicked)
        self.nb_mots = QSpinBox()
        self.nb_mots.setRange(4,10)
        self.nb_mots.setValue(5)
 
        self.first_pass = ["sperme", "exil", "éveil", "ulcère", "tract", "rock", "partie", "étang"]
        self.rep = QListWidget()
        for i in range(0, len(self.first_pass)):
            self.rep.addItem(self.first_pass[i])

        main_layout.addWidget(label1)
        main_layout.addWidget(label2)
        main_layout.addWidget(label3)
        main_layout.addWidget(label4)
        main_layout.addWidget(self.nb_mots)
        main_layout.addWidget(button)
        main_layout.addWidget(self.rep)

    def button_clicked(self):
        self.rep.clear()
        with open("diceware.txt", "r") as file:
            for j in range(0, self.nb_mots.value()):
                rand = secrets.randbelow(2724)
                file.seek(0)
                for i in range(0, rand-1):
                    file.readline()
                self.rep.addItem(file.readline().strip())


app = QApplication()
main_windows = MainWindow()
main_windows.show()

app.exec()
