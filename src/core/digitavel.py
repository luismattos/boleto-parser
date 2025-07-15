from dataclasses import dataclass
from typing import Optional
import regex
from datetime import datetime, timedelta

@dataclass
class CamposDigitavel:

    # 033991614.0 0700000191.2 8155600101.4 4 11370000038936

    """Estrutura para armazenar os campos da linha digitável conforme Febraban"""
    bloco_campo1: str  # AAABCCCCCD (10 dígitos)
    bloco_campo2: str   # DDDDEEEEFF (10 dígitos)
    bloco_campo3: str   # FFFFFGGGGG (10 dígitos)
    dv_geral: str       # H (1 dígito - DV geral)
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
        return self.bloco_campo1[:-1]
    @property
    def campo2_sem_dv(self) -> str:
        return self.bloco_campo2[:-1]
    @property
    def campo3_sem_dv(self) -> str:
        return self.bloco_campo3[:-1]
    @property
    def dv_campo1(self) -> str:
        return self.bloco_campo1[-1]
    @property
    def dv_campo2(self) -> str:
        return self.bloco_campo2[-1]
    @property
    def dv_campo3(self) -> str:
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
        except:
            return 0.0
    
    @property
    def data_vencimento(self) -> Optional[str]:
        """Converte fator de vencimento para data (base: 07/10/1997)"""
        try:
            fator = int(self.fator_vencimento)
            data_base = datetime(1997, 10, 7)
            data_vencimento = data_base + timedelta(days=fator)
            return data_vencimento.strftime("%d/%m/%Y")
        except:
            return None

