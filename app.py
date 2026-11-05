"""Dashboard: reguły asocjacyjne dla paragonów sklepu. Uruchomienie: streamlit run app.py"""
import os

import pandas as pd
import streamlit as st

import koszyk as k

PLIK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dane", "paragony.csv")
st.set_page_config(page_title="Analiza koszyka", layout="wide")


@st.cache_data
def dane():
    df = k.wczytaj(PLIK)
    info = df.groupby("id_paragonu").agg(data=("data", "first"), godzina=("godzina", "first"))
    return k.macierz_koszykow(df), info


K, info = dane()
st.title("Analiza koszyka: EconoShop Express")
st.caption("Dane syntetyczne do zajęć z eksploracji danych: paragony z września i października 2026 r. Reguła A → B: klienci z A na paragonie mają też B.")

with st.sidebar:
    st.header("Ustawienia")
    okres = st.selectbox("Okres", ["wrzesień i październik", "tylko wrzesień", "tylko październik"])
    godziny = st.slider("Godziny zakupu", 7, 21, (7, 21))
    min_w = st.select_slider("Minimalne wsparcie (% paragonów)", [0.3, 0.5, 1.0, 2.0, 3.0, 5.0], value=1.0)
    min_l = st.slider("Minimalny lift", 1.0, 5.0, 1.2, step=0.1)
    pary = st.checkbox("Tylko pary produktów (A → B)", value=True)

maska = info["godzina"].between(*godziny).reindex(K.index)
if okres != "wrzesień i październik":
    maska &= (info["data"].dt.month == (9 if okres == "tylko wrzesień" else 10)).reindex(K.index)
Ks = K[maska]
r = k.reguly(Ks, min_w / 100, min_l, max_dlugosc=2 if pary else 3)

c1, c2, c3 = st.columns(3)
c1.metric("Paragony", f"{len(Ks):,}".replace(",", " "))
c2.metric("Reguły", len(r))
c3.metric("Najwyższy lift", f"{r.lift.max():.2f}".replace(".", ",") if len(r) else "brak")

st.subheader("Reguły (posortowane po lift)")
st.dataframe(r.round({"wsparcie": 4, "pewnosc": 3, "lift": 2}), width="stretch", hide_index=True)

st.subheader("Sprawdź parę produktów")
a, b = st.columns(2)
A = a.selectbox("Poprzednik A", sorted(K.columns), index=sorted(K.columns).index("makaron"))
B = b.selectbox("Następnik B", sorted(K.columns), index=sorted(K.columns).index("sos pomidorowy"))
if A != B and k.liczba(Ks, A) > 0 and k.liczba(Ks, B) > 0:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Paragony z A i B", k.liczba(Ks, [A, B]))
    m2.metric("Wsparcie A i B", f"{k.wsparcie(Ks, [A, B]) * 100:.2f}%".replace(".", ","))
    m3.metric("Pewność A → B", f"{k.pewnosc(Ks, A, B):.3f}".replace(".", ","))
    m4.metric("Lift", f"{k.lift(Ks, A, B):.2f}".replace(".", ","))
    if k.liczba(Ks, [A, B]) < 30:
        st.warning("Mniej niż 30 paragonów z A i B: wynik może być przypadkowy.")
else:
    st.info("Wybierz dwa różne produkty, które występują w wybranym okresie.")
st.download_button("Pobierz reguły (CSV)", r.to_csv(index=False).encode("utf-8"), file_name="reguly.csv", mime="text/csv")
