import streamlit as st
import pandas as pd
import datetime
import pytz
import io

st.set_page_config(page_title="Swartland Rugby Stats", layout="wide")

# Donkerblou tema, Swartland-goud aksente, versteekte nav-balk en belynde etikette
st.markdown("""
    <style>
    header[data-testid="stHeader"], .stAppHeader {
        display: none !important;
    }
    
    .stAppViewMain {
        padding-top: 0px !important;
    }

    .stApp {
        background-color: #0b132b !important;
        color: #ffffff !important;
    }
    
    .stAppViewContainer::before {
        content: "";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 85vw;
        height: 85vw;
        max-width: 380px;
        max-height: 380px;
        background-image: url('https://raw.githubusercontent.com/konradtoerien/Rugbystats/main/211923.jpg');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        opacity: 0.10;
        pointer-events: none;
        z-index: 0;
    }

    .stButton>button {
        width: 100%;
        height: 28px !important;
        font-size: 8.5px !important;
        font-weight: bold;
        border-radius: 4px;
        padding: 0px 0px !important;
        border: 1px solid #f4c430 !important;
        background-color: #1c2541 !important;
        color: #ffffff !important;
        margin-bottom: 0px !important;
    }

    .match-control-btn > button {
        height: 38px !important;
        font-size: 11px !important;
        background-color: #f4c430 !important;
        color: #0b132b !important;
        border: 1px solid #ffffff !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0.1rem !important;
        align-items: center !important;
    }
    
    .element-container {
        margin-bottom: 0.1rem !important;
    }

    h1, h2, h3, h4, label, p {
        color: #f4c430 !important;
        margin-bottom: 0.1rem !important;
    }
    
    .player-label {
        font-size: 11px;
        font-weight: bold;
        color: #ffffff;
        line-height: 28px;
        height: 28px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        display: flex;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

if "events" not in st.session_state:
    st.session_state.events = []
if "score_us" not in st.session_state:
    st.session_state.score_us = 0
if "score_them" not in st.session_state:
    st.session_state.score_them = 0

st.title("🏉 Swartland Rugby Stats")

with st.expander("⚙️ Wedstryd Instellings & Name", expanded=False):
    col_m1, col_m2 = st.columns(2)
    wedstryd_nr = col_m1.text_input("Wedstryd #", value="Wedstryd 1")
    tekenaar = col_m2.text_input("Teenstander", value="Opponent")
    
    default_players = "Speler 1, Speler 2, Speler 3, Speler 4, Speler 5, Speler 6, Speler 7, Speler 8, Speler 9, Speler 10, Speler 11, Speler 12, Speler 13, Speler 14, Speler 15"
    raw_players = st.text_area("Spelername (geskei met 'n komma):", value=default_players)
    player_list = [p.strip() for p in raw_players.split(",") if p.strip()]

st.markdown(f"### 🏆 **Swartland: {st.session_state.score_us}** | **{tekenaar}: {st.session_state.score_them}**")

def log_event(kat, detail, speler, punte=0, vir_ons=True):
    # Stel tydsone eksplisiet na Suid-Afrika (SAST / UTC+2)
    sa_time = datetime.datetime.now(pytz.timezone('Africa/Johannesburg'))
    t_min = sa_time.strftime("%H:%M:%S")
    
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

st.divider()

# 1. SPAN-KNOPPIES
st.markdown("#### 📋 HELE SPAN & TEENSTANDER AKSIES")
c_span_label, s1, s2, s3, s4, s5, s6, s7, s8, s9 = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1, 1])

with c_span_label: st.markdown("<div class='player-label'>HELE SPAN</div>", unsafe_allow_html=True)
if s1.button("🔴 Drie-T (+5)"): log_event("Punte Teen", "Drie Teenstander", tekenaar, punte=5, vir_ons=False)
if s2.button("🔴 Verst-T (+2)"): log_event("Punte Teen", "Verstelling Teenstander", tekenaar, punte=2, vir_ons=False)
if s3.button("🔴 Straf-T (+3)"): log_event("Punte Teen", "Strafskop Teenstander", tekenaar, punte=3, vir_ons=False)
if s4.button("🔴 Skep-T (+3)"): log_event("Punte Teen", "Skepskop Teenstander", tekenaar, punte=3, vir_ons=False)
if s5.button("🚩 Straf Afgestaan"): log_event("Dissipline", "Strafskop Afgestaan", "Span")
if s6.button("🟢 Lynst Gewen"): log_event("Set Piece", "Lynstaan Gewen", "Span")
if s7.button("🔴 Lynst Verloor"): log_event("Set Piece", "Lynstaan Verloor", "Span")
if s8.button("🟢 Skrum Gewen"): log_event("Set Piece", "Skrum Gewen", "Span")
if s9.button("🔴 Skrum Verloor"): log_event("Set Piece", "Skrum Verloor", "Span")

st.divider()

# 2. INDIVIDUELE SPELER ROSTER
st.markdown("#### 🏃 SPELER INDIVIDUELE STATS")

for p_name in player_list:
    c_label, b1, b2, b3, b4, b5, b6, b7, b8, b9 = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    
    with c_label:
        st.markdown(f"<div class='player-label'>{p_name}</div>", unsafe_allow_html=True)
        
    if b1.button("🏉 Drie (+5)", key=f"drie_{p_name}"): log_event("Punte", "Drie Gedruk", p_name, punte=5)
    if b2.button("🎯 Verst (+2)", key=f"verst_{p_name}"): log_event("Punte", "Verstelling Gewen", p_name, punte=2)
    if b3.button("❌ Verst Gem", key=f"verstgem_{p_name}"): log_event("Punte", "Verstelling Gemis", p_name)
    if b4.button("👟 Straf (+3)", key=f"straf_{p_name}"): log_event("Punte", "Strafskop Gewen", p_name, punte=3)
    if b5.button("🎯 Skep (+3)", key=f"skep_{p_name}"): log_event("Punte", "Drop Goal", p_name, punte=3)
    if b6.button("💥 Duik Gewen", key=f"duikgew_{p_name}"): log_event("Verdediging", "Dominante Duikslag", p_name)
    if b7.button("⚠️ Duik Gemis", key=f"duikgem_{p_name}"): log_event("Verdediging", "Gemiste Duikslag", p_name)
    if b8.button("⚡ Omkeer Gew", key=f"omkeer_{p_name}"): log_event("Afbreekpunt", "Turnover Gewen", p_name)
    if b9.button("❌ Aangeslaan", key=f"aangeslaan_{p_name}"): log_event("Fout", "Aangeslaan", p_name)

st.divider()

# 3. HALFTYD & EINDE KNOPPIES
st.markdown("#### ⏱️ WEDSTRYD BEHEER")
m_col1, m_col2 = st.columns(2)

with m_col1:
    st.markdown("<div class='match-control-btn'>", unsafe_allow_html=True)
    if st.button("🔔 HALFTYD"):
        log_event("Wedstryd", "--- HALFTYD ---", "WEDSTRYD")
    st.markdown("</div>", unsafe_allow_html=True)

with m_col2:
    st.markdown("<div class='match-control-btn'>", unsafe_allow_html=True)
    if st.button("🏁 EINDE VAN WEDSTRYD"):
        log_event("Wedstryd", "=== EINDE VAN WEDSTRYD ===", "WEDSTRYD")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# 4. EXCEL EXPORT
if st.session_state.events:
    df_tydlyn = pd.DataFrame(st.session_state.events)
    
    df_actions_only = df_tydlyn[~df_tydlyn["Speler"].isin(["WEDSTRYD"])]
    df_span_totale = df_actions_only.groupby("Aksie").size().reset_index(name="Totale Aantal")
    df_speler_totale = df_actions_only.groupby(["Speler", "Aksie"]).size().reset_index(name="Aantal")

    st.markdown("#### 📊 Wedstryd Log & Totale Opsomming")
    
    t1, t2, t3 = st.tabs([" Span Totale", "🏃 Speler Stats", "⏱️ Wedstryd Tydlyn"])
    with t1: st.dataframe(df_span_totale, use_container_width=True)
    with t2: st.dataframe(df_speler_totale, use_container_width=True)
    with t3: st.dataframe(df_tydlyn.tail(6), use_container_width=True)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_span_totale.to_excel(writer, sheet_name='Alle Stats', startrow=1, index=False)
        
        start_row_speler = len(df_span_totale) + 4
        df_speler_totale.to_excel(writer, sheet_name='Alle Stats', startrow=start_row_speler, index=False)
        
        start_row_tydlyn = start_row_speler + len(df_speler_totale) + 3
        df_tydlyn.to_excel(writer, sheet_name='Alle Stats', startrow=start_row_tydlyn, index=False)

        df_span_totale.to_excel(writer, sheet_name='Span Totale', index=False)
        df_speler_totale.to_excel(writer, sheet_name='Speler Totale', index=False)
        df_tydlyn.to_excel(writer, sheet_name='Wedstryd Tydlyn', index=False)
        
    excel_data = output.getvalue()

    st.download_button(
        label="📊 Laai Volledige Excel Worksheet (.xlsx) Af",
        data=excel_data,
        file_name=f"{wedstryd_nr}_Volledige_Stats.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
