import streamlit as st
import pandas as pd
from supabase_client import get_supabase
from charts import chart_last_month, chart_natural_year, chart_revenue_per_country

st.title("Financial Metrics – Admin Panel")

supabase = get_supabase()

st.header("Insert / Update Month Data")

with st.form("finance_form"):
    month_year = st.text_input("Month (YYYY-MM)")
    rev_sp_saas = st.number_input("Revenue Spain SaaS")
    rev_sp_h = st.number_input("Revenue Spain H")
    rev_sp_o = st.number_input("Revenue Spain Other")
    rev_cl = st.number_input("Revenue Chile Local")
    rev_cl_eur = st.number_input("Revenue Chile EUR")
    rev_br = st.number_input("Revenue Brazil Local")
    rev_br_eur = st.number_input("Revenue Brazil EUR")
    costs = st.number_input("Costs")
    f_rev = st.number_input("Forecast Revenue")
    f_costs = st.number_input("Forecast Costs")
    submitted = st.form_submit_button("Submit")

if submitted:
    if month_year.strip() == "":
        st.error("Month (YYYY-MM) cannot be empty.")
        st.stop()

    # UPSERT
    data = {
        "month_year": month_year,
        "rev_sp_saas": rev_sp_saas,
        "rev_sp_h": rev_sp_h,
        "rev_sp_o": rev_sp_o,
        "rev_cl": rev_cl,
        "rev_cl_eur": rev_cl_eur,
        "rev_br": rev_br,
        "rev_br_eur": rev_br_eur,
        "costs": costs,
        "f_rev": f_rev,
        "f_costs": f_costs 
    }

    response = supabase.table("financial_metrics").upsert(data).execute()
    st.success("Data inserted/updated successfully!")

# ------------------------------
# Load table to generate charts
# ------------------------------
df = supabase.table("financial_metrics").select("*").execute().data
df = pd.DataFrame(df)

if len(df) > 0:
    st.header("Charts")

    # Last month
    st.subheader("Last Month")
    st.download_button("Download PNG", chart_last_month(df), "last_month.png")


    # Natural year
    st.subheader("Natural Year")
    current_year = df["month_year"].max()[:4]
    df_nat = df[df["month_year"].str.startswith(current_year)]
    st.download_button("Download PNG", chart_natural_year(df_nat), "natural_year.png")

    # Revenue
    st.subheader("Revenue per Country")
    latest_month_id = df_sorted["month_id"].max()
    df_last12 = df_sorted[df_sorted["month_id"] > latest_month_id - 12]
    st.download_button("Download PNG", chart_revenue_per_country(df_last12), "revenue.png")
