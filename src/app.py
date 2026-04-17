import json
import pandas as pd
import requests
import streamlit as st
import unicodedata

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "tinyllama" 

# ============ CARREGAR DADOS ============
@st.cache_data
def carregar_dados():
    try:
        # Carregamento estrito dos dados fornecidos
        perfil = json.load(open('./data/perfil_investidor.json', encoding='utf-8'))
        produtos = json.load(open('./data/produtos_financeiros.json', encoding='utf-8'))
        df_transacoes = pd.read_csv('./data/transacoes.csv')
        df_transacoes['valor'] = pd.to_numeric(df_transacoes['valor'], errors='coerce')
        return perfil, produtos, df_transacoes
    except Exception as e:
        st.error(f"Erro ao carregar arquivos: {e}")
        st.stop()

perfil, produtos, df_transacoes = carregar_dados()

# ============ FUNÇÕES AUXILIARES ============
def remover_acentos(texto):
    """Padroniza a busca para evitar erros de digitação ou ortografia."""
    if not isinstance(texto, str):
        return ""
    return "".join(c for c in unicodedata.normalize('NFKD', texto) if unicodedata.category(c) != 'Mn').lower()

# ============ FUNÇÃO DE PROCESSAMENTO ============
def gerar_resposta_edu(pergunta):
    pergunta_clean = remover_acentos(pergunta.strip())

    # 1. REGRA: CONSULTA DE UM INVESTIMENTO ESPECÍFICO (JSON)
    for p in produtos:
        nome_produto_clean = remover_acentos(p['nome'])
        if nome_produto_clean in pergunta_clean:
            yield (f"**{p['nome']}**\n"
                   f"- Categoria: {p['categoria']}\n"
                   f"- Risco: {p['risco']}\n"
                   f"- Rentabilidade: {p['rentabilidade']}\n"
                   f"- Aporte Mínimo: R$ {p['aporte_minimo']:.2f}\n"
                   f"- Indicação: {p['indicado_para']}")
            return

    # 2. REGRA: OPÇÕES DE INVESTIMENTOS (Listagem Geral)
    if any(termo in pergunta_clean for termo in ["opcoes", "quais investimentos", "lista"]):
        lista_opcoes = "\n".join([f"- {p['nome']} ({p['categoria']})" for p in produtos])
        yield f"As opções disponíveis no catálogo são:\n{lista_opcoes}"
        return

    # 3. REGRA: GASTOS E SALDO (CSV)
    if "quanto gastei" in pergunta_clean:
        encontrou_categoria = False
        for cat in df_transacoes['categoria'].unique():
            if remover_acentos(cat) in pergunta_clean:
                total = df_transacoes[(df_transacoes['categoria'] == cat) & (df_transacoes['tipo'] == 'saida')]['valor'].sum()
                yield f"O gasto total em {cat} foi de R$ {total:.2f}."
                encontrou_categoria = True
                break
        if encontrou_categoria: return

    # 4. PROCESSAMENTO IA (OLLAMA) - COM CONTEXTO RESTRITO
    # Criamos uma lista de produtos permitidos para "educar" a IA
    nomes_produtos = ", ".join([p['nome'] for p in produtos])
    
    contexto_investidor = (
        f"Investidor: {perfil['nome']}. Perfil: {perfil['perfil_investidor']}. "
        f"Objetivo: {perfil['objetivo_principal']}. "
        f"Produtos disponíveis: {nomes_produtos}."
    )
    
    prompt_final = (
        f"Você é o Edu, um assistente financeiro direto. "
        f"RESPONDA APENAS EM PORTUGUÊS DO BRASIL. "
        f"USE GRAMÁTICA CORRETA. SEJA EXTREMAMENTE OBJETIVO. "
        f"IMPORTANTE: Indique apenas investimentos presentes na lista de produtos disponíveis. "
        f"Contexto: {contexto_investidor}\n"
        f"Pergunta: {pergunta}\n"
        f"Resposta Técnica:"
    )
    
    try:
        with requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt_final, "stream": True}, stream=True, timeout=120) as r:
            for line in r.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    yield chunk.get("response", "")
    except Exception as e:
        yield f"Erro na conexão com o modelo local: {e}"

# ============ INTERFACE STREAMLIT ============
st.set_page_config(page_title="Edu - Consultoria Técnica", layout="centered")
st.title("🎓 Edu: Inteligência em Investimentos")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if pergunta_usuario := st.chat_input("Pergunte sobre investimentos ou seus gastos:"):
    st.session_state.mensagens.append({"role": "user", "content": pergunta_usuario})
    with st.chat_message("user"):
        st.markdown(pergunta_usuario)

    with st.chat_message("assistant"):
        resposta = st.write_stream(gerar_resposta_edu(pergunta_usuario))
    
    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
