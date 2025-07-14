# Estratégia Universal de Parsing de Boletos

## 🎯 Objetivo
Criar um parser universal que funcione com **qualquer tipo de boleto** (bancário, educacional, comercial, serviço), garantindo a captura de todos os campos obrigatórios e opcionais.

## 📋 Estratégia de Implementação

### Passo 1: Extrair TUDO de uma vez
- Capturar **todo o texto** do PDF sem filtros
- Não tentar identificar nada ainda
- Apenas extrair o texto bruto completo
- Salvar em `texto_extraido` para processamento posterior

### Passo 2: Trabalhar nos Campos Obrigatórios - COMEÇAR PELO CAMPO VARIANTE

#### 2.1 - Decodificar Linha Digitável/Código de Barras
- Encontrar o código no texto extraído
- Usar `BoletoDecoder` para extrair:
  - **Código do banco** (3 dígitos)
  - **Valor exato** do boleto
  - **Data de vencimento** precisa
  - **Campo livre** (informações específicas do banco)

#### 2.2 - Campos Obrigatórios Universais
```python
campos_obrigatorios = {
    "codigo_banco": "3 dígitos",
    "linha_digitavel": "47 dígitos",
    "codigo_barras": "representação gráfica",
    "nome_cedente": "quem emite/recebe",
    "cnpj_cpf_cedente": "documento do cedente",
    "nome_pagador": "quem deve pagar",
    "cnpj_cpf_pagador": "documento do pagador",
    "data_vencimento": "data limite",
    "valor_documento": "valor total",
    "nosso_numero": "código único do banco",
    "carteira": "tipo de boleto",
    "agencia_codigo_cedente": "dados da agência",
    "data_emissao": "data de geração",
    "especie_documento": "tipo do documento",
    "instrucoes": "informações adicionais",
    "moeda": "R$",
    "local_pagamento": "onde pagar",
    "autenticacao_mecanica": "espaço reservado"
}
```

### Passo 3: Padrões Universais para Campos Obrigatórios

```python
padroes_obrigatorios = {
    "nome_cedente": [
        r"BENEFICIÁRIO[:\s]*(.+)",
        r"Beneficiário[:\s]*(.+)",
        r"CEDENTE[:\s]*(.+)",
        r"Cedente[:\s]*(.+)",
        r"FAVORECIDO[:\s]*(.+)"
    ],
    "nome_pagador": [
        r"PAGADOR[:\s]*(.+)",
        r"Pagador[:\s]*(.+)",
        r"SACADO[:\s]*(.+)",
        r"Sacado[:\s]*(.+)"
    ],
    "cnpj_cpf_cedente": [
        r"CNPJ[:\s]*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})",
        r"CPF[:\s]*(\d{3}\.\d{3}\.\d{3}-\d{2})",
        r"CNPJ/CPF[:\s]*([\d\.-]+)"
    ],
    "cnpj_cpf_pagador": [
        r"CPF/CNPJ[:\s]*([\d\.-]+)",
        r"CPF[:\s]*(\d{3}\.\d{3}\.\d{3}-\d{2})",
        r"CNPJ[:\s]*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})"
    ],
    "valor_documento": [
        r"VALOR[:\s]*R\$\s*([\d,]+\.?\d*)",
        r"Valor[:\s]*R\$\s*([\d,]+\.?\d*)",
        r"Total[:\s]*R\$\s*([\d,]+\.?\d*)"
    ],
    "data_vencimento": [
        r"VENCIMENTO[:\s]*(\d{2}/\d{2}/\d{4})",
        r"Vencimento[:\s]*(\d{2}/\d{2}/\d{4})",
        r"Data Vencimento[:\s]*(\d{2}/\d{2}/\d{4})"
    ],
    "data_emissao": [
        r"DATA[:\s]*(\d{2}/\d{2}/\d{4})",
        r"Data[:\s]*(\d{2}/\d{2}/\d{4})",
        r"Emissão[:\s]*(\d{2}/\d{2}/\d{4})"
    ],
    "nosso_numero": [
        r"NOSSO NÚMERO[:\s]*(\d+)",
        r"Nosso Número[:\s]*(\d+)",
        r"Nº[:\s]*(\d+)"
    ],
    "carteira": [
        r"CARTEIRA[:\s]*(\w+)",
        r"Carteira[:\s]*(\w+)"
    ],
    "agencia_codigo_cedente": [
        r"AGÊNCIA[:\s]*(\d+)[/\s]*(\d+)",
        r"Agência[:\s]*(\d+)[/\s]*(\d+)"
    ],
    "especie_documento": [
        r"ESPÉCIE[:\s]*(\w+)",
        r"Espécie[:\s]*(\w+)",
        r"Espécie Doc[:\s]*(\w+)"
    ],
    "local_pagamento": [
        r"LOCAL[:\s]*(.+)",
        r"Local[:\s]*(.+)"
    ]
}
```

