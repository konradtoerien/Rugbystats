import streamlit as st
import pandas as pd
import datetime
st.set_page_config(page_title="7s Rugby Live Stats", layout="centered")
st.markdown("""
 <style>
 .stButton>button {
 width: 100%;
 height: 55px;
 font-size: 16px !important;
 font-weight: bold;
 border-radius: 8px;
 }
 </style>
""", unsafe_allow_html=True)
if "events" not in st.session_state:
 st.session_state.events = []
st.title(" 7s Live Tracker")
col1, col2 = st.columns(2)
wedstryd_nr = col1.text_input("Wedstryd #", value="Wedstryd 1")
tekenaar = col2.text_input("Teenstander", value="Opponent")
def log_event(kat, detail, speler):
 t_min = datetime.datetime.now().strftime("%H:%M:%S")
 st.session_state.events.append({
 "Wedstryd": wedstryd_nr,
 "Tyd": t_min,
 "Speler": speler,
 "Kategorie": kat,
 "Aksie": detail
 })
 st.toast(f" {speler}: {detail}")
st.subheader("1. Kies Speler")
speler_opties = ["Span / Algemeen"] + [f"Speler #{i}" for i in range(1, 13)]
gekoose_speler = st.radio("Aktiewe Speler:", speler_opties, horizontal=True)
st.subheader("2. Tik Aksie")
                               c1, c2 = st.columns(2)
with c1:
 if st.button(" Drie Gedruk"): log_event("Punte", "Drie Gedruk", gekoose_speler)
 if st.button(" Duikslag Gewen"): log_event("Verdediging", "Dominante Duikslag", gekoose_speler)
 if st.button(" Omkeerbal Gewen"): log_event("Afbreekpunt", "Turnover Gewen", gekoose_speler)
 if st.button(" Lynstaan Gewen"): log_event("Set Piece", "Lynstaan Gewen", "Span")
with c2:
 if st.button(" Verstelling"): log_event("Punte", "Verstelling Suksesvol", gekoose_speler)
 if st.button(" Duikslag Gemis"): log_event("Verdediging", "Gemiste Duikslag", gekoose_speler)
 if st.button(" Aangeslaan"): log_event("Fout", "Aangeslaan", gekoose_speler)
 if st.button(" Skrum Gewen"): log_event("Set Piece", "Skrum Gewen", "Span")
if st.session_state.events:
 df = pd.DataFrame(st.session_state.events)
 st.subheader(" Wedstryd Log")
 st.dataframe(df.tail(4), use_container_width=True)
 csv = df.to_csv(index=False).encode('utf-8')
 st.download_button(" Laai Stats Af (CSV)", csv, f"{wedstryd_nr}_stats.csv", "text/csv"
