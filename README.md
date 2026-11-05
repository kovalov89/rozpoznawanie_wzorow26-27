# Szybkie grupowanie opisów binarnych metodą CLASSIX

Projekt indywidualny realizowany w ramach przedmiotu **Rozpoznawanie wzorców**, grupa 2, na Politechnice Opolskiej.

**Autor:** Ivan Kovalov  
**Pytanie badawcze:** Jak zmieniają się koszt i jakość grupowania opisów binarnych wraz z liczbą obiektów oraz rozmyciem grup?

## Cel projektu

Celem jest porównanie CLASSIX w wariancie wykorzystującym odległość Tanimoto (CLASSIX_T) z algorytmem DBSCAN. Badanie będzie prowadzone na syntetycznych wektorach binarnych. Analizowane będą czas wykonania, Adjusted Rand Index (ARI), liczba wykrytych klastrów oraz udział szumu.

## Struktura repozytorium

```text
rozpoznawanie_wzorow26-27/
├── README.md
├── requirements.txt
├── .gitignore
├── protokol_CLASSIX.pdf
├── generate_demo_data.py
├── demo_small.csv
└── notebooks/
    ├── przykladowy_zbior_danych_binarnych.ipynb
    └── przykladowy_zbior_danych_binarnych_colab.pdf
```

- [Protokół projektu (PDF)](protokol_CLASSIX.pdf)
- [Kod Google Colab (notebook)](notebooks/przykladowy_zbior_danych_binarnych.ipynb)
- [Wydruk notebooka (PDF)](notebooks/przykladowy_zbior_danych_binarnych_colab.pdf)

Notebook został odtworzony z wydruku PDF przesłanego z Google Colab; nie jest oryginalnym eksportem `.ipynb`.

## Mały zbiór demonstracyjny

Zbiór demonstracyjny ma 3 klastry, 16 cech i 18 obiektów (po jednym wektorze bazowym i pięć obiektów pochodnych na klaster). Generator wykorzystuje ziarno losowości 42.

Dla wektora bazowego klastra `x_i` prawdopodobieństwo odwrócenia każdego bitu wynosi:

\[
p_i = 0.1 \cdot \frac{\|x_i\|_1}{d},
\]

gdzie `d` jest liczbą cech, a `||x_i||_1` liczbą jedynek w wektorze bazowym. Każdy obiekt pochodny powstaje przez niezależne odwrócenie bitów z prawdopodobieństwem `p_i` (operacja XOR).

Jest to mała demonstracja generatora, a nie pełne odtworzenie eksperymentu z publikacji. W eksperymencie głównym planowane są zbiory 400, 800 i 1600 obiektów oraz 256 cech.

## Uruchomienie generatora

Wymagany jest Python 3.10+ i NumPy.

```bash
pip install -r requirements.txt
python generate_demo_data.py
```

Domyślne ustawienia tworzą plik `demo_small.csv`. Parametry można zmienić, np.:

```bash
python generate_demo_data.py --clusters 3 --features 16 --objects-per-cluster 6 --seed 42
```

Kolumna `cluster_label` zawiera etykietę używaną wyłącznie do oceny jakości grupowania (np. ARI), a nie jako wejście algorytmów.

## Plan eksperymentów

- liczba obiektów: 400, 800 i 1600;
- liczba cech: 256;
- liczba klastrów: 10;
- pięć losowań z ustalonymi ziarnami generatora;
- eksperyment własny dla 800 obiektów z trzema poziomami rozmycia: `0.5 * p`, `1.0 * p`, `2.0 * p`;
- porównanie CLASSIX_T i DBSCAN przy odległości Tanimoto i ustalonych parametrach.

## Źródła

- S. Güttel, K. Roy, *Fast and explainable clustering in the Manhattan and Tanimoto distance*, arXiv:2601.08781 (2026): https://arxiv.org/abs/2601.08781
- Implementacja autorów: https://github.com/kaustubhroy1995/classix_tanimoto_manhattan
