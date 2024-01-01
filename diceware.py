import sys

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QSpinBox, QListWidget, QHBoxLayout, QFileDialog

import secrets

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Diceware")
        self.setFixedSize(300, 388)

        main_layout = QVBoxLayout(self)

        label1 = QLabel("Nombre de mots de la « Pass Phrase »")
        label2 = QLabel("4 : faible, à éviter")
        label3 = QLabel("5 à 8 : selon le degré de sécurité souhaité")
        label4 = QLabel("9 et plus : paranoïaque")

        generate = QPushButton("Générer la « Pass Phrase »")
        generate.clicked.connect(self.generate_clicked)
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
        main_layout.addWidget(generate)
        main_layout.addWidget(self.rep)

        quit_save = QHBoxLayout()
        main_layout.addLayout(quit_save)

        quitter = QPushButton("Quitter")
        quitter.clicked.connect(quit)
        sauvegarder = QPushButton( "Sauvegarder" )
        sauvegarder.clicked.connect(self.sauvegarder)

        quit_save.addWidget(sauvegarder)
        quit_save.addWidget(quitter)

    def sauvegarder(self):
        dialogue = QFileDialog(self)
        dialogue.setDirectory("/home/camille")
        dialogue.setViewMode(QFileDialog.ViewMode.List)
        
        if dialogue.exec():
             file = dialogue.selectedFiles()
             with open(file[0], 'w') as file:
                for i in range (0, self.rep.count()):
                    file.write( self.rep.item(i).text())
                    file.write(' ')
                file.write('\n')

            

    def generate_clicked(self):
        self.rep.clear()
        with open("diceware.txt", "r") as file:
            for j in range(0, self.nb_mots.value()):
                rand = secrets.randbelow(2724)
                file.seek(0)
                for i in range(0, rand-1):
                    file.readline()
                self.rep.addItem(file.readline().strip())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle('Windows')
    main_windows = MainWindow()
    main_windows.show()

    sys.exit(app.exec())
