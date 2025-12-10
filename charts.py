import io
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# Utility: Convert matplotlib fig to bytes
# ------------------------------
def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return buf

# ------------------------------
# 1) Last Month Chart
# ------------------------------
def chart_last_month(df):
    latest_month_id = df['month_id'].max()
    df_latest_month = df[df['month_id'] == latest_month_id]

    total_revenue = df_latest_month[['rev_sp_saas', 'rev_sp_h', 'rev_sp_o', 'rev_cl_eur', 'rev_br_eur']].sum().sum()
    total_costs = df_latest_month['costs'].iloc[0]
    profit_loss = total_revenue - total_costs

    fig, ax = plt.subplots(figsize=(12, 5))

    # Revenue bar
    ax.barh(1.5, total_revenue)
    ax.text(total_revenue, 1.5, f"{total_revenue:,.2f}")

    # Costs + Profit bar
    if profit_loss >= 0:
        ax.barh(0.5, total_costs, color='red')
        ax.barh(0.5, profit_loss, left=total_costs, color='green')
        ax.text(total_costs / 2, 0.5, f"{total_costs:,.2f}", ha="center")
        ax.text(total_costs + profit_loss / 2, 0.5, f"{profit_loss:,.2f}", ha="center")
    else:
        ax.barh(0.5, total_costs, color='red')
        ax.text(total_costs, 0.5, f"{total_costs:,.2f}")
        text_x = total_revenue + (total_costs - total_revenue) / 2
        ax.text(text_x, 1.0, f"Loss: {abs(profit_loss):,.2f}")

    ax.set_yticks([0.5, 1.5])
    ax.set_yticklabels(['Costs & EBITDAC', 'Total Revenue'])
    ax.set_title("Financial Performance – Last Month")
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    return fig_to_bytes(fig)

# ------------------------------
# 2) Last 12 months Chart
# ------------------------------
def chart_last_12(df):
    df = df.copy()
    total_rev = df[['rev_sp_saas', 'rev_sp_h', 'rev_sp_o', 'rev_cl_eur', 'rev_br_eur']].sum().sum()
    total_costs = df['costs'].sum()
    profit_loss = total_rev - total_costs

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.barh(1.5, total_rev)
    ax.barh(0.5, total_costs, color='red')
    if profit_loss >= 0:
        ax.barh(0.5, profit_loss, left=total_costs, color='green')

    ax.set_yticks([0.5, 1.5])
    ax.set_yticklabels(['Costs & EBITDAC', 'Total Revenue'])
    ax.set_title("Financial Performance – Last 12 Months")
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    return fig_to_bytes(fig)

# ------------------------------
# 3) Natural Year Chart
# ------------------------------
def chart_natural_year(df):
    fig, ax = plt.subplots(figsize=(12, 5))

    total_rev = df[['rev_sp_saas', 'rev_sp_h', 'rev_sp_o', 'rev_cl_eur', 'rev_br_eur']].sum().sum()
    total_costs = df['costs'].sum()
    profit_loss = total_rev - total_costs

    ax.barh(1.5, total_rev)
    ax.barh(0.5, total_costs, color='red')
    if profit_loss >= 0:
        ax.barh(0.5, profit_loss, left=total_costs, color='green')

    ax.set_yticks([0.5, 1.5])
    ax.set_yticklabels(['Costs & EBITDAC', 'Total Revenue'])
    ax.set_title("Financial Performance – Natural Year")
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    return fig_to_bytes(fig)

# ------------------------------
# 4) % Growth Chart
# ------------------------------
def chart_growth(df_last12):
    df = df_last12.sort_values("month_year").copy()

    df['rev_sp_saas_growth'] = df['rev_sp_saas'].pct_change() * 100
    df['rev_cl_growth'] = df['rev_cl'].pct_change() * 100
    df['rev_br_growth'] = df['rev_br'].pct_change() * 100

    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(df['month_year'], df['rev_sp_saas_growth'], marker='o', label='Spain')
    ax.plot(df['month_year'], df['rev_cl_growth'], marker='o', label='Chile')
    ax.plot(df['month_year'], df['rev_br_growth'], marker='o', label='Brazil')

    ax.axhline(0, linestyle='--')
    ax.set_title("Revenue Growth % – Last 12 Months")
    ax.set_ylabel("Growth %")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()

    return fig_to_bytes(fig)
