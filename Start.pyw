#!/bin/env python3

import os
import sys
import os.path

from PyQt4 import QtGui
from PyQt4 import QtCore

sys.path.append("data")
try:
    import connectdb
    import neues_rezept
    import konfiguration
    import bearbeite_rezept
except:
    print("Zusätzliche Dateien aus dem Unterordner data nicht laden.Beende")

class Mainwindow(QtGui.QMainWindow):
    def __init__(self, parent=None):

        QtGui.QMainWindow.__init__(self, parent)

        # DB-Verbindung ermöglichen
        self.db_connect = connectdb.connectdb()

        # Diverse weitere Fenster instanzieren
        self.neues_rezept_window = neues_rezept.rezepte_neu()
        self.konfiguration_window = konfiguration.Konfiguration()
        self.rezept_bearbeiten_window = bearbeite_rezept.bearbeite_rezept()

        # Initialisierung des Hauptfensters
        self.setGeometry(300, 300, 750, 550)
        self.setWindowTitle('RezeptDB')

        # Menue und Statusleiste

        self.statusbar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.menuleiste = QtGui.QMenuBar(self)
        self.setMenuBar(self.menuleiste)


        # Aktion zum Beenden des Programms
        self.exitAction = QtGui.QAction(self)
        self.exitAction.setText('Beenden')
        self.exitAction.setStatusTip('Beende Programm')
        self.exitAction.triggered.connect(QtGui.qApp.quit)

        # Aktion für Rezepteverwaltung
        self.rezept_neu_action = QtGui.QAction(self)
        self.rezept_neu_action.setText("Neues Rezept")
        self.rezept_neu_action.triggered.connect(self.rezept_neu_function)

        self.rezept_bearbeiten_action = QtGui.QAction(self)
        self.rezept_bearbeiten_action.setText("Aktuelles Rezept bearbeiten")
        self.rezept_bearbeiten_action.triggered.connect(self.rezept_bearbeiten_function)

        self.export_rezept_action = QtGui.QAction(self)
        self.export_rezept_action.setText("Gewähltes Rezept exportieren")
        self.export_rezept_action.triggered.connect(self.export_rezept)

        self.loesche_rezept_action = QtGui.QAction(self)
        self.loesche_rezept_action.setText("Aktuelles Rezept löschen")
        self.loesche_rezept_action.triggered.connect(self.rezept_loeschen)

        self.konfiguration_action = QtGui.QAction(self)
        self.konfiguration_action.setText("Konfiguration")
        self.konfiguration_action.triggered.connect(self.konfiguration_function)

        self.datei_menu = QtGui.QMenu(self)
        self.datei_menu.setTitle("Datei")
        self.menuleiste.addAction(self.datei_menu.menuAction())

        self.rezepte_menu = QtGui.QMenu(self)
        self.rezepte_menu.setTitle("Rezepte verwalten")
        self.menuleiste.addAction(self.rezepte_menu.menuAction())

        self.kategorie_menu = QtGui.QMenu(self)
        self.kategorie_menu.setTitle("Kategorien/Zutaten verwalten")
        self.menuleiste.addAction(self.konfiguration_action)

        self.datei_menu.addAction(self.exitAction)
        self.rezepte_menu.addAction(self.rezept_neu_action)
        self.rezepte_menu.addAction(self.rezept_bearbeiten_action)
        self.rezepte_menu.addAction(self.export_rezept_action)
        self.rezepte_menu.addAction(self.loesche_rezept_action)

        #############
        # Initialisierung der Anzeige
        #############

        # Combobox für Kategorien
        self.combo_kategorie = QtGui.QComboBox(self)
        self.combo_kategorie.setGeometry(5, 30, 250, 30)

        self.kategorie_items = self.db_connect.get_kategories()
        self.kategorie_items.sort()

        for kategorie in self.kategorie_items:
            self.combo_kategorie.addItem(kategorie[0])

        self.combo_kategorie.activated[str].connect(self.comborezeptliste)

        # Liste fuer ausgewählte Rezepte
        self.rezeptliste = QtGui.QListView(self)
        self.rezeptliste_model = QtGui.QStandardItemModel(self.rezeptliste)
        self.rezeptliste.setGeometry(5, 60, 250, 460)
        self.rezeptliste.setModel(self.rezeptliste_model)
        self.rezeptliste.clicked.connect(self.rezept_changed)

        # Labels (statischer Inhalt)
        self.name_label_anzeige = QtGui.QLabel(self)
        self.name_label_anzeige.setGeometry(QtCore.QRect(265, 40, 70, 15))
        self.name_label_anzeige.setText("Name:")

        self.kategorie_label_anzeige = QtGui.QLabel(self)
        self.kategorie_label_anzeige.setGeometry(QtCore.QRect(265, 80, 75, 15))
        self.kategorie_label_anzeige.setText("Kategorien:")

        self.Zutaten_label = QtGui.QLabel(self)
        self.Zutaten_label.setGeometry(QtCore.QRect(265, 120, 65, 15))
        self.Zutaten_label.setText("Zutaten:")

        self.Zubereitung_label = QtGui.QLabel(self)
        self.Zubereitung_label.setGeometry(QtCore.QRect(270, 300, 80, 15))
        self.Zubereitung_label.setText("Zubereitung:")

        # Labels (dynamischer Inhalt)

        self.Name = QtGui.QTextBrowser(self)
        self.Name.setGeometry(QtCore.QRect(355, 35, 365, 30))

        self.kategorien = QtGui.QTextBrowser(self)
        self.kategorien.setGeometry(QtCore.QRect(355, 70, 365, 30))

        self.Zutaten = QtGui.QTextBrowser(self)
        self.Zutaten.setGeometry(QtCore.QRect(355, 110, 365, 170))

        self.Zubereitung = QtGui.QTextBrowser(self)
        self.Zubereitung.setGeometry(QtCore.QRect(270, 320, 450, 200))

    def export_rezept(self):
        exportdir = "exportierte_rezepte"
        curdir = os.getcwd()
        if not os.path.isdir(exportdir):
            os.makedirs(exportdir)
        messagebox = QtGui.QMessageBox(self)
        messagebox.setGeometry(700, 500, 120, 100)
        rezeptname = self.Name.toPlainText()
        if rezeptname.strip() == '':
            messagebox.setText("Bitte vor dem Export ein Rezept wählen")
            messagebox.show()
            return
        kategorien = self.kategorien.toPlainText()
        zutaten = self.Zutaten.toPlainText()
        zubereitung = self.Zubereitung.toPlainText()
        export = open(os.path.join(curdir, exportdir, rezeptname + ".txt"), "w", encoding="utf8")
        export.write("Rezeptname: " + rezeptname + "\n\n")
        export.write("Kategorien: " + kategorien + "\n\n")
        export.write("Zutaten:\n" + zutaten + "\n\n")
        export.write("Zuereitung:\n" + zubereitung)
        export.close()
        messagebox.setText("Rezept nach " + os.path.join(curdir, exportdir, rezeptname + ".txt") + ".txt exportiert.")
        messagebox.show()

    def rezept_changed(self, index):
        rezeptname = self.rezeptliste_model.data(index)
        rezeptdaten_id_text = self.db_connect.get_rezeptdaten_id_beschreibung(rezeptname)
        if rezeptdaten_id_text is not None:
            rezept_id = rezeptdaten_id_text[0]
            rezept_text = rezeptdaten_id_text[1]
            rezeptdaten_zutaten = self.db_connect.get_rezeptdaten_zutaten(rezept_id)
            self.Name.setText(rezeptname)
            self.Zubereitung.setText(rezept_text)
            self.Zutaten.clear()
            for zeile in rezeptdaten_zutaten:
                self.Zutaten.append(zeile)
            kategorien = self.db_connect.get_rezeptdaten_kategorien(rezept_id)
            self.kategorien.setText(kategorien)
        else:
            self.Name.setText('')
            self.Zubereitung.setText('')
            self.Zutaten.clear()
            self.kategorien.setText('')

    def comborezeptliste(self):
        # Rezeptliste
        rezkat = self.combo_kategorie.currentText()
        rezeptliste_items = self.db_connect.get_rezepte(rezkat)
        rezeptliste_items.sort()
        self.rezeptliste_model.clear()
        for rezept in rezeptliste_items:
            rezeptliste_kategorie_item = QtGui.QStandardItem(rezept[0])
            self.rezeptliste_model.appendRow(rezeptliste_kategorie_item)
        self.rezeptliste.show()


    def rezept_neu_function(self):
        self.neues_rezept_window.show()

    def rezept_bearbeiten_function(self):
        rezeptname = self.Name.toPlainText()
        alte_rezeptid = self.db_connect.get_rezeptid(rezeptname)
        self.rezept_bearbeiten_window.alte_rezeptid = alte_rezeptid[0]
        print(str(self.rezept_bearbeiten_window.alte_rezeptid))
        self.rezept_bearbeiten_window.rezept_name.setText(rezeptname)
        self.rezept_bearbeiten_window.beschreibung_text.setText(self.Zubereitung.toPlainText())
        rezeptdaten_id_text = self.db_connect.get_rezeptdaten_id_beschreibung(rezeptname)
        rezept_id = rezeptdaten_id_text[0]
        rezeptdaten_zutaten = self.db_connect.get_rezeptdaten_zutaten(rezept_id, change=True)
        for zeile in rezeptdaten_zutaten:
            dictteile = zeile.split(":")
            self.rezept_bearbeiten_window.zutaten_dict[dictteile[0]] = dictteile[1]
            zutatenliste_item = QtGui.QStandardItem(zeile)
            self.rezept_bearbeiten_window.zutaten_liste_anzeige_model.appendRow(zutatenliste_item)
        kate_checklist = self.kategorien.toPlainText().split()
        for katid in range(self.rezept_bearbeiten_window.cl_Kategorien_model.rowCount()):
            katname_liste = self.rezept_bearbeiten_window.cl_kategorien_items.__getitem__(katid)[0]
            if katname_liste in kate_checklist:
                self.rezept_bearbeiten_window.cl_Kategorien_model.item(katid).setCheckState(True)
        self.rezept_bearbeiten_window.show()

    def konfiguration_function(self):
        self.konfiguration_window.show()

    def rezept_loeschen(self):
        abfrage_loeschen = QtGui.QMessageBox.question(self, 'Sicherheitsfrage',
                                                      "Soll das Rezept wirklich gelöscht werden?",\
                                                      QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if abfrage_loeschen == QtGui.QMessageBox.Yes:
            rezeptname = self.Name.toPlainText()
            self.db_connect.delete_rezept(rezeptname)
            self.comborezeptliste()
        else:
            pass


if not os.path.isfile(os.path.join("data",'rezepte.db')):
    cb = connectdb.create_database()
    cb.create_new()
    cb.insert_initial()

app = QtGui.QApplication(sys.argv)
mw = Mainwindow()
mw.show()
app.exec_()

