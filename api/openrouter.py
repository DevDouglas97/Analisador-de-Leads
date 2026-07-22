import os
import json
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from models.empresa import Empresa

load_dotenv()

class AnalisadorIA:

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY não foi encontrada no arquivo .env!")

    def analisar_lead_com_empresa(self, empresa: Empresa, mensagem_lead: str, orcamento: str = "Não informado") -> Optional[Dict[str, Any]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        
        prompt = f"""
        Você é um especialista em pré-vendas (SDR/BDR) e qualificação B2B.
        Analise a empresa cadastrada e o interesse do lead para calcular a viabilidade comercial.

        === DADOS DA EMPRESA (Via CNPJ) ===
        - Razão Social: {empresa.razao_social}
        - Nome Fantasia: {empresa.nome_fantasia or 'N/A'}
        - Porte: {empresa.porte}
        - Capital Social: R$ {empresa.capital_social:,.2f}
        - CNAE / Atividade Principal: {empresa.cnae_principal}
        - Localização: {empresa.endereco.cidade} - {empresa.endereco.uf}
        - Situação Cadastral: {empresa.situacao}

        === DADOS DO LEAD ===
        - Mensagem / Dor do Cliente: {mensagem_lead}
        - Orçamento Estimado: {orcamento}

        === INSTRUÇÕES ===
        Retorne ESTRITAMENTE um objeto JSON válido no seguinte formato:
        {{
            "score": <número inteiro de 0 a 100>,
            "classificacao": "<'Frio', 'Morno' ou 'Quente'>",
            "resumo_empresa": "<breve resumo do perfil da empresa em 1 frase>",
            "motivos_qualificacao": ["<motivo 1>", "<motivo 2>"],
            "recomendacao_vendas": "<orientação direta para o vendedor>"
        }}
        """

       
        payload = {
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(
                url=self.url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )

            if response.status_code != 200:
                print(f"[ERRO API OpenRouter - Status {response.status_code}]: {response.text}")
                return None

            dados_resposta = response.json()
            conteudo_texto = dados_resposta['choices'][0]['message']['content']
            
            # Converte a resposta texto de JSON para dicionário Python
            return json.loads(conteudo_texto)

        except Exception as e:
            print(f"[ERRO NO MÓDULO DE IA]: {e}")
            return None