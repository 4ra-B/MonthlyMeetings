import streamlit as st
from supabase import create_client, Client
import pandas as pd
import requests

# --------------------------
# CONFIGURACIÓN SUPABASE
# --------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("📊 Ingreso de Datos Financieros")


# --------------------------
# FORMULARIO
# --------------------------
with st.form("financial_form"):
    st.subheader("Completa los datos financieros del mes")

    month_year = st.text_input("month_year (ID único, formato YYYY-MM)")

    rev_sp_saas = st.number_input("Rev_Sp_Saas (ingresos por Saas en España)", min_value=0.0, step=0.01)
    rev_sp_h = st.number_input("Rev_Sp_H (ingresos por Hardware en España)", min_value=0.0, step=0.01)
    rev_sp_o = st.number_input("Rev_Sp_O (otros ingresos en España)", min_value=0.0, step=0.01)
    rev_cl = st.number_input("Rev_Cl (ingresos en Chile)", min_value=0.0, step=0.01)
    rev_br = st.number_input("Rev_Br (ingresos en Brasil)", min_value=0.0, step=0.01)

    costs = st.number_input("Costs (gastos)", min_value=0.0, step=0.01)
    f_rev = st.number_input("F_Rev (forecast de ingresos)", min_value=0.0, step=0.01)
    f_costs = st.number_input("F_Costs (forecast de gastos)", min_value=0.0, step=0.01)

    submitted = st.form_submit_button("Guardar datos y generar gráficos")


# --------------------------
# ENVÍO A SUPABASE (UPSERT)
# --------------------------
if submitted:
    if month_year.strip() == "":
        st.error("Debes completar el campo 'month_year'.")
        st.stop()

    data = {
        "month_year": month_year,
        "rev_sp_saas": rev_sp_saas,
        "rev_sp_h": rev_sp_h,
        "rev_sp_o": rev_sp_o,
        "rev_cl": rev_cl,
        "rev_br": rev_br,
        "costs": costs,
        "f_rev": f_rev,
        "f_costs": f_costs,
    }

    try:
        response = supabase.table("financial_metrics").upsert(data).execute()
        st.success("Datos guardados correctamente en Supabase (insert o update).")
    except Exception as e:
        st.error(f"Error guardando en Supabase: {e}")
        st.stop()


    # --------------------------
    # OPCIONAL: LLAMAR A COLAB PARA GENERAR GRÁFICOS
    # (Puedes conectar el notebook mediante un webhook o una API expuesta)
    # --------------------------

    # EJEMPLO: si tienes una URL pública del notebook/endpoint
    # colab_url = st.secrets.get("COLAB_WEBHOOK_URL")
    # if colab_url:
    #     res = requests.post(colab_url, json={"trigger": True})
    #     if res.status_code == 200:
    #         st.success("Gráficos generados. Puedes descargarlos aquí:")
    #         st.download_button("Descargar gráficos", res.content, "graficos.zip")
    #     else:
    #         st.warning("Datos guardados, pero no se pudieron generar los gráficos automáticamente.")


st.info("💡 Al guardar los datos, estos se sobrescriben si el month_year ya existía (upsert).")
