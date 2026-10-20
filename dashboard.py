"""Dashboard interativo de temperaturas com Streamlit e Plotly."""
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text
from src.db import get_engine

st.set_page_config(page_title="Dashboard IoT", page_icon="🌡️", layout="wide")
st.title("🌡️ Dashboard de Temperaturas IoT")
st.caption("Leituras de sensores processadas com Python e armazenadas no PostgreSQL.")

@st.cache_data(ttl=30)
def load_data(query: str) -> pd.DataFrame:
    with get_engine().connect() as conn:
        return pd.read_sql(text(query), conn)

try:
    resumo = load_data("SELECT * FROM resumo_dataset")
    if resumo.empty or int(resumo.iloc[0]["total_leituras"]) == 0:
        st.warning("Ainda não há leituras no banco. Execute primeiro: python -m src.ingest")
        st.stop()

    r = resumo.iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Leituras armazenadas", f"{int(r['total_leituras']):,}".replace(",", "."))
    c2.metric("Ambientes identificados", int(r["total_dispositivos"]))
    c3.metric("Período de dados", f"{pd.to_datetime(r['primeira_leitura']).date()} a {pd.to_datetime(r['ultima_leitura']).date()}")

    st.subheader("Média de temperatura por ambiente")
    df_avg = load_data("SELECT * FROM avg_temp_por_dispositivo ORDER BY device_id")
    fig1 = px.bar(df_avg, x="device_id", y="avg_temp", hover_data=["min_temp", "max_temp", "total_leituras"],
                  labels={"device_id": "Ambiente", "avg_temp": "Temperatura média (°C)"},
                  title="Temperatura média por ambiente")
    st.plotly_chart(fig1, width="stretch")

    st.subheader("Distribuição das leituras por hora")
    df_hour = load_data("SELECT * FROM leituras_por_hora ORDER BY hora")
    fig2 = px.bar(df_hour, x="hora", y="contagem",
                  labels={"hora": "Hora do dia", "contagem": "Quantidade de leituras"},
                  title="Quantidade de leituras por hora")
    st.plotly_chart(fig2, width="stretch")

    st.subheader("Temperaturas máximas, mínimas e médias por dia")
    df_day = load_data("SELECT * FROM temp_max_min_por_dia ORDER BY data")
    long_day = df_day.melt(id_vars=["data"], value_vars=["temp_max", "temp_min", "temp_media"],
                           var_name="medida", value_name="temperatura")
    fig3 = px.line(long_day, x="data", y="temperatura", color="medida", markers=True,
                   labels={"data": "Data", "temperatura": "Temperatura (°C)", "medida": "Métrica"},
                   title="Variação diária da temperatura")
    st.plotly_chart(fig3, width="stretch")

    with st.expander("Consultar dados agregados"):
        st.dataframe(df_avg, width="stretch")
        st.dataframe(df_day, width="stretch")

except Exception as exc:
    st.error("Não foi possível consultar o PostgreSQL. Verifique se o Docker está ativo, se o CSV já foi processado e se as views foram criadas.")
    st.code(str(exc))
