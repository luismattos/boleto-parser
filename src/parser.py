import re
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any

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


class BoletoDecoder:
    """Decodificador de códigos de barras e digitáveis de boletos bancários"""
    
    def __init__(self):
        self.logger = get_logger("boleto_decoder")
    
    def decodificar_digitavel(self, digitavel: str) -> Dict[str, Any]:
        """
        Decodifica o código digitável do boleto bancário
        
        Formato esperado: 03399.16140 70000.019182 81556.601014 4 11370000038936
        """
        self.logger.info("Decodificando código digitável", digitavel=digitavel)
        
        # Remove espaços e pontos
        digitavel_limpo = re.sub(r'[.\s]', '', digitavel)
        
        if len(digitavel_limpo) != 47:
            raise ValueError("Código digitável deve ter 47 dígitos")
        
        # Estrutura do código de barras (47 dígitos):
        # 03399.16140 70000.019182 81556.601014 4 11370000038936
        # |-----|------|----------|----------|-|---------------|
        # |Banco|Moeda|FatorVenc|Valor    |D|Campo Livre    |
        
        try:
            # Extrair componentes
            banco = digitavel_limpo[0:3]
            moeda = digitavel_limpo[3:4]
            fator_vencimento = digitavel_limpo[4:8]
            valor = digitavel_limpo[8:17]
            digito_verificador = digitavel_limpo[17:18]
            campo_livre = digitavel_limpo[18:47]
            
            # Converter valor (últimos 2 dígitos são centavos)
            valor_decimal = float(valor) / 100
            
            # Converter fator de vencimento para data
            data_vencimento = self._fator_para_data(int(fator_vencimento))
            
            # Identificar banco
            nome_banco = self._identificar_banco(banco)
            
            resultado = {
                "banco": {
                    "codigo": banco,
                    "nome": nome_banco
                },
                "moeda": moeda,
                "vencimento": data_vencimento,
                "valor": valor_decimal,
                "digito_verificador": digito_verificador,
                "campo_livre": campo_livre,
                "codigo_barras": self._gerar_codigo_barras(digitavel_limpo)
            }
            
            self.logger.info("Código digitável decodificado com sucesso", 
                           banco=nome_banco, valor=valor_decimal)
            
            return resultado
            
        except Exception as e:
            self.logger.error("Erro ao decodificar código digitável", erro=str(e))
            raise ValueError(f"Erro ao decodificar código digitável: {e}")
    
    def _fator_para_data(self, fator: int) -> str:
        """Converte fator de vencimento para data"""
        # Data base: 07/10/1997
        from datetime import datetime, timedelta
        
        data_base = datetime(1997, 10, 7)
        data_vencimento = data_base + timedelta(days=fator)
        return data_vencimento.strftime("%d/%m/%Y")
    
    def _identificar_banco(self, codigo: str) -> str:
        """Identifica o banco pelo código"""
        bancos = {
            "001": "Banco do Brasil",
            "033": "Santander",
            "104": "Caixa Econômica Federal",
            "237": "Bradesco",
            "341": "Itaú",
            "756": "Sicoob",
            "422": "Safra",
            "033": "Santander",
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
            "756": "Sicoob",
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
            "756": "Sicoob"
        }
        return bancos.get(codigo, f"Banco {codigo}")
    
    def _gerar_codigo_barras(self, digitavel: str) -> str:
        """Gera código de barras a partir do digitável"""
        # Remove dígitos verificadores e reorganiza
        # Formato: 03399161407000001918281556601014411370000038936
        return (digitavel[0:4] + digitavel[32:47] + digitavel[4:9] + 
                digitavel[10:20] + digitavel[21:31])


class BoletoParser:
    """Parser inteligente para boletos bancários PDF"""

    def __init__(self):
        self.texto_extraido = ""
        self.logger = get_logger("boleto_parser")
        self.decoder = BoletoDecoder()

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

    def _extrair_dados_extras(self) -> Dict[str, Any]:
        """Extrai dados extras e opcionais que não se encaixam nos campos padrão"""
        dados_extras = {}
        
        # Padrões para dados extras comuns
        padroes_extras = {
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
        
        # Buscar cada padrão no texto
        for nome_campo, padrao in padroes_extras.items():
            match = re.search(padrao, self.texto_extraido, re.IGNORECASE)
            if match:
                valor = match.group(1).strip()
                if valor:  # Só adiciona se não estiver vazio
                    dados_extras[nome_campo] = valor
        
        # Buscar linhas que podem conter informações extras
        linhas = self.texto_extraido.split('\n')
        for linha in linhas:
            linha = linha.strip()
            if linha and ':' in linha and len(linha) > 10:
                # Verificar se é uma linha com informação extra
                if not any(campo in linha.lower() for campo in [
                    'beneficiário', 'pagador', 'vencimento', 'valor', 'cnpj', 
                    'cpf', 'endereço', 'cep', 'aluno', 'matrícula', 'curso',
                    'banco', 'agência', 'carteira', 'espécie', 'aceite',
                    'local', 'multa', 'juros', 'instruções'
                ]):
                    # Pode ser uma informação extra
                    if ':' in linha:
                        chave, valor = linha.split(':', 1)
                        chave = chave.strip().lower().replace(' ', '_')
                        valor = valor.strip()
                        if valor and chave not in dados_extras:
                            dados_extras[f"info_{chave}"] = valor
        
        self.logger.info("Dados extras extraídos", quantidade=len(dados_extras))
        return dados_extras

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
            dados_extras=self._extrair_dados_extras(),
        )

        self.logger.info(
            "Parsing concluído com sucesso",
            beneficiario=dados.beneficiario.nome,
            valor=dados.valores.valor_documento,
            tipo=dados.tipo_boleto,
        )

        return dados
