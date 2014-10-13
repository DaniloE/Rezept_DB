import sqlite3
import collections

import os


class connectdb():
    def __init__(self):
        self.db_name = os.path.join("data", 'rezepte.db')

    def get_kategories(self):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("Select name from kategorie;")
        kat_list = c.fetchall()

        con.close()
        return kat_list

    def test_rezeptname(self, name):
        if name.strip() == '':
            return 1
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("Select count(*) from rezept where lower(name) = lower (?);", (name,))
        rezept_vorhanden = c.fetchone()
        if rezept_vorhanden[0] > 0:
            return 2
        con.close()
        return 0

    def get_rezeptdaten_id_beschreibung(self, rezeptname):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("select id from rezept where name=(?)", (rezeptname,))
        rez_id = c.fetchone()
        if rez_id is None:
            return None
        c.execute("Select text from Beschreibung where FK_Rezept = (?)", (rez_id[0],))
        beschreibungstext = c.fetchall()
        return [rez_id[0], beschreibungstext[0][0]]

    def get_rezeptdaten_zutaten(self, rezid, change=False):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        zutaten_return = []
        c.execute("Select FK_zutat,menge from rezept_zutaten where FK_rezept = (?)", (rezid,))
        zutatenliste = c.fetchall()
        for zutat in zutatenliste:
            zutat_id = zutat[0]
            zutat_menge = zutat[1]
            c.execute("select name from zutaten where id = (?)", (zutat_id,))
            zutat_name = c.fetchone()
            if change:
                zutat_eintrag = str(zutat_name[0]) + ":" + zutat_menge
            else:
                zutat_eintrag = zutat_menge + " " + str(zutat_name[0])
            zutaten_return.append(zutat_eintrag)
        return zutaten_return

    def get_rezeptdaten_kategorien(self, rezid):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("Select FK_kategorie from rezept_kategorie where FK_rezept = (?) ", (rezid,))
        kat_ids = c.fetchall()
        kategorie_namen = ""
        for katid in kat_ids:
            c.execute("select name from kategorie where id = (?)", (katid[0],))
            kategorie_n = c.fetchone()
            kategorie_namen += " " + kategorie_n[0]
        return kategorie_namen

    def get_rezepte(self, kategorie=''):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        rezepte_return = []
        if kategorie == '':
            c.execute("Select name from rezept;")
            rezepte_return = c.fetchall()
        else:
            c.execute("Select id from kategorie where name = (?);", (kategorie,))
            kat_id = c.fetchone()
            c.execute("Select FK_rezept from rezept_kategorie where FK_kategorie = (?);", (kat_id[0],))
            rez_id = c.fetchall()
            if len(rez_id) > 0:
                for id_rez in rez_id:
                    c.execute("select name from rezept where id = (?);", (id_rez[0],))
                    rezeptname = c.fetchone()
                    rezepte_return.append(rezeptname)
            else:
                pass
        if len(rezepte_return) == 0:
            rezepte_return = [('Keine Rezepte gefunden', "")]
        con.close()
        return rezepte_return

    def get_einheiten(self):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("Select name from einheiten")
        einheiten_return = c.fetchall()
        return einheiten_return

    def get_zukat(self):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("select name from zutaten_kategorie;")
        zukaten = c.fetchall()
        return zukaten


    def get_zutaten(self, zukat=''):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("select id from zutaten_kategorie where name = (?);", (zukat,))
        zukat_id = c.fetchone()
        c.execute("Select name from zutaten where FK_zukat_id = (?);", (zukat_id[0],))
        zutaten_return = c.fetchall()
        return zutaten_return

    def create_zutat(self, zuname, zukat):
        if zuname.strip() == '' or zukat.strip() == '':
            return 1
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute(" select count(*) from zutaten where lower(name) = lower(?);", (zuname,))
        vorhanden = c.fetchall()
        if vorhanden[0][0] > 0:
            return 2
        c.execute("select id from zutaten_kategorie where name = (?)", (zukat,))
        kat_id = c.fetchone()
        c.execute("insert into zutaten (name,FK_zukat_id) VALUES (?,?);", (zuname, kat_id[0]))
        con.commit()
        con.close()
        return 0

    def change_zukat(self, zuname, zukat):
        if zuname.strip() == '' or zukat.strip() == '':
            return 1
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("select id from zutaten_kategorie where name = (?);", (zukat,))
        zukat_id = c.fetchone()
        c.execute("Update zutaten set FK_zukat_id = (?) where name = (?);", (zukat_id[0], zuname))
        con.commit()
        con.close()
        return 0

    def zutat_newname(self, zuname, zuname_neu):
        if zuname.strip() == '' or zuname_neu.strip() == '':
            return 1
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        try:
            c.execute("update zutaten set name= (?) where lower(name) = lower((?))", (zuname_neu, zuname))
            con.commit()
            con.close()
            return 0
        except:
            return 2

    def saverezept(self, kategorie_liste, beschreibung, zutaten, rezeptname):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("select count(*) from rezept where name = (?);", (rezeptname,))
        rezepte = c.fetchone()
        c.execute("select * from kategorie;")
        if rezepte[0] == 0:
            try:
                c.execute("insert into rezept (name) values (?);", (rezeptname,))
                c.execute("select id from rezept where name = (?);", (rezeptname,))
                rezept_id = c.fetchone()
                c.execute("insert into beschreibung (text,FK_Rezept) values (?,?);", (beschreibung, rezept_id[0]))
                for zutat in zutaten.keys():
                    c.execute("select id from zutaten where name=(?);", (zutat,))
                    zutat_id = c.fetchone()
                    c.execute("insert into rezept_zutaten (FK_zutat,menge,FK_rezept) Values (?,?,?);",
                              (zutat_id[0], zutaten[zutat], rezept_id[0]))
                for kategorie in kategorie_liste:
                    c.execute("select id from kategorie where name = (?)", (kategorie,))
                    kategorie_id = c.fetchone()
                    c.execute("insert into rezept_kategorie (FK_rezept,FK_Kategorie) Values (?,?);",
                              (rezept_id[0], kategorie_id[0]))
                con.commit()
                return 0
            except:
                return 1
        else:
            return "Rezept bereits in Datenbank eingetragen"

    def get_rezeptid(self, rname):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("select id from rezept where name = (?);", (rname,))
        rid = c.fetchone()
        return rid

    def changerezept(self, kategorie_liste, beschreibung, zutaten, rezeptname, alte_rezeptid):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("Delete from rezept_zutaten where FK_rezept = (?);", (alte_rezeptid,))
        c.execute("Delete from rezept_kategorie where FK_rezept = (?);", (alte_rezeptid,))
        c.execute("Delete from beschreibung where FK_rezept = (?);", (alte_rezeptid,))
        try:
            c.execute("Update rezept set name = (?) where id = (?);", (rezeptname, alte_rezeptid))
            c.execute("insert into beschreibung (text,FK_Rezept) values (?,?);", (beschreibung, alte_rezeptid))
            for zutat in zutaten.keys():
                c.execute("select id from zutaten where name=(?);", (zutat,))
                zutat_id = c.fetchone()
                c.execute("insert into rezept_zutaten (FK_zutat,menge,FK_rezept) Values (?,?,?);",
                          (zutat_id[0], zutaten[zutat], alte_rezeptid))
            for kategorie in kategorie_liste:
                c.execute("select id from kategorie where name = (?)", (kategorie,))
                kategorie_id = c.fetchone()
                c.execute("insert into rezept_kategorie (FK_rezept,FK_Kategorie) Values (?,?);",
                          (alte_rezeptid, kategorie_id[0]))
            con.commit()
            return 0
        except:
            return 1

    def delete_rezept(self, rezeptname):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("select id from rezept where name = (?);", (rezeptname,))
        rezept_id = c.fetchone()
        c.execute("Delete from rezept_zutaten where FK_rezept = (?);", (rezept_id[0],))
        c.execute("Delete from rezept_kategorie where FK_rezept = (?);", (rezept_id[0],))
        c.execute("Delete from beschreibung where FK_rezept = (?);", (rezept_id[0],))
        c.execute("Delete from rezept where id = (?);", (rezept_id[0],))
        con.commit()
        return 0

    def create_kategorie(self, katname=''):
        if katname == '':
            return 1
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("Select count(*) from kategorie where lower(name)= lower(?);", (katname,))
        vorhanden = c.fetchone()
        if vorhanden[0] > 0:
            return 2
        c.execute("insert into kategorie (name) values (?);", (katname,))
        con.commit()
        con.close()
        return 0

    def delete_kategorie(self, katliste):
        if len(katliste) == 0:
            return 1
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        kat_liste = []
        kat_liste_deleted = []
        for kategorie in katliste:
            c.execute("select id from kategorie where name = (?)", (kategorie,))
            kat_id = c.fetchone()
            c.execute("Select count(*) from rezept_kategorie where FK_kategorie = (?);", (kat_id[0],))
            kat_vergeben = c.fetchone()
            if kat_vergeben[0] > 0:
                kat_liste.append(kategorie)
            else:
                c.execute("delete from kategorie where id = (?);", (kat_id[0],))
                con.commit()
                kat_liste_deleted.append(kategorie)
        con.close()
        return [kat_liste, kat_liste_deleted]

    def create_zukat(self, katname=''):
        if katname == '':
            return 1
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute("Select count(*) from zutaten_kategorie where lower(name)= lower(?);", (katname,))
        vorhanden = c.fetchone()
        if vorhanden[0] > 0:
            return 2
        c.execute("insert into zutaten_kategorie (name) values (?);", (katname,))
        con.commit()
        con.close()
        return 0

    def delete_zukat(self, katliste):
        if len(katliste) == 0:
            return 1
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        kat_liste = []
        kat_liste_deleted = []
        for kategorie in katliste:
            c.execute("select id from zutaten_kategorie where name = (?)", (kategorie,))
            kat_id = c.fetchone()
            c.execute("Select count(*) from zutaten where FK_zukat_id = (?);", (kat_id[0],))
            kat_vergeben = c.fetchone()
            if kat_vergeben[0] > 0:
                kat_liste.append(kategorie)
            else:
                c.execute("delete from zutaten_kategorie where id = (?);", (kat_id[0],))
                con.commit()
                kat_liste_deleted.append(kategorie)
        con.close()
        return [kat_liste, kat_liste_deleted]


