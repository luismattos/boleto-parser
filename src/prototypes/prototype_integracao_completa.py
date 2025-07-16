#!/usr/bin/env python3
"""
Protótipo: Integração Completa das Classes
Integrando BoletoDigitavel com BoletoBancario
"""

import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional


class TipoDocumento(Enum):
    """Tipos de documento conforme Febraban"""

    DUPLICATA_MERCANTIL = "DM"
    DUPLICATA_SERVICO = "DS"
    DUPLICATA_RURAL = "DR"
    LETRA_CAMBIO = "LC"
    NOTA_PROMISSORIA = "NP"
    RECIBO = "RC"
    APOLICE_SEGURO = "AP"
    MENSALIDADE_ESCOLAR = "ME"
    PARCELA_CONSORCIO = "PC"
    OUTROS = "OU"


class TipoAceite(Enum):
    """Tipos de aceite"""

    SIM = "S"
    NAO = "N"


@dataclass
class CampoDigitavel:
    """Representa um campo da linha digitável"""

    valor: str
    dv_esperado: str
    dv_calculado: int
    valido: bool
    sem_dv: str


@dataclass
class InformacoesBanco:
    """Informações do banco emissor"""

    codigo: str
    nome: str
    moeda: str = "9"  # Real brasileiro


@dataclass
class CampoLivre:
    """Campo livre do boleto"""

    completo: str
    parte1: str
    parte2: str
    parte3: str


@dataclass
class ValoresBoleto:
    """Valores e datas do boleto"""

    valor_documento: float
    data_vencimento: datetime
    data_emissao: datetime
    fator_vencimento: Optional[str] = None
    valor_centavos: Optional[str] = None

    def __post_init__(self):
        """Calcula fator de vencimento e valor em centavos"""
        if not self.fator_vencimento:
            self.fator_vencimento = self._calcular_fator_vencimento()
        if not self.valor_centavos:
            self.valor_centavos = self._calcular_valor_centavos()

    def _calcular_fator_vencimento(self) -> str:
        """Calcula fator de vencimento (dias desde 07/10/1997)"""
        data_base = datetime(1997, 10, 7)
        dias = (self.data_vencimento - data_base).days
        return str(dias).zfill(4)

    def _calcular_valor_centavos(self) -> str:
        """Converte valor para centavos em string"""
        centavos = int(self.valor_documento * 100)
        return str(centavos).zfill(10)


@dataclass
class ValidacoesDV:
    """Validações dos dígitos verificadores"""

    campo1: bool
    campo2: bool
    campo3: bool
    dv_geral: bool
    todos_validos: bool


