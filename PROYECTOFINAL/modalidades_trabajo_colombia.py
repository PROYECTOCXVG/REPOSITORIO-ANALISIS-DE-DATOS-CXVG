"""
=============================================================================
Modalidades de Trabajo en Colombia 2020-2025
Diagnóstico: Presencial · Trabajo en Casa · Remoto · Teletrabajo
=============================================================================

Este script es el GEMELO Python del proyecto presentado en PowerPoint.
Permite:
  1. Reproducir todos los datos del diagnóstico en forma tabular y gráfica.
  2. Exportar tablas a Excel/CSV.
  3. Generar gráficas con matplotlib (misma paleta de la presentación).
  4. Servir de base analítica para ampliar el estudio con nuevos datos.

Requisitos:
    pip install pandas matplotlib openpyxl

Uso:
    python modalidades_trabajo_colombia.py
    python modalidades_trabajo_colombia.py --export-excel
    python modalidades_trabajo_colombia.py --export-csv
    python modalidades_trabajo_colombia.py --solo-graficas
=============================================================================
"""

import argparse
import sys
from pathlib import Path

# ─── Importaciones opcionales ─────────────────────────────────────────────
try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.ticker import FuncFormatter
except ImportError:
    print("ERROR: instale las dependencias con:\n"
          "  pip install pandas matplotlib openpyxl\n")
    sys.exit(1)

# ─── PALETA (igual que la presentación PowerPoint) ────────────────────────
PALETA = {
    "navy":    "#1A2C5B",
    "teal":    "#0D6E8C",
    "gold":    "#E4A118",
    "gray":    "#64748B",
    "offwhite":"#F4F7FA",
    "red":     "#C0392B",
    "green":   "#1A7A4A",
    "purple":  "#7B3FA0",
}

# ─── DATOS ────────────────────────────────────────────────────────────────

# 1. Evolución de teletrabajadores formales en Colombia
TELETRABAJADORES = pd.DataFrame({
    "Año": [2012, 2016, 2018, 2020, 2023],
    "Teletrabajadores_miles": [31.5, 88.0, 122.3, 209.2, 252.0],
    "Fuente": [
        "MinTIC (primer estudio)",
        "MinTIC (tercer estudio)",
        "MinTIC (cuarto estudio)",
        "MinTIC (quinto estudio)",
        "Estimado — Impacto TIC 2024",
    ],
})

# 2. Marco normativo
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
        "Teletrabajo",
        "Trabajo en Casa",
        "Trabajo en Casa",
        "Trabajo Remoto",
        "Trabajo Remoto",
        "Trabajo en Casa",
        "Todas",
        "Teletrabajo",
        "Teletrabajo",
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

# 3. Adopción de modalidades por período (% empresas)
ADOPCION_EMPRESAS = pd.DataFrame({
    "Modalidad": [
        "Teletrabajo formal",
        "Trabajo en casa",
        "Implementaron y abandonaron",
        "Solo presencial",
    ],
    "2020_pico_pandemia_pct": [18, 43, 12, 27],
    "2023_2024_pospandemia_pct": [10, 8, 0, 82],
})

