import streamlit as st
import pandas as pd
import re

# Configuração visual da página
st.set_page_config(page_title="Busca de CNAEs", layout="wide")
st.title("🔍 Consulta de CNAEs e Resoluções")
st.write("Digite o código CNAE (com ou sem pontuação) ou uma palavra da descrição.")

# Função para carregar o seu arquivo externo de Excel
@st.cache_data
def carregar_dados():
    # Aqui o programa vai ler o arquivo que você vai colocar lá no GitHub.
    # O nome precisa estar exatamente igual ao do arquivo (cuidado com maiúsculas/minúsculas).
    df = pd.read_excel("cnaes_tributos.xlsx")
    
    # Garantir que as colunas sejam texto para não dar erro na busca
    df['CNAE'] = df['CNAE'].astype(str)
    df['Descrição'] = df['Descrição'].astype(str)
    
    # Cria uma coluna "invisível" limpando pontos, traços e barras do CNAE
    # Isso permite que a pessoa busque "0111301" e o sistema encontre o "0111-3/01"
    df['CNAE_limpo'] = df['CNAE'].str.replace(r'[\.\-\/]', '', regex=True)
    
    return df

# Tenta carregar os dados. Se o arquivo não estiver lá, avisa de forma amigável.
try:
    df = carregar_dados()
except FileNotFoundError:
    st.error("⚠️ O arquivo 'cnaes_tributos.xlsx' não foi encontrado. Lembre-se de subi-lo no GitHub junto com este código.")
    st.stop()

# Campo de busca
termo_busca = st.text_input("Pesquisar:")

if termo_busca:
    # Limpa a pontuação do que o usuário digitou (caso seja um número de CNAE)
    termo_limpo = re.sub(r'[\.\-\/]', '', termo_busca)
    
    # Filtra a planilha: busca na descrição normal OU no CNAE limpo
    filtro = df[
        df["Descrição"].str.contains(termo_busca, case=False, na=False) | 
        df["CNAE_limpo"].str.contains(termo_limpo, case=False, na=False)
    ]
    
    if filtro.empty:
        st.warning(f"Nenhum resultado encontrado para a busca '{termo_busca}'.")
    else:
        # Define as colunas exatas que vão aparecer na tela pro usuário
        colunas_para_mostrar = [
            "CNAE", 
            "Descrição", 
            "Resolução: nº 04/2025", 
            "Resolução: nº 05/2025"
        ]
        
        st.subheader("Resultados:")
        # Mostra a tabela filtrada e esconde aquela coluna chata de índice (0, 1, 2...)
        st.dataframe(filtro[colunas_para_mostrar], use_container_width=True, hide_index=True)