class BoletoDigitavel:
    """
    Classe para decodificação e validação do código digitável
    """

    def __init__(self, digitavel: str):
        self.digitavel_original = digitavel
        self.digitavel_limpo = re.sub(r"[.\s]", "", digitavel)
        self.campos: Dict[str, CampoDigitavel] = {}
        self.informacoes_banco: Optional[InformacoesBanco] = None
        self.campo_livre: Optional[CampoLivre] = None
        self.valores: Optional[ValoresBoleto] = None
        self.validacoes: Optional[ValidacoesDV] = None
        self.codigo_barras: Optional[str] = None
        self.digitavel_corrigido: Optional[str] = None

        if len(self.digitavel_limpo) == 47:
            self._decodificar()

    def _calcular_modulo_10(self, numero: str) -> int:
        """Calcula DV Módulo 10"""
        numero_invertido = numero[::-1]
        soma = 0

        for i, digito in enumerate(numero_invertido):
            peso = 2 if i % 2 == 0 else 1
            resultado = int(digito) * peso

            if resultado > 9:
                resultado = sum(int(d) for d in str(resultado))

            soma += resultado

        dv = 10 - (soma % 10)
        if dv == 10:
            dv = 0

        return dv

    def _calcular_modulo_11(self, numero: str) -> int:
        """Calcula DV Módulo 11"""
        numero_invertido = numero[::-1]
        soma = 0

        for i, digito in enumerate(numero_invertido):
            peso = (i % 8) + 2
            resultado = int(digito) * peso
            soma += resultado

        resto = soma % 11
        if resto == 0:
            dv = 1
        elif resto == 1:
            dv = 0
        else:
            dv = 11 - resto

        return dv

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
        return bancos.get(codigo, f"Banco {codigo}")

    def _fator_para_data(self, fator: int) -> str:
        """Converte fator de vencimento para data"""
        data_base = datetime(1997, 10, 7)
        data_vencimento = data_base + timedelta(days=fator)
        return data_vencimento.strftime("%d/%m/%Y")

    def _validar_campo(self, campo: str) -> CampoDigitavel:
        """Valida um campo e retorna informações detalhadas"""
        campo_sem_dv = campo[:-1]
        dv_esperado = campo[-1]
        dv_calculado = self._calcular_modulo_10(campo_sem_dv)
        valido = dv_calculado == int(dv_esperado)

        return CampoDigitavel(
            valor=campo,
            dv_esperado=dv_esperado,
            dv_calculado=dv_calculado,
            valido=valido,
            sem_dv=campo_sem_dv,
        )

    def _decodificar(self):
        """Decodifica o digitável e popula as propriedades"""
        # Campos da linha digitável
        campo1 = self.digitavel_limpo[0:10]
        campo2 = self.digitavel_limpo[10:20]
        campo3 = self.digitavel_limpo[20:30]
        campo4 = self.digitavel_limpo[30:31]
        campo5 = self.digitavel_limpo[31:47]

        # Validar campos
        self.campos = {
            "campo1": self._validar_campo(campo1),
            "campo2": self._validar_campo(campo2),
            "campo3": self._validar_campo(campo3),
        }

        # Informações do banco
        banco_codigo = campo1[0:3]
        moeda = campo1[3:4]
        self.informacoes_banco = InformacoesBanco(
            codigo=banco_codigo, nome=self._identificar_banco(banco_codigo), moeda=moeda
        )

        # Campo livre
        campo_livre_1 = campo1[4:9]
        campo_livre_2 = campo2[0:9]
        campo_livre_3 = campo3[0:9]
        campo_livre_completo = campo_livre_1 + campo_livre_2 + campo_livre_3

        self.campo_livre = CampoLivre(
            completo=campo_livre_completo,
            parte1=campo_livre_1,
            parte2=campo_livre_2,
            parte3=campo_livre_3,
        )

        # Valores e datas
        fator_vencimento = campo5[0:4]
        valor_centavos = campo5[4:14]

        try:
            fator_int = int(fator_vencimento)
            valor_int = int(valor_centavos)
            valor_decimal = valor_int / 100
            data_vencimento = datetime.strptime(
                self._fator_para_data(fator_int), "%d/%m/%Y"
            )
            data_emissao = datetime.now()  # Aproximação

            self.valores = ValoresBoleto(
                valor_documento=valor_decimal,
                data_vencimento=data_vencimento,
                data_emissao=data_emissao,
                fator_vencimento=fator_vencimento,
                valor_centavos=valor_centavos,
            )
        except Exception:
            print("Erro ao processar integração completa")

        # Validação DV geral
        codigo_sem_dv = self._gerar_codigo_barras_sem_dv()
        dv_geral_calculado = self._calcular_modulo_11(codigo_sem_dv)
        dv_geral_esperado = int(campo4)
        dv_geral_valido = dv_geral_calculado == dv_geral_esperado

        # Validações finais
        self.validacoes = ValidacoesDV(
            campo1=self.campos["campo1"].valido,
            campo2=self.campos["campo2"].valido,
            campo3=self.campos["campo3"].valido,
            dv_geral=dv_geral_valido,
            todos_validos=(
                self.campos["campo1"].valido
                and self.campos["campo2"].valido
                and self.campos["campo3"].valido
                and dv_geral_valido
            ),
        )

        # Código de barras
        self.codigo_barras = codigo_sem_dv + str(dv_geral_calculado)

    def _gerar_codigo_barras_sem_dv(self) -> str:
        """Gera código de barras sem DV"""
        banco_moeda = self.digitavel_limpo[0:4]
        campo_livre = (
            self.digitavel_limpo[4:9]
            + self.digitavel_limpo[10:19]
            + self.digitavel_limpo[20:29]
        )
        fator_valor = self.digitavel_limpo[31:47]

        return banco_moeda + campo_livre + fator_valor

    def corrigir_dvs(self) -> bool:
        """Corrige os DVs incorretos e retorna se foi necessário corrigir"""
        if self.validacoes.todos_validos:
            return False  # Já está correto

        # Corrigir campos
        campo1_corrigido = self.campos["campo1"].valor  # Já está correto
        campo2_corrigido = self.campos["campo2"].sem_dv + str(
            self.campos["campo2"].dv_calculado
        )
        campo3_corrigido = self.campos["campo3"].sem_dv + str(
            self.campos["campo3"].dv_calculado
        )

        # Corrigir DV geral
        codigo_sem_dv = self._gerar_codigo_barras_sem_dv()
        dv_geral_calculado = self._calcular_modulo_11(codigo_sem_dv)
        campo4_corrigido = str(dv_geral_calculado)

        # Montar digitável corrigido
        self.digitavel_corrigido = (
            campo1_corrigido
            + campo2_corrigido
            + campo3_corrigido
            + campo4_corrigido
            + self.digitavel_limpo[31:47]
        )

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "digitavel_original": self.digitavel_original,
            "digitavel_limpo": self.digitavel_limpo,
            "digitavel_corrigido": self.digitavel_corrigido,
            "campos": {
                nome: {
                    "valor": campo.valor,
                    "dv_esperado": campo.dv_esperado,
                    "dv_calculado": campo.dv_calculado,
                    "valido": campo.valido,
                    "sem_dv": campo.sem_dv,
                }
                for nome, campo in self.campos.items()
            },
            "informacoes_banco": {
                "codigo": self.informacoes_banco.codigo,
                "nome": self.informacoes_banco.nome,
                "moeda": self.informacoes_banco.moeda,
            }
            if self.informacoes_banco
            else None,
            "campo_livre": {
                "completo": self.campo_livre.completo,
                "parte1": self.campo_livre.parte1,
                "parte2": self.campo_livre.parte2,
                "parte3": self.campo_livre.parte3,
            }
            if self.campo_livre
            else None,
            "valores": {
                "fator_vencimento": self.valores.fator_vencimento,
                "valor_centavos": self.valores.valor_centavos,
                "valor_decimal": self.valores.valor_documento,
                "data_vencimento": self.valores.data_vencimento.strftime("%d/%m/%Y"),
            }
            if self.valores
            else None,
            "validacoes": {
                "campo1": self.validacoes.campo1,
                "campo2": self.validacoes.campo2,
                "campo3": self.validacoes.campo3,
                "dv_geral": self.validacoes.dv_geral,
                "todos_validos": self.validacoes.todos_validos,
            }
            if self.validacoes
            else None,
            "codigo_barras": self.codigo_barras,
        }

    def __str__(self) -> str:
        """Representação string"""
        if not self.validacoes:
            return f"BoletoDigitavel(inválido: {self.digitavel_original})"

        return (
            f"BoletoDigitavel("
            f"banco={self.informacoes_banco.nome}, "
            f"valor=R${self.valores.valor_documento:.2f}, "
            f"valido={self.validacoes.todos_validos}"
            f")"
        )


