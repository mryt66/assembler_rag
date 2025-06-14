// Sprawdzanie czy dana liczba n jest liczb� pierwsz� z wykorzystaniem podprogramu reszty z dzielenia
// zwraca -1 gdy liczba pierwsza
// 0 - je�li nie
         pob d	// dop�ki d < n powtarzaj
start:  ode n
        som test	// d >= n zatem liczba pierwsza
        pob minus1
        stp
test:   pob n	// oblicza n % d
        dns
        pob d
        dns
        sdp mod
        soz nie	// je�li n % d == 0 => liczba n nie jest pierwsza
        pob d	// je�li n % d > 0 sprawdzaj dla kolejnego dzielnika d
        dod jeden
        �ad d
        sob start
nie:    stp        
d:      rst 2	// sprawdzanie zaczynamy od podzielnika 2
n:      rst 7	// sprawdzana liczba
jeden:  rst 1
// obliczanie reszty z dzielenia liczb naturalnych x % y
// liczby przekazane przez stos, wynik zwracany w akumulatorze
// gdy y < 1 zwraca -1
// gdy x < 0 zwraca -1
mod:    pzs
        �ad �lad
        pzs
        �ad y
        som negy
        soz negy
        pzs
        som negx
znowu:  ode y	// powtarza odejmowanie a� w akumulatorze b�dzie liczba ujemna
        som jest
        sob znowu
jest:   dod y	// aby znale�� reszt� trzeba doda� dzielnik
        �ad x	// reszta znaleziona
        pob �lad	// nie wolno zapomnie� o �ladzie
        dns
        pob x
        pwr
negy:   pzs   	// koniecznie pobierz x ze stosu
negx:   pob �lad	// teraz zapisz tam �lad
        dns
        pob minus1	// wynikiem jest -1
        pwr
�lad:   rpa
x:      rpa
y:      rpa
minus1: rst -1