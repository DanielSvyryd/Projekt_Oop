from datetime import datetime, timedelta
from enum import Enum
from abc import ABC, abstractmethod


class TypUzytkownika(Enum):
    STUDENT = 1
    PRACOWNIK_NAUKOWY = 2
    PRACOWNIK_ADMINISTRACYJNY = 3

class Status(Enum):
    DOSTEPNA = 1
    WYPOZYCZONA = 2
    ZAREZERWOWANA = 3
    W_TRAKCIE_NAPRAWY = 4

class Kategoria(Enum):
    INFORMATYKA = 1
    MATEMATYKA = 2
    LITERATURA = 3
    NAUKI_SPOLECZNE = 4

class Osoba(ABC):
    def __init__(self, id, imie, nazwisko, email=None):
        self.id = id
        self.imie = imie
        self.nazwisko = nazwisko
        self.email = email
    
    @abstractmethod
    def przedstaw_sie(self):
        pass

class Uzytkownik(Osoba):
    def __init__(self, id, imie, nazwisko, email, numer_indeksu, typ):
        super().__init__(id, email, imie, nazwisko)
        self.numerIndeksu = numer_indeksu
        self.dataRejestracji = datetime.now()
        self.typ = typ
        self.wypozyczenia = []

    def przedstaw_sie(self):
        return f"Użytkownik: {self.imie} {self.nazwisko}, typ: {self.typ.name}"
        
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
    def __init__(self, id, tytul, autor, isbn, rok_wydania, wydawnictwo, kategoria):
        self.id = id
        self.tytul = tytul
        self.autor = autor
        self.isbn = isbn
        self.rokWydania = rok_wydania
        self.wydawnictwo = wydawnictwo
        self.kategoria = kategoria
        self.status = Status.DOSTEPNA
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
        
    def przedluzTermin(self, dni):
        if self.dataZwrotu is not None:
            raise Exception("Nie można przedłużyć już zwróconego wypożyczenia")
        self.terminZwrotu += timedelta(days=dni)
        return self.terminZwrotu
        
    def obliczKare(self):
        if self.dataZwrotu is None and datetime.now() > self.terminZwrotu:
            self.czyPrzetrzymane = True
            return (datetime.now() - self.terminZwrotu).days * 0.50
        return 0
    
    def zwroc(self):
        self.dataZwrotu = datetime.now()
        self.ksiazka.zmienStatus(Status.DOSTEPNA)
        return self.obliczKare()

class Rezerwacja:
    def __init__(self, id, uzytkownik, ksiazka):
        self.id = id
        self.uzytkownik = uzytkownik
        self.ksiazka = ksiazka
        self.dataRezerwacji = datetime.now()
        self.dataWygasniecia = self.dataRezerwacji + timedelta(days=7)
        ksiazka.zmienStatus(Status.ZAREZERWOWANA)
        
    def anuluj(self):
        self.ksiazka.zmienStatus(Status.DOSTEPNA)
        Biblioteka.usun_rezerwacje(self)

class Bibliotekarz(Osoba):
    def __init__(self, id, imie, nazwisko, login, haslo):
        super().__init__(id, imie, nazwisko)
        self.login = login
        self.haslo = haslo

    def przedstaw_sie(self):
        return f"Bibliotekarz: {self.imie} {self.nazwisko}"
        
    def dodajKsiazke(self, ksiazka):
        Biblioteka.dodaj_ksiazke(ksiazka)
        
    def usunKsiazke(self, ksiazka):
        Biblioteka.usun_ksiazke(ksiazka)
        
    def zatwierdzWypozyczenie(self, wypozyczenie):
        Biblioteka.dodaj_wypozyczenie(wypozyczenie)
        
    def zatwierdzZwrot(self, wypozyczenie):
        kara = wypozyczenie.zwroc()
        if kara > 0:
            print(f"Naliczona kara: {kara:.2f} zł")
        Biblioteka.usun_wypozyczenie(wypozyczenie)
        return kara