@dataclass
class Cedente:
    """Informações do cedente (quem emite o boleto)"""

    nome: str
    cnpj_cpf: str
    agencia: Optional[str] = None
    conta: Optional[str] = None
    codigo_beneficiario: Optional[str] = None
    endereco: Optional[str] = None


@dataclass
class Pagador:
    """Informações do pagador"""

    nome: str
    cnpj_cpf: str
    endereco: Optional[str] = None


@dataclass
class CamposObrigatorios:
    """Campos obrigatórios do boleto conforme Febraban"""

    # Informações do banco
    banco: InformacoesBanco

    # Informações do cedente
    cedente: Cedente

    # Informações do pagador
    pagador: Pagador

    # Valores e datas
    valores: ValoresBoleto

    # Identificação do título
    nosso_numero: str
    carteira: str

    # Documento
    especie_documento: TipoDocumento = TipoDocumento.DUPLICATA_MERCANTIL
    aceite: TipoAceite = TipoAceite.NAO

    # Linha digitável e código de barras
    linha_digitavel: Optional[str] = None
    codigo_barras: Optional[str] = None


@dataclass
class CamposOpcionais:
    """Campos opcionais do boleto"""

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


@dataclass
class Validacoes:
    """Validações do boleto"""

    digitavel_valido: bool = False
    codigo_barras_valido: bool = False
    todos_campos_obrigatorios: bool = False
    estrutura_correta: bool = False


