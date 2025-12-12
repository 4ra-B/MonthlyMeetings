import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ------------------------------------
# Utilidad: convertir figura a bytes
# ------------------------------------
def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return buf


# ================================================================
# 1) LAST MONTH — REAL VS FORECAST
# ================================================================
def chart_last_month(df):
    latest_month_id = df["month_id"].max()
    df_latest = df[df["month_id"] == latest_month_id]

    # Real values
    real_rev = df_latest[['rev_sp_saas','rev_sp_h','rev_sp_o','rev_cl_eur','rev_br_eur']].sum().sum()
    real_costs = df_latest["costs"].iloc[0]
    real_ebitdac = real_rev - real_costs

    # Forecast
    f_rev = df_latest["f_rev"].iloc[0]
    f_costs = df_latest["f_costs"].iloc[0]
    f_ebitdac = f_rev - f_costs

    palette = ["#1C91DD", "#949494", "#22AD5C"]

    fig, ax = plt.subplots(figsize=(15, 7))

    # Real revenue
    ax.barh(2, real_rev, height=0.6, color=palette[0])
    ax.text(real_rev, 2, f" {real_rev:,.2f}")

    # Real costs + EBITDAC
    if real_ebitdac >= 0:
        ax.barh(1, real_costs, height=0.6, color=palette[1])
        ax.barh(1, real_ebitdac, height=0.6, left=real_costs, color=palette[2])

        ax.text(real_costs / 2, 1, f"{real_costs:,.2f}", ha="center")
        ax.text(real_costs + real_ebitdac / 2, 1, f"{real_ebitdac:,.2f}", ha="center", color="white")
    else:
        ax.barh(1, real_costs, height=0.6, color=palette[2])
        ax.text(real_costs, 1, f"{real_costs:,.2f}")

    # Forecast revenue
    ax.barh(0, f_rev, height=0.6, color=palette[0])
    ax.text(f_rev, 0, f" {f_rev:,.2f}")

    # Forecast costs + EBITDAC
    if f_ebitdac >= 0:
        ax.barh(-1, f_costs, height=0.6, color=palette[1])
        ax.barh(-1, f_ebitdac, height=0.6, left=f_costs, color=palette[2])

        ax.text(f_costs / 2, -1, f"{f_costs:,.2f}", ha="center")
        ax.text(f_costs + f_ebitdac / 2, -1, f"{f_ebitdac:,.2f}", ha="center", color="white")
    else:
        ax.barh(-1, f_costs, height=0.6, color=palette[1])
        ax.text(f_costs, -1, f" {f_costs:,.2f}")

    ax.set_yticks([-1, 0, 1, 2])
    ax.set_yticklabels(["F Costs & EBITDAC", "F Revenue", "R Costs & EBITDAC", "R Revenue"])

    ax.set_title("Financial Performance – Last Month (Real vs Forecast)")
    ax.set_xlabel("Amount")

    max_x = max(real_rev, f_rev, real_costs, f_costs) * 1.1
    ax.set_xlim(0, max_x)

    ax.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()

    return fig_to_bytes(fig)


# ================================================================
# 2) NATURAL YEAR — REAL VS FORECAST
# ================================================================
def chart_natural_year(df):
    df = df.copy()
    df["month_year"] = pd.to_datetime(df["month_year"])

    df_sorted = df.sort_values("month_year")
    latest_month = df_sorted["month_year"].max()

    start_year = pd.to_datetime(f"{latest_month.year}-01-01")
    df_nat = df_sorted[df_sorted["month_year"] >= start_year]

    real_rev = df_nat[['rev_sp_saas','rev_sp_h','rev_sp_o','rev_cl_eur','rev_br_eur']].sum().sum()
    real_costs = df_nat["costs"].sum()
    real_ebitdac = real_rev - real_costs

    f_rev = df_nat["f_rev"].sum()
    f_costs = df_nat["f_costs"].sum()
    f_ebitdac = f_rev - f_costs

    palette = ["#1C91DD", "#949494", "#22AD5C"]

    fig, ax = plt.subplots(figsize=(15, 7))

    ax.barh(2, real_rev, height=0.6, color=palette[0])
    ax.text(real_rev, 2, f" {real_rev:,.2f}")

    if real_ebitdac >= 0:
        ax.barh(1, real_costs, height=0.6, color=palette[1])
        ax.barh(1, real_ebitdac, height=0.6, left=real_costs, color=palette[2])
    else:
        ax.barh(1, real_costs, height=0.6, color=palette[2])

    ax.barh(0, f_rev, height=0.6, color=palette[0])
    ax.text(f_rev, 0, f" {f_rev:,.2f}")

    if f_ebitdac >= 0:
        ax.barh(-1, f_costs, height=0.6, color=palette[1])
        ax.barh(-1, f_ebitdac, height=0.6, left=f_costs, color=palette[2])
    else:
        ax.barh(-1, f_costs, height=0.6, color=palette[1])

    ax.set_yticks([-1, 0, 1, 2])
    ax.set_yticklabels(["F Costs & EBITDAC", "F Revenue", "R Costs & EBITDAC", "R Revenue"])

    ax.set_title("Financial Performance – Natural Year (Real vs Forecast)")
    ax.set_xlabel("Amount")

    max_x = max(real_rev, f_rev, real_costs, f_costs) * 1.1
    ax.set_xlim(0, max_x)

    ax.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()

    return fig_to_bytes(fig)


# ================================================================
# 3) SaaS Revenue per Country (Últimos 12 meses)
# ================================================================
def chart_revenue_per_country(df):
    df = df.copy()
    df["month_year"] = pd.to_datetime(df["month_year"], format="%Y-%m")
    df_sorted = df.sort_values(by="month_year", ascending=True)

    latest_month_id = df_sorted["month_id"].max()
    if latest_month_id >= 12:
        df_last12 = df_sorted[df_sorted["month_id"] > (latest_month_id - 12)].copy()
    else:
        df_last12 = df_sorted.copy()

    palette = ["#1C91DD", "#e36e22", "#22AD5C"]

    fig, ax = plt.subplots(figsize=(18, 8))

    # Plot each country's revenue as a line with markers
    ax.plot(df_last12["month_year"], df_last12["rev_sp_saas"], label="España (SaaS)", marker="o", color=palette[0])
    ax.plot(df_last12["month_year"], df_last12["rev_cl_eur"], label="Chile", marker="o", color=palette[1])
    ax.plot(df_last12["month_year"], df_last12["rev_br_eur"], label="Brasil", marker="o", color=palette[2])

    ax.set_title("Ingresos por País en Euros (Últimos 12 Meses)")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Ingreso en Euros")
    ax.set_xticks(df_last12["month_year"])
    ax.set_xticklabels(df_last12["month_year"].dt.strftime("%Y-%m"), rotation=45, ha="right")

    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()

    return fig_to_bytes(fig)
