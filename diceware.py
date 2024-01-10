import sys

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QSpinBox, QListWidget, QHBoxLayout, QFileDialog, QComboBox, QDialog, QDialogButtonBox, QMainWindow, QButtonGroup, QRadioButton#, QMenuBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QAction, QIcon

import secrets

from click import group
#################################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.sep = " "
        self.svg = False

        self.setWindowTitle("Diceware")
        self.setFixedSize(275, 415)

        container = QWidget(self)
        container.setStyleSheet("background-color: rgb(252, 247, 232)")

        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(5)

        self.setCentralWidget(container)

        statusBar = self.statusBar()
        statusBar.showMessage(self.windowTitle())

        ### Actions
        # fichier: sauvegarder
        self.actSauvegarder = QAction(QIcon("icons/save.png"), "Sau&vegarder", self)
        self.actSauvegarder.setShortcut("Ctrl+S")
        self.actSauvegarder.setStatusTip("Sauvegarder la phrase secrète")
        self.actSauvegarder.triggered.connect(self.sauvegarder)
        # fichier: sortir
        self.actSortir = QAction(QIcon("icons/exit.png"), "&Sortir", self)
        self.actSortir.setShortcut("Ctrl+Q")
        self.actSortir.setStatusTip("Quitter")
        self.actSortir.triggered.connect(self.closeEvent)
        # créer: séparateur
        self.actSep = QAction(QIcon(""), "&Choisir le séparateur", self)
        self.actSep.setShortcut("Ctrl+P")
        self.actSep.setStatusTip("Choisir le séparateur")
        self.actSep.triggered.connect(self.choisir_separateur)
        #créer: générer
        self.actNouvellePhrase = QAction(QIcon(""), "&Générer une nouvelle phrase", self)
        self.actNouvellePhrase.setShortcut("Ctrl+G")
        self.actNouvellePhrase.setStatusTip("Générer une nouvelle phase secrète")
        self.actNouvellePhrase.triggered.connect(self.generate_clicked)
        # aide: à propos
        self.actAPropos = QAction(QIcon("icons/about.png)"), "À pr&opos", self)
        self.actAPropos.setShortcut("Crtl+A")
        self.actAPropos.setStatusTip("À propos")
        self.actAPropos.triggered.connect(self.apropos)
        # aide: aide
        self.actAide = QAction(QIcon("icons/help.png"), "&Aide", self)
        self.actAide.setShortcut("F1")
        self.actAide.setStatusTip("Instruction pour l'utilisation du générateur")
        self.actAide.triggered.connect(self.aide)

        ### Barre de menu
        mb = self.menuBar()
        fich = mb.addMenu("&Fichier")
        creer = mb.addMenu("&Créer")
        aide = mb.addMenu("&Aide")

        ### Ajout des actions au menu
        fich.addAction(self.actSauvegarder)
        fich.addAction(self.actSortir)
        creer.addAction(self.actSep)
        creer.addAction(self.actNouvellePhrase)
        aide.addAction(self.actAPropos)
        aide.addAction(self.actAide)

        label1 = QLabel("Générateur de Phrases Secrètes")
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Utopia", 12)
        label1.setStyleSheet("background-color: rgb(119,137,189); color:white; border: 3px solid rgb(49,68,125); border-radius: 5px; margin-bottom: 5px")
        label1.setFont(font)
        label2 = QLabel("Choisir le nombre de mots (entre 4 et 10)\n   4 : sécurité faible, à éviter\n   5 à 8 : selon le degré de sécurité souhaité\n   9 et plus : niveau paranoïaque (en 2024 !)")
        label2.setStyleSheet("background-color: rgb(232,238,252); color: black; border-width: 1px; border-style: outset; border-radius: 2px")

        generate = QPushButton("Générer une Phrase Secrète")
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
        quitter.clicked.connect(self.closeEvent)
        sauvegarder = QPushButton( "Sauvegarder" )
        sauvegarder.setFixedSize(80,25)
        sauvegarder.setStyleSheet("background-color: rgb(166,155,128)")
        sauvegarder.clicked.connect(self.sauvegarder)

        bsvg.addWidget(sauvegarder)
        self.cb = QComboBox()
        self.cb.view().setMinimumWidth(70)
        self.cb.setFixedSize(20,25)
        self.cb.setStyleSheet("background-color: rgb(166,155,128)")
        self.sep_noms = ("Rien", "Tiret haut", "Tiret bas", "Plus", "Espace")
        for i in range(5):
            self.cb.insertItem(i, self.sep_noms[i] )

        self.cb.activated.connect(self.quel_sep)

        bsvg.addWidget(self.cb)

        quit_save.addWidget(quitter)
