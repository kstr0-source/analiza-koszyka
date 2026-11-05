"""Testy funkcji z koszyk.py. Uruchomienie: pytest -q (w katalogu projektu)."""
import os, sys

import pandas as pd
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import koszyk as k

KATALOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 10 paragonów z wykładu
MINI = {"P1": ["chleb", "mleko", "masło"], "P2": ["chleb", "mleko"], "P3": ["makaron", "sos", "chleb"], "P4": ["mleko", "kawa"],
        "P5": ["makaron", "sos"], "P6": ["chleb", "masło"], "P7": ["mleko", "kawa", "chleb"], "P8": ["makaron", "mleko"],
        "P9": ["chleb", "mleko", "kawa"], "P10": ["woda"]}


@pytest.fixture
def K():
    df = pd.DataFrame([(p, x) for p, l in MINI.items() for x in l], columns=["id_paragonu", "produkt"])
    return k.macierz_koszykow(df)


def test_wsparcie_jednego_produktu(K):
    assert k.wsparcie(K, "chleb") == pytest.approx(0.6)        # 6 z 10 paragonów


def test_wsparcie_pary(K):
    assert k.wsparcie(K, ["chleb", "mleko"]) == pytest.approx(0.4)   # P1, P2, P7, P9


def test_pewnosc_nie_jest_symetryczna(K):
    assert k.pewnosc(K, "makaron", "sos") == pytest.approx(2 / 3)
    assert k.pewnosc(K, "sos", "makaron") == pytest.approx(1.0)


def test_lift_jest_symetryczny(K):
    assert k.lift(K, "makaron", "sos") == pytest.approx(10 / 3)
    assert k.lift(K, "sos", "makaron") == pytest.approx(k.lift(K, "makaron", "sos"))


def test_lift_bliski_1_mimo_wysokiej_pewnosci(K):
    # chleb -> mleko: pewność 0,67, ale mleko jest na 60% wszystkich paragonów
    assert k.pewnosc(K, "chleb", "mleko") == pytest.approx(4 / 6)
    assert k.lift(K, "chleb", "mleko") == pytest.approx((4 / 6) / 0.6)


def test_apriori_zgadza_sie_z_wlasnymi_funkcjami(K):
    r = k.reguly(K, min_wsparcie=0.2, min_lift=1.0)
    w = r[(r.poprzednik == "makaron") & (r.nastepnik == "sos")].iloc[0]
    assert w.pewnosc == pytest.approx(k.pewnosc(K, "makaron", "sos"))
    assert w.lift == pytest.approx(k.lift(K, "makaron", "sos"))


def test_dane_sklepu():
    K = k.macierz_koszykow(k.wczytaj(os.path.join(KATALOG, "dane", "paragony.csv")))
    assert K.shape == (7968, 34)
    assert k.lift(K, "makaron", "sos pomidorowy") == pytest.approx(5.97, abs=0.01)
