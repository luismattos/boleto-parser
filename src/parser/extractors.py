"""
Extratores especializados para diferentes tipos de dados de boletos.

Este módulo contém classes especializadas para extrair diferentes tipos
de informações de boletos bancários a partir do texto extraído.
"""

import re
from typing import Any, Dict, Optional

from ..models import (
    DadosAluno,
    DadosBeneficiario,
    DadosPagador,
    EnderecoInstituicao,
    InformacoesBancarias,
    Instrucoes,
    Valores,
)
from ..utils.logger import get_logger


class BoletoDataExtractor:
    """Classe base para extratores de dados de boletos"""

    def __init__(self, texto_extraido: str):
        self.texto_extraido = texto_extraido
        self.logger = get_logger(self.__class__.__name__)

    def _extrair_com_regex(self, padrao: str, grupo: int = 1) -> str:
        """Extrai valor usando regex com tratamento de erro"""
        match = re.search(padrao, self.texto_extraido)
        return match.group(grupo).strip() if match else ""

    def _extrair_valor_monetario(self, padrao: str) -> float:
        """Extrai valor monetário usando regex"""
        match = re.search(padrao, self.texto_extraido)
        if match:
            valor_str = match.group(1).replace(",", ".")
            return float(valor_str)
        return 0.0


class BeneficiarioExtractor(BoletoDataExtractor):
    """Extrator de dados do beneficiário"""

    def extrair(self) -> DadosBeneficiario:
        """Extrai dados do beneficiário"""
        nome, cnpj = self._extrair_nome_cnpj()
        agencia, codigo = self._extrair_agencia_codigo()
        nosso_numero = self._extrair_nosso_numero()

        return DadosBeneficiario(
            nome=nome,
            cnpj=cnpj,
            agencia=agencia,
            codigo_beneficiario=codigo,
            nosso_numero=nosso_numero,
        )

    def _extrair_nome_cnpj(self) -> tuple[str, str]:
        """Extrai nome e CNPJ do beneficiário"""
        padrao = r"Beneficiário\s*(.+?)\s*-\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})"
        match = re.search(padrao, self.texto_extraido)

        nome = match.group(1).strip() if match else ""
        cnpj = match.group(2) if match else ""

        return nome, cnpj

    def _extrair_agencia_codigo(self) -> tuple[str, str]:
        """Extrai agência e código do beneficiário"""
        padrao = r"Agência / Código do Beneficiário\s*(\d+)\s*/\s*(\d+)"
        match = re.search(padrao, self.texto_extraido)

        agencia = match.group(1) if match else ""
        codigo = match.group(2) if match else ""

        return agencia, codigo

    def _extrair_nosso_numero(self) -> str:
        """Extrai nosso número"""
        return self._extrair_com_regex(r"Nosso Número\s*(\d+)")


class PagadorExtractor(BoletoDataExtractor):
    """Extrator de dados do pagador"""

    def extrair(self) -> DadosPagador:
        """Extrai dados do pagador"""
        nome, cpf = self._extrair_nome_cpf()
        endereco, cep = self._extrair_endereco_cep()

        return DadosPagador(nome=nome, cpf_cnpj=cpf, endereco=endereco, cep=cep)

    def _extrair_nome_cpf(self) -> tuple[str, str]:
        """Extrai nome e CPF/CNPJ do pagador"""
        padrao = r"Pagador:\s*(.+?)\s*-\s*CPF/CNPJ:\s*([\d\.-]+)"
        match = re.search(padrao, self.texto_extraido)

        nome = match.group(1).strip() if match else ""
        cpf = match.group(2) if match else ""

        return nome, cpf

    def _extrair_endereco_cep(self) -> tuple[str, str]:
        """Extrai endereço e CEP do pagador"""
        padrao = r"R\s+([^C]+?)\s+CEP:\s*(\d{5}-\d{3})"
        match = re.search(padrao, self.texto_extraido)

        endereco = match.group(1).strip() if match else ""
        cep = match.group(2) if match else ""

        return endereco, cep


class AlunoExtractor(BoletoDataExtractor):
    """Extrator de dados do aluno (boletos educacionais)"""

    def extrair(self) -> Optional[DadosAluno]:
        """Extrai dados do aluno se for boleto educacional"""
        nome = self._extrair_com_regex(r"Nome do Aluno:\s*(.+)")
        matricula = self._extrair_com_regex(r"Matrícula:\s*(\d+)")

        if not nome or not matricula:
            return None

        curso, turno, codigo = self._extrair_curso_turno()

        return DadosAluno(
            nome=nome,
            matricula=matricula,
            curso=curso,
            turno=turno,
            codigo=codigo,
        )

    def _extrair_curso_turno(self) -> tuple[str, str, str]:
        """Extrai informações do curso e turno"""
        padrao = r"Curso/Turno\s*(.+?)/(.+?)/(\d+)"
        match = re.search(padrao, self.texto_extraido)

        if match:
            curso = match.group(1).strip()
            turno = match.group(2).strip()
            codigo = match.group(3)
        else:
            curso = ""
            turno = ""
            codigo = ""

        return curso, turno, codigo