#--------------------------------------------------------------------------------
    def apropos(self):
        msg = "Ici viendront les informations de\n l'à propos : auteur, copyright, etc."
        ap = CustomDialog(lb1="Fermer",texte=msg, titre="À propos")
        ap.exec()
#--------------------------------------------------------------------------------
    def aide(self):
        msg = "Ici viendront les instructions\n pour l'utilisation de diceware"
        ap = CustomDialog(lb1="Fermer",texte=msg, titre="Instructions")
        ap.exec()
#--------------------------------------------------------------------------------
    def choisir_separateur(self):
        choixSep = ChoixSeparateur()
        choixSep.retStatus = " " # pour éviter erreur si fermeture fenêtre
        choixSep.exec()
        self.sep = choixSep.retStatus
#--------------------------------------------------------------------------------
    def quel_sep(self, index):
        self.cb.setCurrentIndex(index)
        sep_type = self.cb.currentText()
        sep = ("", "-", "_", "+", " ")
        self.sep = sep[index]
#--------------------------------------------------------------------------------
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
#--------------------------------------------------------------------------------
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
#--------------------------------------------------------------------------------
    def closeEvent(self, event) -> None:
        if self.svg:
            quit()
        texte_msg = "La phrase secrète n'est pas sauvegardée\nQuitter quand même ?"
        couleur = "rgb(140,70,35)"
        choix = CustomDialog(lb1="Quitter",lb2="Annuler",texte=texte_msg, coul_fond=couleur)
        choix.exec()
        if choix.retStatus == "1":
            quit()
        elif not isinstance(event, bool):
            event.ignore()
        #return super().closeEvent(event)

#################################################################################
class ChoixSeparateur(QDialog):
    def __init__(self):
        super().__init__()
        self.dict_sep = { "Espace": " ", "Rien": "", "Tiret haut": "-", "Tiret bas": "_", "Plus": "+"}
        bouton = list()
        self.group = QButtonGroup(self)
        container = QWidget(self)
        rb_layout = QVBoxLayout(container)
        self.setLayout(rb_layout)
        container.setFixedSize(210,250)
        container.setStyleSheet("background-color: rgb(220,238,252)")

        titre = QLabel("Choisissez le séparateur de mots")
        titre.setStyleSheet("color: #333")
        rb_layout.addWidget(titre)

        i = 0
        for label in self.dict_sep:
            b = QRadioButton(label, self)
            if not i:
                b.setChecked(True)
            h = 30
            v = 20*(i+1)
            b.move(h,v )
            bouton.append(b)
            self.group.addButton(bouton[i], i)
            rb_layout.addWidget(bouton[i], i)
            i += 1

        self.group.buttonClicked.connect(self.slot)
        
    def slot(self, b):
        self.retStatus = self.dict_sep[b.text()]
        self.close()
#################################################################################
class CustomDialog(QDialog):
    def __init__(self, lb1 = "", lb2 = "", texte="", titre="Avertissement", coul_fond="gray"):
        super().__init__()

        self.setWindowTitle(titre)
        self.retStatus = "X" # pour éviter une erreur si fermeture de la fenêtre

        coul_bouton = "rgb(166,155,128)"

        self.btn_1 = QPushButton(lb1)
        self.btn_1.setStyleSheet(f"background-color: {coul_bouton}")
        self.btn_1.clicked.connect(self.act_bt1)
        self.btn_2 = QPushButton(lb2)
        self.btn_2.setStyleSheet(f"background-color: {coul_bouton}")
        self.btn_2.clicked.connect(self.act_bt2)

        self.dlg = QDialogButtonBox()
        self.dlg.addButton(self.btn_1,QDialogButtonBox.ButtonRole.AcceptRole)
        if lb1 and lb2:
            self.dlg.addButton(self.btn_2,QDialogButtonBox.ButtonRole.RejectRole)

        message = QLabel(texte)
        message.setStyleSheet("color:rgb(220,220,220)")

        container = QWidget(self)
        cd_layout = QVBoxLayout(container)
        container.setStyleSheet(f"background-color: {coul_fond}")
        container.setFixedSize(250,200)
        cd_layout.addWidget(message)
        cd_layout.addWidget(self.dlg)
        self.setLayout(cd_layout)
#--------------------------------------------------------------------------------
    def act_bt1(self):
        self.retStatus = "1"
        self.close()
#--------------------------------------------------------------------------------
    def act_bt2(self):
        self.retStatus = "2"
        self.close()
#################################################################################


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle('Windows')
    main_windows = MainWindow()
    main_windows.show()

    sys.exit(app.exec())

# à faire : layout.setSpacing()
# à faire : main_layout.setContentsMargins(5,0,0,5)
# à faire : setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
# <PySide6.QtCore.QEvent(QEvent::Close)>
