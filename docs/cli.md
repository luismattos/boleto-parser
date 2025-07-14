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
Teste básico de processamento.

```bash
python -m src dev test arquivo.pdf [--benchmark]
```

### dev format
Formata o código usando black e isort.

```bash
python -m src dev format
```

### dev lint
Executa verificações de linting.

```bash
python -m src dev lint
```

### dev test-all
Executa todos os testes com cobertura.

```bash
python -m src dev test-all
```

### dev schema
Gera JSON de exemplo baseado nos models atuais.

```bash
python -m src dev schema
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

---
*Documentação gerada automaticamente em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
