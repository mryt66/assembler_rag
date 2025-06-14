// Pot�gowanie a^b z wykorzystaniem podprogramu mno�enia
start:  pob b	// je�li wyk�adnik r�wny 0 - nic nie trzeba robi�
        ode jeden
        som jest
        �ad b	// w ka�dym przebiegu p�tli wyk�adnik jest zmniejszany
        pob a	// mno�enie podstawy przez dotychczasowy wynik
        dns
        pob s
        dns
        sdp mnoz
        �ad s
        sob start	// powtarzamy a� wyk�adnik r�wny 0
jest:   pob s	// wynik znaleziony
        stp
a:      rst 5	// podstawa
b:      rst 3	// wyk�adnik
s:      rst 1	// wynik zainicjowany warto�ci� 1
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