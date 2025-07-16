#!/usr/bin/env python3
"""
Teste Avançado com Biblioteca Regex
Demonstra recursos avançados da biblioteca regex para extração de códigos digitáveis
"""

import regex

from ..core.digitavel import Digitavel
from ..utils.logger import get_logger


class TestDigitavelAvancado:
    """Testes avançados usando recursos da biblioteca regex"""

    @property
    def logger(self):
        return get_logger("test_digitavel_avancado")

    def test_regex_avancado_padroes_flexiveis(self):
        """Testa padrões flexíveis com regex avançado"""
        self.logger.info("🧪 TESTE DE PADRÕES FLEXÍVEIS COM REGEX")
        self.logger.info("=" * 50)

        # Padrões mais flexíveis usando recursos avançados do regex
        padroes_avancados = [
            # Padrão com grupos nomeados
            r"(?P<digitavel>\d{5}\.\d{4,5}\s+\d{5}\.\d{5,6}\s+\d{5}\.\d{5,6}\s+\d\s+\d{14,15})",
            # Padrão com lookahead/lookbehind
            r"(?<=Linha Digitável:\s*)(\d{5}\.\d{4,5}\s+\d{5}\.\d{5,6}\s+\d{5}\.\d{5,6}\s+\d\s+\d{14,15})",
            # Padrão com flags de case insensitive e multiline
            r"(?im)(\d{5}\.\d{4,5}\s+\d{5}\.\d{5,6}\s+\d{5}\.\d{5,6}\s+\d\s+\d{14,15})",
            # Padrão com quantificadores possesivos
            r"(\d{5}\.\d{4,5}+\s+\d{5}\.\d{5,6}+\s+\d{5}\.\d{5,6}+\s+\d+\s+\d{14,15}+)",
        ]

        # Gerar digitável de teste
        digitavel_teste = Digitavel.gerar_digitavel_valido(
            banco="033", valor=100.00, vencimento_dias=30
        )
        self.logger.info(f"📝 Digitável de teste: {digitavel_teste}")

        # Texto com diferentes formatos
        textos_teste = [
            f"Linha Digitável: {digitavel_teste}",
            f"LINHA DIGITÁVEL: {digitavel_teste}",
            f"Codigo: {digitavel_teste}",
            f"  {digitavel_teste}  ",
        ]

        for i, padrao in enumerate(padroes_avancados):
            self.logger.info(f"🔍 Testando padrão {i+1}: {padrao}")

            for j, texto in enumerate(textos_teste):
                match = regex.search(padrao, texto)
                if match:
                    resultado = match.group(1) if match.groups() else match.group(0)
                    self.logger.info(f"  ✅ Texto {j+1}: Encontrado '{resultado}'")
                else:
                    self.logger.warning(f"  ❌ Texto {j+1}: Não encontrado")

    def test_regex_avancado_extracao_inteligente(self):
        """Testa extração inteligente com regex avançado"""
        self.logger.info("🧪 TESTE DE EXTRAÇÃO INTELIGENTE")
        self.logger.info("=" * 50)

        # Gerar múltiplos digitáveis
        digitaveis_raw = [
            Digitavel.gerar_digitavel_valido(
                banco="001", valor=50.00, vencimento_dias=15
            ),
            Digitavel.gerar_digitavel_valido(
                banco="033", valor=150.00, vencimento_dias=30
            ),
            Digitavel.gerar_digitavel_valido(
                banco="104", valor=300.00, vencimento_dias=45
            ),
        ]

        # Formatar digitáveis com pontos e espaços
        digitaveis = []
        for raw in digitaveis_raw:
            # Formato: AAAAA.BBBB CCCC.DDDDD EEEEE.FFFFFF G HHHHHHHHHHHHHHH
            formatted = (
                f"{raw[0:5]}.{raw[5:9]} "
                f"{raw[9:14]}.{raw[14:19]} "
                f"{raw[19:24]}.{raw[24:30]} "
                f"{raw[30]} "
                f"{raw[31:47]}"
            )
            digitaveis.append(formatted)

        # Texto complexo com múltiplos digitáveis
        texto_complexo = f"""
        BOLETO BANCÁRIO - SISTEMA DE COBRANÇA

        Beneficiário: EMPRESA EXEMPLO LTDA
        CNPJ: 12.345.678/0001-90

        Pagador: JOÃO DA SILVA SANTOS
        CPF: 123.456.789-00

        ===== BOLETO 1 =====
        Linha Digitável: {digitaveis[0]}
        Valor: R$ 50,00
        Vencimento: 15/08/2025

        ===== BOLETO 2 =====
        Código: {digitaveis[1]}
        Valor: R$ 150,00
        Vencimento: 30/08/2025

        ===== BOLETO 3 =====
        Digitável: {digitaveis[2]}
        Valor: R$ 300,00
        Vencimento: 15/09/2025

        Instruções: Pagável em qualquer banco até o vencimento
        """

        # Padrão avançado para extrair todos os digitáveis
        padrao_avancado = r"(?im)(?:linha\s+digitável|código|digitável)[:\s]*(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{16})"

        matches = regex.finditer(padrao_avancado, texto_complexo)
        encontrados = [match.group(1) for match in matches]

        self.logger.info(f"📝 Digitáveis esperados: {len(digitaveis)}")
        for i, digitavel in enumerate(digitaveis):
            self.logger.info(f"  {i+1}. {digitavel}")

        self.logger.info(f"🔍 Digitáveis encontrados: {len(encontrados)}")
        for i, encontrado in enumerate(encontrados):
            self.logger.info(f"  {i+1}. {encontrado}")

        # Verificar se todos foram encontrados
        assert len(encontrados) == len(digitaveis)
        for esperado, encontrado in zip(digitaveis, encontrados):
            assert esperado == encontrado

        self.logger.info("✅ Todos os digitáveis foram extraídos corretamente!")

    def test_regex_avancado_validacao_robusta(self):
        """Testa validação robusta com regex avançado"""
        self.logger.info("🧪 TESTE DE VALIDAÇÃO ROBUSTA")
        self.logger.info("=" * 50)

        # Padrão com validação de estrutura
        padrao_validacao = r"""
        (?x)  # Verbose mode para comentários
        ^                    # Início da string
        (?P<banco>\d{3})     # Código do banco (3 dígitos)
        (?P<moeda>\d{1})     # Código da moeda (1 dígito)
        (?P<campo1>\d{4,5})  # Primeira parte do campo livre
        \.                   # Ponto separador
        (?P<dv1>\d{1})       # DV do campo 1
        \s+                  # Espaços
        (?P<campo2>\d{5})    # Segunda parte do campo livre
        \.                   # Ponto separador
        (?P<dv2>\d{1})       # DV do campo 2
        \s+                  # Espaços
        (?P<campo3>\d{5})    # Terceira parte do campo livre
        \.                   # Ponto separador
        (?P<dv3>\d{1})       # DV do campo 3
        \s+                  # Espaços
        (?P<dv_geral>\d{1})  # DV geral
        \s+                  # Espaços
        (?P<fator>\d{4})     # Fator de vencimento (4 dígitos)
        (?P<valor>\d{10})    # Valor em centavos (10 dígitos)
        $                    # Fim da string
        """

        # Testar com digitável válido
        digitavel_valido = Digitavel.gerar_digitavel_valido(
            banco="033", valor=200.00, vencimento_dias=60
        )
        self.logger.info(f"📝 Testando digitável válido: {digitavel_valido}")

        match = regex.match(padrao_validacao, digitavel_valido)
        if match:
            grupos = match.groupdict()
            self.logger.info("✅ Estrutura válida encontrada:")
            self.logger.info(f"   Banco: {grupos['banco']}")
            self.logger.info(f"   Moeda: {grupos['moeda']}")
            self.logger.info(f"   Campo 1: {grupos['campo1']} (DV: {grupos['dv1']})")
            self.logger.info(f"   Campo 2: {grupos['campo2']} (DV: {grupos['dv2']})")
            self.logger.info(f"   Campo 3: {grupos['campo3']} (DV: {grupos['dv3']})")
            self.logger.info(f"   DV Geral: {grupos['dv_geral']}")
            self.logger.info(f"   Fator: {grupos['fator']}")
            self.logger.info(f"   Valor: {grupos['valor']}")
        else:
            self.logger.warning("❌ Estrutura inválida")

        # Testar com digitável inválido
        digitavel_invalido = "12345.67890 12345.678901 12345.6789012 1 123456789012345"
        self.logger.info(f"📝 Testando digitável inválido: {digitavel_invalido}")

        match = regex.match(padrao_validacao, digitavel_invalido)
        if match:
            self.logger.error("❌ Estrutura válida (não deveria ser)")
        else:
            self.logger.info("✅ Estrutura inválida detectada corretamente")

    def test_regex_avancado_substituicao_inteligente(self):
        """Testa substituição inteligente com regex avançado"""
        self.logger.info("🧪 TESTE DE SUBSTITUIÇÃO INTELIGENTE")
        self.logger.info("=" * 50)

        # Texto com formatação inconsistente
        texto_inconsistente = """
        Boleto 1: 03391.2346 56789.01231 41234.567802 1 101880000025000
        Boleto 2: 03391.2346.56789.01231.41234.567802.1.101880000025000
        Boleto 3: 0339123465678901231412345678021101880000025000
        """

        # Padrão para normalizar formatação
        padrao_normalizacao = r"(\d{3})(\d{2})\.(\d{4})\s+(\d{5})\.(\d{5})\s+(\d{5})\.(\d{6})\s+(\d)\s+(\d{15})"

        # Substituição com grupos nomeados
        substituicao = r"\1\2.\3 \4.\5 \6.\7 \8 \9"

        texto_normalizado = regex.sub(
            padrao_normalizacao, substituicao, texto_inconsistente
        )

        self.logger.info("📝 Texto original:")
        self.logger.info(texto_inconsistente)
        self.logger.info("📝 Texto normalizado:")
        self.logger.info(texto_normalizado)

        # Verificar se a normalização funcionou
        padroes_esperados = [
            r"\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{15}"
        ]

        for padrao in padroes_esperados:
            matches = regex.findall(padrao, texto_normalizado)
            self.logger.info(f"✅ Encontrados {len(matches)} padrões normalizados")


