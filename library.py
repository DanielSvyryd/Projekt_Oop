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
    
     def zarezerwuj(self, ksiazka):
        if ksiazka.status != Status.DOSTEPNA:
            raise Exception("Książka nie jest dostępna do rezerwacji")
        rezerwacja = Rezerwacja(len(Biblioteka.rezerwacje) + 1, self, ksiazka)
        Biblioteka.dodaj_rezerwacje(rezerwacja)
        return rezerwacja

        
    def przedluzTermin(self, wypozyczenie):
        if wypozyczenie.uzytkownik != self:
            raise Exception("Nie możesz przedłużyć nie swojego wypożyczenia")
        wypozyczenie.przedluzTermin(7)
        return wypozyczenie.terminZwrotu
    
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

  def zmienStatus(self, nowyStatus):
        self.status = nowyStatus
        if nowyStatus == Status.DOSTEPNA:
            self.dataDostepnosci = None
        elif nowyStatus == Status.WYPOZYCZONA:
            self.dataDostepnosci = datetime.now() + timedelta(days=30)
            
    def ustawDateDostepnosci(self, data):
        self.dataDostepnosci = data



class Wypozyczenie:
    def __init__(self, id, uzytkownik, ksiazka):
        self.id = id
        self.uzytkownik = uzytkownik
        self.ksiazka = ksiazka
        self.dataWypozyczenia = datetime.now()
        self.terminZwrotu = self.dataWypozyczenia + timedelta(days=30)
        self.dataZwrotu = None
        self.czyPrzetrzymane = False
        ksiazka.zmienStatus(Status.WYPOZYCZONA)
        uzytkownik.wypozyczenia.append(self)

class Rezerwacja:
    def __init__(self, id, uzytkownik, ksiazka):
        self.id = id
        self.uzytkownik = uzytkownik
        self.ksiazka = ksiazka
        self.dataRezerwacji = datetime.now()
        self.dataWygasniecia = self.dataRezerwacji + timedelta(days=7)
        ksiazka.zmienStatus(Status.ZAREZERWOWANA)
    

class Bibliotekarz:
    def __init__(self, id, imie, nazwisko, login, haslo):
        self.id = id
        self.imie = imie
        self.nazwisko = nazwisko
        self.login = login
        self.haslo = haslo

class Biblioteka:
    _instance = None
    uzytkownicy = []
    ksiazki = []
    wypozyczenia = []
    rezerwacje = []
    bibliotekarze = []
 
