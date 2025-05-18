from datetime import datetime, timedelta
from enum import Enum


class TypUzytkownica(Enum):
    STUDENT = 1
    PRACOWNIK_NAUKOWCY = 2
    PRACOWNIK_ADMINISTRACYJNY = 3

class Status(Enum):
    DOSTEPA = 1
    WYPOZYCZONA = 2
    ZAREZERWOWANA = 3
    W_TRAKCIE_NAPRAWY = 4

class Kategoria(Enum):
    INFORMATIKA = 1
    MATEMATYKA = 2
    LITERATURA = 3
    NAUKI_SPOLECZNE = 4

class Uzytkownic:
    def __init__(self, id, imie, nazwisko, email, numer_indeksu, typ):
        self.id = id 
        self.imie = imie
        self.nazwisko = nazwisko
        self.email = email
        self.numerIndeksu = numer_indeksu
        self.dataRejestracji = datetime.now()
        self.typ = typ
        self.wypozyczenia = []
    
    
    
class Ksiazka:
    def __init__(self, id, tytul, autor, rok_wydania, wydawnictwo, kategoria):
        self.id = id
        self.tytul = tytul
        self.autor = autor
        self.rokWydania = rok_wydania
        self.wydawnictwo = wydawnictwo
        self.kategoria = kategoria
        self.status = Status.DOSTEPA
        self.dataDostepnosci = None
