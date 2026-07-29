import streamlit as st
import pandas as pd
import re

# 1. Configuração visual (ícone na aba e layout centralizado ficam mais elegantes)
st.set_page_config(page_title="Sistema CNAE", page_icon="🏢", layout="centered")

# 2. Cabeçalho customizado (dá uma cara de sistema oficial e moderno)
st.markdown("<h1 style='text-align: center; color: #1f4e79;'>🔍 Consulta de CNAEs e Resoluções</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #555;'>Sistema rápido para verificação de atividades e dispensas</p>", unsafe_allow_html=True)
st.divider()

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
    st.error("⚠️ O arquivo 'cnaes_tributos.xlsx' não foi encontrado. Lembre-se de subi-lo no GitHub.")
    st.stop()

# 3. Criando colunas para alinhar o campo de busca e o botão lado a lado
col1, col2 = st.columns([4, 1])

with col1:
    # O placeholder deixa uma dica clarinha dentro da caixa antes da pessoa digitar
    termo_busca = st.text_input("O que você procura hoje?", placeholder="Ex: 0111-3/01 ou transporte...")

with col2:
    # Esses espaços vazios ajudam a empurrar o botão para baixo, alinhando com a caixa de texto
    st.write("") 
    st.write("")
    # O type="primary" deixa o botão com cor de destaque
    botao_buscar = st.button("Pesquisar 🔎", use_container_width=True, type="primary")

# A busca acontece se a pessoa apertar Enter ou clicar no botão
if termo_busca:
    termo_limpo = re.sub(r'[\.\-\/]', '', termo_busca)
    palavras = termo_busca.split()
    
    mascara_descricao = pd.Series(True, index=df.index)
    for palavra in palavras:
        mascara_descricao = mascara_descricao & df["Descrição"].str.contains(palavra, case=False, na=False, regex=False)
        
    mascara_cnae = df["CNAE_limpo"].str.contains(termo_limpo, case=False, na=False, regex=False)
    filtro = df[mascara_descricao | mascara_cnae]
    
    st.divider() # Linha elegante para separar a área de busca dos resultados
    
    if filtro.empty:
        st.warning(f"Poxa, nenhum resultado encontrado para '{termo_busca}'. Tente buscar de outra forma.")
    else:
        # Feedback visual de quantos resultados foram achados
        st.success(f"Busca concluída! Encontramos {len(filtro)} resultado(s).")
        
        # Mostra a tabela de forma limpa
        filtro_para_mostrar = filtro.drop(columns=['CNAE_limpo'], errors='ignore')
        st.dataframe(filtro_para_mostrar, use_container_width=True, hide_index=True)
else:
    # Quando o app abre (sem busca), mostra uma mensagem amigável em vez de uma tela em branco
    st.info("💡 Digite um código CNAE ou uma palavra-chave da descrição acima para começar a consulta.")
