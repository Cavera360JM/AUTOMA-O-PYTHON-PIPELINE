import streamlit as st
import pandas as pd
from src.processor import DataPipeline
from src.generator import generate_fake_data
from src.database import MySQLConnection # Nova integração
import os

st.markdown("""
    <style>
    .stMetric {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    [data-testid="stSidebar"] {
        background-color: #0f172a;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="DataOps Hub - MySQL Edition", layout="wide")

st.title("🚀 Pipeline de Dados: CSV → MySQL → Dashboard")

# Instancia a conexão
db = MySQLConnection()

if st.sidebar.button("Executar ETL Completo"):
    with st.status("Processando Pipeline...", expanded=True) as status:
        # 1. Gera dados fictícios
        RAW_PATH = "data/raw_sales.csv"
        if not os.path.exists("data"): os.makedirs("data")
        generate_fake_data(RAW_PATH, num_rows=200)
        
        # 2. Processamento via Classe Sênior
        pipeline = DataPipeline(RAW_PATH, type='csv')
        pipeline.extract().transform()
        
        # 3. Envio para o MySQL (O diferencial)
        st.write("Enviando dados para o MySQL (localhost)...")
        db.save_data(pipeline.df)
        
        st.session_state['data_ready'] = True
        status.update(label="Carga no MySQL concluída!", state="complete")

# Exibição de Insights vindos do BANCO DE DADOS
if st.session_state.get('data_ready'):
    df_db = db.get_data()
    df_db['transaction_date'] = pd.to_datetime(df_db['transaction_date'])

    # --- FILTROS NA BARRA LATERAL ---
    st.sidebar.markdown("### Filtros de Análise")
    produtos = st.sidebar.multiselect("Filtrar por Produto", options=df_db['product'].unique(), default=df_db['product'].unique())
    df_filtrado = df_db[df_db['product'].isin(produtos)]

    # --- LINHA 1: KPIs RESUMO (HIGH LEVEL) ---
    st.subheader("🎯 Indicadores Chave de Performance (KPIs)")
    k1, k2, k3, k4 = st.columns(4)
    
    receita_total = df_filtrado['total_price'].sum()
    lucro_estimado = df_filtrado['net_revenue'].sum()
    imposto_total = df_filtrado['tax_amount'].sum()
    ticket_medio = df_filtrado['total_price'].mean()

    k1.metric("Faturamento Bruto", f"R$ {receita_total:,.2f}")
    k2.metric("Lucro Líquido", f"R$ {lucro_estimado:,.2f}", delta=f"{(lucro_estimado/receita_total)*100:.1f}% Margem")
    k3.metric("Impostos (18%)", f"R$ {imposto_total:,.2f}", delta_color="inverse")
    k4.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

    st.divider()

    # --- LINHA 2: ANÁLISE TEMPORAL E DISTRIBUIÇÃO ---
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("📅 Evolução Diária de Vendas")
        # Agrupando por dia para um gráfico limpo
        vendas_diarias = df_filtrado.set_index('transaction_date')['total_price'].resample('D').sum().reset_index()
        st.area_chart(vendas_diarias.set_index('transaction_date'), color="#29b5e8")

    with c2:
        st.subheader("📦 Participação por Produto")
        pizza_data = df_filtrado.groupby('product')['total_price'].sum()
        st.write("Volume Financeiro por Categoria")
        st.bar_chart(pizza_data, horizontal=True)

    st.divider()

    # --- LINHA 3: DETALHAMENTO TÉCNICO ---
    st.subheader("🔍 Auditoria de Transações")
    aba_dados, aba_estatistica = st.tabs(["Tabela de Dados", "Análise Estatística"])
    
    with aba_dados:
        st.dataframe(df_filtrado.sort_values(by='transaction_date', ascending=False), use_container_width=True)
    
    with aba_estatistica:
        st.write("Resumo Estatístico das Operações:")
        st.table(df_filtrado[['quantity', 'total_price', 'tax_amount', 'net_revenue']].describe())