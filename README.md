# Analiza koszyka: reguły asocjacyjne (EconoShop Express)

Eksploracja danych, laboratorium 6. Dane syntetyczne: 7 968 paragonów sklepu osiedlowego z września i października 2026 r. (`dane/paragony.csv`, jeden wiersz = jeden produkt na paragonie).

| Plik | Co to jest |
|---|---|
| `koszyk.py` | funkcje: macierz koszyków, wsparcie, pewność, lift, Apriori, scenariusz zysku (TODO 1–3 uzupełnione) |
| `tests/test_koszyk.py` | testy (`pytest -q`); oczekiwany wynik po uzupełnieniu: `7 passed` |
| `lab6_student.ipynb` | notatnik z zadaniami Z1–Z6 |
| `app.py` | dashboard Streamlit |
| `render.yaml` | wdrożenie na Render |
| `.devcontainer/` | konfiguracja GitHub Codespaces (Python 3.13 i biblioteki instalują się same) |
| `.github/workflows/testy.yml` | testy na GitHubie po każdym push |

## 1. Praca w GitHub Codespaces

1. **Code → Codespaces → Create codespace on main**; poczekaj na koniec instalacji.
2. W terminalu: `pytest -q` (funkcje TODO 1–3 są już uzupełnione; cel: `7 passed`).
3. Otwórz `lab6_student.ipynb` → **Select Kernel → Python 3.13** → uruchamiaj komórki po kolei (Shift + Enter).
4. `streamlit run app.py` → **Open in Browser** (albo zakładka PORTS → 8501).

W lokalnym JupyterLab można wykonać ten sam projekt z katalogu głównego: `pytest -q`, następnie otworzyć `lab6_student.ipynb` i wybrać **Restart Kernel and Run All Cells**. W razie braku bibliotek uruchomić `python -m pip install -r requirements.txt`.

## 2. Zapis zmian

Panel **Source Control** → opis → **Commit** → **Sync Changes** (albo `git add .`, `git commit -m "..."`, `git push`). Zakładka **Actions**: zielony znaczek = testy przechodzą.

## 3. Render

**New → Blueprint** → **Connect** przy tym repozytorium → **Deploy Blueprint**. Ręcznie: **New → Web Service**, Build `pip install -r requirements.txt`, Start `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`, zmienna `PYTHON_VERSION` = `3.13.5`. Usługa Free usypia po 15 min bez ruchu.

## 4. Rekomendacja dla kierownika sklepu

W danych z 7 968 paragonów reguła **makaron → sos pomidorowy** występuje na **207 paragonach**, ma pewność **31,2%** i lift **5,97**, dlatego proponuję przetestować ustawienie sosu obok makaronu bez rabatu.  
Druga reguła to **pieluchy → chusteczki nawilżane**: **108 wspólnych paragonów**, pewność **30,7%** i lift **6,33**, więc warto sprawdzić ekspozycję chusteczek w sąsiedztwie pieluch.  
Nie polecam promocji opartej wyłącznie na regule **mleko → chleb**, mimo **1 144 wspólnych paragonów** i pewności **39,9%**, ponieważ lift wynosi zaledwie **1,07**, a chleb jest po prostu popularny.  
W przypadku makaronu i sosu bezrabata ekspozycja daje w przyjętym scenariuszu **+47,99 zł** marży w dwa miesiące, podczas gdy rabat 20% dawałby **−273,80 zł**.  
Wyniki te wynikają z przyjętej konwersji 5%, marży 2,10 zł i rabatu 1,40 zł, dlatego nie oznaczają potwierdzonego skutku zmiany półki.  
Proponuję przez **4 tygodnie** przeprowadzić test A/B: w losowo wybranej połowie porównywalnych sklepów zmienić ekspozycję, a w drugiej pozostawić ją bez zmian.  
Porównamy sprzedaż sosu na 100 paragonów z makaronem oraz marżę między grupami i zdecydujemy o dalszym wdrożeniu dopiero po teście.

**Adres aplikacji Render:** https://analiza-koszyka-0v8p.onrender.com