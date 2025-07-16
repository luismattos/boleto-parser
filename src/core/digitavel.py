"""
Representação e manipulação da linha digitável de boletos bancários.

Este módulo contém as classes para trabalhar com a linha digitável
conforme especificações da Febraban.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

import regex

from ..utils.dv import modulo_10, modulo_11
from ..utils.logger import get_logger


@dataclass
class CamposDigitavel:
    """
    Estrutura para armazenar os campos da linha digitável conforme Febraban

    Estrutura: 033991614.0 0700000191.2 8155600101.4 4 11370000038936
    """

    bloco_campo1: str  # AAABCCCCCD (10 dígitos)
    bloco_campo2: str  # DDDDEEEEFF (10 dígitos)
    bloco_campo3: str  # FFFFFGGGGG (10 dígitos)
    dv_geral: str  # H (1 dígito - DV geral)
    fator_valor_e_valor: str  # TTTTTTTTTT (16 dígitos)

    @property
    def banco(self) -> str:
        """Retorna o código do banco (primeiros 3 dígitos do campo 1)"""
        return self.bloco_campo1[:3]

    @property
    def moeda(self) -> str:
        """Retorna o código da moeda (4º dígito do campo 1)"""
        return self.bloco_campo1[3:4]

    @property
    def campo_livre(self) -> str:
        """Retorna o campo livre completo (25 dígitos) - dados brutos sem interpretação"""
        return self.bloco_campo1[4:9] + self.bloco_campo2[:9] + self.bloco_campo3[:9]

    @property
    def campo1_sem_dv(self) -> str:
        """Retorna o campo 1 sem o dígito verificador"""
        return self.bloco_campo1[:-1]

    @property
    def campo2_sem_dv(self) -> str:
        """Retorna o campo 2 sem o dígito verificador"""
        return self.bloco_campo2[:-1]

    @property
    def campo3_sem_dv(self) -> str:
        """Retorna o campo 3 sem o dígito verificador"""
        return self.bloco_campo3[:-1]

    @property
    def dv_campo1(self) -> str:
        """Retorna o DV do campo 1"""
        return self.bloco_campo1[-1]

    @property
    def dv_campo2(self) -> str:
        """Retorna o DV do campo 2"""
        return self.bloco_campo2[-1]

    @property
    def dv_campo3(self) -> str:
        """Retorna o DV do campo 3"""
        return self.bloco_campo3[-1]

    @property
    def fator_vencimento(self) -> str:
        """Retorna o fator de vencimento (primeiros 4 dígitos do campo 5)"""
        return self.fator_valor_e_valor[:4]

    @property
    def valor_centavos(self) -> str:
        """Retorna o valor em centavos (últimos 10 dígitos do campo 5)"""
        return self.fator_valor_e_valor[4:14]

    @property
    def valor_decimal(self) -> float:
        """Retorna o valor em reais (decimal)"""
        try:
            return float(self.valor_centavos) / 100
        except (ValueError, TypeError):
            return 0.0

    @property
    def data_vencimento(self) -> Optional[str]:
        """Converte fator de vencimento para data (base: 07/10/1997)"""
        try:
            fator = int(self.fator_vencimento)
            data_base = datetime(1997, 10, 7)
            data_vencimento = data_base + timedelta(days=fator)
            return data_vencimento.strftime("%d/%m/%Y")
        except (ValueError, TypeError):
            return None


class Digitavel:
    """
    Representa a linha digitável de um boleto bancário.

    Responsável por parsing, validação e extração de campos conforme Febraban.
    """

    def __init__(self, valor: str):
        """
        Inicializa o objeto Digitavel

        Args:
            valor: Linha digitável para processar
        """
        self.logger = get_logger("digitavel")
        self.valor = self._normalizar(valor)
        self._campos: Optional[CamposDigitavel] = None

        # Extrair campos se tiver tamanho adequado
        if len(self.valor) >= 47:
            self._extrair_campos()

    def _normalizar(self, valor: str) -> str:
        """
        Normaliza a linha digitável removendo espaços e pontos

        Args:
            valor: Valor para normalizar

        Returns:
            Valor normalizado
        """
        if not valor:
            return ""

        # Normalizar: remover espaços e pontos, mantendo apenas dígitos
        return regex.sub(r"[.\s]", "", valor)

    def _extrair_campos(self) -> None:
        """
        Extrai os campos da linha digitável normalizada (47 dígitos)

        Estrutura correta:
        Campo 1: 0-9 (9 dígitos) + DV 9 (1 dígito) = 10
        Campo 2: 10-20 (10 dígitos) + DV 20 (1 dígito) = 11
        Campo 3: 21-31 (10 dígitos) + DV 31 (1 dígito) = 11
        Campo 4: 32 (1 dígito)
        Campo 5: 33-46 (14 dígitos)
        """
        try:
            bloco_campo1 = self.valor[0:10]  # 9 dígitos + DV
            bloco_campo2 = self.valor[10:21]  # 10 dígitos + DV
            bloco_campo3 = self.valor[21:32]  # 10 dígitos + DV
            dv_geral = self.valor[32:33]  # 1 dígito
            fator_valor_e_valor = self.valor[33:47]  # 14 dígitos

            self._campos = CamposDigitavel(
                bloco_campo1=bloco_campo1,
                bloco_campo2=bloco_campo2,
                bloco_campo3=bloco_campo3,
                dv_geral=dv_geral,
                fator_valor_e_valor=fator_valor_e_valor,
            )
            self.logger.info(
                "Campos extraídos:",
                campos=self._campos,
            )
        except Exception as e:
            self.logger.error("Erro ao extrair campos", erro=str(e))
            self._campos = None

    def _validar_campo(self, campo: str) -> bool:
        """
        Valida o DV de um campo usando Módulo 10

        Args:
            campo: Campo para validar

        Returns:
            True se válido, False caso contrário
        """
        if len(campo) < 2:
            return False

        try:
            campo_sem_dv = campo[:-1]
            dv_esperado = int(campo[-1])
            dv_calculado = modulo_10(campo_sem_dv)

            return dv_calculado == dv_esperado
        except (ValueError, TypeError):
            return False

    def _validar_dv_geral(self, codigo_barras: str) -> bool:
        """
        Valida o DV geral do código de barras usando Módulo 11

        Args:
            codigo_barras: Código de barras para validar

        Returns:
            True se válido, False caso contrário
        """
        if len(codigo_barras) < 2:
            return False

        try:
            codigo_sem_dv = codigo_barras[:-1]
            dv_esperado = int(codigo_barras[-1])
            dv_calculado = modulo_11(codigo_sem_dv)

            return dv_calculado == dv_esperado
        except (ValueError, TypeError):
            return False

    def validar(self) -> bool:
        """
        Valida a linha digitável:
        - Deve conter apenas dígitos
        - Deve ter 47 dígitos
        - DVs dos campos devem ser válidos
        - DV geral deve ser válido

        Returns:
            True se válida, False caso contrário
        """
        if not self.valor.isdigit() or len(self.valor) != 47 or not self._campos:
            return False

        # Validar DVs dos campos
        if not all(
            [
                self._validar_campo(self._campos.bloco_campo1),
                self._validar_campo(self._campos.bloco_campo2),
                self._validar_campo(self._campos.bloco_campo3),
            ]
        ):
            return False

        # Validação DV geral (Módulo 11)
        codigo_barras = self._gerar_codigo_barras()
        self.logger.info(
            "Código de barras gerado:",
            codigo=codigo_barras,
        )
        if not self._validar_dv_geral(codigo_barras):
            return False

        return True

    def _gerar_codigo_barras(self) -> str:
        """
        Gera o código de barras a partir da linha digitável

        Returns:
            Código de barras gerado
        """
        if not self._campos or len(self.valor) < 47:
            return ""

        try:
            # Composição do código de barras (44 dígitos + DV geral)
            banco_moeda = self.valor[0:4]
            campo_livre = self._campos.campo_livre
            fator_valor = self._campos.fator_valor_e_valor

            codigo_sem_dv = banco_moeda + campo_livre + fator_valor
            dv_geral = modulo_11(codigo_sem_dv)

            return codigo_sem_dv + str(dv_geral)
        except Exception as e:
            self.logger.error("Erro ao gerar código de barras", erro=str(e))
            return ""

    def corrigir_dv(self) -> str:
        """
        Sugere uma linha digitável com DVs corrigidos

        Returns:
            Linha digitável com DVs corrigidos
        """
        if not self._campos or len(self.valor) < 47:
            return self.valor

        try:
            # Corrigir campo 2
            campo2_sem_dv = self._campos.bloco_campo2[:-1]
            dv_campo2_calculado = modulo_10(campo2_sem_dv)
            campo2_corrigido = campo2_sem_dv + str(dv_campo2_calculado)

            # Corrigir campo 3
            campo3_sem_dv = self._campos.bloco_campo3[:-1]
            dv_campo3_calculado = modulo_10(campo3_sem_dv)
            campo3_corrigido = campo3_sem_dv + str(dv_campo3_calculado)

            # Corrigir DV geral
            banco_moeda = self.valor[0:4]
            campo_livre = (
                self._campos.bloco_campo1[4:9]
                + campo2_corrigido[:-1]
                + campo3_corrigido[:-1]
            )
            fator_valor = self._campos.fator_valor_e_valor

            codigo_sem_dv = banco_moeda + campo_livre + fator_valor
            dv_geral_calculado = modulo_11(codigo_sem_dv)
            campo4_corrigido = str(dv_geral_calculado)

            # Montar digitável corrigido
            digitavel_corrigido = (
                self._campos.bloco_campo1
                + campo2_corrigido
                + campo3_corrigido
                + campo4_corrigido
                + self._campos.fator_valor_e_valor
            )

            return digitavel_corrigido
        except Exception as e:
            self.logger.error("Erro ao corrigir DVs", erro=str(e))
            return self.valor

    # === PROPRIEDADES ===

    @property
    def banco(self) -> Optional[str]:
        """Retorna o código do banco"""
        return self._campos.banco if self._campos else None

    @property
    def valor_documento(self) -> Optional[float]:
        """Retorna o valor do documento em reais"""
        return self._campos.valor_decimal if self._campos else None

    @property
    def data_vencimento(self) -> Optional[str]:
        """Retorna a data de vencimento"""
        return self._campos.data_vencimento if self._campos else None

    @property
    def fator_vencimento(self) -> Optional[str]:
        """Retorna o fator de vencimento"""
        return self._campos.fator_vencimento if self._campos else None

    @property
    def valor_centavos(self) -> Optional[str]:
        """Retorna o valor em centavos"""
        return self._campos.valor_centavos if self._campos else None

    @property
    def campo_livre(self) -> Optional[str]:
        """Retorna o campo livre completo (25 dígitos) - dados brutos sem interpretação"""
        return self._campos.campo_livre if self._campos else None

    @property
    def codigo_barras(self) -> Optional[str]:
        """Retorna o código de barras gerado"""
        return self._gerar_codigo_barras() if self._campos else None

    # === MÉTODOS ESTÁTICOS ===

    @staticmethod
    def gerar_digitavel_valido(
        banco: str = "033", valor: float = 150.00, vencimento_dias: int = 30
    ) -> str:
        """
        Gera um código digitável válido seguindo as especificações Febraban

        Args:
            banco: Código do banco (3 dígitos)
            valor: Valor do documento
            vencimento_dias: Dias para vencimento

        Returns:
            Linha digitável válida
        """
        try:
            # Data base: 07/10/1997
            data_base = datetime(1997, 10, 7)
            data_vencimento = datetime.now() + timedelta(days=vencimento_dias)
            fator_vencimento = (data_vencimento - data_base).days

            # Valor em centavos (10 dígitos)
            valor_centavos = int(valor * 100)
            valor_str = f"{valor_centavos:010d}"

            # Fator de vencimento (4 dígitos)
            fator_str = f"{fator_vencimento:04d}"

            # Campo livre dummy (25 dígitos)
            campo_livre = "1" * 25

            # Montar campos para linha digitável (estrutura correta)
            campo1_base = banco + "9" + campo_livre[:4]  # 3+1+4 = 8 dígitos
            campo2_base = campo_livre[4:14]  # 10 dígitos
            campo3_base = campo_livre[14:24]  # 10 dígitos

            # Calcular DVs dos campos 1, 2, 3 (Módulo 10)
            dv1 = modulo_10(campo1_base)
            dv2 = modulo_10(campo2_base)
            dv3 = modulo_10(campo3_base)

            campo1 = campo1_base + str(dv1)  # 9 dígitos
            campo2 = campo2_base + str(dv2)  # 11 dígitos
            campo3 = campo3_base + str(dv3)  # 11 dígitos

            # Código de barras sem DV geral (44 dígitos)
            banco_moeda = banco + "9"
            codigo_sem_dv = banco_moeda + campo_livre + fator_str + valor_str
            dv_geral = modulo_11(codigo_sem_dv)

            # Montar linha digitável (47 dígitos)
            digitavel_str = (
                campo1 + campo2 + campo3 + str(dv_geral) + fator_str + valor_str
            )
            return digitavel_str
        except Exception as e:
            logger = get_logger("digitavel")
            logger.error("Erro ao gerar digitável válido", erro=str(e))
            return ""
