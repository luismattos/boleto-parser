"""
Parser principal para boletos bancários PDF.

Este módulo contém a classe BoletoParser que coordena a extração
de dados de boletos bancários usando extratores especializados.
"""

import re
import subprocess
from pathlib import Path
from typing import Dict

from ..models import BoletoData
from ..utils.logger import get_logger
from .decoder import BoletoDecoder
from .extractors import (
    AlunoExtractor,
    BeneficiarioExtractor,
    DadosExtrasExtractor,
    EnderecoInstituicaoExtractor,
    InformacoesBancariasExtractor,
    InstrucoesExtractor,
    PagadorExtractor,
    ValoresExtractor,
)


class BoletoParser:
    """Parser inteligente para boletos bancários PDF"""

    def __init__(self):
        self.logger = get_logger("boleto_parser")
        self.decoder = BoletoDecoder()
        self.texto_extraido = ""

    def parse(self, caminho_arquivo: str) -> BoletoData:
        """
        Método principal que faz todo o parsing do boleto

        Args:
            caminho_arquivo: Caminho para o arquivo PDF do boleto

        Returns:
            Objeto BoletoData com todos os dados extraídos

        Raises:
            FileNotFoundError: Se o arquivo não for encontrado
            ValueError: Se o arquivo não for um PDF válido
        """
        self.logger.info("Iniciando parsing do boleto", arquivo=caminho_arquivo)

        self._validar_arquivo(caminho_arquivo)
        self._extrair_texto_pdf(caminho_arquivo)

        tipo_boleto = self._identificar_tipo_boleto()
        self.logger.info("Tipo de boleto identificado", tipo=tipo_boleto)

        dados = self._extrair_dados_completos(tipo_boleto)

        self.logger.info(
            "Parsing concluído com sucesso",
            beneficiario=dados.beneficiario.nome,
            valor=dados.valores.valor_documento,
            tipo=dados.tipo_boleto,
        )

        return dados

    def _validar_arquivo(self, caminho_arquivo: str) -> None:
        """Valida se o arquivo existe e é um PDF válido"""
        if not Path(caminho_arquivo).exists():
            self.logger.error("Arquivo não encontrado", arquivo=caminho_arquivo)
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

        tipo_arquivo = self._detectar_tipo_arquivo(caminho_arquivo)
        if "PDF" not in tipo_arquivo:
            self.logger.error("Arquivo não é PDF válido", tipo=tipo_arquivo)
            raise ValueError(f"Arquivo não é um PDF válido: {tipo_arquivo}")

    def _detectar_tipo_arquivo(self, caminho_arquivo: str) -> str:
        """Detecta o tipo do arquivo usando o comando 'file'"""
        self.logger.info("Detectando tipo do arquivo", arquivo=caminho_arquivo)
        try:
            resultado = subprocess.run(
                ["file", caminho_arquivo], capture_output=True, text=True, check=True
            )
            tipo_arquivo = resultado.stdout.strip()
            self.logger.info("Tipo do arquivo detectado", tipo=tipo_arquivo)
            return tipo_arquivo
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao detectar tipo do arquivo", erro=str(e))
            raise ValueError(f"Erro ao detectar tipo do arquivo: {e}")

    def _extrair_texto_pdf(self, caminho_arquivo: str) -> None:
        """Extrai texto do PDF usando pdftotext"""
        self.logger.info("Extraindo texto do PDF", arquivo=caminho_arquivo)
        try:
            resultado = subprocess.run(
                ["pdftotext", caminho_arquivo, "-"],
                capture_output=True,
                text=True,
                check=True,
            )
            self.texto_extraido = resultado.stdout
            self.logger.info(
                "Texto extraído com sucesso", tamanho=len(self.texto_extraido)
            )
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao extrair texto do PDF", erro=str(e))
            raise ValueError(f"Erro ao extrair texto do PDF: {e}")
        except FileNotFoundError:
            self.logger.error("Comando pdftotext não encontrado")
            raise ValueError(
                "Comando 'pdftotext' não encontrado. Instale o poppler-utils."
            )

    def _identificar_tipo_boleto(self) -> str:
        """Identifica o tipo do boleto baseado no conteúdo"""
        if (
            "Nome do Aluno:" in self.texto_extraido
            and "Curso/Turno" in self.texto_extraido
        ):
            return "educacional"
        elif "Beneficiário" in self.texto_extraido:
            return "bancario"
        else:
            return "desconhecido"

    def _extrair_dados_completos(self, tipo_boleto: str) -> BoletoData:
        """Extrai todos os dados do boleto usando extratores especializados"""
        self.logger.info("Extraindo dados do boleto")

        # Criar extratores
        beneficiario_extractor = BeneficiarioExtractor(self.texto_extraido)
        pagador_extractor = PagadorExtractor(self.texto_extraido)
        valores_extractor = ValoresExtractor(self.texto_extraido)
        info_bancarias_extractor = InformacoesBancariasExtractor(self.texto_extraido)
        instrucoes_extractor = InstrucoesExtractor(self.texto_extraido)
        endereco_extractor = EnderecoInstituicaoExtractor(self.texto_extraido)
        dados_extras_extractor = DadosExtrasExtractor(self.texto_extraido)

        # Extrair dados básicos
        dados_basicos = self._extrair_dados_basicos()

        # Extrair dados específicos por tipo
        aluno = None
        if tipo_boleto == "educacional":
            aluno_extractor = AlunoExtractor(self.texto_extraido)
            aluno = aluno_extractor.extrair()

        return BoletoData(
            cnpj_instituicao=dados_basicos["cnpj_instituicao"],
            numero_boleto=dados_basicos["numero_boleto"],
            vencimento=dados_basicos["vencimento"],
            data_documento=dados_basicos["data_documento"],
            beneficiario=beneficiario_extractor.extrair(),
            pagador=pagador_extractor.extrair(),
            aluno=aluno,
            valores=valores_extractor.extrair(),
            informacoes_bancarias=info_bancarias_extractor.extrair(),
            instrucoes=instrucoes_extractor.extrair(),
            endereco_instituicao=endereco_extractor.extrair(),
            tipo_boleto=tipo_boleto,
            texto_extraido=self.texto_extraido,
            dados_extras=dados_extras_extractor.extrair(),
        )

    def _extrair_dados_basicos(self) -> Dict[str, str]:
        """Extrai dados básicos do boleto"""
        return {
            "cnpj_instituicao": self._extrair_cnpj_instituicao(),
            "numero_boleto": self._extrair_numero_boleto(),
            "vencimento": self._extrair_vencimento(),
            "data_documento": self._extrair_data_documento(),
        }

    def _extrair_cnpj_instituicao(self) -> str:
        """Extrai CNPJ da instituição"""
        padrao = r"CNPJ da Instituição:\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})"
        match = re.search(padrao, self.texto_extraido)
        return match.group(1) if match else ""

    def _extrair_numero_boleto(self) -> str:
        """Extrai número do boleto"""
        padrao = r"Boleto:\s*(\d+)"
        match = re.search(padrao, self.texto_extraido)
        return match.group(1) if match else ""

    def _extrair_vencimento(self) -> str:
        """Extrai data de vencimento"""
        padrao = r"Vencimento:\s*(\d{2}/\d{2}/\d{4})"
        match = re.search(padrao, self.texto_extraido)
        return match.group(1) if match else ""

    def _extrair_data_documento(self) -> str:
        """Extrai data do documento"""
        padrao = r"Data do documento\s*(\d{2}/\d{2}/\d{4})"
        match = re.search(padrao, self.texto_extraido)
        return match.group(1) if match else ""
