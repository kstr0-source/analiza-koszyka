"""SZKIELET DLA STUDENTÓW: uzupełnij TODO 1–3 (pytest -q pokaże, co jeszcze nie działa).

Analiza koszyka: reguły asocjacyjne dla paragonów sklepu (zajęcia 6, eksploracja danych).

Słowniczek: wsparcie (support) = jaka część paragonów zawiera dane produkty;
pewność (confidence) reguły A → B = jaka część paragonów z A zawiera też B;
lift = pewność / wsparcie(B): ile razy częściej B pojawia się przy A niż przeciętnie (1 = brak związku).
"""
from __future__ import annotations

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


def wczytaj(sciezka: str) -> pd.DataFrame:
    """Paragony w formacie długim: jeden wiersz = jeden produkt na paragonie."""
    return pd.read_csv(sciezka, parse_dates=["data"])


def macierz_koszykow(df: pd.DataFrame) -> pd.DataFrame:
    """Tabela paragon × produkt: True, gdy produkt jest na paragonie."""
    return pd.crosstab(df["id_paragonu"], df["produkt"]).gt(0)


def _lista(x) -> list[str]:
    return [x] if isinstance(x, str) else list(x)


def wsparcie(K: pd.DataFrame, produkty) -> float:
    """Część paragonów, na których są wszystkie podane produkty."""
    return float(K[_lista(produkty)].all(axis=1).mean())


def pewnosc(K: pd.DataFrame, A, B) -> float:
    """Pewność reguły A → B."""
    return wsparcie(K, _lista(A) + _lista(B)) / wsparcie(K, A)


def lift(K: pd.DataFrame, A, B) -> float:
    """Lift reguły A → B."""
    return pewnosc(K, A, B) / wsparcie(K, B)


def liczba(K: pd.DataFrame, produkty) -> int:
    """Liczba paragonów ze wszystkimi podanymi produktami."""
    return int(K[_lista(produkty)].all(axis=1).sum())


def reguly(K: pd.DataFrame, min_wsparcie: float = 0.01, min_lift: float = 1.0, max_dlugosc: int = 3) -> pd.DataFrame:
    """Algorytm Apriori (biblioteka mlxtend): zbiory częste, potem reguły z lift >= min_lift.
    Zwraca czytelną tabelę posortowaną malejąco po lift."""
    czeste = apriori(K, min_support=min_wsparcie, use_colnames=True, max_len=max_dlugosc)
    if czeste.empty:
        return pd.DataFrame(columns=["poprzednik", "nastepnik", "wsparcie", "pewnosc", "lift", "paragony"])
    r = association_rules(czeste, metric="lift", min_threshold=min_lift)
    out = pd.DataFrame({
        "poprzednik": r["antecedents"].apply(lambda s: " + ".join(sorted(s))),
        "nastepnik": r["consequents"].apply(lambda s: " + ".join(sorted(s))),
        "wsparcie": r["support"], "pewnosc": r["confidence"], "lift": r["lift"],
        "paragony": (r["support"] * len(K)).round().astype(int),
    })
    return out.sort_values(["lift", "wsparcie"], ascending=False, ignore_index=True)


def potencjal(K: pd.DataFrame, A, B, konwersja: float, marza_zl: float) -> dict:
    """Scenariusz: ilu klientów z A (bez B) zobaczy ofertę B, ilu kupi (konwersja), ile zarobimy (marża na sztuce B).
    To górna, robocza ocena: czy warto testować. Nie mówi, czy oferta naprawdę zmienia zachowanie (do tego test A/B)."""
    z_A = K[_lista(A)].all(axis=1)
    bez_B = int((z_A & ~K[_lista(B)].all(axis=1)).sum())
    kupi = bez_B * konwersja
    return {"paragony_z_A_bez_B": bez_B, "dodatkowe_sztuki": kupi, "dodatkowa_marza_zl": kupi * marza_zl}
