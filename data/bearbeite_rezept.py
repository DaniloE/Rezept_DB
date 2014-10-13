import sys

from PyQt4 import QtGui
from PyQt4 import QtCore


sys.path.append("data")
try:
    import connectdb
except:
    print("Zusätzliche Dateien aus dem Unterordner data nicht laden.Beende")


class bearbeite_rezept(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.zutat_index = ''
        self.db_connect = connectdb.connectdb()
        self.alte_rezeptid = 0
        # Initialisierung des Hauptfensters
        self.setGeometry(300, 300, 530, 580)
        self.setWindowTitle('Rezept bearbeiten')

        # Checkliste fuer kategorien
        self.cl_kategorien_items = self.db_connect.get_kategories()
        self.cl_kategorien_items.sort()

        self.cl_kategorien = QtGui.QListView(self)
        self.cl_Kategorien_model = QtGui.QStandardItemModel(self.cl_kategorien)
        # rezeptliste.setMinimumSize(200,700)
        self.cl_kategorien.setGeometry(5, 70, 150, 250)
        self.cl_kategorien.setModel(self.cl_Kategorien_model)

        self.kat_label = QtGui.QLabel(self)
        self.kat_label.setGeometry(5, 50, 75, 15)
        self.kat_label.setText("Kategorien:")

        for kategorie in self.cl_kategorien_items:
            self.cl_kategorien_items_item = QtGui.QStandardItem(kategorie[0])
            self.cl_kategorien_items_item.setCheckable(True)
            self.cl_kategorien_items_item.setEditable(False)
            self.cl_Kategorien_model.appendRow(self.cl_kategorien_items_item)

        self.cl_kategorien.show()

        self.cl_Kategorien_model.itemChanged.connect(self.kategorie_changed)

        # Textfeld für Rezeptname + Label
        self.rezept_name = QtGui.QLineEdit(self)
        self.rezept_name.setGeometry(70, 5, 250, 30)

        self.name_label_anzeige = QtGui.QLabel(self)
        self.name_label_anzeige.setGeometry(QtCore.QRect(5, 15, 65, 15))
        self.name_label_anzeige.setText("Name:")

        # Textfeld für Anweisungeingabe

        self.beschreibung_text = QtGui.QTextEdit(self)
        self.beschreibung_text.setGeometry(5, 360, 500, 200)
        self.beschreibung_label = QtGui.QLabel(self)
        self.beschreibung_label.setGeometry(5, 340, 90, 15)
        self.beschreibung_label.setText("Beschreibung:")

        # Zutatenliste

        self.zutaten_liste = []
        self.zutaten_liste_anzeige = QtGui.QListView(self)
        self.zutaten_liste_anzeige_model = QtGui.QStandardItemModel(self.zutaten_liste_anzeige)
        self.zutaten_liste_anzeige.setModel(self.zutaten_liste_anzeige_model)
        self.zutaten_liste_anzeige.setGeometry(330, 70, 180, 250)
        self.zutaten_liste_anzeige.clicked.connect(self.zutat_rowid)

        # Textfeld für Menge
        self.menge_label = QtGui.QLabel(self)
        self.menge_label.setGeometry(QtCore.QRect(170, 50, 65, 15))
        self.menge_label.setText("Menge:")
        self.menge = QtGui.QLineEdit(self)
        self.menge.setGeometry(170, 70, 150, 30)

        # Combobox fuerZutatenkategorien
        self.combo_zukat = QtGui.QComboBox(self)
        self.combo_zukat.setGeometry(170, 110, 150, 30)
        self.combo_zukat.activated[str].connect(self.setzutaten)

        self.zukat_items = self.db_connect.get_zukat()
        self.zukat_items.sort()
        for zukat in self.zukat_items:
            self.combo_zukat.addItem(zukat[0])

        # Combobox für Zutaten
        self.combo_zutaten = QtGui.QComboBox(self)
        self.combo_zutaten.setGeometry(170, 150, 150, 30)

        # Button Zutat hinzufügen
        self.zutat_plus_button = QtGui.QPushButton(self)
        self.zutat_plus_button.setGeometry(170, 190, 140, 30)
        self.zutat_plus_button.setText("Zutat hinzufügen")

        # Button Zutat entfernen
        self.zutat_minus_button = QtGui.QPushButton(self)
        self.zutat_minus_button.setGeometry(170, 290, 140, 30)
        self.zutat_minus_button.setText("Zutat entfernen")

        # Button zum Speichern des Rezepts
        self.speichern_button = QtGui.QPushButton(self)
        self.speichern_button.setGeometry(350, 10, 140, 30)
        self.speichern_button.setText("Rezept speichern")

        # Button Aktionen
        self.zutaten_dict = {}
        self.kategorie_checked = []
        self.zutat_plus_button.clicked.connect(self.zutat_plus)
        self.zutat_minus_button.clicked.connect(self.zutat_minus)
        self.speichern_button.clicked.connect(self.save_rezept)
        #self.cl_kategorien.clicked.connect(self.kategorie_clicked)

        # Initial laden der ersten Zutatenliste
        self.setzutaten()

    def setzutaten(self):
        zukat_name = self.combo_zukat.currentText()
        self.combo_zutaten.clear()
        zutaten_items = self.db_connect.get_zutaten(zukat_name)
        zutaten_items.sort()
        for zutat in zutaten_items:
            self.combo_zutaten.addItem(zutat[0])


    def kategorie_changed(self):
        self.kategorie_checked = []
        i = 0
        while self.cl_Kategorien_model.item(i):
            if not self.cl_Kategorien_model.item(i).checkState():
                pass
            else:
                if self.cl_Kategorien_model.item(i) in self.kategorie_checked:
                    pass
                else:
                    self.kategorie_checked.append(self.cl_Kategorien_model.item(i))
            i += 1

    def zutat_plus(self):
        menge = str(self.menge.text())
        zutat = str(self.combo_zutaten.currentText())
        self.zutaten_liste_anzeige_model.clear()
        self.zutaten_dict[zutat] = menge
        for key in self.zutaten_dict.keys():
            eintrag = str(key) + " : " + str(self.zutaten_dict[key])
            zutatenliste_item = QtGui.QStandardItem(eintrag)
            self.zutaten_liste_anzeige_model.appendRow(zutatenliste_item)
        self.zutaten_liste_anzeige.repaint()

    def zutat_rowid(self, index):
        self.zutat_index = index

    def zutat_minus(self):
        zutat = ''
        try:
            zutat = self.zutaten_liste_anzeige_model.data(self.zutat_index)
        except:
            pass
        if zutat and len(zutat) > 0:
            zutat = zutat.split(":")
            keyitem = zutat[0].strip()
            self.zutaten_dict.__delitem__(keyitem)
            self.zutaten_liste_anzeige_model.clear()
            for key in self.zutaten_dict.keys():
                eintrag = str(self.zutaten_dict[key]) + " " + str(key)
                zutatenliste_item = QtGui.QStandardItem(eintrag)
                self.zutaten_liste_anzeige_model.appendRow(zutatenliste_item)
            self.zutaten_liste_anzeige.repaint()

    def save_rezept(self):
        kategorie_liste = []
        for kat in self.kategorie_checked:
            indexnummer = self.zutaten_liste_anzeige_model.indexFromItem(kat)
            kategorie_liste.append(self.zutaten_liste_anzeige_model.data(indexnummer))
        beschreibung = self.beschreibung_text.toPlainText()
        zutaten = self.zutaten_dict
        rezeptname = self.rezept_name.text()
        save_rezept_messagebox = QtGui.QMessageBox(self)
        save_rezept_messagebox.setGeometry(700, 500, 120, 100)
        return_insert = self.db_connect.changerezept(kategorie_liste, beschreibung, zutaten, rezeptname,
                                                     self.alte_rezeptid)
        if return_insert == 0:
            save_rezept_messagebox.setText("Rezept geändert")
            save_rezept_messagebox.show()
            self.rezept_name.setText("")
            self.beschreibung_text.setText("")
            self.zutaten_dict = {}
            self.zutaten_liste_anzeige_model.clear()
            self.zutaten_liste_anzeige.repaint()
            self.menge.setText("")
            i = 0
            while self.cl_Kategorien_model.item(i):
                if self.cl_Kategorien_model.item(i).checkState():
                    self.cl_Kategorien_model.item(i).setCheckState(QtCore.Qt.Unchecked)
                i += 1
        elif return_insert == 1:
            save_rezept_messagebox.setText("Rezept konnte nicht in die Datenbank eingetragen werden.")
            save_rezept_messagebox.show()
        else:
            save_rezept_messagebox.setText("Es ist ein nicht erwarteter Fehler aufgetreten. Sieh zu...")
            save_rezept_messagebox.show()

