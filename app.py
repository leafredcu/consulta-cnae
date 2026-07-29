import streamlit as st
import pandas as pd
import re

# Configuração da página (sem ícone de lupa)
st.set_page_config(page_title="Sistema CNAE", layout="centered")

# 1. Injeção de CSS para o design corporativo e elegante
st.markdown("""
    <style>
    /* Muda a fonte de todo o sistema para um padrão mais limpo e profissional */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Fundo levemente acinzentado para delimitar a área do programa */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Estilo do Título Oficial */
    .titulo-oficial {
        color: #1e293b;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 0px;
        padding-bottom: 15px;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .subtitulo {
        color: #64748b; 
        font-size: 16px; 
        margin-top: 10px;
        margin-bottom: 30px;
    }
    
    /* Arredondando e estilizando a caixa de pesquisa (inspirado no anexo) */
    div[data-baseweb="input"] {
        border-radius: 25px !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        padding: 2px 10px;
    }
    
    /* Arredondando e escurecendo o botão de busca */
    div[data-testid="stButton"] > button {
        border-radius: 25px !important;
        background-color: #333333 !important;
        color: white !important;
        border: none !important;
        height: 45px;
        font-weight: 600;
        transition: 0.3s;
    }
    
    /* Cor do botão quando passa o mouse */
    div[data-testid="stButton"] > button:hover {
        background-color: #000000 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Cabeçalho limpo
st.markdown("<div class='titulo-oficial'>Consulta de CNAEs e Resoluções</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>Sistema integrado para verificação de atividades e dispensas</div>", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    df = pd.read_excel("cnaes_tributos.xlsx")
    df['CNAE'] = df['CNAE'].astype(str)
    df['Descrição'] = df['Descrição'].astype(str)
    df['CNAE_limpo'] = df['CNAE'].str.replace(r'[\.\-\/]', '', regex=True)
    return df

try:
    df = carregar_dados()
except FileNotFoundError:
    st.error("Arquivo 'cnaes_tributos.xlsx' não encontrado no repositório.")
    st.stop()

# 3. Layout da barra de pesquisa
col1, col2 = st.columns([4, 1])

with col1:
    # label_visibility="collapsed" some com o texto acima da caixa, deixando igual ao seu print
    termo_busca = st.text_input("Busca", placeholder="Digite o CNAE ou palavra-chave...", label_visibility="collapsed")

with col2:
    botao_buscar = st.button("Buscar", use_container_width=True)

# 4. Lógica que roda ao apertar Enter ou clicar no botão
if termo_busca or botao_buscar:
    if termo_busca:
        termo_limpo = re.sub(r'[\.\-\/]', '', termo_busca)
        palavras = termo_busca.split()
        
        mascara_descricao = pd.Series(True, index=df.index)
        for palavra in palavras:
            mascara_descricao = mascara_descricao & df["Descrição"].str.contains(palavra, case=False, na=False, regex=False)
            
        mascara_cnae = df["CNAE_limpo"].str.contains(termo_limpo, case=False, na=False, regex=False)
        filtro = df[mascara_descricao | mascara_cnae]
        
        st.write("") # Dá um respiro visual antes da tabela
        
        if filtro.empty:
            st.warning(f"Nenhum registro encontrado para '{termo_busca}'.")
        else:
            st.markdown(f"<p style='color: #334155; font-weight: 600;'>{len(filtro)} resultado(s) encontrado(s):</p>", unsafe_allow_html=True)
            filtro_para_mostrar = filtro.drop(columns=['CNAE_limpo'], errors='ignore')
            st.dataframe(filtro_para_mostrar, use_container_width=True, hide_index=True)
