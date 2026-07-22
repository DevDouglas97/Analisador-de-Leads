import re
import requests
from typing import Optional
from models.empresa import Empresa, Endereco, Socio

class ConsultaCNPJ:

    def __init__(self, cnpj: str):
        # Remove caracteres especiais (pontos, barras, traços)
        self.cnpj = re.sub(r'\D', '', cnpj)

    def consultar(self) -> Optional[Empresa]:
        url = f"https://publica.cnpj.ws/cnpj/{self.cnpj}"

        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 429:
                print("\n[Aviso] Limite de requisições atingido na CNPJ.ws (máx 3 por minuto no plano gratuito). Aguarde 1 minuto.")
                return None
            elif response.status_code != 200:
                print(f"[DEBUG] Status Code da API: {response.status_code}")
                print(f"[DEBUG] Resposta: {response.text}")
                return None

            dados = response.json()
            est = dados.get("estabelecimento", {})

            # Trata o endereço que fica dentro de 'estabelecimento'
            cidade_nome = est.get("cidade", {}).get("nome", "") if est.get("cidade") else ""
            estado_sigla = est.get("estado", {}).get("sigla", "") if est.get("estado") else ""

            endereco = Endereco(
                cep=str(est.get("cep", "") or ""),
                logradouro=str(est.get("logradouro", "") or ""),
                numero=str(est.get("numero", "") or ""),
                complemento=str(est.get("complemento", "") or ""),
                bairro=str(est.get("bairro", "") or ""),
                cidade=cidade_nome,
                uf=estado_sigla
            )

            # Processa a lista de sócios
            socios = []
            for s in dados.get("socios", []):
                qualificacao = s.get("qualificacao_socio", {}).get("descricao", "") if s.get("qualificacao_socio") else ""
                socio = Socio(
                    nome=str(s.get("nome", "")),
                    qualificacao=qualificacao,
                    data_entrada=s.get("data_entrada", None)
                )
                socios.append(socio)

            # Converte capital social de forma segura
            capital = dados.get("razao_social", 0)  # pega do objeto raiz
            capital_str = dados.get("capital_social", 0)
            try:
                capital_float = float(capital_str)
            except (ValueError, TypeError):
                capital_float = 0.0

            cnae_desc = est.get("atividade_principal", {}).get("descricao", "") if est.get("atividade_principal") else ""
            situacao_desc = est.get("situacao_cadastral", "")

            # Formata telefone (DDD + Telefone)
            ddd = est.get("ddd1", "")
            tel = est.get("telefone1", "")
            telefone_completo = f"({ddd}) {tel}" if ddd and tel else (tel or "")

            # Porte da empresa
            porte_desc = dados.get("porte", {}).get("descricao", "") if dados.get("porte") else ""

            # Natureza jurídica
            nat_juridica = dados.get("natureza_juridica", {}).get("descricao", "") if dados.get("natureza_juridica") else ""

            empresa = Empresa(
                cnpj=str(est.get("cnpj", self.cnpj)),
                razao_social=str(dados.get("razao_social", "")),
                nome_fantasia=str(est.get("nome_fantasia", "") or ""),
                situacao=situacao_desc,
                data_inicio_atividade=str(est.get("data_inicio_atividade", "")),
                porte=porte_desc,
                natureza_juridica=nat_juridica,
                capital_social=capital_float,
                cnae_principal=cnae_desc,
                telefone=telefone_completo,
                email=str(est.get("email", "") or ""),
                endereco=endereco,
                socios=socios
            )

            return empresa

        except Exception as e:
            print(f"[ERRO NO CÓDIGO]: {e}")
            return None