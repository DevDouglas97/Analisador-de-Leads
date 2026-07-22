from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Endereco:
    cep: str
    logradouro: str
    numero: str
    complemento: Optional[str]
    bairro: str
    cidade: str
    uf: str

@dataclass
class Socio:
    nome: str
    qualificacao: str
    data_entrada: Optional[str] = None

@dataclass
class Empresa:
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str]
    situacao: str
    data_inicio_atividade: str
    porte: str
    natureza_juridica: str
    capital_social: float
    cnae_principal: str
    telefone: Optional[str]
    email: Optional[str]
    endereco: Endereco
    socios: List[Socio] = field(default_factory=list)