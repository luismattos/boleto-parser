# Documentação da CLI - Boleto Parser

## Comandos Principais

### parse
Parse um arquivo PDF de boleto bancário e extrai dados estruturados.

```bash
python -m src parse arquivo.pdf [OPÇÕES]
```

**Opções:**
- `--output, -o`: Arquivo de saída JSON
- `--format, -f`: Formato de saída (json, pretty, table)
- `--verbose, -v`: Modo verboso
- `--force`: Sobrescrever arquivo de saída sem confirmar

### validate
Valida se um arquivo PDF é um boleto válido.

```bash
python -m src validate arquivo.pdf [--strict]
```

### extract-text
Extrai apenas o texto bruto do PDF.

```bash
python -m src extract-text arquivo.pdf [--output arquivo.txt]
```

## Comandos de Desenvolvimento

### dev test
Teste básico de processamento de boleto.

```bash
python -m src dev test arquivo.pdf [--benchmark] [--verbose]
```

**Opções:**
- `--benchmark`: Executar benchmark de performance
- `--verbose, -v`: Modo verboso com detalhes completos

### dev format
Formata o código usando black e isort.

```bash
python -m src dev format
```

### dev lint
Executa verificações de qualidade do código.

```bash
python -m src dev lint
```

**Verificações incluídas:**
- Black (formatação)
- isort (organização de imports)
- flake8 (estilo e erros)
- mypy (verificação de tipos)

### dev test-all
Executa todos os testes com cobertura.

```bash
python -m src dev test-all
```

### dev check
Executa todas as verificações de desenvolvimento de uma vez.

```bash
python -m src dev check
```

**Este comando executa:**
1. Formatação (black + isort)
2. Verificações de qualidade (lint)
3. Testes com cobertura

### dev schema
Gera JSON de exemplo baseado nos models atuais.

```bash
python -m src dev schema
```

### dev docs
Gera documentação automática da CLI.

```bash
python -m src dev docs
```

## Comandos de Produção

### prod batch
Processa múltiplos arquivos PDF em lote.

```bash
python -m src prod batch diretorio/ [--pattern "*.pdf"] [--output-dir ./resultados/]
```

## Opções Globais

- `--log-level, -l`: Nível de logging (DEBUG, INFO, WARNING, ERROR)
- `--log-file`: Arquivo de log (opcional)
- `--json-logs`: Usar formato JSON para logs
- `--quiet, -q`: Modo silencioso

## Fluxo de Desenvolvimento Recomendado

1. **Desenvolvimento:**
   ```bash
   python -m src dev test meu-boleto.pdf --verbose
   ```

2. **Formatação:**
   ```bash
   python -m src dev format
   ```

3. **Verificação de qualidade:**
   ```bash
   python -m src dev lint
   ```

4. **Testes:**
   ```bash
   python -m src dev test-all
   ```

5. **Verificação completa:**
   ```bash
   python -m src dev check
   ```

## Exemplos de Uso

### Desenvolvimento Diário
```bash
# Testar um boleto com detalhes
python -m src dev test boleto-exemplo.pdf --verbose

# Formatar código
python -m src dev format

# Verificar qualidade
python -m src dev lint

# Executar todos os testes
python -m src dev test-all

# Ou fazer tudo de uma vez
python -m src dev check
```

### Produção
```bash
# Processar um boleto
python -m src parse boleto.pdf --format pretty

# Processar múltiplos boletos
python -m src prod batch ./boletos/ --output-dir ./resultados/
```

---
*Documentação atualizada em 2025-01-14*
