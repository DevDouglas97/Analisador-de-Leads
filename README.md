#  Analisador de Leads B2B com IA

Uma aplicação em Python para **enriquecimento automático de dados cadastrais** e **qualificação inteligente de leads B2B**. 

O sistema consulta dados cadastrais através da API **CNPJ.ws** e processa o contexto comercial e as dores do cliente utilizando **Modelos de Linguagem (LLMs)** integrados pela **OpenRouter**.

---

##  Funcionalidades

- **Sanitização de Dados:** Validação e tratamento de CNPJs inseridos via regex.
- **Enriquecimento Fiscais:** Busca automática de Razão Social, Nome Fantasia, Porte, Capital Social, Localização, CNAE principal e Situação Cadastral.
- **Análise Qualitativa por IA:** Envio do contexto do lead (mensagem + orçamento + dados da empresa) para LLMs avaliarem o perfil da oportunidade.
- **Output Estruturado:** Devolução dos resultados em formato JSON estrito contendo:
  - **Score de Qualificação (0 a 100)**
  - **Classificação:** Frio, Morno ou Quente
  - **Resumo do Perfil da Empresa**
  - **Lista de Motivos/Critérios**
  - **Recomendação Direta para o Time de Vendas**

---

## Tecnologias Utilizadas

- **[Python 3.x](https://www.python.org/):** Linguagem base da aplicação.
- **[Requests](https://requests.readthedocs.io/):** Biblioteca para consumo de APIs RESTful.
- **[CNPJ.ws API](https://cnpj.ws/):** API REST para consulta de dados cadastrais de pessoas jurídicas.
- **[OpenRouter API](https://openrouter.ai/):** Gateway unificado para modelos de Inteligência Artificial / LLMs.
- **[Python-Dotenv](https://pypi.org/project/python-dotenv/):** Gerenciamento seguro de credenciais via variáveis de ambiente.
- **[Dataclasses](https://docs.python.org/3/library/dataclasses.html):** Modelagem de dados limpa e tipada.

---

## Como Executar o Projeto
* Pré-requisitos
- Python 3.8 ou superior instalado.
- Chave de API da OpenRouter.

### Passo a Passo:

1. ***Clone o repositório:*** 
```bash 
git clone [https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/seu-usuario/nome-do-repositorio.git)
cd "nome-do-repositorio" 
```
2. ***Crie e ative um ambiente virtual:***
```bash 
python -m venv venv
```
``` bash
source venv/bin/activate 
```
no Linux/Mac ou no Windows: 
```bash 
venv\Scripts\activate
```
3. Instale as dependências: 
```bash 
pip install -r requirements.txt
```

4. Configure a sua Chave de API:
- Crie um arquivo .env na raiz do projeto (ou copie a partir do .env.example):
  cp .env.example .env
- Edite o arquivo .env e insira sua chave da OpenRouter:
  OPENROUTER_API_KEY=sk-or-v1-sua-chave-aqui

5. Execute a aplicação: 
```bash
python main.py
```

---

##  Estrutura do Projeto

```text
Analisador de Leads/
├── api/
│   ├── cnpjws.py        # Módulo de integração e tratamento com a API CNPJ.ws
│   └── ai_analyzer.py   # Módulo de comunicação com LLMs via OpenRouter
├── models/
│   └── empresa.py       # Dataclasses (Empresa, Endereco, Socio)
├── .env.example         # Exemplo das variáveis de ambiente necessárias
├── .gitignore           # Proteção de chaves e ambiente local
├── main.py              # Ponto de entrada e orquestração do fluxo do sistema
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação
```

## Contribuição e Licença

Sinta-se à vontade para abrir Issues ou enviar Pull Requests com melhorias na análise do prompt, integração com novos CRMs ou adição de testes unitários!

Projeto desenvolvido para fins de aprendizado e portfólio prático de engenharia de software e integração com IA.

## Autor: 
Douglas Soares Paz


