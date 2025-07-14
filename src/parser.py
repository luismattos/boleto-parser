import re
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from .logger import get_logger
from .models import (
    BoletoData,
    DadosAluno,
    DadosBeneficiario,
    DadosPagador,
    EnderecoInstituicao,
    InformacoesBancarias,
    Instrucoes,
    Valores,
)


class BoletoParser:
    """Parser inteligente para boletos bancários PDF"""

    def __init__(self):
        self.texto_extraido = ""
        self.logger = get_logger("boleto_parser")

    def detectar_tipo_arquivo(self, caminho_arquivo: str) -> str:
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

    def extrair_texto_pdf(self, caminho_arquivo: str) -> str:
        """Extrai texto do PDF usando pdftotext"""
        self.logger.info("Extraindo texto do PDF", arquivo=caminho_arquivo)
        try:
            resultado = subprocess.run(
                ["pdftotext", caminho_arquivo, "-"],
                capture_output=True,
                text=True,
                check=True,
            )
            texto_extraido = resultado.stdout
            self.logger.info("Texto extraído com sucesso", tamanho=len(texto_extraido))
            return texto_extraido
        except subprocess.CalledProcessError as e:
            self.logger.error("Erro ao extrair texto do PDF", erro=str(e))
            raise ValueError(f"Erro ao extrair texto do PDF: {e}")
        except FileNotFoundError:
            self.logger.error("Comando pdftotext não encontrado")
            raise ValueError(
                "Comando 'pdftotext' não encontrado. Instale o poppler-utils."
            )

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

    def _extrair_dados_beneficiario(self) -> DadosBeneficiario:
        """Extrai dados do beneficiário"""
        # Nome do beneficiário
        padrao_nome = r"Beneficiário\s*(.+?)\s*-\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})"
        match = re.search(padrao_nome, self.texto_extraido)

        nome = match.group(1).strip() if match else ""
        cnpj = match.group(2) if match else ""

        # Agência e código
        padrao_agencia = r"Agência / Código do Beneficiário\s*(\d+)\s*/\s*(\d+)"
        match_agencia = re.search(padrao_agencia, self.texto_extraido)

        agencia = match_agencia.group(1) if match_agencia else ""
        codigo = match_agencia.group(2) if match_agencia else ""

        # Nosso número
        padrao_nosso_numero = r"Nosso Número\s*(\d+)"
        match_nosso = re.search(padrao_nosso_numero, self.texto_extraido)
        nosso_numero = match_nosso.group(1) if match_nosso else ""

        return DadosBeneficiario(
            nome=nome,
            cnpj=cnpj,
            agencia=agencia,
            codigo_beneficiario=codigo,
            nosso_numero=nosso_numero,
        )

    def _extrair_dados_pagador(self) -> DadosPagador:
        """Extrai dados do pagador"""
        # Nome e CPF
        padrao_pagador = r"Pagador:\s*(.+?)\s*-\s*CPF/CNPJ:\s*([\d\.-]+)"
        match = re.search(padrao_pagador, self.texto_extraido)

        nome = match.group(1).strip() if match else ""
        cpf = match.group(2) if match else ""

        # Endereço
        padrao_endereco = r"R\s+([^C]+?)\s+CEP:\s*(\d{5}-\d{3})"
        match_endereco = re.search(padrao_endereco, self.texto_extraido)

        endereco = match_endereco.group(1).strip() if match_endereco else ""
        cep = match_endereco.group(2) if match_endereco else ""

        return DadosPagador(nome=nome, cpf_cnpj=cpf, endereco=endereco, cep=cep)

    def _extrair_dados_aluno(self) -> Optional[DadosAluno]:
        """Extrai dados do aluno (se for boleto educacional)"""
        # Nome do aluno
        padrao_nome = r"Nome do Aluno:\s*(.+)"
        match_nome = re.search(padrao_nome, self.texto_extraido)
        nome = match_nome.group(1).strip() if match_nome else ""

        # Matrícula
        padrao_matricula = r"Matrícula:\s*(\d+)"
        match_matricula = re.search(padrao_matricula, self.texto_extraido)
        matricula = match_matricula.group(1) if match_matricula else ""

        # Curso/Turno
        padrao_curso = r"Curso/Turno\s*(.+?)/(.+?)/(\d+)"
        match_curso = re.search(padrao_curso, self.texto_extraido)

        if match_curso:
            curso = match_curso.group(1).strip()
            turno = match_curso.group(2).strip()
            codigo = match_curso.group(3)
        else:
            curso = ""
            turno = ""
            codigo = ""

        if nome and matricula:
            return DadosAluno(
                nome=nome, matricula=matricula, curso=curso, turno=turno, codigo=codigo
            )
        return None

    def _extrair_valores(self) -> Valores:
        """Extrai valores do boleto"""
        # Valor do documento
        padrao_valor = r"Valor do documento\s*R\$\s*([\d,]+\.?\d*)"
        match_valor = re.search(padrao_valor, self.texto_extraido)
        valor_documento = (
            float(match_valor.group(1).replace(",", ".")) if match_valor else 0.0
        )

        # Valor cobrado
        padrao_cobrado = r"Valor Cobrado\s*R\$\s*([\d,]+\.?\d*)"
        match_cobrado = re.search(padrao_cobrado, self.texto_extraido)
        valor_cobrado = (
            float(match_cobrado.group(1).replace(",", "."))
            if match_cobrado
            else valor_documento
        )

        # Total de débitos
        padrao_debitos = r"Total de Débitos:\s*R\$\s*([\d,]+\.?\d*)"
        match_debitos = re.search(padrao_debitos, self.texto_extraido)
        total_debitos = (
            float(match_debitos.group(1).replace(",", ".")) if match_debitos else None
        )

        return Valores(
            valor_documento=valor_documento,
            valor_cobrado=valor_cobrado,
            total_debitos=total_debitos,
        )

    def _extrair_informacoes_bancarias(self) -> InformacoesBancarias:
        """Extrai informações bancárias"""
        # Banco
        padrao_banco = r"BANCO\s+(.+?)\s+S\.\s*A\."
        match_banco = re.search(padrao_banco, self.texto_extraido)
        banco = match_banco.group(1).strip() if match_banco else ""

        # Código de barras
        padrao_barras = r"(\d{3}\d{3}\d{3}\.\d{1}\s+\d{3}\d{3}\d{3}\d{3}\d{3}\.\d{1}\s+\d{3}\d{3}\d{3}\d{3}\d{3}\.\d{1}\s+\d{1}\s+\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3})"
        match_barras = re.search(padrao_barras, self.texto_extraido)
        codigo_barras = match_barras.group(1) if match_barras else ""

        # Carteira
        padrao_carteira = r"Carteira\s*(\w+)"
        match_carteira = re.search(padrao_carteira, self.texto_extraido)
        carteira = match_carteira.group(1) if match_carteira else ""

        # Espécie
        padrao_especie = r"Espécie\s*(\w+)"
        match_especie = re.search(padrao_especie, self.texto_extraido)
        especie = match_especie.group(1) if match_especie else ""

        # Aceite
        padrao_aceite = r"Aceite\s*(\w)"
        match_aceite = re.search(padrao_aceite, self.texto_extraido)
        aceite = match_aceite.group(1) if match_aceite else ""

        return InformacoesBancarias(
            banco=banco,
            codigo_barras=codigo_barras,
            carteira=carteira,
            especie=especie,
            aceite=aceite,
        )

    def _extrair_instrucoes(self) -> Instrucoes:
        """Extrai instruções de pagamento"""
        # Local de pagamento
        padrao_local = r"Local do Pagamento\s*(.+?)\n"
        match_local = re.search(padrao_local, self.texto_extraido)
        local_pagamento = match_local.group(1).strip() if match_local else ""

        # Multa
        padrao_multa = r"Multa após o vencimento:\s*(.+?)\."
        match_multa = re.search(padrao_multa, self.texto_extraido)
        multa = match_multa.group(1) if match_multa else None

        # Juros
        padrao_juros = r"juros de\s*(.+?)\s+por dia"
        match_juros = re.search(padrao_juros, self.texto_extraido)
        juros = match_juros.group(1) if match_juros else None

        # Restrições
        padrao_restricoes = r"Instruções\s*(.+?)(?=\n\n|\n[A-Z]|$)"
        match_restricoes = re.search(padrao_restricoes, self.texto_extraido, re.DOTALL)
        restricoes = match_restricoes.group(1).strip() if match_restricoes else None

        return Instrucoes(
            local_pagamento=local_pagamento,
            multa_vencimento=multa,
            juros_dia_atraso=juros,
            restricoes=restricoes,
        )

    def _extrair_endereco_instituicao(self) -> EnderecoInstituicao:
        """Extrai endereço da instituição"""
        padrao = r"Endereço da Instituição:\s*(.+?)\s+CEP:\s*(\d{5}-\d{3})"
        match = re.search(padrao, self.texto_extraido)

        if match:
            endereco = match.group(1).strip()
            cep = match.group(2)
        else:
            endereco = ""
            cep = ""

        return EnderecoInstituicao(endereco=endereco, cep=cep)

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

    def parse(self, caminho_arquivo: str) -> BoletoData:
        """Método principal que faz todo o parsing do boleto"""
        self.logger.info("Iniciando parsing do boleto", arquivo=caminho_arquivo)

        # Verificar se arquivo existe
        if not Path(caminho_arquivo).exists():
            self.logger.error("Arquivo não encontrado", arquivo=caminho_arquivo)
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

        # Detectar tipo do arquivo
        tipo_arquivo = self.detectar_tipo_arquivo(caminho_arquivo)
        if "PDF" not in tipo_arquivo:
            self.logger.error("Arquivo não é PDF válido", tipo=tipo_arquivo)
            raise ValueError(f"Arquivo não é um PDF válido: {tipo_arquivo}")

        # Extrair texto do PDF
        self.texto_extraido = self.extrair_texto_pdf(caminho_arquivo)

        # Identificar tipo do boleto
        tipo_boleto = self._identificar_tipo_boleto()
        self.logger.info("Tipo de boleto identificado", tipo=tipo_boleto)

        # Extrair todos os dados
        self.logger.info("Extraindo dados do boleto")
        dados = BoletoData(
            cnpj_instituicao=self._extrair_cnpj_instituicao(),
            numero_boleto=self._extrair_numero_boleto(),
            vencimento=self._extrair_vencimento(),
            data_documento=self._extrair_data_documento(),
            beneficiario=self._extrair_dados_beneficiario(),
            pagador=self._extrair_dados_pagador(),
            aluno=self._extrair_dados_aluno(),
            valores=self._extrair_valores(),
            informacoes_bancarias=self._extrair_informacoes_bancarias(),
            instrucoes=self._extrair_instrucoes(),
            endereco_instituicao=self._extrair_endereco_instituicao(),
            tipo_boleto=tipo_boleto,
            texto_extraido=self.texto_extraido,
        )

        self.logger.info(
            "Parsing concluído com sucesso",
            beneficiario=dados.beneficiario.nome,
            valor=dados.valores.valor_documento,
            tipo=dados.tipo_boleto,
        )

        return dados
