"""
=============================================================================
Modalidades de Trabajo en Colombia 2020-2025
Dashboard Streamlit — Diagnóstico interactivo
=============================================================================

Requisitos:
    pip install streamlit pandas matplotlib openpyxl

Ejecutar:
    streamlit run app_modalidades_trabajo.py
=============================================================================
"""

import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ─── Configuración de página ──────────────────────────────────────────────
st.set_page_config(
    page_title="Modalidades de Trabajo · Colombia 2020-2025",
    page_icon="🇨🇴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── PALETA ───────────────────────────────────────────────────────────────
P = {
    "navy":     "#1A2C5B",
    "teal":     "#0D6E8C",
    "gold":     "#E4A118",
    "gray":     "#64748B",
    "offwhite": "#F4F7FA",
    "red":      "#C0392B",
    "green":    "#1A7A4A",
    "purple":   "#7B3FA0",
    "lightblue":"#EEF4F9",
}

# ─── CSS personalizado ────────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* Sidebar */
  [data-testid="stSidebar"] {{
      background-color: {P['navy']};
  }}
  [data-testid="stSidebar"] * {{
      color: white !important;
  }}
  /* Métricas */
  [data-testid="metric-container"] {{
      background: white;
      border-left: 5px solid {P['teal']};
      border-radius: 6px;
      padding: 12px 16px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.07);
  }}
  [data-testid="stMetricValue"] {{
      color: {P['navy']} !important;
      font-size: 2rem !important;
      font-weight: 800 !important;
  }}
  [data-testid="stMetricLabel"] {{
      color: {P['gray']} !important;
      font-size: 0.8rem !important;
  }}
  /* Títulos */
  h1 {{ color: {P['navy']} !important; }}
  h2 {{ color: {P['teal']} !important; }}
  h3 {{ color: {P['navy']} !important; font-size: 1.05rem !important; }}
  /* Tabs */
  [data-baseweb="tab-list"] {{
      gap: 6px;
      border-bottom: 2px solid {P['teal']};
  }}
  [data-baseweb="tab"] {{
      background-color: {P['lightblue']};
      border-radius: 6px 6px 0 0;
      color: {P['navy']} !important;
      font-weight: 600;
  }}
  [aria-selected="true"] {{
      background-color: {P['teal']} !important;
      color: white !important;
  }}
  /* Contenedor general */
  .block-container {{ padding-top: 1.5rem; }}