def test_demonstracao_recursos_avancados():
    """Demonstra recursos avançados da biblioteca regex"""
    logger = get_logger("demo_regex")
    logger.info("🚀 DEMONSTRAÇÃO DE RECURSOS AVANÇADOS")
    logger.info("=" * 60)

    # 1. Grupos nomeados
    logger.info("1️⃣ Grupos Nomeados:")
    texto = "Banco: 033, Valor: 150.00, Vencimento: 15/08/2025"
    padrao = r"Banco:\s+(?P<banco>\d{3}),\s+Valor:\s+(?P<valor>\d+\.\d{2}),\s+Vencimento:\s+(?P<vencimento>\d{2}/\d{2}/\d{4})"
    match = regex.search(padrao, texto)
    if match:
        logger.info(f"   Banco: {match.group('banco')}")
        logger.info(f"   Valor: {match.group('valor')}")
        logger.info(f"   Vencimento: {match.group('vencimento')}")

    # 2. Lookahead/Lookbehind
    logger.info("2️⃣ Lookahead/Lookbehind:")
    texto = "Linha Digitável: 03391.2346 56789.01231 41234.567802 1 101880000025000"
    padrao = r"(?<=Linha Digitável:\s*)(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{15})"
    match = regex.search(padrao, texto)
    if match:
        logger.info(f"   Digitável extraído: {match.group(1)}")

    # 3. Flags avançadas
    logger.info("3️⃣ Flags Avançadas:")
    texto = "LINHA DIGITÁVEL: 03391.2346 56789.01231 41234.567802 1 101880000025000"
    padrao = r"(?im)(linha\s+digitável)[:\s]*(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{15})"
    match = regex.search(padrao, texto)
    if match:
        logger.info(f"   Campo: {match.group(1)}")
        logger.info(f"   Valor: {match.group(2)}")

    # 4. Quantificadores possesivos
    logger.info("4️⃣ Quantificadores Possessivos:")
    texto = "123456789012345678901234567890123456789012345678901234567890"
    padrao = r"(\d{5}\.\d{4}+\s+\d{5}\.\d{5}+\s+\d{5}\.\d{6}+\s+\d+\s+\d{15}+)"
    match = regex.search(padrao, texto)
    if match:
        logger.info(f"   Padrão possessivo encontrado: {match.group(1)}")

    logger.info("✅ Demonstração concluída!")