@dataclass
class Digitavel:
    """
    Representa a linha digitável de um boleto bancário.
    Responsável por parsing, validação e extração de campos conforme Febraban.
    """
    valor: str
    _campos: Optional[CamposDigitavel] = None

    def __post_init__(self):
        """
        Normaliza a linha digitável removendo espaços e pontos
        """
        # Normalizar: remover espaços e pontos, mantendo apenas dígitos
        self.valor = regex.sub(r'[.\s]', '', self.valor or "")
        
        # Extrair campos se tiver tamanho adequado
        if len(self.valor) >= 47:
            self._extrair_campos()
    
    def _extrair_campos(self):
        """
        Extrai os campos da linha digitável normalizada (47 dígitos)
        Estrutura correta:
        Campo 1: 0-9 (9 dígitos) + DV 9 (1 dígito) = 10
        Campo 2: 10-20 (10 dígitos) + DV 20 (1 dígito) = 11
        Campo 3: 21-31 (10 dígitos) + DV 31 (1 dígito) = 11
        Campo 4: 32 (1 dígito)
        Campo 5: 33-46 (14 dígitos)
        """
        bloco_campo1 = self.valor[0:10]   # 9 dígitos + DV
        bloco_campo2 = self.valor[10:21]  # 10 dígitos + DV
        bloco_campo3 = self.valor[21:32]  # 10 dígitos + DV
        dv_geral = self.valor[32:33]      # 1 dígito
        fator_valor_e_valor = self.valor[33:47]  # 14 dígitos

        self._campos = CamposDigitavel(
            bloco_campo1=bloco_campo1,
            bloco_campo2=bloco_campo2,
            bloco_campo3=bloco_campo3,
            dv_geral=dv_geral,
            fator_valor_e_valor=fator_valor_e_valor
        )

    def _calcular_modulo_10(self, numero: str) -> int:
        """
        Calcula o dígito verificador usando Módulo 10
        
        Algoritmo:
        1. Multiplica cada dígito alternadamente por 2 e 1 (da direita para esquerda)
        2. Se o resultado > 9, subtrai-se 9 (ou soma-se os dígitos do resultado)
        3. Soma todos os resultados
        4. DV = 10 - (soma % 10)
        """
        numero_invertido = numero[::-1]
        soma = 0
        
        for i, digito in enumerate(numero_invertido):
            peso = 2 if i % 2 == 0 else 1
            resultado = int(digito) * peso
            
            # Se resultado > 9, subtrai-se 9
            if resultado > 9:
                resultado = resultado - 9
            
            soma += resultado
        
        # Calcula o DV
        dv = 10 - (soma % 10)
        if dv == 10:
            dv = 0
        
        return dv

    def _calcular_modulo_11(self, numero: str) -> int:
        """
        Calcula o dígito verificador usando Módulo 11
        
        Algoritmo:
        1. Multiplica cada dígito por pesos de 2 a 9 (cíclicos, da direita para esquerda)
        2. Soma todos os resultados
        3. DV = 11 - (soma % 11)
        4. Se resultado for 0, 10 ou 11, DV = 1
        """
        numero_invertido = numero[::-1]
        soma = 0
        
        for i, digito in enumerate(numero_invertido):
            peso = (i % 8) + 2  # Pesos de 2 a 9 (cíclicos)
            resultado = int(digito) * peso
            soma += resultado
        
        # Calcula o DV
        resto = soma % 11
        if resto == 0:
            dv = 1
        elif resto == 1:
            dv = 0
        else:
            dv = 11 - resto
        
        return dv

    def _validar_campo(self, campo: str) -> bool:
        """
        Valida o DV de um campo usando Módulo 10
        """
        if len(campo) < 2:
            return False
        
        campo_sem_dv = campo[:-1]
        dv_esperado = int(campo[-1])
        dv_calculado = self._calcular_modulo_10(campo_sem_dv)
        
        return dv_calculado == dv_esperado

    def _validar_dv_geral(self, codigo_barras: str) -> bool:
        """
        Valida o DV geral do código de barras usando Módulo 11
        """
        if len(codigo_barras) < 2:
            return False
        
        codigo_sem_dv = codigo_barras[:-1]
        dv_esperado = int(codigo_barras[-1])
        dv_calculado = self._calcular_modulo_11(codigo_sem_dv)
        
        return dv_calculado == dv_esperado

    def validar(self) -> bool:
        """
        Valida a linha digitável:
        - Deve conter apenas dígitos
        - Deve ter 47 dígitos
        - DVs dos campos devem ser válidos
        - DV geral deve ser válido
        """
        if not self.valor.isdigit():
            return False
        if len(self.valor) != 47:
            return False
        
        if not self._campos:
            return False
        
        # Validação dos campos (Módulo 10)
        if not self._validar_campo(self._campos.bloco_campo1):
            return False
        if not self._validar_campo(self._campos.bloco_campo2):
            return False
        if not self._validar_campo(self._campos.bloco_campo3):
            return False
        
        # Validação DV geral (Módulo 11)
        codigo_barras = self._gerar_codigo_barras()
        if not self._validar_dv_geral(codigo_barras):
            return False
        
        return True

    def _gerar_codigo_barras(self) -> str:
        """
        Gera o código de barras a partir da linha digitável
        """
        if not self._campos or len(self.valor) < 47:
            return ""
        
        # Composição do código de barras (44 dígitos + DV geral)
        banco_moeda = self.valor[0:4]
        campo_livre = self._campos.campo_livre
        fator_valor = self._campos.fator_valor_e_valor
        
        codigo_sem_dv = banco_moeda + campo_livre + fator_valor
        dv_geral = self._calcular_modulo_11(codigo_sem_dv)
        
        return codigo_sem_dv + str(dv_geral)

    def corrigir_dv(self) -> str:
        """
        Sugere uma linha digitável com DVs corrigidos
        """
        if not self._campos or len(self.valor) < 47:
            return self.valor
        
        # Corrigir campo 2
        campo2_sem_dv = self._campos.bloco_campo2[:-1]
        dv_campo2_calculado = self._calcular_modulo_10(campo2_sem_dv)
        campo2_corrigido = campo2_sem_dv + str(dv_campo2_calculado)
        
        # Corrigir campo 3
        campo3_sem_dv = self._campos.bloco_campo3[:-1]
        dv_campo3_calculado = self._calcular_modulo_10(campo3_sem_dv)
        campo3_corrigido = campo3_sem_dv + str(dv_campo3_calculado)
        
        # Corrigir DV geral
        banco_moeda = self.valor[0:4]
        campo_livre = self._campos.bloco_campo1[4:9] + campo2_corrigido[:-1] + campo3_corrigido[:-1]
        fator_valor = self._campos.fator_valor_e_valor
        
        codigo_sem_dv = banco_moeda + campo_livre + fator_valor
        dv_geral_calculado = self._calcular_modulo_11(codigo_sem_dv)
        campo4_corrigido = str(dv_geral_calculado)
        
        # Montar digitável corrigido
        digitavel_corrigido = (
            self._campos.bloco_campo1 +
            campo2_corrigido +
            campo3_corrigido +
            campo4_corrigido +
            self._campos.fator_valor_e_valor
        )
        
        return digitavel_corrigido

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
    
    @staticmethod
    def gerar_digitavel_valido(banco="033", valor=150.00, vencimento_dias=30):
        """
        Gera um código digitável válido seguindo as especificações Febraban
        Campo livre é preenchido com '1' (dummy), mas todos os DVs são válidos.
        """
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
        digitavel = Digitavel("")
        dv1 = digitavel._calcular_modulo_10(campo1_base)
        dv2 = digitavel._calcular_modulo_10(campo2_base)
        dv3 = digitavel._calcular_modulo_10(campo3_base)
        
        campo1 = campo1_base + str(dv1)  # 9 dígitos
        campo2 = campo2_base + str(dv2)  # 11 dígitos
        campo3 = campo3_base + str(dv3)  # 11 dígitos
        
        # Código de barras sem DV geral (44 dígitos)
        banco_moeda = banco + "9"
        codigo_sem_dv = banco_moeda + campo_livre + fator_str + valor_str
        dv_geral = digitavel._calcular_modulo_11(codigo_sem_dv)
        
        # Montar linha digitável (47 dígitos)
        digitavel_str = campo1 + campo2 + campo3 + str(dv_geral) + fator_str + valor_str
        return digitavel_str 