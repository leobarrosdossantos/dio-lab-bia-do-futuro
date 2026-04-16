import json
import pandas as pd
import requests
import streamlit as st

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "tinyllama" 

# ============ CARREGAR DADOS ============
@st.cache_data
def carregar_dados():
    try:
        # Carregando arquivos da pasta 'data' conforme sua estrutura
        perfil = json.load(open('./data/perfil_investidor.json', encoding='utf-8'))
        produtos = json.load(open('./data/produtos_financeiros.json', encoding='utf-8'))
        
        # Carregando transações
        df_transacoes = pd.read_csv('./data/transacoes.csv')
        df_transacoes['valor'] = pd.to_numeric(df_transacoes['valor'], errors='coerce')
        
        return perfil, produtos, df_transacoes
    except Exception as e:
        st.error(f"Erro ao carregar arquivos: {e}")
        st.stop()

perfil, produtos, df_transacoes = carregar_dados()

# ============ CONTEXTO DINÂMICO ============
lista_produtos = ""
for p in produtos:
    lista_produtos += f"- {p['nome']} (Risco: {p['risco']}, Indicado para: {p['indicado_para']})\n"

contexto_usuario = f"""
DADOS DO CLIENTE:
- Nome: {perfil['nome']}
- Perfil: {perfil['perfil_investidor']}
- Objetivo: {perfil['objetivo_principal']}
- Reserva Atual: R$ {perfil['reserva_emergencia_atual']}

PRODUTOS DISPONÍVEIS:
{lista_produtos}
"""

SYSTEM_PROMPT = """Você é o Edu, um educador financeiro amigável.
Use os DADOS DO CLIENTE para sugerir produtos do catálogo que combinem com o perfil dele.
Responda de forma curta e educativa."""

# ============ FUNÇÃO DE PROCESSAMENTO ============
def gerar_resposta_edu(pergunta):
    pergunta_clean = pergunta.lower().strip()

    # 1. REGRA: ALIMENTAÇÃO (Baseado no CSV)
    if "quanto gastei" in pergunta_clean and "alimentação" in pergunta_clean:
        filtro = (df_transacoes['categoria'].str.lower() == 'alimentacao') & (df_transacoes['tipo'] == 'saida')
        total = df_transacoes[filtro]['valor'].sum()
        yield f"Você gastou um total de **R$ {total:.2f}** com alimentação, conforme seus registros."
        return

    # 2. REGRA: PREVISÃO DO TEMPO (Resposta Fixa)
    if "previsão do tempo" in pergunta_clean or "previsao do tempo" in pergunta_clean:
        yield ("Desculpe, não posso ajudar com previsão do tempo. Sou um educador financeiro e posso esclarecer "
               "conceitos de finanças pessoais. Se quiser, podemos conversar sobre como montar uma reserva de "
               "emergência ou organizar seu orçamento mensal.\n\nEntendeu?")
        return

    # 3. REGRA: BBDC3 (Existente)
    if "bbdc3" in pergunta_clean:
        yield ("Desculpe, mas não tenho a informação atual sobre o rendimento do BBDC3 na Bovespa. "
               "Posso explicar como funciona a rentabilidade de ações...")
        return

    # 4. PROCESSAMENTO IA (OLLAMA)
    prompt_final = f"{SYSTEM_PROMPT}\n\n{contexto_usuario}\n\nPergunta: {pergunta}"
    
    try:
        with requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt_final, "stream": True}, stream=True, timeout=120) as r:
            for line in r.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    yield chunk.get("response", "")
    except Exception as e:
        yield f"⚠️ Erro: {e}"

# ============ INTERFACE STREAMLIT ============
st.set_page_config(page_title="Edu - Consultor Financeiro")
st.title("🎓 Edu, o Educador Financeiro")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if pergunta_usuario := st.chat_input("Sua dúvida sobre finanças..."):
    st.session_state.mensagens.append({"role": "user", "content": pergunta_usuario})
    with st.chat_message("user"):
        st.markdown(pergunta_usuario)

    with st.chat_message("assistant"):
        resposta = st.write_stream(gerar_resposta_edu(pergunta_usuario))
    
    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
