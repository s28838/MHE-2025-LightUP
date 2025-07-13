### Uruchamianie za pomocą linii komend.
python compare.py --input board_5x5.txt
### Pobieranie parametrów z linii komend a nie z standardowego wejścia.
python main.py --method genetic --input board_6x6.txt --generations 5000 --pop_size 50
### Pobieranie danych (zadanie do rozwiązania) z pliku albo z standardowego wejścia.

## Implementacja problemu optymalizacyjnego (3)
Przygotuj swoją funkcję celu dla zadanego problemu.
Przygotuj metodę która będzie zwracała bliskie "sąsiedztwo" bieżącego rozwiązania.
Przygotuj funkcję która wygeneruje losowe rozwiązanie

## Algorytm pełnego przeglądu (1)
Zaimplementuj algorytm pełnego przeglądu. Prawdopodobnie będzie potrzebna metoda generowania kolejnych punktów z dziedziny rozwiązania w taki sposób, aby udało się przejść wszystkie.
 
## Algorytm wspinaczkowy (1)
Zaimplementuj algorytm wspinaczkowy. Zdecyduj się na wersję, albo przygotuj obie:
 klasyczny z deterministycznym wyborem najlepszego sąsiada punktu roboczego

## Algorytm genetyczny (4 + 1*)
Zaimplementuj GA dla Twojego zadania. Może być klasyczny, albo jako program ewolucyjny). Jest tu sporo elementów, dlatego dopuszczam częściowe rozwiązania i każde będę oceniał indywidualnie. Niech będzie:
(1) 2 metody krzyżowania
(1) 2 metody mutacji
(1) 2 warunki zakończenia
(1) Główna pętla algorytmu - cały działający algorytm
(*1) Elita

## Eksperyment porównujący metody (2)
Zaimplementuj skrypt (dowolny język) porównujący przynajmniej 2 metody rozwiązywania Twojego zadania. Im więcej metod sprawdzisz, tym więcej punktów będzie. Wnioski jakie powinieneś dać radę otrzymać to:
jaki zestaw parametrów daje najlepsze wyniki dla każdej metody
jaka metoda kończy się najszybciej (porównujemy dla najlepszych parametrów)