### Passo 4: Validação dos Obrigatórios

**Hierarquia de confiabilidade:**
1. **Código de barras** (mais confiável - dados padronizados)
2. **Padrões universais** (médio - podem variar de layout)
3. **Validação cruzada:** Comparar dados do código de barras com dados extraídos do texto

### Passo 5: Campos Opcionais (só depois dos obrigatórios)

```python
campos_opcionais = {
    "instrucoes_pos_vencimento": "juros, multas, mora",
    "descontos": "descontos antecipados",
    "numero_documento": "código interno",
    "aceite": "S/N",
    "sacador_avalista": "garantidor",
    "informacoes_adicionais": "mensagens específicas",
    "endereco_cedente": "endereço completo",
    "endereco_pagador": "endereço completo",
    "codigo_beneficiario": "identificador adicional",
    "protesto": "instruções de protesto",
    "uso_banco": "anotações internas"
}
```

### Passo 6: Estrutura Final

```json
{
  "campos_obrigatorios": {
    "codigo_banco": "033",
    "linha_digitavel": "03399.16140...",
    "codigo_barras": "033991614...",
    "nome_cedente": "NU PAGAMENTOS S/A",
    "cnpj_cpf_cedente": "12.345.678/0001-90",
    "nome_pagador": "João Silva",
    "cnpj_cpf_pagador": "123.456.789-00",
    "data_vencimento": "15/05/2025",
    "valor_documento": 150.00,
    "nosso_numero": "12345678",
    "carteira": "00",
    "agencia_codigo_cedente": "1234/567890",
    "data_emissao": "01/05/2025",
    "especie_documento": "DM",
    "instrucoes": "Pagável em qualquer banco",
    "moeda": "R$",
    "local_pagamento": "Qualquer banco",
    "autenticacao_mecanica": "reservado"
  },
  "campos_opcionais": { ... },
  "tipo_boleto": "bancario|educacional|comercial|servico"
}
```

## 🚀 Vantagens desta Abordagem

1. **Universal:** Funciona com qualquer boleto
2. **Robusto:** Não perde informações críticas
3. **Confíavel:** Validação cruzada de dados
4. **Organizado:** Separação clara entre obrigatórios e opcionais
5. **Extensível:** Fácil adicionar novos tipos de boleto

## 📝 Campos Obrigatórios (Febraban)

### Campos que SEMPRE existem em qualquer boleto:
1. **Código do Banco:** Número de três dígitos que identifica o banco emissor
2. **Linha Digitável:** Sequência numérica (47 dígitos) para pagamento
3. **Código de Barras:** Representação gráfica da linha digitável
4. **Nome do Cedente:** Quem emite/recebe o pagamento
5. **CNPJ/CPF do Cedente:** Documento do emitente
6. **Nome do Pagador:** Quem deve realizar o pagamento
7. **CNPJ/CPF do Pagador:** Documento do pagador
8. **Data de Vencimento:** Data limite para pagamento sem encargos
9. **Valor do Documento:** Valor total a ser pago
10. **Nosso Número:** Código único gerado pelo banco
11. **Carteira:** Tipo de boleto (com/sem registro)
12. **Agência/Código do Cedente:** Dados da agência e conta
13. **Data de Emissão:** Data em que o boleto foi gerado
14. **Espécie do Documento:** Tipo de documento (DM, etc.)
15. **Instruções:** Informações adicionais ao pagador
16. **Moeda:** R$
17. **Local de Pagamento:** Onde pode ser pago
18. **Autenticação Mecânica:** Espaço reservado

## 📝 Campos Opcionais

### Campos que podem variar:
- **Instruções para Pagamento Após o Vencimento:** Juros, multas, mora
- **Descontos:** Descontos antecipados
- **Número do Documento:** Código interno do cedente
- **Aceite:** S/N
- **Sacador/Avalista:** Garantidor
- **Informações Adicionais:** Mensagens específicas
- **Endereço do Cedente/Pagador:** Endereços completos
- **Código do Beneficiário:** Identificador adicional
- **Protesto:** Instruções de protesto
- **Uso do Banco:** Anotações internas

## 🔄 Status de Implementação

- [ ] Passo 1: Extrair tudo de uma vez
- [ ] Passo 2: Implementar decodificação universal
- [ ] Passo 3: Padrões universais para obrigatórios
- [ ] Passo 4: Validação cruzada
- [ ] Passo 5: Campos opcionais
- [ ] Passo 6: Estrutura final

## 📋 Próximos Passos

1. Refatorar `BoletoParser` para seguir esta estratégia
2. Implementar padrões universais
3. Criar validação cruzada
4. Testar com diferentes tipos de boleto
5. Documentar casos de uso específicos 