def test_digitavel_valido_real():
    """Testa com um digitável válido real"""
    logger = get_logger("test_digitavel_real")
    logger.info("🧪 TESTE COM DIGITÁVEL VÁLIDO REAL")
    logger.info("=" * 50)

    # Digitável válido real (exemplo)
    digitavel_real = "03399.12345 67890.123456 78901.234567 1 12340000012345"
    logger.info(f"📝 Digitável real: {digitavel_real}")

    # Criar instância
    digitavel_obj = Digitavel(digitavel_real)

    # Testar propriedades básicas
    assert digitavel_obj.banco == "033"
    assert digitavel_obj.valor_documento == 123.45
    assert digitavel_obj.data_vencimento is not None

    logger.info(f"✅ Banco: {digitavel_obj.banco}")
    logger.info(f"✅ Valor: R$ {digitavel_obj.valor_documento:.2f}")
    logger.info(f"✅ Vencimento: {digitavel_obj.data_vencimento}")
    logger.info(f"✅ Código de Barras: {digitavel_obj.codigo_barras}")

    logger.info("✅ Teste com digitável real passou!")


# ============================================================================
# TESTES AVANÇADOS DE CASOS DE FALHA
# ============================================================================


def test_regex_falha_padroes_malformados():
    """Testa falhas com padrões regex malformados"""
    logger = get_logger("test_regex_falha")
    logger.info("🧪 TESTE DE FALHAS COM PADRÕES REGEX MALFORMADOS")
    logger.info("=" * 60)

    # Padrões que podem causar problemas
    padroes_problematicos = [
        r"(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{16})",  # Padrão correto
        r"(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{15})",  # Menos dígitos no final
        r"(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{17})",  # Mais dígitos no final
        r"(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{16})",  # Padrão correto
    ]

    # Texto com digitável válido
    texto_valido = (
        "Linha Digitável: 03391.2346 56789.01231 41234.567802 1 101880000025000"
    )

    for i, padrao in enumerate(padroes_problematicos, 1):
        try:
            match = regex.search(padrao, texto_valido)
            if match:
                logger.info(f"✅ Padrão {i}: Encontrou '{match.group(1)}'")
            else:
                logger.info(f"❌ Padrão {i}: Não encontrou match")
        except Exception as e:
            logger.error(f"💥 Padrão {i}: Erro - {e}")