</style>
""", unsafe_allow_html=True)

# ─── DATOS ────────────────────────────────────────────────────────────────

TELETRABAJADORES = pd.DataFrame({
    "Año": [2012, 2016, 2018, 2020, 2023],
    "Teletrabajadores_miles": [31.5, 88.0, 122.3, 209.2, 252.0],
    "Variación_%": [None, 179.4, 39.0, 71.1, 20.5],
    "Fuente": [
        "MinTIC — 1.er estudio",
        "MinTIC — 3.er estudio",
        "MinTIC — 4.o estudio",
        "MinTIC — 5.o estudio",
        "Estimado — Impacto TIC 2024",
    ],
})

NORMATIVIDAD = pd.DataFrame({
    "Año":   [2008, 2020, 2021, 2021, 2022, 2022, 2022, 2022, 2024],
    "Norma": [
        "Ley 1221",
        "Decreto 555 (COVID)",
        "Ley 2088",
        "Ley 2121",
        "Decreto 555",
        "Decreto 649",
        "Ley 2191",
        "Decreto 1227",
        "Resolución 2007",
    ],
    "Modalidad": [
        "Teletrabajo", "Trabajo en Casa", "Trabajo en Casa",
        "Trabajo Remoto", "Trabajo Remoto", "Trabajo en Casa",
        "Todas", "Teletrabajo", "Teletrabajo",
    ],
    "Objeto": [
        "Régimen de Teletrabajo — primera regulación en Colombia",
        "Habilitación emergencia sanitaria — trabajo en casa COVID-19",
        "Regula el Trabajo en Casa (temporal y ocasional, máx. 6 meses)",
        "Crea el Trabajo Remoto (100 % virtual, contrato indefinido)",
        "Reglamenta Ley 2121 — Trabajo Remoto (Mintrabajo)",
        "Reglamenta Ley 2088 — Trabajo en Casa (sector privado)",
        "Derecho a la Desconexión Laboral (todas las modalidades)",
        "Flexibilización del Teletrabajo — modalidad suplementaria",
        "Reglamenta Teletrabajo para servidores del Ministerio de Trabajo",
    ],
})

ADOPCION = pd.DataFrame({
    "Modalidad": [
        "Teletrabajo formal",
        "Trabajo en casa",
        "Implementaron y abandonaron",
        "Solo presencial",
    ],
    "2020 — Pico pandemia (%)": [18, 43, 12, 27],
    "2023-2024 — Pospandemia (%)": [10, 8, 0, 82],
})

PERCEPCION_TRABAJADORES = pd.DataFrame({
    "Indicador": [
        "Querían continuar en remoto (DANE, 2022)",
        "Prefieren teletrabajo 2-3 días/semana (EY, 2024)",
        "Valoran positivamente el modelo híbrido",
        "Prefieren modelo híbrido (WeWork/Page Group, 2025)",
        "Interés en ser nómadas digitales (WeWork/Page Group, 2025)",
        "Regresarían a oficina a cambio de beneficios (HubSpot, 2023)",
    ],
    "Porcentaje": [87.6, 90.0, 64.0, 59.0, 73.0, 70.0],
    "Fuente": [
        "DANE 2022",
        "EY Work Reimagined 2024",
        "Impacto TIC 2024",
        "WeWork / Page Group, mayo 2025",
        "WeWork / Page Group, mayo 2025",
        "HubSpot Reporte Trabajo Híbrido 2023",
    ],
})

PERCEPCION_EMPRESARIOS = pd.DataFrame({
    "Modelo": ["Híbrido", "Presencial total", "Teletrabajo completo"],
    "Porcentaje": [63, 31, 7],
    "Fuente": ["Cornerstone 2024"] * 3,
})

SECTOR_PUBLICO = pd.DataFrame({
    "Modalidad": ["Trabajo en Casa", "Teletrabajo", "Trabajo Remoto"],
    "Porcentaje": [53, 41, 6],
    "Fuente": ["MinTIC Estudio Percepción 2021"] * 3,
})

DIAGNOSTICO = pd.DataFrame({
    "Modalidad":        ["Presencial", "Trabajo en Casa", "Teletrabajo", "Trabajo Remoto"],
    "Ley base":         ["—", "Ley 2088/2021", "Ley 1221/2008", "Ley 2121/2021"],
    "Tipo":             ["Permanente", "Temporal (máx. 6 meses)", "Indefinido / parcial", "Indefinido / 100 % remoto"],
    "Adopción 2023-24 (%)": [82, 8, 10, 6],
    "Percepción trabajador": [
        "Positiva para cultura e interacción social",
        "Positiva en pandemia; declining pospandemia",
        "Muy positiva si hay flexibilidad real",
        "Positiva en sectores tech; baja adopción general",
    ],
    "Percepción empresario": [
        "Preferida para control y cultura (31 %)",
        "Herramienta de contingencia, no estratégica",
        "Favorita en sectores admin/financiero",
        "Incipiente; solo 7 % opta por remoto total",
    ],
    "Reto principal": [
        "Congestión urbana, costos de desplazamiento",
        "No reemplaza contratos formales de largo plazo",
        "Fragmentación con otras 2 modalidades",
        "Baja penetración; confusión con teletrabajo",
    ],
})

# ─── HELPERS GRÁFICAS ──────────────────────────────────────────────────────

def fig_a_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    return buf


def plot_evolucion():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    vals = TELETRABAJADORES["Teletrabajadores_miles"]
    años = TELETRABAJADORES["Año"].astype(str)
    bars = ax.bar(años, vals, color=P["teal"], width=0.5, zorder=3)
    ax.bar_label(bars, labels=[f"{v:.0f} k" for v in vals],
                 padding=5, color=P["navy"], fontweight="bold", fontsize=10)
    ax.set_title("Teletrabajadores formales registrados (miles)", fontsize=13,
                 color=P["navy"], fontweight="bold", pad=12)
    ax.set_ylabel("Miles de trabajadores", color=P["gray"], fontsize=10)
    ax.tick_params(colors=P["gray"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(P["gray"])
    ax.yaxis.grid(True, color="#E2E8F0", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.annotate("+565 %\n(2012 → 2023)", xy=(4, vals.iloc[-1]),
                xytext=(3.2, 225), fontsize=10, color=P["gold"], fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=P["gold"]))
    ax.text(0.99, 0.02, "* 2023 estimado — Impacto TIC 2024",
            transform=ax.transAxes, fontsize=8, color=P["gray"], ha="right", style="italic")
    plt.tight_layout()
    return fig


def plot_adopcion():
    fig, ax = plt.subplots(figsize=(10, 4.5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    df = ADOPCION
    x = range(len(df))
    w = 0.35
    b1 = ax.bar([i - w / 2 for i in x], df["2020 — Pico pandemia (%)"],
                width=w, label="2020 — Pico pandemia", color=P["teal"], zorder=3)
    b2 = ax.bar([i + w / 2 for i in x], df["2023-2024 — Pospandemia (%)"],
                width=w, label="2023-2024 — Pospandemia", color=P["gold"], zorder=3)
    ax.bar_label(b1, fmt="%d %%", padding=4, color=P["navy"], fontsize=9)
    ax.bar_label(b2, fmt="%d %%", padding=4, color=P["navy"], fontsize=9)
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["Modalidad"], color=P["gray"], fontsize=10)
    ax.set_ylabel("% de empresas", color=P["gray"])
    ax.set_title("Adopción por modalidad — Empresas colombianas\n2020 vs. 2023-2024",
                 fontsize=13, color=P["navy"], fontweight="bold")
    ax.tick_params(colors=P["gray"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color="#E2E8F0", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, labelcolor=P["gray"])
    plt.tight_layout()
    return fig


def plot_percepcion_trabajadores():
    fig, ax = plt.subplots(figsize=(10, 4.5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    df = PERCEPCION_TRABAJADORES.sort_values("Porcentaje")
    colores = [P["teal"] if p >= 70 else P["navy"] for p in df["Porcentaje"]]
    bars = ax.barh(range(len(df)), df["Porcentaje"], color=colores, height=0.5, zorder=3)
    ax.bar_label(bars, fmt="%.1f %%", padding=6, color=P["navy"], fontweight="bold", fontsize=10)
    etiquetas = [t[:50] + "…" if len(t) > 50 else t for t in df["Indicador"]]
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(etiquetas, color=P["gray"], fontsize=9)
    ax.set_xlabel("Porcentaje (%)", color=P["gray"])
    ax.set_title("Percepción de los trabajadores colombianos",
                 fontsize=13, color=P["navy"], fontweight="bold")
    ax.tick_params(colors=P["gray"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.xaxis.grid(True, color="#E2E8F0", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(0, 110)
    plt.tight_layout()
    return fig


def plot_torta_empresarios():
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor("white")
    colores = [P["teal"], P["navy"], P["gold"]]
    wedges, texts, autotexts = ax.pie(
        PERCEPCION_EMPRESARIOS["Porcentaje"],
        labels=PERCEPCION_EMPRESARIOS["Modelo"],
        autopct="%1.0f %%",
        colors=colores,
        explode=(0.03, 0.03, 0.03),
        startangle=90,
        textprops={"fontweight": "bold", "fontsize": 11},
    )
    for t in texts:
        t.set_color(P["gray"])
        t.set_fontsize(11)
    for at in autotexts:
        at.set_color("white")
    ax.set_title("Preferencia de modelo laboral\n(Empresas — Cornerstone 2024)",
                 fontsize=12, color=P["navy"], fontweight="bold")
    plt.tight_layout()
    return fig


def plot_sector_publico():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    colores = [P["teal"], P["navy"], P["gold"]]
    bars = ax.barh(SECTOR_PUBLICO["Modalidad"], SECTOR_PUBLICO["Porcentaje"],
                   color=colores, height=0.4, zorder=3)
    ax.bar_label(bars, fmt="%d %%", padding=6, color=P["navy"], fontweight="bold", fontsize=12)
    ax.set_xlabel("% de servidores públicos", color=P["gray"])
    ax.set_title("Distribución en sector público\n(MinTIC Estudio Percepción 2021)",
                 fontsize=12, color=P["navy"], fontweight="bold")
    ax.tick_params(colors=P["gray"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.xaxis.grid(True, color="#E2E8F0", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(0, 70)
    plt.tight_layout()
    return fig


# ─── SIDEBAR ──────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🇨🇴 Modalidades de Trabajo")
    st.markdown("**Colombia · 2020–2025**")
    st.markdown("---")

    seccion = st.radio(
        "Navegación",
        options=[
            "🏠 Resumen ejecutivo",
            "📋 Marco normativo",
            "📈 Evolución estadística",
            "🏢 Percepción empresarios",
            "👤 Percepción trabajadores",
            "🏛️ Sector público",
            "🔍 Diagnóstico integral",
            "📥 Exportar datos",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        "<small>Fuentes: MinTIC · DANE · Mintrabajo · ANDI · EY · WeWork · HubSpot · Cornerstone · Impacto TIC</small>",
        unsafe_allow_html=True,
    )

# ─── ENCABEZADO ───────────────────────────────────────────────────────────

st.markdown(
    f"""
    <div style='background:{P["navy"]};padding:18px 24px;border-radius:8px;
                border-left:6px solid {P["gold"]};margin-bottom:20px'>
      <h1 style='color:white;margin:0;font-size:1.6rem'>
        Modalidades de Trabajo en Colombia · 2020–2025
      </h1>
      <p style='color:#AECDE8;margin:4px 0 0'>
        Diagnóstico: presencial · trabajo en casa · remoto · teletrabajo
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — RESUMEN EJECUTIVO
# ═══════════════════════════════════════════════════════════════════════════
if seccion == "🏠 Resumen ejecutivo":
    st.markdown("## Resumen ejecutivo")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Teletrabajadores 2020", "209.173", "+71 % vs. 2018")
    col2.metric("Estimado 2023", "~252.000", "+565 % vs. 2012")
    col3.metric("Empresas solo presencial", "82 %", "2023-2024")
    col4.metric("Prefieren modelo híbrido", "59-63 %", "2025")

    st.markdown("---")

    col_l, col_r = st.columns([1.1, 1])

    with col_l:
        st.markdown("### Hitos clave del período")
        hitos = [
            ("2020", P["red"],    "COVID-19 — Explosión del trabajo en casa: 43 % de empresas lo adoptan"),
            ("2021", P["teal"],   "Leyes 2088 y 2121 regulan Trabajo en Casa y Trabajo Remoto"),
            ("2022", P["navy"],   "Ley 2191 de Desconexión Laboral · Retorno masivo a presencialidad"),
            ("2023", P["gold"],   "82 % de empresas vuelven a ser 100 % presenciales"),
            ("2024", P["purple"], "Resolución 2007: teletrabajo para servidores del Mintrabajo"),
            ("2025", P["green"],  "Modelo híbrido emerge como nuevo consenso (59-63 % de preferencia)"),
        ]
        for año, color, texto in hitos:
            st.markdown(
                f"""<div style='display:flex;align-items:flex-start;margin-bottom:10px'>
                    <div style='background:{color};color:white;font-weight:700;font-size:0.8rem;
                                padding:3px 8px;border-radius:4px;min-width:42px;text-align:center;
                                margin-right:12px;margin-top:2px'>{año}</div>
                    <div style='color:{P["gray"]};font-size:0.93rem'>{texto}</div>
                    </div>""",
                unsafe_allow_html=True,
            )

    with col_r:
        st.markdown("### Conclusiones principales")
        conclusiones = [
            "Colombia pasó de **1 a 4 modalidades** formales reguladas (2008-2024).",
            "El teletrabajo creció **+565 %** entre 2012 y 2023.",
            "La pandemia fue catalizadora pero el **retorno presencial fue dominante** en 2022-2023.",
            "El modelo **híbrido** es el nuevo consenso: preferido por 59-63 % de actores.",
            "La **informalidad laboral (55,9 %)** limita la adopción de modalidades remotas.",
            "Urge **unificar el régimen** no presencial y actualizar estudios oficiales.",
        ]
        for c in conclusiones:
            st.markdown(f"✅ {c}")