class Biblioteka:
    _instance = None
    uzytkownicy = []
    ksiazki = []
    wypozyczenia = []
    rezerwacje = []
    bibliotekarze = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Biblioteka, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def dodaj_uzytkownika(cls, uzytkownik):
        cls.uzytkownicy.append(uzytkownik)
        
    @classmethod
    def dodaj_ksiazke(cls, ksiazka):
        cls.ksiazki.append(ksiazka)
        
    @classmethod
    def dodaj_wypozyczenie(cls, wypozyczenie):
        cls.wypozyczenia.append(wypozyczenie)
        
    @classmethod
    def dodaj_rezerwacje(cls, rezerwacja):
        cls.rezerwacje.append(rezerwacja)
        
    @classmethod
    def usun_ksiazke(cls, ksiazka):
        cls.ksiazki.remove(ksiazka)
        
    @classmethod
    def usun_wypozyczenie(cls, wypozyczenie):
        cls.wypozyczenia.remove(wypozyczenie)
        
    @classmethod
    def usun_rezerwacje(cls, rezerwacja):
        cls.rezerwacje.remove(rezerwacja)
        
    @classmethod
    def znajdz_ksiazke_po_tytule(cls, tytul):
        return [k for k in cls.ksiazki if tytul.lower() in k.tytul.lower()]
    
    @classmethod
    def znajdz_uzytkownika_po_nazwisku(cls, nazwisko):
        return [u for u in cls.uzytkownicy if nazwisko.lower() in u.nazwisko.lower()]


if __name__ == "__main__":

    biblioteka = Biblioteka()


    bibliotekarz = Bibliotekarz(1, "Anna", "Nowak", "anowak", "haslo123")
    biblioteka.bibliotekarze.append(bibliotekarz)


    u1 = Uzytkownik(1, "Jan", "Kowalski", "jan.kowalski@student.uw.edu.pl", "123456", TypUzytkownika.STUDENT)
    u2 = Uzytkownik(2, "Adam", "Nowak", "adam.nowak@uw.edu.pl", "654321", TypUzytkownika.PRACOWNIK_NAUKOWY)
    u3 = Uzytkownik(3, "Maria", "Wiśniewska", "maria.wisniewska@student.uw.edu.pl", "111222", TypUzytkownika.STUDENT)
    u4 = Uzytkownik(4, "Piotr", "Zieliński", "piotr.zielinski@student.uw.edu.pl", "333444", TypUzytkownika.STUDENT)
    u5 = Uzytkownik(5, "Ewa", "Dąbrowska", "ewa.dabrowska@uw.edu.pl", "555666", TypUzytkownika.PRACOWNIK_ADMINISTRACYJNY)
    u6 = Uzytkownik(6, "Tomasz", "Lewandowski", "t.lewandowski@uw.edu.pl", "777888", TypUzytkownika.PRACOWNIK_NAUKOWY)

    for u in [u1, u2, u3, u4, u5, u6]:
        biblioteka.dodaj_uzytkownika(u)

   
    ks1 = Ksiazka(1, "Wzorce projektowe", "Erich Gamma", "978-83-283-0234-1", 2010, "Helion", Kategoria.INFORMATYKA)
    ks2 = Ksiazka(2, "Python dla każdego", "Michael Dawson", "978-83-283-5067-0", 2018, "Helion", Kategoria.INFORMATYKA)
    ks3 = Ksiazka(3, "Statystyka stosowana", "Jan Nowak", "978-83-123-4567-0", 2015, "PWN", Kategoria.MATEMATYKA)
    ks4 = Ksiazka(4, "Duma i uprzedzenie", "Jane Austen", "978-83-456-7890-1", 2001, "Znak", Kategoria.LITERATURA)
    ks5 = Ksiazka(5, "Socjologia na co dzień", "Zofia Kowalska", "978-83-222-3333-2", 2020, "Uniwersytet", Kategoria.NAUKI_SPOLECZNE)
    ks6 = Ksiazka(6, "Algorytmy", "Thomas Cormen", "978-83-876-1200-1", 2012, "MIT Press", Kategoria.INFORMATYKA)

    for ks in [ks1, ks2, ks3, ks4, ks5, ks6]:
        biblioteka.dodaj_ksiazke(ks)

 
    wyp1 = Wypozyczenie(1, u1, ks1)  
    bibliotekarz.zatwierdzWypozyczenie(wyp1)

    wyp2 = Wypozyczenie(2, u3, ks3)  
    bibliotekarz.zatwierdzWypozyczenie(wyp2)


    rezerwacja1 = u2.zarezerwuj(ks2)  
    rezerwacja2 = u5.zarezerwuj(ks4) 


    print("\n Raport książek:")
    for k in biblioteka.ksiazki:
        status = k.status.name
        print(f"• {k.tytul} – {status}")


    print("\n Użytkownicy:")
    for u in biblioteka.uzytkownicy:
        print(f"{u.imie} {u.nazwisko} – {u.typ.name}")