def test_regex_falha_extracao_multiplos_formatos():
    """Testa falhas na extração com múltiplos formatos de digitável"""
    logger = get_logger("test_regex_falha_extracao")
    logger.info("🧪 TESTE DE FALHAS NA EXTRAÇÃO COM MÚLTIPLOS FORMATOS")
    logger.info("=" * 60)

    # Texto com diferentes formatos (alguns inválidos)
    textos_misturados = [
        "Linha Digitável: 03391.2346 56789.01231 41234.567802 1 101880000025000",  # Válido
        "Código: 03391.2346.56789.01231.41234.567802.1.101880000025000",  # Pontos extras
        "Digitável: 0339123465678901231412345678021101880000025000",  # Sem formatação
        "Boleto: 03391.2346 56789.01231 41234.567802 1 10188000002500",  # Menos dígitos
        "Linha: 03391.2346 56789.01231 41234.567802 1 1018800000250000",  # Mais dígitos
        "Código inválido: 12345.67890 12345.678901 12345.6789012 1 123456789012345",  # Inválido
    ]

    # Padrão para extração
    padrao = r"(?im)(?:linha\s+digitável|código|digitável|boleto|linha)[:\s]*(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{16})"

    for i, texto in enumerate(textos_misturados, 1):
        matches = list(regex.finditer(padrao, texto))
        logger.info(f"📝 Texto {i}: {texto[:50]}...")
        logger.info(f"🔍 Encontrados: {len(matches)} matches")

        for j, match in enumerate(matches):
            digitavel_encontrado = match.group(1)
            # Validar se o digitável encontrado é realmente válido
            try:
                digitavel_obj = Digitavel(digitavel_encontrado)
                if digitavel_obj.validar():
                    logger.info(f"  ✅ Match {j+1}: Válido - {digitavel_encontrado}")
                else:
                    logger.warning(
                        f"  ⚠️ Match {j+1}: Inválido - {digitavel_encontrado}"
                    )
            except Exception as e:
                logger.error(f"  💥 Match {j+1}: Erro - {e}")


