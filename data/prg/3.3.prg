// Obliczanie warto�ci wyznacznika macierzy 2 x 2 przy wykorzystaniu podprogramu mno�enia
// a11 * a22 - a12 * a21
start:  pob a12	// a12 * a21
        dns
        pob a21
        dns
        sdp mnoz
        �ad s
        pob a11	// a11 * a22
        dns
        pob a22
        dns
        sdp mnoz
        ode s	// a11 * a22 - a12 * a21
        �ad s
        stp        
a11:    rst 5	// elementy macierzy a
a12:    rst 4
a21:    rst 1
a22:    rst 2
s:      rst 0	// zmienna pomocnicza
// mno�enie liczb ca�kowitych x i y
// liczby przekazane przez stos, wynik zwracany w akumulatorze
mnoz:   pzs
        �ad �lad
        pzs
        �ad y
        som neg
        pzs
        �ad x
        sob next
neg:    pob zero 	// je�li mno�nik ujemny - zamie� znaki argument�w
        ode y
        �ad y
        pzs
        �ad x
        pob zero
        ode x
        �ad x         
next:   pob �lad	// �lad od razu na stos aby potem nie zapomnie�
        dns
        pob zero
        �ad wynik
petla:  pob y	// dekrementacja mno�nika
        ode jeden
        �ad y
        som ready	// gdy mno�nik ujemny - koniec
        pob wynik	// mno�enie przez wielokrotne dodawanie mno�nej x
        dod x
        �ad wynik
        sob petla
ready:  pob wynik
        pwr
�lad:   rpa	// miejsce na �lad
x:      rpa		// mno�na
y:      rpa		// mno�nik
wynik:  rpa	// wynik musi by� zainicjowany w kodzie warto�ci� 0
zero:   rst 0
jeden:  rst 1