class BoletoBancario:
    """
    Classe principal para representar um boleto bancário completo
    conforme especificações da Febraban
    """

    def __init__(
        self,
        campos_obrigatorios: CamposObrigatorios,
        campos_opcionais: Optional[CamposOpcionais] = None,
        digitavel: Optional[str] = None,
    ):
        self.obrigatorios = campos_obrigatorios
        self.opcionais = campos_opcionais or CamposOpcionais()
        self.validacoes = Validacoes()
        self.digitavel_decodificado: Optional[BoletoDigitavel] = None

        # Se forneceu digitável, decodificar
        if digitavel:
            self.digitavel_decodificado = BoletoDigitavel(digitavel)
            self._integrar_digitavel()

        self._validar_campos_obrigatorios()

    def _integrar_digitavel(self):
        """Integra informações do digitável com o boleto"""
        if (
            not self.digitavel_decodificado
            or not self.digitavel_decodificado.validacoes
        ):
            return

        # Atualizar informações do banco
        if self.digitavel_decodificado.informacoes_banco:
            self.obrigatorios.banco = self.digitavel_decodificado.informacoes_banco

        # Atualizar valores
        if self.digitavel_decodificado.valores:
            self.obrigatorios.valores = self.digitavel_decodificado.valores

        # Atualizar linha digitável e código de barras
        self.obrigatorios.linha_digitavel = (
            self.digitavel_decodificado.digitavel_original
        )
        self.obrigatorios.codigo_barras = self.digitavel_decodificado.codigo_barras

        # Atualizar validações
        self.validacoes.digitavel_valido = (
            self.digitavel_decodificado.validacoes.todos_validos
        )
        self.validacoes.codigo_barras_valido = (
            self.digitavel_decodificado.validacoes.todos_validos
        )

    def _validar_campos_obrigatorios(self):
        """Valida se todos os campos obrigatórios estão preenchidos"""
        campos_ok = (
            self.obrigatorios.banco.codigo
            and self.obrigatorios.cedente.nome
            and self.obrigatorios.cedente.cnpj_cpf
            and self.obrigatorios.pagador.nome
            and self.obrigatorios.pagador.cnpj_cpf
            and self.obrigatorios.nosso_numero
            and self.obrigatorios.carteira
            and self.obrigatorios.valores.valor_documento > 0
        )

        self.validacoes.todos_campos_obrigatorios = campos_ok
        self.validacoes.estrutura_correta = campos_ok

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        resultado = {
            "campos_obrigatorios": {
                "banco": {
                    "codigo": self.obrigatorios.banco.codigo,
                    "nome": self.obrigatorios.banco.nome,
                    "moeda": self.obrigatorios.banco.moeda,
                },
                "cedente": {
                    "nome": self.obrigatorios.cedente.nome,
                    "cnpj_cpf": self.obrigatorios.cedente.cnpj_cpf,
                    "agencia": self.obrigatorios.cedente.agencia,
                    "conta": self.obrigatorios.cedente.conta,
                    "codigo_beneficiario": self.obrigatorios.cedente.codigo_beneficiario,
                    "endereco": self.obrigatorios.cedente.endereco,
                },
                "pagador": {
                    "nome": self.obrigatorios.pagador.nome,
                    "cnpj_cpf": self.obrigatorios.pagador.cnpj_cpf,
                    "endereco": self.obrigatorios.pagador.endereco,
                },
                "valores": {
                    "valor_documento": self.obrigatorios.valores.valor_documento,
                    "data_vencimento": self.obrigatorios.valores.data_vencimento.isoformat(),
                    "data_emissao": self.obrigatorios.valores.data_emissao.isoformat(),
                    "fator_vencimento": self.obrigatorios.valores.fator_vencimento,
                    "valor_centavos": self.obrigatorios.valores.valor_centavos,
                },
                "nosso_numero": self.obrigatorios.nosso_numero,
                "carteira": self.obrigatorios.carteira,
                "especie_documento": self.obrigatorios.especie_documento.value,
                "aceite": self.obrigatorios.aceite.value,
                "linha_digitavel": self.obrigatorios.linha_digitavel,
                "codigo_barras": self.obrigatorios.codigo_barras,
            },
            "campos_opcionais": {
                "instrucoes": self.opcionais.instrucoes,
                "desconto_valor": self.opcionais.desconto_valor,
                "desconto_data": self.opcionais.desconto_data.isoformat()
                if self.opcionais.desconto_data
                else None,
                "desconto_percentual": self.opcionais.desconto_percentual,
                "juros_percentual": self.opcionais.juros_percentual,
                "multa_percentual": self.opcionais.multa_percentual,
                "multa_valor": self.opcionais.multa_valor,
                "numero_documento": self.opcionais.numero_documento,
                "sacador_avalista": self.opcionais.sacador_avalista,
                "informacoes_adicionais": self.opcionais.informacoes_adicionais,
                "protesto_dias": self.opcionais.protesto_dias,
                "protesto_instrucao": self.opcionais.protesto_instrucao,
                "uso_banco": self.opcionais.uso_banco,
                "local_pagamento": self.opcionais.local_pagamento,
            },
            "validacoes": {
                "digitavel_valido": self.validacoes.digitavel_valido,
                "codigo_barras_valido": self.validacoes.codigo_barras_valido,
                "todos_campos_obrigatorios": self.validacoes.todos_campos_obrigatorios,
                "estrutura_correta": self.validacoes.estrutura_correta,
            },
        }

        # Adicionar informações do digitável se disponível
        if self.digitavel_decodificado:
            resultado["digitavel_decodificado"] = self.digitavel_decodificado.to_dict()

        return resultado

    def __str__(self) -> str:
        """Representação string do boleto"""
        return (
            f"BoletoBancario("
            f"banco={self.obrigatorios.banco.nome}, "
            f"cedente={self.obrigatorios.cedente.nome}, "
            f"valor=R${self.obrigatorios.valores.valor_documento:.2f}, "
            f"vencimento={self.obrigatorios.valores.data_vencimento.strftime('%d/%m/%Y')}, "
            f"valido={self.validacoes.estrutura_correta}"
            f")"
        )