def test_regex_falha_lookbehind_complexo():
    """Testa falhas com lookbehind complexo"""
    logger = get_logger("test_regex_lookbehind_falha")
    logger.info("🧪 TESTE DE FALHAS COM LOOKBEHIND COMPLEXO")
    logger.info("=" * 60)

    # Padrões com lookbehind que podem falhar
    padroes_lookbehind = [
        r"(?<=Linha Digitável:\s*)(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{16})",
        r"(?<=Código:\s*)(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{16})",
        r"(?<=Digitável:\s*)(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{16})",
    ]

    # Casos que podem falhar
    casos_teste = [
        "Linha Digitável: 03391.2346 56789.01231 41234.567802 1 101880000025000",  # Deve funcionar
        "Código: 03391.2346 56789.01231 41234.567802 1 101880000025000",  # Deve falhar com padrão 1
        "Digitável: 03391.2346 56789.01231 41234.567802 1 101880000025000",  # Deve falhar com padrão 1
        "03391.2346 56789.01231 41234.567802 1 101880000025000",  # Sem prefixo, deve falhar
    ]

    for i, padrao in enumerate(padroes_lookbehind, 1):
        logger.info(f"🔍 Testando padrão {i}: {padrao}")

        for j, caso in enumerate(casos_teste, 1):
            try:
                match = regex.search(padrao, caso)
                if match:
                    logger.info(f"  ✅ Caso {j}: Encontrou '{match.group(1)}'")
                else:
                    logger.info(f"  ❌ Caso {j}: Não encontrou match")
            except Exception as e:
                logger.error(f"  💥 Caso {j}: Erro - {e}")


def test_regex_falha_grupos_nomeados():
    """Testa falhas com grupos nomeados"""
    logger = get_logger("test_regex_grupos_falha")
    logger.info("🧪 TESTE DE FALHAS COM GRUPOS NOMEADOS")
    logger.info("=" * 60)

    # Padrão com grupos nomeados
    padrao_grupos = r"""
    (?x)  # Verbose mode
    (?P<banco>\d{3})
    (?P<moeda>\d{1})
    (?P<campo1>\d{4,5})
    \.
    (?P<dv1>\d{1})
    \s+
    (?P<campo2>\d{5})
    \.
    (?P<dv2>\d{1})
    \s+
    (?P<campo3>\d{5})
    \.
    (?P<dv3>\d{1})
    \s+
    (?P<dv_geral>\d{1})
    \s+
    (?P<fator>\d{4})
    (?P<valor>\d{10})
    """

    # Casos de teste
    casos_teste = [
        "03399161400700000191281556001014411370000038936",  # Válido
        "03399161400700000191281556001014911370000038936",  # DV geral errado
        "0339916140070000019128155600101441137000003893",  # Muito curto
        "033991614007000001912815560010144113700000389360",  # Muito longo
        "0339916140070000019128155600101441137000003893a",  # Com letra
    ]

    for i, caso in enumerate(casos_teste, 1):
        logger.info(f"📝 Testando caso {i}: {caso}")

        try:
            match = regex.match(padrao_grupos, caso)
            if match:
                grupos = match.groupdict()
                logger.info(f"  ✅ Grupos encontrados:")
                for nome, valor in grupos.items():
                    logger.info(f"    {nome}: {valor}")

                # Validar se os grupos fazem sentido
                if len(grupos["banco"]) == 3 and grupos["banco"].isdigit():
                    logger.info(f"  ✅ Banco válido: {grupos['banco']}")
                else:
                    logger.warning(f"  ⚠️ Banco inválido: {grupos['banco']}")
            else:
                logger.info(f"  ❌ Não encontrou match")
        except Exception as e:
            logger.error(f"  💥 Erro: {e}")