# 4. Percepción de trabajadores (% encuestados)
PERCEPCION_TRABAJADORES = pd.DataFrame({
    "Indicador": [
        "Querían continuar en remoto (DANE, 2022)",
        "Prefieren teletrabajo 2-3 días/semana (EY, 2024)",
        "Valoran positivamente el híbrido",
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

# 5. Percepción de empresarios (preferencia de modelo)
PERCEPCION_EMPRESARIOS = pd.DataFrame({
    "Modelo": ["Híbrido", "Presencial total", "Teletrabajo completo"],
    "Porcentaje": [63, 31, 7],
    "Fuente": ["Cornerstone 2024"] * 3,
})

# 6. Sector público (distribución de modalidades)
SECTOR_PUBLICO = pd.DataFrame({
    "Modalidad": ["Trabajo en Casa", "Teletrabajo", "Trabajo Remoto"],
    "Porcentaje": [53, 41, 6],
    "Fuente": ["MinTIC Estudio Percepción 2021"] * 3,
})

# 7. Diagnóstico integral por modalidad
DIAGNOSTICO = pd.DataFrame({
    "Modalidad": ["Presencial", "Trabajo en Casa", "Teletrabajo", "Trabajo Remoto"],
    "Ley_base": ["N/A", "Ley 2088/2021", "Ley 1221/2008", "Ley 2121/2021"],
    "Tipo": ["Permanente", "Temporal (máx. 6 meses)", "Indefinido / parcial", "Indefinido / 100 % remoto"],
    "Adopcion_2023_2024_pct": [82, 8, 10, 6],
    "Percepcion_trabajador": [
        "Positiva para cultura e interacción social",
        "Positiva en pandemia; declining pospandemia",
        "Muy positiva si hay flexibilidad real",
        "Positiva en sectores tech; baja adopción general",
    ],
    "Percepcion_empresario": [
        "Preferida para control y cultura (31 %)",
        "Herramienta de contingencia, no estratégica",
        "Favorita en sectores admin/financiero",
        "Incipiente; solo 7 % opta por remoto total",
    ],
    "Reto_principal": [
        "Congestión urbana, costos de desplazamiento",
        "No reemplaza contratos formales de largo plazo",
        "Fragmentación con otras 2 modalidades",
        "Baja penetración; confusión con teletrabajo",
    ],
})


# ─── GRÁFICAS ─────────────────────────────────────────────────────────────

def grafica_evolucion_teletrabajadores(guardar: bool = False):
    """Barras — crecimiento de teletrabajadores formales."""
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor(PALETA["offwhite"])
    ax.set_facecolor("white")

    años = TELETRABAJADORES["Año"].astype(str)
    vals = TELETRABAJADORES["Teletrabajadores_miles"]

    bars = ax.bar(años, vals, color=PALETA["teal"], width=0.55, zorder=3)
    ax.bar_label(bars, fmt="%.1f k", padding=5, color=PALETA["navy"], fontweight="bold", fontsize=10)

    ax.set_title("Teletrabajadores formales en Colombia (miles)", fontsize=14,
                 color=PALETA["navy"], fontweight="bold", pad=14)
    ax.set_ylabel("Miles de trabajadores", color=PALETA["gray"])
    ax.tick_params(colors=PALETA["gray"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(PALETA["gray"])
    ax.yaxis.grid(True, color="#E2E8F0", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)

    # Anotación crecimiento
    ax.annotate("+565 %\n(2012 → 2023)", xy=(4, vals.iloc[-1]),
                xytext=(3.3, 230), fontsize=10, color=PALETA["gold"],
                fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=PALETA["gold"]))

    ax.text(0.99, 0.02, "* 2023 estimado — Impacto TIC 2024",
            transform=ax.transAxes, fontsize=8, color=PALETA["gray"],
            ha="right", style="italic")

    plt.tight_layout()
    if guardar:
        plt.savefig("grafica_evolucion_teletrabajadores.png", dpi=150, bbox_inches="tight")
        print("  → grafica_evolucion_teletrabajadores.png")
    else:
        plt.show()
    plt.close()


def grafica_adopcion_empresas(guardar: bool = False):
    """Barras agrupadas — adopción por modalidad 2020 vs. 2023-2024."""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(PALETA["offwhite"])
    ax.set_facecolor("white")

    df = ADOPCION_EMPRESAS
    x = range(len(df))
    ancho = 0.35

    b1 = ax.bar([i - ancho / 2 for i in x], df["2020_pico_pandemia_pct"],
                width=ancho, label="2020 (pico pandemia)", color=PALETA["teal"], zorder=3)
    b2 = ax.bar([i + ancho / 2 for i in x], df["2023_2024_pospandemia_pct"],
                width=ancho, label="2023–2024 (pospandemia)", color=PALETA["gold"], zorder=3)

    ax.bar_label(b1, fmt="%d %%", padding=4, color=PALETA["navy"], fontsize=9)
    ax.bar_label(b2, fmt="%d %%", padding=4, color=PALETA["navy"], fontsize=9)

    ax.set_xticks(list(x))
    ax.set_xticklabels(df["Modalidad"], color=PALETA["gray"])
    ax.set_ylabel("% de empresas", color=PALETA["gray"])
    ax.set_title("Adopción de modalidades laborales en Colombia\n2020 vs. 2023–2024",
                 fontsize=13, color=PALETA["navy"], fontweight="bold")
    ax.tick_params(colors=PALETA["gray"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color="#E2E8F0", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, labelcolor=PALETA["gray"])

    plt.tight_layout()
    if guardar:
        plt.savefig("grafica_adopcion_empresas.png", dpi=150, bbox_inches="tight")
        print("  → grafica_adopcion_empresas.png")
    else:
        plt.show()
    plt.close()


def grafica_percepcion_trabajadores(guardar: bool = False):
    """Barras horizontales — percepciones de trabajadores."""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(PALETA["offwhite"])
    ax.set_facecolor("white")

    df = PERCEPCION_TRABAJADORES.sort_values("Porcentaje")
    colores = [PALETA["teal"] if p >= 70 else PALETA["navy"] for p in df["Porcentaje"]]

    bars = ax.barh(range(len(df)), df["Porcentaje"], color=colores, height=0.55, zorder=3)
    ax.bar_label(bars, fmt="%.1f %%", padding=6, color=PALETA["navy"], fontweight="bold", fontsize=10)

    ax.set_yticks(range(len(df)))
    etiquetas = [t if len(t) <= 48 else t[:46] + "…" for t in df["Indicador"]]
    ax.set_yticklabels(etiquetas, color=PALETA["gray"], fontsize=9)
    ax.set_xlabel("Porcentaje (%)", color=PALETA["gray"])
    ax.set_title("Percepción de los trabajadores colombianos\nsobre modalidades de trabajo",
                 fontsize=13, color=PALETA["navy"], fontweight="bold")
    ax.tick_params(colors=PALETA["gray"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.xaxis.grid(True, color="#E2E8F0", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(0, 110)

    plt.tight_layout()
    if guardar:
        plt.savefig("grafica_percepcion_trabajadores.png", dpi=150, bbox_inches="tight")
        print("  → grafica_percepcion_trabajadores.png")
    else:
        plt.show()
    plt.close()


def grafica_torta_empresarios(guardar: bool = False):
    """Torta — preferencia de modelo por parte de empresarios."""
    fig, ax = plt.subplots(figsize=(7, 6))
    fig.patch.set_facecolor(PALETA["offwhite"])

    colores = [PALETA["teal"], PALETA["navy"], PALETA["gold"]]
    explode = (0.03, 0.03, 0.03)

    wedges, texts, autotexts = ax.pie(
        PERCEPCION_EMPRESARIOS["Porcentaje"],
        labels=PERCEPCION_EMPRESARIOS["Modelo"],
        autopct="%1.0f %%",
        colors=colores,
        explode=explode,
        startangle=90,
        textprops={"color": "white", "fontweight": "bold", "fontsize": 11},
    )
    for t in texts:
        t.set_color(PALETA["gray"])
        t.set_fontsize(11)

    ax.set_title("Preferencia de modelo laboral — Empresas\n(Cornerstone, 2024 — Colombia/Latinoamérica)",
                 fontsize=12, color=PALETA["navy"], fontweight="bold")

    plt.tight_layout()
    if guardar:
        plt.savefig("grafica_torta_empresarios.png", dpi=150, bbox_inches="tight")
        print("  → grafica_torta_empresarios.png")
    else:
        plt.show()
    plt.close()


def grafica_sector_publico(guardar: bool = False):
    """Barras horizontales — distribución en sector público."""
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor(PALETA["offwhite"])
    ax.set_facecolor("white")

    df = SECTOR_PUBLICO
    colores = [PALETA["teal"], PALETA["navy"], PALETA["gold"]]

    bars = ax.barh(df["Modalidad"], df["Porcentaje"],
                   color=colores, height=0.45, zorder=3)
    ax.bar_label(bars, fmt="%d %%", padding=6, color=PALETA["navy"],
                 fontweight="bold", fontsize=12)

    ax.set_xlabel("% de servidores públicos", color=PALETA["gray"])
    ax.set_title("Distribución de modalidades en entidades públicas\n(MinTIC Estudio Percepción 2021)",
                 fontsize=12, color=PALETA["navy"], fontweight="bold")
    ax.tick_params(colors=PALETA["gray"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.xaxis.grid(True, color="#E2E8F0", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(0, 70)

    plt.tight_layout()
    if guardar:
        plt.savefig("grafica_sector_publico.png", dpi=150, bbox_inches="tight")
        print("  → grafica_sector_publico.png")
    else:
        plt.show()
    plt.close()


# ─── EXPORTACIÓN ─────────────────────────────────────────────────────────

def exportar_excel(ruta: str = "diagnostico_modalidades_trabajo_colombia.xlsx"):
    """Exporta todos los datasets a un archivo Excel con hojas nombradas."""
    hojas = {
        "Teletrabajadores": TELETRABAJADORES,
        "Normatividad": NORMATIVIDAD,
        "Adopcion_Empresas": ADOPCION_EMPRESAS,
        "Percepcion_Trabajadores": PERCEPCION_TRABAJADORES,
        "Percepcion_Empresarios": PERCEPCION_EMPRESARIOS,
        "Sector_Publico": SECTOR_PUBLICO,
        "Diagnostico_Integral": DIAGNOSTICO,
    }
    with pd.ExcelWriter(ruta, engine="openpyxl") as writer:
        for hoja, df in hojas.items():
            df.to_excel(writer, sheet_name=hoja, index=False)
    print(f"✅ Excel exportado: {ruta}")


def exportar_csv(directorio: str = "."):
    """Exporta cada dataset como CSV independiente."""
    p = Path(directorio)
    p.mkdir(exist_ok=True)
    datasets = {
        "teletrabajadores": TELETRABAJADORES,
        "normatividad": NORMATIVIDAD,
        "adopcion_empresas": ADOPCION_EMPRESAS,
        "percepcion_trabajadores": PERCEPCION_TRABAJADORES,
        "percepcion_empresarios": PERCEPCION_EMPRESARIOS,
        "sector_publico": SECTOR_PUBLICO,
        "diagnostico_integral": DIAGNOSTICO,
    }
    for nombre, df in datasets.items():
        ruta = p / f"colombia_trabajo_{nombre}.csv"
        df.to_csv(ruta, index=False, encoding="utf-8-sig")
        print(f"  → {ruta}")
    print("✅ CSVs exportados")


# ─── RESUMEN CONSOLA ──────────────────────────────────────────────────────

def imprimir_resumen():
    separador = "=" * 70

    print(f"\n{separador}")
    print("  DIAGNÓSTICO — MODALIDADES DE TRABAJO EN COLOMBIA 2020-2025")
    print(separador)

    print("\n📋 MARCO NORMATIVO")
    print(NORMATIVIDAD[["Año", "Norma", "Modalidad", "Objeto"]].to_string(index=False))

    print(f"\n{separador}")
    print("\n📈 EVOLUCIÓN TELETRABAJADORES FORMALES")
    df_evol = TELETRABAJADORES.copy()
    df_evol["Var_%"] = df_evol["Teletrabajadores_miles"].pct_change().mul(100).round(1)
    print(df_evol.to_string(index=False))

    print(f"\n{separador}")
    print("\n🏢 ADOPCIÓN DE MODALIDADES — EMPRESAS COLOMBIANAS")
    print(ADOPCION_EMPRESAS.to_string(index=False))

    print(f"\n{separador}")
    print("\n👤 PERCEPCIÓN DE TRABAJADORES")
    print(PERCEPCION_TRABAJADORES[["Indicador", "Porcentaje", "Fuente"]].to_string(index=False))

    print(f"\n{separador}")
    print("\n🏛️  SECTOR PÚBLICO — DISTRIBUCIÓN DE MODALIDADES")
    print(SECTOR_PUBLICO.to_string(index=False))

    print(f"\n{separador}")
    print("\n🔍 DIAGNÓSTICO INTEGRAL POR MODALIDAD")
    print(DIAGNOSTICO.to_string(index=False))

    print(f"\n{separador}")
    print("\n📌 CONCLUSIONES CLAVE")
    conclusiones = [
        "Colombia pasó de 1 a 4 modalidades formales reguladas entre 2008 y 2024.",
        "El teletrabajo creció +565 % entre 2012 y 2023 (31.5 k → ~252 k trabajadores).",
        "La pandemia impulsó el trabajo en casa al 43 % de empresas en 2020.",
        "El retorno presencial fue dominante en 2022-2023 (82 % del mercado).",
        "El modelo híbrido es el nuevo consenso: 59-63 % de preferencia en 2025.",
        "Alta informalidad (55,9 %) limita la adopción real de modalidades remotas.",
        "Reto: actualizar estudios oficiales y unificar el régimen no presencial.",
    ]
    for i, c in enumerate(conclusiones, 1):
        print(f"  {i}. {c}")

    print(f"\n{separador}\n")


# ─── MAIN ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Diagnóstico Modalidades de Trabajo Colombia 2020-2025"
    )
    parser.add_argument("--export-excel",  action="store_true",
                        help="Exportar todos los datos a Excel")
    parser.add_argument("--export-csv",    action="store_true",
                        help="Exportar cada dataset como CSV")
    parser.add_argument("--solo-graficas", action="store_true",
                        help="Mostrar gráficas en pantalla sin guardar")
    parser.add_argument("--guardar-graficas", action="store_true",
                        help="Guardar todas las gráficas como PNG")
    args = parser.parse_args()

    # Siempre imprime resumen en consola
    imprimir_resumen()

    guardar = args.guardar_graficas

    if not args.solo_graficas:
        # Por defecto muestra gráficas en pantalla a menos que se indique lo contrario
        pass

    print("📊 Generando gráficas...")
    grafica_evolucion_teletrabajadores(guardar=guardar)
    grafica_adopcion_empresas(guardar=guardar)
    grafica_percepcion_trabajadores(guardar=guardar)
    grafica_torta_empresarios(guardar=guardar)
    grafica_sector_publico(guardar=guardar)

    if args.export_excel:
        print("\n💾 Exportando a Excel...")
        exportar_excel()

    if args.export_csv:
        print("\n💾 Exportando a CSV...")
        exportar_csv()

    print("\n✅ Proceso completado.")


if __name__ == "__main__":
    main()