def testar_integracao():
    """Testa a integração das classes"""
    print("🧪 TESTANDO INTEGRAÇÃO DAS CLASSES")
    print("=" * 70)

    # Digitável real
    digitavel_real = "033991614.0 0700000191.2 8155600101.4 4 11370000038936"

    # Criar boleto com digitável
    boleto = BoletoBancario(
        campos_obrigatorios=CamposObrigatorios(
            banco=InformacoesBanco("033", "Santander"),
            cedente=Cedente("EMPRESA EXEMPLO", "12.345.678/0001-90"),
            pagador=Pagador("CLIENTE EXEMPLO", "123.456.789-00"),
            valores=ValoresBoleto(389.36, datetime(2025, 7, 9), datetime(2025, 6, 9)),
            nosso_numero="123456789",
            carteira="101",
        ),
        digitavel=digitavel_real,
    )

    print("📊 INFORMAÇÕES DO BOLETO:")
    print(f"   {boleto}")

    print("\n🔍 INFORMAÇÕES DO DIGITÁVEL:")
    if boleto.digitavel_decodificado:
        digitavel = boleto.digitavel_decodificado
        print(f"   Digitável Original: {digitavel.digitavel_original}")
        print(f"   Banco: {digitavel.informacoes_banco.nome}")
        print(f"   Valor: R$ {digitavel.valores.valor_documento:.2f}")
        print(f"   Válido: {digitavel.validacoes.todos_validos}")

        if digitavel.digitavel_corrigido:
            print(f"   Digitável Corrigido: {digitavel.digitavel_corrigido}")

    print("\n✅ VALIDAÇÕES:")
    validacoes = boleto.validacoes
    print(f"   Estrutura Correta: {validacoes.estrutura_correta}")
    print(f"   Todos Campos Obrigatórios: {validacoes.todos_campos_obrigatorios}")
    print(f"   Digitável Válido: {validacoes.digitavel_valido}")
    print(f"   Código de Barras Válido: {validacoes.codigo_barras_valido}")

    # Converter para dicionário
    print("\n📋 REPRESENTAÇÃO EM DICIONÁRIO:")
    resultado_dict = boleto.to_dict()
    for chave, valor in resultado_dict.items():
        if chave != "campos_obrigatorios" and chave != "campos_opcionais":
            print(f"   {chave}: {valor}")

    return boleto


if __name__ == "__main__":
    testar_integracao()
