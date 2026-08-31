import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="7s Rugby Live Stats", layout="centered")

# Kompakte CSS vir kleiner knoppies sodat alles op een skerm pas
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 42px;
        font-size: 13px !important;
        font-weight: bold;
        border-radius: 6px;
        padding: 2px 4px;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 0.3rem;
    }
    </style>
""", unsafe_allow_html=True)

# Inisialiseer Session States
if "events" not in st.session_state:
    st.session_state.events = []
if "score_us" not in st.session_state:
    st.session_state.score_us = 0
if "score_them" not in st.session_state:
    st.session_state.score_them = 0

st.title("🏉 7s Live Stats Tracker")

# 1. Wedstryd Instellings & Spelernames
with st.expander("⚙️ Wedstryd Instellings & Spelername", expanded=False):
    col_m1, col_m2 = st.columns(2)
    wedstryd_nr = col_m1.text_input("Wedstryd #", value="Wedstryd 1")
    tekenaar = col_m2.text_input("Teenstander", value="Opponent")
    
    default_players = "Speler 1, Speler 2, Speler 3, Speler 4, Speler 5, Speler 6, Speler 7, Speler 8, Speler 9, Speler 10, Speler 11, Speler 12"
    raw_players = st.text_area("Spelername (geskei met 'n komma):", value=default_players)
    player_list = [p.strip() for p in raw_players.split(",") if p.strip()]

# Telbord
st.markdown(f"### 🏆 **Ons: {st.session_state.score_us}** | **{tekenaar}: {st.session_state.score_them}**")

def log_event(kat, detail, speler, punte=0, vir_ons=True):
    t_min = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.events.append({
        "Wedstryd": wedstryd_nr,
        "Tyd": t_min,
        "Speler": speler,
        "Kategorie": kat,
        "Aksie": detail,
        "Punte": punte
    })
    
    if punte > 0:
        if vir_ons:
            st.session_state.score_us += punte
        else:
            st.session_state.score_them += punte
            
    st.toast(f"✅ {speler}: {detail}")

# 2. Kies Speler
st.markdown("#### 1. Kies Speler")
speler_opties = ["Span / Algemeen"] + player_list
gekoose_speler = st.selectbox("Aktiewe Speler:", speler_opties, label_visibility="collapsed")

# 3. Aksie Knoppies (Kompak)
st.markdown("#### 2. Tik Aksie")

# Punte-afdeling
st.markdown("**Punte & Kicks**")
p1, p2, p3, p4 = st.columns(4)
if p1.button("🏉 Drie (+5)"): log_event("Punte", "Drie Gedruk", gekoose_speler, punte=5)
if p2.button("🎯 Verstell. (+2)"): log_event("Punte", "Verstelling Suksesvol", gekoose_speler, punte=2)
if p3.button("❌ Verstell. Gemis"): log_event("Punte", "Verstelling Gemis", gekoose_speler)
if p4.button("👟 Strafskop (+3)"): log_event("Punte", "Strafskop Suksesvol", gekoose_speler, punte=3)

p5, p6, p7 = st.columns(3)
if p5.button("🎯 Skepskop (+3)"): log_event("Punte", "Drop Goal Suksesvol", gekoose_speler, punte=3)
if p6.button("🔴 Drie Teenstander (+5)"): log_event("Punte Teen", "Drie Teenstander", tekenaar, punte=5, vir_ons=False)
if p7.button("🔴 Verstell. Teen (+2)"): log_event("Punte Teen", "Verstelling Teenstander", tekenaar, punte=2, vir_ons=False)

st.markdown("**Spelaksies & Foute**")
c1, c2, c3 = st.columns(3)
if c1.button("💥 Duikslag Gewen"): log_event("Verdediging", "Dominante Duikslag", gekoose_speler)
if c2.button("⚠️ Duikslag Gemis"): log_event("Verdediging", "Gemiste Duikslag", gekoose_speler)
if c3.button("⚡ Omkeerbal Gewen"): log_event("Afbreekpunt", "Turnover Gewen", gekoose_speler)

c4, c5, c6 = st.columns(3)
if c4.button("❌ Aangeslaan"): log_event("Fout", "Aangeslaan", gekoose_speler)
if c5.button("🟢 Lynstaan Gewen"): log_event("Set Piece", "Lynstaan Gewen", "Span")
if c6.button("🔴 Skrum Gewen"): log_event("Set Piece", "Skrum Gewen", "Span")

st.divider()

# 4. Wedstryd Log & Export
if st.session_state.events:
    df = pd.DataFrame(st.session_state.events)
    st.markdown("#### 📊 Wedstryd Log")
    st.dataframe(df.tail(3), use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Laai Stats Af (CSV)", csv, f"{wedstryd_nr}_stats.csv", "text/csv")
