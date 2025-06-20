# 💡 Akari Solver (Light Up)

**Akari Solver** to rozbudowany system rozwiązywania japońskiej łamigłówki logicznej Akari (znanej także jako Light Up). Projekt obsługuje wiele podejść algorytmicznych – od brute-force po metaheurystyki takie jak symulowane wyżarzanie, algorytmy genetyczne i strategie ewolucyjne.

---

## 📜 Zasady gry Akari

- Gra rozgrywa się na prostokątnej planszy składającej się z białych i czarnych pól.
- Czarne pola mogą zawierać liczby od 0 do 4, oznaczające **liczbę żarówek** w sąsiednich komórkach (góra, dół, lewo, prawo).
- Żarówka oświetla wszystkie pola w swoim wierszu i kolumnie aż do napotkania ściany (czarne pole).
- Żadne dwie żarówki **nie mogą się wzajemnie oświetlać**.
- Wszystkie białe pola muszą być oświetlone.

---

## 🧠 Implementowane algorytmy

Znajdują się w katalogu `solvers/`:

- `brute_force.py` – przeszukiwanie pełne
- `hill_climb.py` – wspinaczka górska
- `tabu.py` – tabu search
- `simulated_annealing.py` – symulowane wyżarzanie
- `genetic.py` – algorytm genetyczny
- `island_ga.py` – algorytm wyspowy (wiele populacji)
- `evolutionary_strategy.py` – strategia ewolucyjna

---
