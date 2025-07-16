"""
Classe principal para Boleto Bancário.

Este módulo contém a classe BoletoBancario que representa um boleto
bancário conforme especificações da Febraban.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from ..utils.logger import get_logger
from .enums import TipoAceite, TipoDocumento, TipoMoeda
from .validators import BoletoValidator


@dataclass
class BoletoBancario:
    """
    Classe principal para representar um boleto bancário
    conforme especificações da Febraban
    """

    # === CAMPOS OBRIGATÓRIOS ===

    # Código do Banco (3 dígitos)
    codigo_banco: str

    # Linha Digitável (47 dígitos)
    linha_digitavel: str

    # Código de Barras
    codigo_barras: str

    # Nome do Cedente
    nome_cedente: str

    # CNPJ/CPF do Cedente
    cnpj_cpf_cedente: str

    # Nome do Pagador
    nome_pagador: str

    # CNPJ/CPF do Pagador
    cnpj_cpf_pagador: str

    # Data de Vencimento
    data_vencimento: datetime

    # Valor do Documento
    valor_documento: float

    # Nosso Número
    nosso_numero: str

    # Carteira
    carteira: str

    # Data de Emissão
    data_emissao: datetime

    # === CAMPOS OPCIONAIS ===

    # Espécie do Documento
    especie_documento: TipoDocumento = TipoDocumento.DUPLICATA_MERCANTIL

    # Aceite
    aceite: TipoAceite = TipoAceite.NAO

    # Moeda
    moeda: TipoMoeda = TipoMoeda.REAL

    # Agência/Código do Cedente
    agencia_cedente: Optional[str] = None

    # Conta do Cedente
    conta_cedente: Optional[str] = None

    # Instruções
    instrucoes: List[str] = field(default_factory=list)

    # Descontos
    desconto_valor: Optional[float] = None
    desconto_data: Optional[datetime] = None
    desconto_percentual: Optional[float] = None

    # Juros e multas
    juros_percentual: Optional[float] = None
    multa_percentual: Optional[float] = None
    multa_valor: Optional[float] = None

    # Informações adicionais
    numero_documento: Optional[str] = None
    sacador_avalista: Optional[str] = None
    informacoes_adicionais: List[str] = field(default_factory=list)

    # Protesto
    protesto_dias: Optional[int] = None
    protesto_instrucao: Optional[str] = None

    # Uso do banco
    uso_banco: Optional[str] = None

    # Local de pagamento
    local_pagamento: str = "PAGÁVEL EM QUALQUER BANCO ATÉ O VENCIMENTO"

    # Endereços
    endereco_cedente: Optional[str] = None
    endereco_pagador: Optional[str] = None

    # Código do beneficiário
    codigo_beneficiario: Optional[str] = None

    def __post_init__(self):
        """Inicialização pós-criação do objeto"""
        self.logger = get_logger("boleto_bancario")
        self.validator = BoletoValidator()

    def validar_campos_obrigatorios(self) -> bool:
        """
        Valida se todos os campos obrigatórios estão preenchidos

        Returns:
            True se todos os campos obrigatórios são válidos
        """
        return (
            self.validator.validar_codigo_banco(self.codigo_banco)
            and self.validator.validar_linha_digitavel(self.linha_digitavel)
            and self.validator.validar_codigo_barras(self.codigo_barras)
            and bool(self.nome_cedente)
            and self.validator.validar_cnpj_cpf(self.cnpj_cpf_cedente)
            and bool(self.nome_pagador)
            and self.validator.validar_cnpj_cpf(self.cnpj_cpf_pagador)
            and self.validator.validar_nosso_numero(self.nosso_numero)
            and self.validator.validar_carteira(self.carteira)
            and self.validator.validar_valor(self.valor_documento)
        )

    def validar_dados_completos(self) -> List[str]:
        """
        Valida todos os dados do boleto e retorna lista de erros

        Returns:
            Lista de mensagens de erro (vazia se não houver erros)
        """
        erros = []

        # Validar campos obrigatórios
        if not self.validar_campos_obrigatorios():
            erros.append("Campos obrigatórios inválidos")

        # Validar datas
        if not self.validator.validar_data_vencimento(self.data_vencimento):
            erros.append("Data de vencimento inválida")

        if not isinstance(self.data_emissao, datetime):
            erros.append("Data de emissão inválida")

        # Validar valores opcionais
        if self.desconto_valor is not None and not self.validator.validar_valor(
            self.desconto_valor
        ):
            erros.append("Valor de desconto inválido")

        if self.multa_valor is not None and not self.validator.validar_valor(
            self.multa_valor
        ):
            erros.append("Valor de multa inválido")

        # Validar percentuais
        if self.desconto_percentual is not None and (
            self.desconto_percentual < 0 or self.desconto_percentual > 100
        ):
            erros.append("Percentual de desconto inválido")

        if self.juros_percentual is not None and (
            self.juros_percentual < 0 or self.juros_percentual > 100
        ):
            erros.append("Percentual de juros inválido")

        if self.multa_percentual is not None and (
            self.multa_percentual < 0 or self.multa_percentual > 100
        ):
            erros.append("Percentual de multa inválido")

        # Validar agência e conta se fornecidas
        if self.agencia_cedente and not self.validator.validar_agencia(
            self.agencia_cedente
        ):
            erros.append("Agência do cedente inválida")

        if self.conta_cedente and not self.validator.validar_conta(self.conta_cedente):
            erros.append("Conta do cedente inválida")

        return erros

    def is_valido(self) -> bool:
        """
        Verifica se o boleto é válido

        Returns:
            True se o boleto é válido
        """
        return len(self.validar_dados_completos()) == 0

    def calcular_valor_total(self) -> float:
        """
        Calcula o valor total a ser pago (incluindo juros e multas)

        Returns:
            Valor total calculado
        """
        valor_total = self.valor_documento

        # Aplicar desconto se houver
        if self.desconto_valor:
            valor_total -= self.desconto_valor
        elif self.desconto_percentual:
            valor_total -= self.valor_documento * self.desconto_percentual / 100

        # Aplicar multa se houver
        if self.multa_valor:
            valor_total += self.multa_valor
        elif self.multa_percentual:
            valor_total += self.valor_documento * self.multa_percentual / 100

        # Aplicar juros se houver
        if self.juros_percentual:
            valor_total += self.valor_documento * self.juros_percentual / 100

        return max(0, valor_total)

    def is_vencido(self) -> bool:
        """
        Verifica se o boleto está vencido

        Returns:
            True se o boleto está vencido
        """
        from datetime import datetime

        return datetime.now() > self.data_vencimento

    def dias_vencimento(self) -> int:
        """
        Calcula quantos dias faltam para o vencimento

        Returns:
            Número de dias (negativo se vencido)
        """
        from datetime import datetime

        delta = self.data_vencimento - datetime.now()
        return delta.days

    def __str__(self) -> str:
        """Representação string do boleto"""
        return (
            f"BoletoBancario("
            f"banco={self.codigo_banco}, "
            f"cedente={self.nome_cedente}, "
            f"valor=R${self.valor_documento:.2f}, "
            f"vencimento={self.data_vencimento.strftime('%d/%m/%Y')}"
            f")"
        )

    def to_dict(self) -> dict:
        """
        Converte o boleto para dicionário

        Returns:
            Dicionário com os dados do boleto
        """
        return {
            "codigo_banco": self.codigo_banco,
            "linha_digitavel": self.linha_digitavel,
            "codigo_barras": self.codigo_barras,
            "nome_cedente": self.nome_cedente,
            "cnpj_cpf_cedente": self.cnpj_cpf_cedente,
            "nome_pagador": self.nome_pagador,
            "cnpj_cpf_pagador": self.cnpj_cpf_pagador,
            "data_vencimento": self.data_vencimento.isoformat(),
            "valor_documento": self.valor_documento,
            "nosso_numero": self.nosso_numero,
            "carteira": self.carteira,
            "data_emissao": self.data_emissao.isoformat(),
            "especie_documento": self.especie_documento.value,
            "aceite": self.aceite.value,
            "moeda": self.moeda.value,
            "agencia_cedente": self.agencia_cedente,
            "conta_cedente": self.conta_cedente,
            "instrucoes": self.instrucoes,
            "desconto_valor": self.desconto_valor,
            "desconto_data": self.desconto_data.isoformat()
            if self.desconto_data
            else None,
            "desconto_percentual": self.desconto_percentual,
            "juros_percentual": self.juros_percentual,
            "multa_percentual": self.multa_percentual,
            "multa_valor": self.multa_valor,
            "numero_documento": self.numero_documento,
            "sacador_avalista": self.sacador_avalista,
            "informacoes_adicionais": self.informacoes_adicionais,
            "protesto_dias": self.protesto_dias,
            "protesto_instrucao": self.protesto_instrucao,
            "uso_banco": self.uso_banco,
            "local_pagamento": self.local_pagamento,
            "endereco_cedente": self.endereco_cedente,
            "endereco_pagador": self.endereco_pagador,
            "codigo_beneficiario": self.codigo_beneficiario,
        }
