# Passo a Passo de Execução

## Setup do Ollama

``` bash
# 1. Instalar Ollama (ollama.com)
# 2. Baixar um modelo leve
ollama pull tinyllama

# 3. Testar se funciona
ollama run tinyllama "Oi"
```

## Código Completo

Todo código-fonte está no arquivo `app.py`.

## Como Rodar

```bash
# 1. Instalar dependências
pip install streamlit pandas requests

# 2. Garantir que o Ollama está rodando
ollama serve

# 3. Rodar o app
streamlit run .\src\app.py
```

## Evidência de Execução

<img width="1366" height="655" alt="image" src="https://github.com/user-attachments/assets/24344d91-4c70-4b88-9441-6b9d4648ee0b" />