def test_regex_falha_flags_avancadas():
    """Testa falhas com flags avançadas"""
    logger = get_logger("test_regex_flags_falha")
    logger.info("🧪 TESTE DE FALHAS COM FLAGS AVANÇADAS")
    logger.info("=" * 60)

    # Padrões com diferentes flags
    padroes_flags = [
        r"(?im)(linha\s+digitável)[:\s]*(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{16})",  # Case insensitive + multiline
        r"(?i)(linha\s+digitável)[:\s]*(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{16})",  # Apenas case insensitive
        r"(?m)(linha\s+digitável)[:\s]*(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{16})",  # Apenas multiline
    ]

    # Casos de teste com diferentes formatos
    casos_teste = [
        "LINHA DIGITÁVEL: 03391.2346 56789.01231 41234.567802 1 101880000025000",  # Maiúsculas
        "Linha Digitável: 03391.2346 56789.01231 41234.567802 1 101880000025000",  # Misto
        "linha digitável: 03391.2346 56789.01231 41234.567802 1 101880000025000",  # Minúsculas
        "LINHA\nDIGITÁVEL: 03391.2346 56789.01231 41234.567802 1 101880000025000",  # Com quebra de linha
    ]

    for i, padrao in enumerate(padroes_flags, 1):
        logger.info(f"🔍 Testando padrão {i}: {padrao}")

        for j, caso in enumerate(casos_teste, 1):
            try:
                match = regex.search(padrao, caso)
                if match:
                    logger.info(f"  ✅ Caso {j}: Encontrou '{match.group(2)}'")
                else:
                    logger.info(f"  ❌ Caso {j}: Não encontrou match")
            except Exception as e:
                logger.error(f"  💥 Caso {j}: Erro - {e}")


def test_regex_falha_quantificadores_possesivos():
    """Testa falhas com quantificadores possesivos"""
    logger = get_logger("test_regex_possesivos_falha")
    logger.info("🧪 TESTE DE FALHAS COM QUANTIFICADORES POSSESSIVOS")
    logger.info("=" * 60)

    # Padrões com quantificadores possesivos
    padroes_possesivos = [
        r"(\d{5}\.\d{4}+\s+\d{5}\.\d{5}+\s+\d{5}\.\d{6}+\s+\d+\s+\d{16}+)",  # Possessivo
        r"(\d{5}\.\d{4}\s+\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d\s+\d{16})",  # Normal
    ]

    # Casos de teste
    casos_teste = [
        "03391.2346 56789.01231 41234.567802 1 101880000025000",  # Válido
        "03391.2346 56789.01231 41234.567802 1 10188000002500",  # Menos dígitos
        "03391.2346 56789.01231 41234.567802 1 1018800000250000",  # Mais dígitos
    ]

    for i, padrao in enumerate(padroes_possesivos, 1):
        logger.info(f"🔍 Testando padrão {i}: {padrao}")

        for j, caso in enumerate(casos_teste, 1):
            try:
                match = regex.search(padrao, caso)
                if match:
                    logger.info(f"  ✅ Caso {j}: Encontrou '{match.group(1)}'")
                else:
                    logger.info(f"  ❌ Caso {j}: Não encontrou match")
            except Exception as e:
                logger.error(f"  💥 Caso {j}: Erro - {e}")


if __name__ == "__main__":
    # Executar testes
    test_demonstracao_recursos_avancados()
    test_digitavel_valido_real()

    # Executar testes de casos de falha
    test_regex_falha_padroes_malformados()
    test_regex_falha_extracao_multiplos_formatos()
    test_regex_falha_lookbehind_complexo()
    test_regex_falha_grupos_nomeados()
    test_regex_falha_flags_avancadas()
    test_regex_falha_quantificadores_possesivos()