# ═══════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — MARCO NORMATIVO
# ═══════════════════════════════════════════════════════════════════════════
elif seccion == "📋 Marco normativo":
    st.markdown("## Marco normativo · 2008–2024")

    # Filtro por modalidad
    modalidades = ["Todas"] + sorted(NORMATIVIDAD["Modalidad"].unique().tolist())
    filtro = st.selectbox("Filtrar por modalidad", modalidades)

    df_norm = NORMATIVIDAD if filtro == "Todas" else NORMATIVIDAD[NORMATIVIDAD["Modalidad"] == filtro]

    # Colorear filas por modalidad
    color_map = {
        "Teletrabajo":     P["teal"],
        "Trabajo en Casa": P["gold"],
        "Trabajo Remoto":  P["purple"],
        "Todas":           P["navy"],
    }

    for _, row in df_norm.iterrows():
        color = color_map.get(row["Modalidad"], P["gray"])
        st.markdown(
            f"""<div style='display:flex;align-items:stretch;margin-bottom:8px;
                            border-radius:6px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.08)'>
                <div style='background:{color};color:white;font-weight:700;font-size:0.85rem;
                            padding:10px 14px;min-width:60px;text-align:center;
                            display:flex;align-items:center;justify-content:center'>{row['Año']}</div>
                <div style='background:{color};color:white;font-size:0.82rem;
                            padding:10px 12px;min-width:140px;
                            display:flex;align-items:center;font-weight:600'>{row['Norma']}</div>
                <div style='background:white;padding:10px 16px;flex:1;
                            font-size:0.9rem;color:{P["gray"]};
                            display:flex;align-items:center'>{row['Objeto']}</div>
                <div style='background:{color}22;padding:10px 12px;min-width:130px;
                            font-size:0.8rem;color:{color};font-weight:600;
                            display:flex;align-items:center;justify-content:center'>{row['Modalidad']}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.info("💡 Colombia es uno de los pocos países de América Latina con tres regímenes específicos de trabajo no presencial regulados por ley.")

# ═══════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — EVOLUCIÓN ESTADÍSTICA
# ═══════════════════════════════════════════════════════════════════════════
elif seccion == "📈 Evolución estadística":
    st.markdown("## Evolución estadística · 2012–2025")

    tab1, tab2 = st.tabs(["📊 Teletrabajadores formales", "🏢 Adopción por modalidad"])

    with tab1:
        st.pyplot(plot_evolucion())
        st.markdown("#### Datos fuente")
        st.dataframe(
            TELETRABAJADORES.style.format({"Teletrabajadores_miles": "{:.1f}", "Variación_%": "{:.1f} %"}),
            use_container_width=True,
        )

    with tab2:
        st.pyplot(plot_adopcion())
        st.markdown("#### Datos fuente")
        st.dataframe(ADOPCION, use_container_width=True)
        st.caption("Fuente: MinTIC Quinto Estudio 2020 · GeoVictoria 2022 · Impacto TIC 2024")

# ═══════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — PERCEPCIÓN EMPRESARIOS
# ═══════════════════════════════════════════════════════════════════════════
elif seccion == "🏢 Percepción empresarios":
    st.markdown("## Percepción de empresarios colombianos")

    col_l, col_r = st.columns([1, 1.2])

    with col_l:
        st.pyplot(plot_torta_empresarios())

    with col_r:
        st.markdown("### Hallazgos clave")
        hallazgos = [
            ("39,8 %",  "de empresas no estaba seguro de mantener el remoto post-pandemia (ANDI, 2021)"),
            ("10 %",    "de empresas tenían planes concretos de teletrabajo en 2023, detrás de México y Chile"),
            ("94 %",    "de colaboradores sin trabajo remoto a finales de 2023 (sectores de alta presencialidad)"),
            ("100 %",   "retorno presencial en retail grande, minería y agroindustria en 2022"),
            ("80 %",    "adopción de teletrabajo en áreas admin/financieras en 2020 (vs. 44 % en 2018)"),
            ("90 %",    "de empresas diseñando esquemas flexibles/híbridos para retener talento (KPMG, 2024)"),
        ]
        for pct, texto in hallazgos:
            st.markdown(
                f"""<div style='display:flex;align-items:center;margin-bottom:10px;
                                background:white;border-radius:6px;padding:10px 14px;
                                box-shadow:0 1px 4px rgba(0,0,0,0.07)'>
                    <span style='font-size:1.35rem;font-weight:800;color:{P["teal"]};
                                 min-width:68px'>{pct}</span>
                    <span style='color:{P["gray"]};font-size:0.9rem'>{texto}</span>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.dataframe(PERCEPCION_EMPRESARIOS, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# SECCIÓN 5 — PERCEPCIÓN TRABAJADORES
# ═══════════════════════════════════════════════════════════════════════════
elif seccion == "👤 Percepción trabajadores":
    st.markdown("## Percepción de los trabajadores colombianos")

    st.pyplot(plot_percepcion_trabajadores())

    st.markdown("---")
    st.markdown("### Tabla detallada")
    st.dataframe(PERCEPCION_TRABAJADORES, use_container_width=True)

    st.markdown("---")
    st.markdown("### Tensión principal del período")
    col1, col2, col3 = st.columns(3)
    col1.metric("Querían seguir en remoto (2022)", "87,6 %", "DANE")
    col2.metric("Prefieren híbrido (2025)", "59 %", "WeWork / Page Group")
    col3.metric("Regresarían por beneficios", "70 %", "HubSpot 2023")

    st.info("💡 La preferencia de los trabajadores evolucionó: de querer el remoto total (2021-2022) a preferir el modelo híbrido como equilibrio (2024-2025).")

# ═══════════════════════════════════════════════════════════════════════════
# SECCIÓN 6 — SECTOR PÚBLICO
# ═══════════════════════════════════════════════════════════════════════════
elif seccion == "🏛️ Sector público":
    st.markdown("## Sector público — Adopción y percepción institucional")

    col_l, col_r = st.columns([1.1, 1])

    with col_l:
        st.pyplot(plot_sector_publico())
        st.dataframe(SECTOR_PUBLICO, use_container_width=True)

    with col_r:
        st.markdown("### Hitos institucionales")
        hitos = [
            ("MinTIC", "Lanzó el portal **teletrabajo.gov.co** y ofrece asesorías gratuitas a entidades públicas y privadas."),
            ("Resolución 2007/2024", "Reglamentó el teletrabajo específicamente para servidores del Ministerio de Trabajo."),
            ("DAFP + MinTIC", "Emitieron guías metodológicas para implementar el teletrabajo en el sector público."),
            ("Pandemia 2020", "El sector público fue pionero: el **53 % de empleados** trabajó en casa durante la emergencia."),
            ("Estudio 2021", "El **41 %** de servidores públicos encuestados teletrabajaba formalmente, y el **6 %** usaba trabajo remoto."),
        ]
        for titulo, texto in hitos:
            st.markdown(
                f"""<div style='background:white;border-left:4px solid {P["teal"]};
                                border-radius:4px;padding:12px 16px;margin-bottom:10px;
                                box-shadow:0 1px 4px rgba(0,0,0,0.07)'>
                    <strong style='color:{P["navy"]}'>{titulo}</strong><br>
                    <span style='color:{P["gray"]};font-size:0.9rem'>{texto}</span>
                </div>""",
                unsafe_allow_html=True,
            )

# ═══════════════════════════════════════════════════════════════════════════
# SECCIÓN 7 — DIAGNÓSTICO INTEGRAL
# ═══════════════════════════════════════════════════════════════════════════
elif seccion == "🔍 Diagnóstico integral":
    st.markdown("## Diagnóstico integral por modalidad")

    colores_modal = {
        "Presencial":        P["navy"],
        "Trabajo en Casa":   P["teal"],
        "Teletrabajo":       P["gold"],
        "Trabajo Remoto":    P["purple"],
    }

    for _, row in DIAGNOSTICO.iterrows():
        color = colores_modal.get(row["Modalidad"], P["gray"])
        with st.expander(f"**{row['Modalidad']}** — {row['Ley base']} · Adopción 2023-24: {row['Adopción 2023-24 (%)']} %", expanded=True):
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Tipo:** {row['Tipo']}")
            c2.markdown(f"**Adopción actual:** {row['Adopción 2023-24 (%)']} %")
            c3.markdown(f"**Ley base:** {row['Ley base']}")
            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown(
                    f"<div style='background:{color}15;border-left:4px solid {color};"
                    f"padding:10px;border-radius:4px'>"
                    f"<strong style='color:{color}'>👤 Percepción trabajador</strong><br>"
                    f"<span style='color:{P['gray']};font-size:0.9rem'>{row['Percepción trabajador']}</span></div>",
                    unsafe_allow_html=True,
                )
            with col_b:
                st.markdown(
                    f"<div style='background:{color}15;border-left:4px solid {color};"
                    f"padding:10px;border-radius:4px'>"
                    f"<strong style='color:{color}'>🏢 Percepción empresario</strong><br>"
                    f"<span style='color:{P['gray']};font-size:0.9rem'>{row['Percepción empresario']}</span></div>",
                    unsafe_allow_html=True,
                )
            with col_c:
                st.markdown(
                    f"<div style='background:{P['red']}11;border-left:4px solid {P['red']};"
                    f"padding:10px;border-radius:4px'>"
                    f"<strong style='color:{P['red']}'>⚠️ Reto principal</strong><br>"
                    f"<span style='color:{P['gray']};font-size:0.9rem'>{row['Reto principal']}</span></div>",
                    unsafe_allow_html=True,
                )

    st.markdown("---")
    st.markdown("### Brechas estructurales identificadas")
    brechas = [
        ("⚡ Brecha digital",          "Alta informalidad (55,9 %) y baja conectividad rural limitan el acceso real a modalidades remotas."),
        ("⚖️ Fragmentación normativa",  "Tres regímenes coexistentes generan confusión en empleadores y trabajadores sobre derechos y obligaciones."),
        ("🔒 Cultura de control",       "70 % del retorno a presencialidad se motiva en control gerencial, no en evidencia de baja productividad."),
        ("⚕️ Salud mental",             "Aislamiento y sobrecarga en trabajo en casa evidenciaron riesgos psicosociales no regulados suficientemente."),
        ("📊 Vacío de datos oficiales", "No existe un estudio actualizado post-2022. La toma de decisiones carece de información estadística reciente."),
        ("🌐 Regulación híbrida",       "El modelo híbrido carece aún de un régimen específico, siendo la modalidad de mayor preferencia en 2025."),
    ]
    col1, col2 = st.columns(2)
    for i, (titulo, desc) in enumerate(brechas):
        col = col1 if i % 2 == 0 else col2
        col.markdown(
            f"""<div style='background:white;border-radius:6px;padding:12px 16px;
                            margin-bottom:10px;box-shadow:0 1px 4px rgba(0,0,0,0.08)'>
                <strong style='color:{P["navy"]}'>{titulo}</strong><br>
                <span style='color:{P["gray"]};font-size:0.88rem'>{desc}</span>
            </div>""",
            unsafe_allow_html=True,
        )

# ═══════════════════════════════════════════════════════════════════════════
# SECCIÓN 8 — EXPORTAR DATOS
# ═══════════════════════════════════════════════════════════════════════════
elif seccion == "📥 Exportar datos":
    st.markdown("## Exportar datos del diagnóstico")
    st.markdown("Descarga cualquiera de los datasets en formato CSV o el paquete completo en Excel.")

    datasets = {
        "Teletrabajadores":        TELETRABAJADORES,
        "Normatividad":            NORMATIVIDAD,
        "Adopción Empresas":       ADOPCION,
        "Percepción Trabajadores": PERCEPCION_TRABAJADORES,
        "Percepción Empresarios":  PERCEPCION_EMPRESARIOS,
        "Sector Público":          SECTOR_PUBLICO,
        "Diagnóstico Integral":    DIAGNOSTICO,
    }

    st.markdown("### Descarga por tabla (CSV)")
    cols = st.columns(3)
    for i, (nombre, df) in enumerate(datasets.items()):
        col = cols[i % 3]
        csv = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        col.download_button(
            label=f"⬇️ {nombre}",
            data=csv,
            file_name=f"colombia_trabajo_{nombre.lower().replace(' ', '_')}.csv",
            mime="text/csv",
        )

    st.markdown("---")
    st.markdown("### Descarga paquete Excel (todas las tablas)")

    buf = io.BytesIO()
    nombres_hojas = {
        "Teletrabajadores":        "Teletrabajadores",
        "Normatividad":            "Normatividad",
        "Adopción Empresas":       "Adopcion_Empresas",
        "Percepción Trabajadores": "Percepcion_Trabajadores",
        "Percepción Empresarios":  "Percepcion_Empresarios",
        "Sector Público":          "Sector_Publico",
        "Diagnóstico Integral":    "Diagnostico_Integral",
    }
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        for nombre, df in datasets.items():
            df.to_excel(writer, sheet_name=nombres_hojas[nombre], index=False)
    buf.seek(0)
    st.download_button(
        label="⬇️ Descargar Excel completo (7 hojas)",
        data=buf,
        file_name="diagnostico_modalidades_trabajo_colombia.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    st.markdown("---")
    st.markdown("### Descarga gráficas (PNG)")
    graficas = [
        ("Evolución Teletrabajadores", plot_evolucion, "grafica_evolucion_teletrabajadores.png"),
        ("Adopción Empresas",          plot_adopcion,  "grafica_adopcion_empresas.png"),
        ("Percepción Trabajadores",    plot_percepcion_trabajadores, "grafica_percepcion_trabajadores.png"),
        ("Preferencia Empresarios",    plot_torta_empresarios,       "grafica_torta_empresarios.png"),
        ("Sector Público",             plot_sector_publico,           "grafica_sector_publico.png"),
    ]
    cols_g = st.columns(3)
    for i, (nombre, fn, fname) in enumerate(graficas):
        fig = fn()
        buf_img = fig_a_bytes(fig)
        plt.close(fig)
        cols_g[i % 3].download_button(
            label=f"🖼️ {nombre}",
            data=buf_img,
            file_name=fname,
            mime="image/png",
        )
