import sys

from PyQt4 import QtGui
from PyQt4 import QtCore


sys.path.append("data")

try:
    import connectdb
except:
    print("Zusätzliche Dateien aus dem Unterordner data nicht laden.Beende")


class Konfiguration(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.db_connect = connectdb.connectdb()

        # Initialisierung des Hauptfensters
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Konfiguration')

        # Initialisierung der Tabulatorstruktur
        tabwidget = QtGui.QTabWidget(self)
        tabwidget.setGeometry(QtCore.QRect(5, 10, 590, 390))

        # Hinzufuegen der Tabs
        tab_kategorie = QtGui.QWidget()
        tabwidget.addTab(tab_kategorie, "Kategorien(Gerichte)")
        tab_zutat_kategorie = QtGui.QWidget()
        tabwidget.addTab(tab_zutat_kategorie, "Kategorien(Zutaten)")
        tab_zutat = QtGui.QWidget()
        tabwidget.addTab(tab_zutat, "Zutat ändern")
        tab_zutat_neu = QtGui.QWidget()
        tabwidget.addTab(tab_zutat_neu, "Neue Zutat")


        # ----------------------#
        # Tabulator Kategorien (Gerichte) #
        #----------------------#


        # Checkliste fuer kategorien
        self.cl_kategorien_items = self.db_connect.get_kategories()
        self.cl_kategorien_items.sort()

        self.cl_kategorien = QtGui.QListView(tab_kategorie)
        self.cl_Kategorien_model = QtGui.QStandardItemModel(self.cl_kategorien)
        #rezeptliste.setMinimumSize(200,700)
        self.cl_kategorien.setGeometry(10, 70, 300, 250)
        self.cl_kategorien.setModel(self.cl_Kategorien_model)

        for kategorie in self.cl_kategorien_items:
            self.cl_kategorien_items_item = QtGui.QStandardItem(kategorie[0])
            self.cl_kategorien_items_item.setCheckable(True)
            self.cl_Kategorien_model.appendRow(self.cl_kategorien_items_item)

        self.cl_kategorien.show()

        self.kat_plus_label = QtGui.QLabel(tab_kategorie)
        self.kat_plus_label.setGeometry(10, 5, 370, 30)
        self.kat_plus_label.setText("Name einer neuen Kategorie")
        self.kat_plus_name = QtGui.QLineEdit(tab_kategorie)
        self.kat_plus_name.setGeometry(10, 30, 370, 30)

        self.kat_delete_button = QtGui.QPushButton(tab_kategorie)
        self.kat_delete_button.setGeometry(330, 100, 200, 30)
        self.kat_delete_button.setText("Ausgewählte Kategorien löschen")
        self.kat_delete_button.clicked.connect(self.kat_delete)

        self.kat_plus_button = QtGui.QPushButton(tab_kategorie)
        self.kat_plus_button.setGeometry(430, 30, 150, 30)
        self.kat_plus_button.setText("Kategorie hinzufügen")
        self.kat_plus_button.clicked.connect(self.kat_plus)

        #--------------------------------#
        # Tabulator Kategorien (Zutaten) #
        #--------------------------------#

        self.zut_kat_plus_label = QtGui.QLabel(tab_zutat_kategorie)
        self.zut_kat_plus_label.setGeometry(10, 5, 370, 30)
        self.zut_kat_plus_label.setText("Neue Zutaten-Kategorie")
        self.zut_kat_plus_name = QtGui.QLineEdit(tab_zutat_kategorie)
        self.zut_kat_plus_name.setGeometry(10, 30, 370, 30)

        self.zut_kat_plus_button = QtGui.QPushButton(tab_zutat_kategorie)
        self.zut_kat_plus_button.setGeometry(430, 30, 150, 30)
        self.zut_kat_plus_button.setText("Kategorie hinzufügen")
        self.zut_kat_plus_button.clicked.connect(self.zukat_plus)

        self.zut_kat_delete_button = QtGui.QPushButton(tab_zutat_kategorie)
        self.zut_kat_delete_button.setGeometry(330, 100, 200, 30)
        self.zut_kat_delete_button.setText("Ausgewählte Kategorien löschen")
        self.zut_kat_delete_button.clicked.connect(self.zukat_delete)

        self.zut_kat_kategorien_items = self.db_connect.get_zukat()
        self.zut_kat_kategorien_items.sort()

        self.zut_kat_kategorien = QtGui.QListView(tab_zutat_kategorie)
        self.zut_kat_Kategorien_model = QtGui.QStandardItemModel(self.zut_kat_kategorien)
        self.zut_kat_kategorien.setGeometry(10, 70, 300, 250)
        self.zut_kat_kategorien.setModel(self.zut_kat_Kategorien_model)

        for kategorie in self.zut_kat_kategorien_items:
            self.zut_kat_kategorien_items_item = QtGui.QStandardItem(kategorie[0])
            self.zut_kat_kategorien_items_item.setCheckable(True)
            self.zut_kat_Kategorien_model.appendRow(self.zut_kat_kategorien_items_item)

        self.zut_kat_kategorien.show()

        #----------------------#
        # Tabulator Neue Zutat #
        #----------------------#

        self.zut_plus_label = QtGui.QLabel(tab_zutat_neu)
        self.zut_plus_label.setGeometry(10, 5, 370, 30)
        self.zut_plus_label.setText("Name")
        self.zut_plus_name = QtGui.QLineEdit(tab_zutat_neu)
        self.zut_plus_name.setGeometry(10, 30, 370, 30)

        self.zut_plus_kat_label = QtGui.QLabel(tab_zutat_neu)
        self.zut_plus_kat_label.setGeometry(10, 65, 250, 30)
        self.zut_plus_kat_label.setText("Kategorie")

        # Combobox fuer Zutatenkategorien
        self.zukat_combo = QtGui.QComboBox(tab_zutat_neu)
        self.zukat_combo.setGeometry(10, 90, 240, 30)

        self.zukat_items = self.db_connect.get_zukat()
        self.zukat_items.sort()
        for zukat in self.zukat_items:
            self.zukat_combo.addItem(zukat[0])

        self.zut_plus_button = QtGui.QPushButton(tab_zutat_neu)
        self.zut_plus_button.setGeometry(430, 30, 150, 30)
        self.zut_plus_button.setText("Zutat hinzufügen")
        self.zut_plus_button.clicked.connect(self.zut_plus)




        #----------------------------------------#
        # Tab für Änderung einer einzelnen Zutat #
        #----------------------------------------#


        # Combobox für Kategorie
        self.zukat_alt_label = QtGui.QLabel(tab_zutat)
        self.zukat_alt_label.setGeometry(10, 10, 300, 30)
        self.zukat_alt_label.setText("Kategorie wählen")
        self.zukat_combo_alt = QtGui.QComboBox(tab_zutat)
        self.zukat_combo_alt.setGeometry(10, 40, 240, 30)
        self.zukat_combo_alt.activated[str].connect(self.setzutaten)
        self.zukat_items_alt = self.db_connect.get_zukat()
        self.zukat_items_alt.sort()
        for zukat_alt in self.zukat_items_alt:
            self.zukat_combo_alt.addItem(zukat_alt[0])

        # Combobox für Zutaten der in der Kategorie (alt) gewählten Zutat
        self.zutat_label = QtGui.QLabel(tab_zutat)
        self.zutat_label.setGeometry(300, 10, 150, 30)
        self.zutat_label.setText("Zutat wählen")
        self.combo_zutaten = QtGui.QComboBox(tab_zutat)
        self.combo_zutaten.setGeometry(300, 40, 240, 30)

        # Label für Zutat ändern
        self.zut_kat_change_label = QtGui.QLabel(tab_zutat)
        self.zut_kat_change_label.setGeometry(200, 120, 250, 30)
        self.zut_kat_change_label.setText("Kategorie der oben gewählten Zutat ändern")

        # Combobox für neue Kategorie
        # self.zukat_neu_label = QtGui.QLabel(tab_zutat)
        # self.zukat_neu_label.setGeometry(10, 150, 300, 30)
        # self.zukat_neu_label.setText("Neue Kategorie wählen")
        self.zukat_combo_neu = QtGui.QComboBox(tab_zutat)
        self.zukat_combo_neu.setGeometry(10, 160, 240, 30)

        self.zukat_items_neu = self.db_connect.get_zukat()
        self.zukat_items_neu.sort()
        for zukat_neu in self.zukat_items_neu:
            self.zukat_combo_neu.addItem(zukat_neu[0])

        # Button für Übernehmen der neuen Kategorie
        self.zut_change_button = QtGui.QPushButton(tab_zutat)
        self.zut_change_button.setGeometry(300, 160, 110, 30)
        self.zut_change_button.setText("Kategorie wechseln")
        self.zut_change_button.clicked.connect(self.zut_change)

        #
        # Zutat Umbenennen (label,Lineedit,Button)
        #

        self.zut_newname_label = QtGui.QLabel(tab_zutat)
        self.zut_newname_label.setGeometry(200, 250, 250, 30)
        self.zut_newname_label.setText("Oben gewählte Zutat umbenennen")
        # Textfeld für neue Zutatenbezeichnung
        self.zut_newname_name = QtGui.QLineEdit(tab_zutat)
        self.zut_newname_name.setGeometry(10, 290, 250, 30)
        #
        self.zut_newname_button = QtGui.QPushButton(tab_zutat)
        self.zut_newname_button.setGeometry(300, 290, 100, 30)
        self.zut_newname_button.setText("Namen Ändern")
        self.zut_newname_button.clicked.connect(self.zut_newname)


    def zut_newname(self):
        zuname_neu = self.zut_newname_name.text()
        zuname = self.combo_zutaten.currentText()
        messagebox = QtGui.QMessageBox(self)
        messagebox.setGeometry(700, 500, 120, 100)
        rename_zutat = self.db_connect.zutat_newname(zuname, zuname_neu)
        if rename_zutat == 0:
            messagebox.setText("Zutat wurde umbenannt.")
            messagebox.show()
            self.setzutaten()
            self.zut_newname_name.clear()
        elif rename_zutat == 1:
            messagebox.setText("Bitte einen neuen Namen für die Zutat angeben.")
            messagebox.show()
        elif rename_zutat == 2:
            messagebox.setText("Name konnte nicht aktualisiert werden.")
            messagebox.show()
        else:
            messagebox.setText("Es ist ein unerwarteter Fehler aufgetreten.")
            messagebox.show()


    def zut_plus(self):
        zutat_name = self.zut_plus_name.text()
        zukat_name = self.zukat_combo.currentText()
        messagebox = QtGui.QMessageBox(self)
        messagebox.setGeometry(700, 500, 120, 100)
        insert_zutat = self.db_connect.create_zutat(zutat_name, zukat_name)
        if insert_zutat == 0:
            messagebox.setText("Zutat wurde hinzugefügt")
            messagebox.show()
        elif insert_zutat == 1:
            messagebox.setText(
                "Bitte sowohl einen Namen vergeben, wie auch eine Kategorie für die neue Zutat auswählen")
            messagebox.show()
        elif insert_zutat == 2:
            messagebox.setText("Es existiert bereits eine Zutat mit diesem Namen")
            messagebox.show()

    def zut_change(self):
        # zukat_alt=self.zukat_combo_alt.currentText()
        zukat_neu = self.zukat_combo_neu.currentText()
        zutat_name = self.combo_zutaten.currentText()
        messagebox = QtGui.QMessageBox(self)
        messagebox.setGeometry(700, 500, 120, 100)
        change_zutat = self.db_connect.change_zukat(zutat_name, zukat_neu)
        if change_zutat == 1:
            messagebox.setText("Bitte sowohl eine Zutat, wie auch eine neue Kategorie auswählen")
            messagebox.show()
        elif change_zutat == 0:
            messagebox.setText("Kategorie erfolgreich aktualisiert")
            messagebox.show()

    def setzutaten(self):
        zukat_name = self.zukat_combo_alt.currentText()
        self.combo_zutaten.clear()
        zutaten_items = self.db_connect.get_zutaten(zukat_name)
        zutaten_items.sort()
        for zutat in zutaten_items:
            self.combo_zutaten.addItem(zutat[0])

    def kat_plus(self):
        save_kat_messagebox = QtGui.QMessageBox(self)
        save_kat_messagebox.setGeometry(700, 500, 120, 100)
        kategorie_name = self.kat_plus_name.text()
        insert_kategorie = self.db_connect.create_kategorie(kategorie_name)
        if insert_kategorie == 0:
            self.refresh_kategories()
            # save_kat_messagebox.setText("Kategorie erfolgreich eingetragen")
            #save_kat_messagebox.show()
        elif insert_kategorie == 1:
            save_kat_messagebox.setText("Es wurde kein Name eingetragen")
            save_kat_messagebox.show()
        elif insert_kategorie == 2:
            save_kat_messagebox.setText("Die kategorie existiert bereits")
            save_kat_messagebox.show()

    def refresh_kategories(self):
        self.cl_kategorien_items = self.db_connect.get_kategories()
        self.cl_kategorien_items.sort()
        self.cl_Kategorien_model.clear()
        for kategorie in self.cl_kategorien_items:
            self.cl_kategorien_items_item = QtGui.QStandardItem(kategorie[0])
            self.cl_kategorien_items_item.setCheckable(True)
            self.cl_Kategorien_model.appendRow(self.cl_kategorien_items_item)
            self.cl_kategorien.repaint()
        self.kat_plus_name.setText('')

    def refresh_zukat(self):
        self.zut_kat_kategorien_items = self.db_connect.get_zukat()
        self.zut_kat_kategorien_items.sort()
        self.zut_kat_Kategorien_model.clear()
        for kategorie in self.zut_kat_kategorien_items:
            self.zut_kat_kategorien_items_item = QtGui.QStandardItem(kategorie[0])
            self.zut_kat_kategorien_items_item.setCheckable(True)
            self.zut_kat_Kategorien_model.appendRow(self.zut_kat_kategorien_items_item)
            self.zut_kat_kategorien.repaint()
        self.zut_kat_plus_name.setText('')

    def kat_delete(self):
        delete_kat_messagebox = QtGui.QMessageBox(self)
        delete_kat_messagebox.setGeometry(700, 500, 120, 100)
        kategorie_checked = []
        kategorie_liste = []
        i = 0
        while self.cl_Kategorien_model.item(i):
            if not self.cl_Kategorien_model.item(i).checkState():
                pass
            else:
                if self.cl_Kategorien_model.item(i) in kategorie_checked:
                    pass
                else:
                    self.kategorie_checked.append(self.cl_Kategorien_model.item(i))
            i += 1
        for kat in self.kategorie_checked:
            indexnummer = self.cl_Kategorien_model.indexFromItem(kat)
            kategorie_liste.append(self.cl_Kategorien_model.data(indexnummer))
        delete_kat = self.db_connect.delete_kategorie(kategorie_liste)
        kat_problem = delete_kat[0]
        kat_deleted = delete_kat[1]
        delete_kat_messagetext = ''
        if len(kat_problem) > 0:
            delete_kat_messagetext = "Folgenden Kategorien sind noch Rezepte zugeteilt und konnten nicht gelöscht werden:\n"
            for kat_prob in kat_problem:
                delete_kat_messagetext += "\n" + kat_prob
        if len(kat_deleted) > 0:
            delete_kat_messagetext += "\n\nFolgende Kategorien wurden erfolgreich gelöscht:"
            for kat in kat_deleted:
                delete_kat_messagetext += "\n" + kat
        message_length = len(kat_problem) + len(kat_deleted) + 40
        delete_kat_messagebox.setGeometry(700, 500, message_length, 100)
        delete_kat_messagebox.setText(delete_kat_messagetext)
        self.refresh_kategories()
        delete_kat_messagebox.show()

    def zukat_plus(self):
        save_zukat_messagebox = QtGui.QMessageBox(self)
        save_zukat_messagebox.setGeometry(700, 500, 120, 100)
        kategorie_name = self.zut_kat_plus_name.text()
        insert_kategorie = self.db_connect.create_zukat(kategorie_name)
        if insert_kategorie == 0:
            self.refresh_zukat()
            # save_kat_messagebox.setText("Kategorie erfolgreich eingetragen")
            #save_kat_messagebox.show()
        elif insert_kategorie == 1:
            save_zukat_messagebox.setText("Es wurde kein Name eingetragen")
            save_zukat_messagebox.show()
        elif insert_kategorie == 2:
            save_zukat_messagebox.setText("Die kategorie existiert bereits")
            save_zukat_messagebox.show()

    def zukat_delete(self):
        delete_zukat_messagebox = QtGui.QMessageBox(self)
        delete_zukat_messagebox.setGeometry(700, 500, 120, 100)
        zukat_checked = []
        kategorie_liste = []
        i = 0
        while self.zut_kat_Kategorien_model.item(i):
            if not self.zut_kat_Kategorien_model.item(i).checkState():
                pass
            else:
                if self.zut_kat_Kategorien_model.item(i) in zukat_checked:
                    pass
                else:
                    self.zukat_checked.append(self.zut_kat_Kategorien_model.item(i))
            i += 1
        for kat in self.zukat_checked:
            indexnummer = self.zut_kat_Kategorien_model.indexFromItem(kat)
            kategorie_liste.append(self.zut_kat_Kategorien_model.data(indexnummer))
        delete_kat = self.db_connect.delete_zukat(kategorie_liste)
        kat_problem = delete_kat[0]
        kat_deleted = delete_kat[1]
        delete_zukat_messagetext = ''
        if len(kat_problem) > 0:
            delete_zukat_messagetext = "In folgenden Kategorien sind noch Zutaten enthalten und konnten nicht gelöscht werden:\n"
            for kat_prob in kat_problem:
                delete_zukat_messagetext += "\n" + kat_prob
        if len(kat_deleted) > 0:
            delete_zukat_messagetext += "\n\nFolgende Kategorien wurden erfolgreich gelöscht:"
            for kat in kat_deleted:
                delete_zukat_messagetext += "\n" + kat
        message_length = len(kat_problem) + len(kat_deleted) + 40
        delete_zukat_messagebox.setGeometry(700, 500, message_length, 100)
        delete_zukat_messagebox.setText(delete_zukat_messagetext)
        self.refresh_zukat()
        delete_zukat_messagebox.show()