class ValoresExtractor(BoletoDataExtractor):
    """Extrator de valores do boleto"""

    def extrair(self) -> Valores:
        """Extrai valores do boleto"""
        valor_documento = self._extrair_valor_documento()
        valor_cobrado = self._extrair_valor_cobrado(valor_documento)
        total_debitos = self._extrair_total_debitos()

        return Valores(
            valor_documento=valor_documento,
            valor_cobrado=valor_cobrado,
            total_debitos=total_debitos,
        )

    def _extrair_valor_documento(self) -> float:
        """Extrai valor do documento"""
        return self._extrair_valor_monetario(
            r"Valor do documento\s*R\$\s*([\d,]+\.?\d*)"
        )

    def _extrair_valor_cobrado(self, valor_documento: float) -> float:
        """Extrai valor cobrado"""
        valor_cobrado = self._extrair_valor_monetario(
            r"Valor Cobrado\s*R\$\s*([\d,]+\.?\d*)"
        )
        return valor_cobrado if valor_cobrado > 0 else valor_documento

    def _extrair_total_debitos(self) -> Optional[float]:
        """Extrai total de débitos"""
        valor = self._extrair_valor_monetario(
            r"Total de Débitos:\s*R\$\s*([\d,]+\.?\d*)"
        )
        return valor if valor > 0 else None


class InformacoesBancariasExtractor(BoletoDataExtractor):
    """Extrator de informações bancárias"""

    def extrair(self) -> InformacoesBancarias:
        """Extrai informações bancárias"""
        banco = self._extrair_com_regex(r"BANCO\s+(.+?)\s+S\.\s*A\.")
        codigo_barras = self._extrair_codigo_barras()
        carteira = self._extrair_com_regex(r"Carteira\s*(\w+)")
        especie = self._extrair_com_regex(r"Espécie\s*(\w+)")
        aceite = self._extrair_com_regex(r"Aceite\s*(\w)")

        return InformacoesBancarias(
            banco=banco,
            codigo_barras=codigo_barras,
            carteira=carteira,
            especie=especie,
            aceite=aceite,
        )

    def _extrair_codigo_barras(self) -> str:
        """Extrai código de barras"""
        padrao = r"(\d{3}\d{3}\d{3}\.\d{1}\s+\d{3}\d{3}\d{3}\d{3}\d{3}\.\d{1}\s+\d{3}\d{3}\d{3}\d{3}\d{3}\.\d{1}\s+\d{1}\s+\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3})"
        return self._extrair_com_regex(padrao)


class InstrucoesExtractor(BoletoDataExtractor):
    """Extrator de instruções de pagamento"""

    def extrair(self) -> Instrucoes:
        """Extrai instruções de pagamento"""
        local_pagamento = self._extrair_com_regex(r"Local do Pagamento\s*(.+?)\n")
        multa = self._extrair_com_regex(r"Multa após o vencimento:\s*(.+?)\.")
        juros = self._extrair_com_regex(r"juros de\s*(.+?)\s+por dia")
        restricoes = self._extrair_restricoes()

        return Instrucoes(
            local_pagamento=local_pagamento,
            multa_vencimento=multa if multa else None,
            juros_dia_atraso=juros if juros else None,
            restricoes=restricoes,
        )

    def _extrair_restricoes(self) -> Optional[str]:
        """Extrai restrições das instruções"""
        padrao = r"Instruções\s*(.+?)(?=\n\n|\n[A-Z]|$)"
        match = re.search(padrao, self.texto_extraido, re.DOTALL)
        return match.group(1).strip() if match else None


class EnderecoInstituicaoExtractor(BoletoDataExtractor):
    """Extrator de endereço da instituição"""

    def extrair(self) -> EnderecoInstituicao:
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