class create_database():
    def __init__(self):
        self.db_name = os.path.join("data", 'rezepte.db')

    def create_new(self):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()
        c.execute('''PRAGMA foreign_keys = ON;''')
        c.execute('''Create table zutaten_kategorie (\
            id INTEGER PRIMARY KEY,\
            name varchar(30))\
            ;''')
        c.execute('''Create table zutaten (\
            id INTEGER PRIMARY KEY ASC,\
            name varchar(50),\
            FK_zukat_id int,\
            FOREIGN KEY(FK_zukat_id) REFERENCES zutaten_kategorie(id))\
            ;''')
        c.execute('''Create table beschreibung (\
            id INTEGER PRIMARY KEY ASC,\
            FK_Rezept int,\
            text text,\
            FOREIGN KEY(FK_rezept) REFERENCES rezept(id))\
            ; ''')
        c.execute('''Create table kategorie (\
            id INTEGER PRIMARY KEY ASC,\
            name varchar(100))\
            ; ''')
        c.execute('''Create table rezept (\
            id INTEGER PRIMARY KEY ASC,\
            name varchar(100))\
            ;''')
        c.execute('''Create table rezept_kategorie (\
            FK_rezept int,\
             FK_kategorie int,\
             FOREIGN KEY(FK_kategorie) REFERENCES kategorie(id),\
             FOREIGN KEY(FK_rezept) REFERENCES rezept(id))\
             ;''')
        c.execute('''Create table rezept_zutaten (\
            id INTEGER PRIMARY KEY ASC,\
            FK_zutat int,\
            menge varchar(20),\
            FK_rezept int,\
            FOREIGN KEY(FK_zutat) REFERENCES zutat(id),\
            FOREIGN KEY(FK_rezept) REFERENCES rezept(id))\
            ;''')

        con.commit()
        con.close()
        return True

    def yield_list(self, liste):
        for data in liste:
            yield (data,)

    def insert_initial(self):
        con = sqlite3.connect(self.db_name)
        c = con.cursor()

        # Eintrag in die Zutaten und Zutaten_Kategorien
        initial_zutaten = collections.defaultdict(list, (
            ('Gewürze',
             ['Salz', 'Pfeffer(Schwarz)', 'Zucker', 'Curry', 'Oregano', 'Majoran', 'Pfeffer(Weiss)', 'Paprika(Scharf)',
              'Paprika(Mild)', 'Knoblauch(Pulver)', 'Zimt', 'Basilikum']),
            ('Fleisch',
             ['Schweinerücken', 'Geflügelbrust', 'Rumpsteak', 'Schweinefilet']),
            ('Gemüse',
             ['Kartoffeln', 'Paprika', 'Tomate(n)', 'Gurke(n)', 'Zucchini(s)', 'Radieschen', 'Zwiebel(n)',
              'Karrotte(n)']),
            ('Obst',
             ['Kirschen', 'Ananas', 'Äpfel', 'Orangen', 'Zitronen', 'Himbeeren', 'Heidelbeeren', 'Johannisbeeren',
              'Bananen']),
            ('Beilagen',
             ['Basmatireis', 'Wildreis', 'Jasminreis', 'Kartoffelpüree', 'Klöße', 'Knödel', 'Vollkornbrot']),
            ('Milchprodukte',
             ['Milch', 'Magerjoghurt', 'Frischkäse(Magerstufe)', 'Frischkäse(Doppelrahmstufe)', 'Magerquark',
              'Schlagsahne', 'Saure Sahne', 'Creme fraiche', 'Margarine', 'Butter', 'Schokolade']),
            ('Sonstiges',
             ['Mehl', 'Eier', 'Olivenöl', 'Rapsöl', 'Haselnüsse', 'Walnüsse', 'Champignons', 'Wasser']),
            ('Fisch',
             ['Pangasiusfilet', 'Heringsfilet', 'Lachsfilet', 'Rollmops', 'Schollenfilet', 'Garnele(n)', 'Shrimps'])
        )
        )
        for zukat in initial_zutaten.keys():
            c.execute("Insert into zutaten_kategorie (name) VALUES (?);", (zukat,))
            con.commit()
            c.execute("Select id from zutaten_kategorie where name = (?);", (zukat,))
            zukat_id = c.fetchone()
            for zutat in initial_zutaten[zukat]:
                c.execute("insert into zutaten (name,FK_zukat_id) VALUES (?,?);", (zutat, zukat_id[0]))
            con.commit()
        # Eintrag in Kategorie
        initial_kategorie = ['Frühstück', 'Mittag', 'Abendessen', 'Snack', 'Rind', 'Schwein', 'Fisch', 'Aperitif',
                             'Cocktails', 'Digestif', 'Gebäck', 'Getränk', 'Vorspeisen', 'Dessert', 'Liköre']
        c.executemany("insert into kategorie (name) values (?)", self.yield_list(initial_kategorie))

        con.commit()
        con.close()
        return True