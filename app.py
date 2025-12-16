import streamlit as st
import pandas as pd
from supabase_client import get_supabase
from charts import (
    chart_last_month,
    chart_natural_year,
    chart_revenue_per_country
)

st.title("Financial Metrics – Admin Panel")

supabase = get_supabase()

# ==================================================
# FORM
# ==================================================
st.header("Insert / Update Month Data")

with st.form("finance_form"):
    month_year = st.text_input("Month (YYYY-MM)")
    rev_sp_saas = st.number_input("Revenue Spain SaaS", min_value=0.0)
    rev_sp_h = st.number_input("Revenue Spain H", min_value=0.0)
    rev_sp_o = st.number_input("Revenue Spain Other", min_value=0.0)
    rev_cl = st.number_input("Revenue Chile Local", min_value=0.0)
    rev_cl_eur = st.number_input("Revenue Chile EUR", min_value=0.0)
    rev_br = st.number_input("Revenue Brazil Local", min_value=0.0)
    rev_br_eur = st.number_input("Revenue Brazil EUR", min_value=0.0)
    costs = st.number_input("Costs", min_value=0.0)
    f_rev = st.number_input("Forecast Revenue", min_value=0.0)
    f_costs = st.number_input("Forecast Costs", min_value=0.0)

    submitted = st.form_submit_button("Submit")

if submitted:
    if not month_year.strip():
        st.error("Month (YYYY-MM) cannot be empty.")
        st.stop()

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

    supabase.table("financial_metrics").upsert(data).execute()
    st.success("Data inserted / updated successfully!")

# ==================================================
# LOAD DATA
# ==================================================
response = supabase.table("financial_metrics").select("*").execute()
df = pd.DataFrame(response.data)

if not df.empty:
    st.header("Charts")

    # ------------------------------
    # Last month
    # ------------------------------
    st.subheader("Last Month")
    st.download_button(
        "Download PNG",
        chart_last_month(df),
        "last_month.png"
    )

    # ------------------------------
    # Natural year
    # ------------------------------
    st.subheader("Natural Year")
    st.download_button(
        "Download PNG",
        chart_natural_year(df),
        "natural_year.png"
    )

    # ------------------------------
    # Revenue per country
    # ------------------------------
    st.subheader("Revenue per Country (Last 12 Months)")
    st.download_button(
        "Download PNG",
        chart_revenue_per_country(df),
        "revenue_per_country.png"
    )
