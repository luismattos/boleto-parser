from .aluno import DadosAluno
from .banco import InformacoesBancarias
from .beneficiario import DadosBeneficiario
from .boleto_data import BoletoData
from .endereco import EnderecoInstituicao
from .instrucoes import Instrucoes
from .pagador import DadosPagador
from .valores import Valores

__all__ = [
    "DadosBeneficiario",
    "DadosPagador",
    "DadosAluno",
    "Valores",
    "InformacoesBancarias",
    "Instrucoes",
    "EnderecoInstituicao",
    "BoletoData",
]
