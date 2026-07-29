import streamlit as st
import pandas as pd
import re

# Configuração da página
st.set_page_config(page_title="Sistema CNAE", layout="centered")

# 1. Injeção de CSS (O visual da página)
st.markdown("""
    <style>
    /* Muda a fonte de todo o sistema */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* 1. O FUNDO TEXTURIZADO NAS LATERAIS */
    .stApp {
        background-color: #f0f4f8; 
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='192' height='192' viewBox='0 0 192 192'%3E%3Cpath fill='%239C92AC' fill-opacity='0.15' d='M192 15v2a11 11 0 0 0-11 11c0 1.94 1.16 4.75 2.53 6.11l2.36 2.36a6.93 6.93 0 0 1 1.22 7.56l-.43.84a8.08 8.08 0 0 1-6.66 4.13H145v35.02a6.1 6.1 0 0 0 3.03 4.87l.84.43c1.58.79 4 .4 5.24-.85l2.36-2.36a12.04 12.04 0 0 1 7.51-3.11 13 13 0 1 1 .02 26 12 12 0 0 1-7.53-3.11l-2.36-2.36a4.93 4.93 0 0 0-5.24-.85l-.84.43a6.1 6.1 0 0 0-3.03 4.87V143h35.02a8.08 8.08 0 0 1 6.66 4.13l.43.84a6.91 6.91 0 0 1-1.22 7.56l-2.36 2.36A10.06 10.06 0 0 0 181 164a11 11 0 0 0 11 11v2a13 13 0 0 1-13-13 12 12 0 0 1 3.11-7.53l2.36-2.36a4.93 4.93 0 0 0 .85-5.24l-.43-.84a6.1 6.1 0 0 0-4.87-3.03H145v35.02a8.08 8.08 0 0 1-4.13 6.66l-.84.43a6.91 6.91 0 0 1-7.56-1.22l-2.36-2.36A10.06 10.06 0 0 0 124 181a11 11 0 0 0-11 11h-2a13 13 0 0 1 13-13c2.47 0 5.79 1.37 7.53 3.11l2.36 2.36a4.94 4.94 0 0 0 5.24.85l.84-.43a6.1 6.1 0 0 0 3.03-4.87V145h-35.02a8.08 8.08 0 0 1-6.66-4.13l-.43-.84a6.91 6.91 0 0 1 1.22-7.56l2.36-2.36A10.06 10.06 0 0 0 107 124a11 11 0 0 0-22 0c0 1.94 1.16 4.75 2.53 6.11l2.36 2.36a6.93 6.93 0 0 1 1.22 7.56l-.43.84a8.08 8.08 0 0 1-6.66 4.13H49v35.02a6.1 6.1 0 0 0 3.03 4.87l.84.43c1.58.79 4 .4 5.24-.85l2.36-2.36a12.04 12.04 0 0 1 7.51-3.11A13 13 0 0 1 81 192h-2a11 11 0 0 0-11-11c-1.94 0-4.75 1.16-6.11 2.53l-2.36 2.36a6.93 6.93 0 0 1-7.56 1.22l-.84-.43a8.08 8.08 0 0 1-4.13-6.66V145H11.98a6.1 6.1 0 0 0-4.87 3.03l-.43.84c-.79 1.58-.4 4 .85 5.24l2.36 2.36a12.04 12.04 0 0 1 3.11 7.51A13 13 0 0 1 0 177v-2a11 11 0 0 0 11-11c0-1.94-1.16-4.75-2.53-6.11l-2.36-2.36a6.93 6.93 0 0 1-1.22-7.56l.43-.84a8.08 8.08 0 0 1 6.66-4.13H47v-35.02a6.1 6.1 0 0 0-3.03-4.87l-.84-.43c-1.59-.8-4-.4-5.24.85l-2.36 2.36A12 12 0 0 1 28 109a13 13 0 1 1 0-26c2.47 0 5.79 1.37 7.53 3.11l2.36 2.36a4.94 4.94 0 0 0 5.24.85l.84-.43A6.1 6.1 0 0 0 47 84.02V49H11.98a8.08 8.08 0 0 1-6.66-4.13l-.43-.84a6.91 6.91 0 0 1 1.22-7.56l2.36-2.36A10.06 10.06 0 0 0 11 28 11 11 0 0 0 0 17v-2a13 13 0 0 1 13 13c0 2.47-1.37 5.79-3.11 7.53l-2.36 2.36a4.94 4.94 0 0 0-.85 5.24l.43.84A6.1 6.1 0 0 0 11.98 47H47V11.98a8.08 8.08 0 0 1 4.13-6.66l.84-.43a6.91 6.91 0 0 1 7.56 1.22l2.36 2.36A10.06 10.06 0 0 0 68 11 11 11 0 0 0 79 0h2a13 13 0 0 1-13 13 12 12 0 0 1-7.53-3.11l-2.36-2.36a4.93 4.93 0 0 0-5.24-.85l-.84.43A6.1 6.1 0 0 0 49 11.98V47h35.02a8.08 8.08 0 0 1 6.66 4.13l.43.84a6.91 6.91 0 0 1-1.22 7.56l-2.36 2.36A10.06 10.06 0 0 0 85 68a11 11 0 0 0 22 0c0-1.94-1.16-4.75-2.53-6.11l-2.36-2.36a6.93 6.93 0 0 1-1.22-7.56l.43-.84a8.08 8.08 0 0 1 6.66-4.13H143V11.98a6.1 6.1 0 0 0-3.03-4.87l-.84-.43c-1.59-.8-4-.4-5.24.85l-2.36 2.36A12 12 0 0 1 124 13a13 13 0 0 1-13-13h2a11 11 0 0 0 11 11c1.94 0 4.75-1.16 6.11-2.53l2.36-2.36a6.93 6.93 0 0 1 7.56-1.22l.84.43a8.08 8.08 0 0 1 4.13 6.66V47h35.02a6.1 6.1 0 0 0 4.87-3.03l.43-.84c.8-1.59.4-4-.85-5.24l-2.36-2.36A12 12 0 0 1 179 28a13 13 0 0 1 13-13zM84.02 143a6.1 6.1 0 0 0 4.87-3.03l.43-.84c.8-1.59.4-4-.85-5.24l-2.36-2.36A12 12 0 0 1 83 124a13 13 0 1 1 26 0c0 2.47-1.37 5.79-3.11 7.53l-2.36 2.36a4.94 4.94 0 0 0-.85 5.24l.43.84a6.1 6.1 0 0 0 4.87 3.03H143v-35.02a8.08 8.08 0 0 1 4.13-6.66l.84-.43a6.91 6.91 0 0 1 7.56 1.22l2.36 2.36A10.06 10.06 0 0 0 164 107a11 11 0 0 0 0-22c-1.94 0-4.75 1.16-6.11 2.53l-2.36 2.36a6.93 6.93 0 0 1-7.56 1.22l-.84-.43a8.08 8.08 0 0 1-4.13-6.66V49h-35.02a6.1 6.1 0 0 0-4.87 3.03l-.43.84c-.79 1.58-.4 4 .85 5.24l2.36 2.36a12.04 12.04 0 0 1 3.11 7.51A13 13 0 1 1 83 68a12 12 0 0 1 3.11-7.53l2.36-2.36a4.93 4.93 0 0 0 .85-5.24l-.43-.84A6.1 6.1 0 0 0 84.02 49H49v35.02a8.08 8.08 0 0 1-4.13 6.66l-.84.43a6.91 6.91 0 0 1-7.56-1.22l-2.36-2.36A10.06 10.06 0 0 0 28 85a11 11 0 0 0 0 22c1.94 0 4.75-1.16 6.11-2.53l2.36-2.36a6.93 6.93 0 0 1 7.56-1.22l.84.43a8.08 8.08 0 0 1 4.13 6.66V143h35.02z'%3E%3C/path%3E%3C/svg%3E");
    }
    
    /* 2. O QUADRO BRANCO NO CENTRO */
    [data-testid="stMainBlockContainer"] {
        background-color: #ffffff;
        padding: 3rem;
        border-radius: 15px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.05);
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    /* 3. ESTILO DOS TEXTOS */
    .titulo-oficial {
        color: #1e293b;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 0px;
        padding-bottom: 15px;
        border-bottom: 2px solid #f1f5f9;
    }
    
    .subtitulo {
        color: #64748b; 
        font-size: 16px; 
        margin-top: 10px;
        margin-bottom: 30px;
    }
    
    /* 4. BARRA DE PESQUISA ARREDONDADA E LIMITADA */
    div[data-baseweb="input"] {
        border-radius: 25px !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        padding: 2px 10px;
    }
    
    /* 5. BOTÃO DE BUSCA ESCURO E ARREDONDADO */
    div[data-testid="stButton"] > button {
        border-radius: 25px !important;
        background-color: #333333 !important;
        color: white !important;
        border: none !important;
        height: 45px;
        font-weight: 600;
        transition: 0.3s;
    }
    
    div[data-testid="stButton"] > button:hover {
        background-color: #000000 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Cabeçalho limpo e corporativo
st.markdown("<div class='titulo-oficial'>Consulta de CNAEs e Resoluções</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>Sistema integrado para verificação de atividades e dispensas</div>", unsafe_allow_html=True)

# 3. Lógica para carregar os dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("cnaes_tributos.xlsx")
    df['CNAE'] = df['CNAE'].astype(str)
    df['Descrição'] = df['Descrição'].astype(str)
    # Coluna invisível para ignorar pontos e traços na busca
    df['CNAE_limpo'] = df['CNAE'].str.replace(r'[\.\-\/]', '', regex=True)
    return df

try:
    df = carregar_dados()
except FileNotFoundError:
    st.error("⚠️ Arquivo 'cnaes_tributos.xlsx' não encontrado no repositório do GitHub.")
    st.stop()

# 4. Layout da barra de pesquisa e botão (Lado a Lado)
col1, col2 = st.columns([4, 1])

with col1:
    # label_visibility="collapsed" tira o título da caixa para ficar igual ao seu print
    termo_busca = st.text_input("Busca", placeholder="Digite o CNAE ou palavra-chave...", label_visibility="collapsed")

with col2:
    botao_buscar = st.button("Buscar", use_container_width=True)

# 5. Sistema de Busca Inteligente
# Roda tanto ao dar Enter (termo_busca) quanto ao clicar no botão (botao_buscar)
if termo_busca or botao_buscar:
    if termo_busca:
        # Limpa pontuações para busca de CNAE
        termo_limpo = re.sub(r'[\.\-\/]', '', termo_busca)
        
        # Divide as palavras para a busca flexível na descrição
        palavras = termo_busca.split()
        
        # Busca todas as palavras digitadas na descrição (independente da ordem)
        mascara_descricao = pd.Series(True, index=df.index)
        for palavra in palavras:
            mascara_descricao = mascara_descricao & df["Descrição"].str.contains(palavra, case=False, na=False, regex=False)
            
        # Busca pelo CNAE limpo
        mascara_cnae = df["CNAE_limpo"].str.contains(termo_limpo, case=False, na=False, regex=False)
        
        # Junta os dois filtros
        filtro = df[mascara_descricao | mascara_cnae]
        
        st.write("") # Respiro visual
        
        # Exibe os resultados
        if filtro.empty:
            st.warning(f"Nenhum registro encontrado para '{termo_busca}'.")
        else:
            st.markdown(f"<p style='color: #334155; font-weight: 600;'>{len(filtro)} resultado(s) encontrado(s):</p>", unsafe_allow_html=True)
            
            # Tira a coluna invisível antes de mostrar
            filtro_para_mostrar = filtro.drop(columns=['CNAE_limpo'], errors='ignore')
            
            # Exibe a tabela sem o índice
            st.dataframe(filtro_para_mostrar, use_container_width=True, hide_index=True)
else:
    # Mensagem caso o usuário ainda não tenha pesquisado nada
    st.write("")
    st.info("💡 Digite um código CNAE ou uma palavra-chave para verificar a resolução.")