class DadosExtrasExtractor(BoletoDataExtractor):
    """Extrator de dados extras e opcionais"""

    def extrair(self) -> Dict[str, Any]:
        """Extrai dados extras que não se encaixam nos campos padrão"""
        dados_extras = {}

        # Extrair usando padrões predefinidos
        self._extrair_padroes_predefinidos(dados_extras)

        # Extrair linhas com informações extras
        self._extrair_linhas_extras(dados_extras)

        self.logger.info("Dados extras extraídos", quantidade=len(dados_extras))
        return dados_extras

    def _extrair_padroes_predefinidos(self, dados_extras: Dict[str, Any]) -> None:
        """Extrai dados usando padrões predefinidos"""
        padroes = {
            "protocolo": r"Protocolo[:\s]*(\d+)",
            "codigo_curso": r"Código do Curso[:\s]*(\d+)",
            "turma": r"Turma[:\s]*([A-Z0-9]+)",
            "disciplina": r"Disciplina[:\s]*([A-Za-z\s]+)",
            "periodo": r"Período[:\s]*(\d+)",
            "semestre": r"Semestre[:\s]*(\d+)",
            "ano_letivo": r"Ano Letivo[:\s]*(\d{4})",
            "codigo_baixa": r"Código de Baixa[:\s]*(\d+)",
            "uso_banco": r"Uso do Banco[:\s]*([A-Za-z0-9\s]+)",
            "quantidade": r"Quantidade[:\s]*(\d+)",
            "data_processamento": r"Data processamento[:\s]*(\d{2}/\d{2}/\d{4})",
            "especie_doc": r"Espécie Doc\s*\n([A-Za-z]{2,})",
            "aceite": r"Aceite[:\s]*([A-Z])",
            "codigo_beneficiario_completo": r"Código do Beneficiário[:\s]*(\d+)",
            "agencia_completa": r"Agência[:\s]*(\d+)",
            "conta_corrente": r"Conta[:\s]*(\d+)",
            "nosso_numero_completo": r"Nosso Número[:\s]*(\d+)",
            "numero_documento": r"Nº do Documento[:\s]*(\d+)",
            "carteira_completa": r"Carteira[:\s]*([A-Za-z0-9]+)",
            "especie_completa": r"Espécie[:\s]*([A-Za-z]+)",
            "valor_abatimento": r"Abatimento[:\s]*R\$\s*([\d,]+\.?\d*)",
            "valor_desconto": r"Desconto[:\s]*R\$\s*([\d,]+\.?\d*)",
            "valor_outras_deducoes": r"Outras Deduções[:\s]*R\$\s*([\d,]+\.?\d*)",
            "valor_mora_multa": r"Mora / Multa[:\s]*R\$\s*([\d,]+\.?\d*)",
            "valor_outros_acrescimos": r"Outros Acréscimos[:\s]*R\$\s*([\d,]+\.?\d*)",
            "valor_cobrado": r"Valor Cobrado[:\s]*R\$\s*([\d,]+\.?\d*)",
            "autenticacao": r"Autenticação[:\s]*([A-Za-z0-9\s]+)",
            "ficha_compensacao": r"Ficha de Compensação[:\s]*([A-Za-z0-9\s]+)",
            "codigo_operacional": r"Código Operacional[:\s]*(\d+)",
            "valor_operacional": r"Valor Operacional[:\s]*R\$\s*([\d,]+\.?\d*)",
            "data_operacional": r"Data Operacional[:\s]*(\d{2}/\d{2}/\d{4})",
            "tipo_operacao": r"Tipo de Operação[:\s]*([A-Za-z\s]+)",
            "responsavel": r"Responsável[:\s]*([A-Za-z\s]+)",
            "codigo_responsavel": r"Código do Responsável[:\s]*(\d+)",
            "matricula_responsavel": r"Matrícula do Responsável[:\s]*(\d+)",
            "endereco_pagador": r"Endereço do Pagador[:\s]*([A-Za-z0-9\s,.-]+)",
            "telefone_pagador": r"Telefone[:\s]*([\d\s\-\(\)]+)",
            "email_pagador": r"Email[:\s]*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
            "observacoes": r"Observações[:\s]*([A-Za-z0-9\s,.-]+)",
            "instrucoes_especiais": r"Instruções Especiais[:\s]*([A-Za-z0-9\s,.-]+)",
            "codigo_barras_digitavel": r"(\d{3}\d{3}\d{3}\.\d{1}\s+\d{3}\d{3}\d{3}\d{3}\d{3}\.\d{1}\s+\d{3}\d{3}\d{3}\d{3}\d{3}\.\d{1}\s+\d{1}\s+\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3})",
            "linha_digitavel": r"(\d{3}\d{3}\d{3}\.\d{1}\s+\d{3}\d{3}\d{3}\d{3}\d{3}\.\d{1}\s+\d{3}\d{3}\d{3}\d{3}\d{3}\.\d{1}\s+\d{1}\s+\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3}\d{3})",
        }

        for nome_campo, padrao in padroes.items():
            match = re.search(padrao, self.texto_extraido, re.IGNORECASE)
            if match:
                valor = match.group(1).strip()
                if valor:
                    dados_extras[nome_campo] = valor

    def _extrair_linhas_extras(self, dados_extras: Dict[str, Any]) -> None:
        """Extrai informações extras de linhas não padronizadas"""
        campos_conhecidos = [
            "beneficiário",
            "pagador",
            "vencimento",
            "valor",
            "cnpj",
            "cpf",
            "endereço",
            "cep",
            "aluno",
            "matrícula",
            "curso",
            "banco",
            "agência",
            "carteira",
            "espécie",
            "aceite",
            "local",
            "multa",
            "juros",
            "instruções",
        ]

        linhas = self.texto_extraido.split("\n")
        for linha in linhas:
            linha = linha.strip()
            if linha and ":" in linha and len(linha) > 10:
                if not any(campo in linha.lower() for campo in campos_conhecidos):
                    if ":" in linha:
                        chave, valor = linha.split(":", 1)
                        chave = chave.strip().lower().replace(" ", "_")
                        valor = valor.strip()
                        if valor and chave not in dados_extras:
                            dados_extras[f"info_{chave}"] = valor
