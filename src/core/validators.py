"""
Validadores para boletos bancários.

Este módulo contém classes e funções para validação de dados
de boletos bancários conforme especificações da Febraban.
"""

import re
from datetime import datetime

from ..utils.logger import get_logger


class BoletoValidator:
    """Validador principal para boletos bancários"""

    def __init__(self):
        self.logger = get_logger("boleto_validator")

    def validar_cnpj_cpf(self, documento: str) -> bool:
        """
        Valida CNPJ ou CPF

        Args:
            documento: CNPJ ou CPF para validar

        Returns:
            True se válido, False caso contrário
        """
        if not documento:
            return False

        # Remove caracteres não numéricos
        documento_limpo = re.sub(r"[^\d]", "", documento)

        if len(documento_limpo) == 11:
            return self._validar_cpf(documento_limpo)
        elif len(documento_limpo) == 14:
            return self._validar_cnpj(documento_limpo)
        else:
            return False

    def _validar_cpf(self, cpf: str) -> bool:
        """Valida CPF usando algoritmo oficial"""
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        # Validação do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        dv1 = 0 if resto < 2 else 11 - resto

        if int(cpf[9]) != dv1:
            return False

        # Validação do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        dv2 = 0 if resto < 2 else 11 - resto

        return int(cpf[10]) == dv2

    def _validar_cnpj(self, cnpj: str) -> bool:
        """Valida CNPJ usando algoritmo oficial"""
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False

        # Validação do primeiro dígito verificador
        pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos[i] for i in range(12))
        resto = soma % 11
        dv1 = 0 if resto < 2 else 11 - resto

        if int(cnpj[12]) != dv1:
            return False

        # Validação do segundo dígito verificador
        pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos[i] for i in range(13))
        resto = soma % 11
        dv2 = 0 if resto < 2 else 11 - resto

        return int(cnpj[13]) == dv2

    def validar_codigo_banco(self, codigo: str) -> bool:
        """
        Valida código do banco

        Args:
            codigo: Código do banco (3 dígitos)

        Returns:
            True se válido, False caso contrário
        """
        if not codigo or len(codigo) != 3:
            return False

        return codigo.isdigit()

    def validar_valor(self, valor: float) -> bool:
        """
        Valida valor do documento

        Args:
            valor: Valor para validar

        Returns:
            True se válido, False caso contrário
        """
        return isinstance(valor, (int, float)) and valor > 0

    def validar_data_vencimento(self, data: datetime) -> bool:
        """
        Valida data de vencimento

        Args:
            data: Data para validar

        Returns:
            True se válida, False caso contrário
        """
        if not isinstance(data, datetime):
            return False

        # Data não pode ser no passado (considerando margem de 1 dia)
        from datetime import timedelta

        hoje = datetime.now().date()
        return data.date() >= hoje - timedelta(days=1)

    def validar_nosso_numero(self, nosso_numero: str) -> bool:
        """
        Valida nosso número

        Args:
            nosso_numero: Nosso número para validar

        Returns:
            True se válido, False caso contrário
        """
        if not nosso_numero:
            return False

        # Nosso número deve ter entre 1 e 20 dígitos
        return nosso_numero.isdigit() and 1 <= len(nosso_numero) <= 20

    def validar_carteira(self, carteira: str) -> bool:
        """
        Valida carteira

        Args:
            carteira: Carteira para validar

        Returns:
            True se válida, False caso contrário
        """
        if not carteira:
            return False

        # Carteira deve ter entre 1 e 3 dígitos
        return carteira.isdigit() and 1 <= len(carteira) <= 3

    def validar_linha_digitavel(self, linha: str) -> bool:
        """
        Valida linha digitável

        Args:
            linha: Linha digitável para validar

        Returns:
            True se válida, False caso contrário
        """
        if not linha:
            return False

        # Remove espaços e pontos
        linha_limpa = re.sub(r"[.\s]", "", linha)

        # Deve ter exatamente 47 dígitos
        return linha_limpa.isdigit() and len(linha_limpa) == 47

    def validar_codigo_barras(self, codigo: str) -> bool:
        """
        Valida código de barras

        Args:
            codigo: Código de barras para validar

        Returns:
            True se válido, False caso contrário
        """
        if not codigo:
            return False

        # Deve ter exatamente 44 dígitos
        return codigo.isdigit() and len(codigo) == 44

    def validar_cep(self, cep: str) -> bool:
        """
        Valida CEP

        Args:
            cep: CEP para validar

        Returns:
            True se válido, False caso contrário
        """
        if not cep:
            return False

        # Remove caracteres não numéricos
        cep_limpo = re.sub(r"[^\d]", "", cep)

        # Deve ter 8 dígitos
        return cep_limpo.isdigit() and len(cep_limpo) == 8

    def validar_agencia(self, agencia: str) -> bool:
        """
        Valida agência

        Args:
            agencia: Agência para validar

        Returns:
            True se válida, False caso contrário
        """
        if not agencia:
            return False

        # Agência deve ter entre 1 e 5 dígitos
        return agencia.isdigit() and 1 <= len(agencia) <= 5

    def validar_conta(self, conta: str) -> bool:
        """
        Valida conta

        Args:
            conta: Conta para validar

        Returns:
            True se válida, False caso contrário
        """
        if not conta:
            return False

        # Conta deve ter entre 1 e 12 dígitos
        return conta.isdigit() and 1 <= len(conta) <= 12


class DigitavelValidator:
    """Validador específico para linha digitável"""

    def __init__(self):
        self.logger = get_logger("digitavel_validator")

    def validar_formato(self, digitavel: str) -> bool:
        """
        Valida formato da linha digitável

        Args:
            digitavel: Linha digitável para validar

        Returns:
            True se formato válido, False caso contrário
        """
        if not digitavel:
            return False

        # Remove espaços e pontos
        digitavel_limpo = re.sub(r"[.\s]", "", digitavel)

        # Deve ter exatamente 47 dígitos
        if not digitavel_limpo.isdigit() or len(digitavel_limpo) != 47:
            return False

        return True

    def validar_dvs(self, digitavel: str) -> bool:
        """
        Valida dígitos verificadores da linha digitável

        Args:
            digitavel: Linha digitável para validar

        Returns:
            True se DVs válidos, False caso contrário
        """
        from .digitavel import Digitavel

        try:
            dig = Digitavel(digitavel)
            return dig.validar()
        except Exception as e:
            self.logger.error("Erro ao validar DVs", erro=str(e))
            return False

    def validar_estrutura(self, digitavel: str) -> bool:
        """
        Valida estrutura da linha digitável

        Args:
            digitavel: Linha digitável para validar

        Returns:
            True se estrutura válida, False caso contrário
        """
        if not self.validar_formato(digitavel):
            return False

        # Remove espaços e pontos
        digitavel_limpo = re.sub(r"[.\s]", "", digitavel)

        # Validar estrutura dos campos
        campo1 = digitavel_limpo[0:10]  # 9 dígitos + DV
        campo2 = digitavel_limpo[10:21]  # 10 dígitos + DV
        campo3 = digitavel_limpo[21:32]  # 10 dígitos + DV
        dv_geral = digitavel_limpo[32:33]  # 1 dígito
        campo5 = digitavel_limpo[33:47]  # 14 dígitos

        # Validar tamanhos dos campos
        if len(campo1) != 10 or len(campo2) != 11 or len(campo3) != 11:
            return False

        if len(dv_geral) != 1 or len(campo5) != 14:
            return False

        return True
