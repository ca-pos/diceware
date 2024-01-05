import sys

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QSpinBox, QListWidget, QHBoxLayout, QFileDialog, QComboBox, QCommandLinkButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

import secrets

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.sep = " "
        self.svg = False

        self.setWindowTitle("Diceware")
        #self.setFixedSize(275, 515)
        self.setFixedSize(275, 415)

        container = QWidget(self)
        container.setStyleSheet("background-color: rgb(252, 247, 232)")

        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(5)

        label1 = QLabel("Générateur de « Pass Phrases »")
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Utopia", 12)
        label1.setStyleSheet("background-color: rgb(119,137,189); color:white; border: 3px solid rgb(49,68,125); border-radius: 5px; margin-bottom: 5px")
        label1.setFont(font)
        label2 = QLabel("Choisir le nombre de mots (entre 4 et 10)\n   4 : sécurité faible, à éviter\n   5 à 8 : selon le degré de sécurité souhaité\n   9 et plus : niveau paranoïaque (en 2024 !)")
        label2.setStyleSheet("background-color: rgb(232,238,252); color: black; border-width: 1px; border-style: outset; border-radius: 2px")

        generate = QPushButton("Générer la « Pass Phrase »")
        generate.clicked.connect(self.generate_clicked)
        generate.setStyleSheet("background-color: rgb(166,155,128)")
        self.nb_mots = QSpinBox()
        self.nb_mots.setRange(4,10)
        self.nb_mots.setValue(8)
        self.nb_mots.setStyleSheet("background-color: rgb(232,238,252)")
 
        self.first_pass = ["sperme", "exil", "éveil", "ulcère", "tract", "rock", "partie", "étang"]
        self.rep = QListWidget()
        self.rep.setStyleSheet("background-color: rgb(232,238,252)")
        for i in range(0, len(self.first_pass)):
            self.rep.addItem(self.first_pass[i])

        main_layout.addWidget(label1)
        main_layout.addWidget(label2)
        main_layout.addWidget(self.nb_mots)
        main_layout.addWidget(generate)
        main_layout.addWidget(self.rep)

        quit_save = QHBoxLayout()
        bsvg = QHBoxLayout()
        bsvg.setSpacing(0)
        quit_save.addLayout(bsvg)
        main_layout.addLayout(quit_save)

        quitter = QPushButton("Quitter")
        quitter.setStyleSheet("background-color: rgb(166,155,128)")
        quitter.setFixedSize(100,25)
        quitter.clicked.connect(quit)
        sauvegarder = QPushButton( "Sauvegarder" )
        sauvegarder.setFixedSize(80,25)
        sauvegarder.setStyleSheet("background-color: rgb(166,155,128)")
        sauvegarder.clicked.connect(self.sauvegarder)

        bsvg.addWidget(sauvegarder)
        cb = QComboBox()
        cb.view().setMinimumWidth(70)
        cb.setFixedSize(20,25)
        cb.setStyleSheet("background-color: rgb(166,155,128)")
        sep_noms = ("Rien", "Tiret haut", "Tiret bas", "Plus", "Espace")
        for i in range(5):
            cb.insertItem(i, sep_noms[i] )

        cb.activated.connect(self.quel_sep)

        bsvg.addWidget(cb)

        quit_save.addWidget(quitter)

    def quel_sep(self, index):
        sep = ("", "-", "_", "+", " ")
        self.sep = sep[index]

    def sauvegarder(self):
        dialogue = QFileDialog(self)
        dialogue.setDirectory("/home/camille")
        dialogue.setViewMode(QFileDialog.ViewMode.List)
        
        if dialogue.exec():
             file = dialogue.selectedFiles()
             der = self.rep.count()
             with open(file[0], 'w') as file:
                for i in range (0, der):
                    file.write( self.rep.item(i).text())
                    if i != der-1:
                        file.write(self.sep)
                file.write('\n')

        self.svg = True

    def generate_clicked(self):
        self.rep.clear()
        self.svg = False
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

# à faire : layout.setSpacing()
# main_layout.setContentsMargins(5,0,0,5)
# à faire : setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
# à faire : 
