💰 Edu — Educador Financeiro com IA

Agente conversacional de educação financeira desenvolvido com Amazon Bedrock + Claude 3 Sonnet, como solução para o desafio BIA do Futuro da DIO.


🤖 Sobre o Projeto
Edu é um assistente virtual especializado em educação financeira, capaz de ajudar usuários a entender conceitos como orçamento, investimentos, dívidas e planejamento financeiro de forma acessível e didática.
O projeto foi desenvolvido como resposta ao desafio proposto pela DIO, utilizando agentes de IA generativa na AWS para criar uma solução funcional e documentada.

🛠️ Tecnologias Utilizadas
TecnologiaFinalidadeAmazon BedrockPlataforma de IA generativaClaude 3 Sonnet (Anthropic)Modelo de linguagem do agenteAWS LambdaExecução das action groupsAmazon S3Armazenamento da base de conhecimentoPythonLógica das funções Lambda

🧠 Arquitetura do Agente
Usuário
   │
   ▼
Amazon Bedrock Agent (Edu)
   ├── Instruções & Persona
   ├── Base de Conhecimento (S3)
   └── Action Groups (Lambda)
         ├── calcular_juros_compostos
         ├── simular_investimento
         └── analisar_orcamento

📋 Funcionalidades

Explicação de conceitos financeiros de forma simples
Cálculo de juros compostos e simulações de investimento
Análise básica de orçamento pessoal
Recomendações de planejamento financeiro
Respostas personalizadas ao perfil do usuário


📁 Estrutura do Repositório
dio-lab-bia-do-futuro/
├── lambda/
│   └── edu_actions.py         # Funções das Action Groups
├── knowledge-base/
│   └── educacao_financeira.pdf  # Base de conhecimento do Edu
├── agent-config/
│   └── instrucoes_edu.txt     # Prompt de sistema e persona
└── README.md

🚀 Como Reproduzir

Pré-requisitos: conta AWS com acesso ao Amazon Bedrock e permissão para usar o modelo Claude 3 Sonnet.
Base de conhecimento: faça upload do arquivo em knowledge-base/ para um bucket S3 e crie um Knowledge Base no Bedrock apontando para ele.
Action Groups: faça deploy da função em lambda/edu_actions.py no AWS Lambda e vincule ao agente no Bedrock.
Criação do Agente: no console do Amazon Bedrock, crie um novo agente usando as instruções em agent-config/instrucoes_edu.txt e associe a base de conhecimento e as action groups.
Teste: use o playground do Bedrock para interagir com o Edu e validar as respostas.


📎 Links

🔗 Repositório no GitHub
🎓 Desafio BIA do Futuro — DIO


👤 Autor
Leonardo Barros dos Santos
Desenvolvido como parte do bootcamp da DIO — desafio de IA generativa com Amazon Bedrock.
