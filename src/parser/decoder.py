"""
Decodificador de códigos de barras e digitáveis de boletos bancários.

Este módulo contém a classe BoletoDecoder responsável por decodificar
códigos digitáveis e gerar códigos de barras de boletos bancários.
"""

import re
from datetime import datetime, timedelta
from typing import Any, Dict

from ..utils.logger import get_logger


class BoletoDecoder:
    """Decodificador de códigos de barras e digitáveis de boletos bancários"""

    def __init__(self):
        self.logger = get_logger("boleto_decoder")
        self._bancos = self._inicializar_bancos()

    def decodificar_digitavel(self, digitavel: str) -> Dict[str, Any]:
        """
        Decodifica o código digitável do boleto bancário

        Args:
            digitavel: Código digitável no formato 03399.16140 70000.019182 81556.601014 4 11370000038936

        Returns:
            Dicionário com os dados decodificados

        Raises:
            ValueError: Se o código digitável for inválido
        """
        self.logger.info("Decodificando código digitável", digitavel=digitavel)

        digitavel_limpo = self._limpar_digitavel(digitavel)
        self._validar_digitavel(digitavel_limpo)

        try:
            componentes = self._extrair_componentes(digitavel_limpo)
            resultado = self._montar_resultado(componentes)

            self.logger.info(
                "Código digitável decodificado com sucesso",
                banco=resultado["banco"]["nome"],
                valor=resultado["valor"],
            )

            return resultado

        except Exception as e:
            self.logger.error("Erro ao decodificar código digitável", erro=str(e))
            raise ValueError(f"Erro ao decodificar código digitável: {e}")

    def _limpar_digitavel(self, digitavel: str) -> str:
        """Remove espaços e pontos do código digitável"""
        return re.sub(r"[.\s]", "", digitavel)

    def _validar_digitavel(self, digitavel: str) -> None:
        """Valida se o código digitável tem o tamanho correto"""
        if len(digitavel) != 47:
            raise ValueError("Código digitável deve ter 47 dígitos")

    def _extrair_componentes(self, digitavel: str) -> Dict[str, str]:
        """Extrai os componentes do código digitável"""
        return {
            "banco": digitavel[0:3],
            "moeda": digitavel[3:4],
            "fator_vencimento": digitavel[4:8],
            "valor": digitavel[8:17],
            "digito_verificador": digitavel[17:18],
            "campo_livre": digitavel[18:47],
        }

    def _montar_resultado(self, componentes: Dict[str, str]) -> Dict[str, Any]:
        """Monta o resultado final da decodificação"""
        valor_decimal = float(componentes["valor"]) / 100
        data_vencimento = self._fator_para_data(int(componentes["fator_vencimento"]))
        nome_banco = self._identificar_banco(componentes["banco"])

        return {
            "banco": {"codigo": componentes["banco"], "nome": nome_banco},
            "moeda": componentes["moeda"],
            "vencimento": data_vencimento,
            "valor": valor_decimal,
            "digito_verificador": componentes["digito_verificador"],
            "campo_livre": componentes["campo_livre"],
            "codigo_barras": self._gerar_codigo_barras(
                componentes["banco"]
                + componentes["moeda"]
                + componentes["fator_vencimento"]
                + componentes["valor"]
                + componentes["digito_verificador"]
                + componentes["campo_livre"]
            ),
        }

    def _fator_para_data(self, fator: int) -> str:
        """Converte fator de vencimento para data"""
        # Data base: 07/10/1997
        data_base = datetime(1997, 10, 7)
        data_vencimento = data_base + timedelta(days=fator)
        return data_vencimento.strftime("%d/%m/%Y")

    def _identificar_banco(self, codigo: str) -> str:
        """Identifica o banco pelo código"""
        return self._bancos.get(codigo, f"Banco {codigo}")

    def _gerar_codigo_barras(self, digitavel: str) -> str:
        """Gera código de barras a partir do digitável"""
        # Remove dígitos verificadores e reorganiza
        # Formato: 03399161407000001918281556601014411370000038936
        return (
            digitavel[0:4]
            + digitavel[32:47]
            + digitavel[4:9]
            + digitavel[10:20]
            + digitavel[21:31]
        )

    def _inicializar_bancos(self) -> Dict[str, str]:
        """Inicializa o dicionário de bancos"""
        return {
            "001": "Banco do Brasil",
            "033": "Santander",
            "104": "Caixa Econômica Federal",
            "237": "Bradesco",
            "341": "Itaú",
            "756": "Sicoob",
            "422": "Safra",
            "077": "Inter",
            "212": "Banco Original",
            "260": "Nu Pagamentos",
            "336": "C6 Bank",
            "655": "Banco Votorantim",
            "041": "Banrisul",
            "004": "Banco do Nordeste",
            "021": "Banestes",
            "047": "Banco do Estado de Sergipe",
            "085": "Cecred",
            "097": "Credisis",
            "136": "Unicred",
            "151": "Cooperativa Sicredi",
            "318": "Banco BMG",
            "356": "Banco Real",
            "389": "Banco Mercantil",
            "399": "HSBC",
            "633": "Banco Rendimento",
            "652": "Itaú Unibanco",
            "745": "Citibank",
            "748": "Sicredi",
        }
