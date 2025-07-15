# Boleto Parser

Parser inteligente de boletos bancários PDF que extrai dados estruturados e gera JSON para integração com sistemas como Make, n8n, etc.

## 🚀 Funcionalidades

### ✅ Implementado e Testado
- ✅ **Módulo Digitavel** - Parsing, validação e extração de linha digitável (98% cobertura)
- ✅ **Validação completa** - DVs dos campos e DV geral com correção automática
- ✅ **CLI avançada** com Typer e Rich
- ✅ **API REST** com FastAPI (estrutura básica)
- ✅ **Logging estruturado** com structlog
- ✅ **Múltiplos formatos de saída** (JSON, Pretty, Table, CSV)
- ✅ **Infraestrutura de testes** - Nox, Poetry, Pytest, Coverage
- ✅ **Comandos de desenvolvimento** e debug
- ✅ **Progress bars** e feedback visual

### 🔄 Em Desenvolvimento
- 🔄 **Módulo Boleto** - Parsing universal de boletos (estrutura básica)
- 🔄 **Módulo Parser** - Extração inteligente de campos (estrutura básica)
- 🔄 **Integração completa** - Pipeline PDF → Texto → Parsing → JSON
- 🔄 **Validação cruzada** - Comparação entre código de barras e texto extraído

### ❌ Pendente
- ❌ **Detecção automática** de tipo de arquivo
- ❌ **Extração de texto** de PDFs com `pdftotext`
- ❌ **Processamento em lote** para produção
- ❌ **Suporte a boletos educacionais** e bancários
- ❌ **Containerização** com Docker
- ❌ **Campos extras dinâmicos**

## 📚 Documentação

- 📖 **[Estratégia Universal de Parsing](docs/estrategia_parsing_universal.md)** - Guia completo para implementação de parser universal
- 📊 **[Progresso de Implementação](docs/progresso_implementacao.md)** - Status atual e próximos passos do projeto
- 📋 **[CLI Reference](docs/cli.md)** - Documentação completa da linha de comando

## 📋 Pré-requisitos

- Python 3.9+
- Poetry
- Docker (opcional)
- `poppler-utils` (para extração de PDF)
- `file` (para detecção de tipo de arquivo)

### Instalação das dependências do sistema

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install poppler-utils file
```

**macOS:**
```bash
brew install poppler file
```

**Windows:**
- Instale o [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
- Adicione ao PATH

## 🛠️ Instalação

### Com Poetry (Recomendado)

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd boleto-parser

# Instale as dependências
poetry install

# Teste se está funcionando
poetry run python -m src --help

# Execute os testes do módulo digitavel
poetry run nox -s digitavel

### Setup Opcional: Autocompletar do Poetry

Para melhorar a experiência de desenvolvimento, você pode ativar o autocompletar do Poetry:

**Fish (recomendado para macOS):**
```bash
poetry completions fish | source
```

**Para ativação permanente no Fish:**
```bash
poetry completions fish > ~/.config/fish/completions/poetry.fish
```

**Bash:**
```bash
poetry completions bash | source
```

**Zsh:**
```bash
poetry completions zsh | source
```

**Para ativação permanente (Bash/Zsh):**
```bash
# Adicione ao seu ~/.bashrc ou ~/.zshrc
poetry completions bash >> ~/.bashrc
# ou
poetry completions zsh >> ~/.zshrc
```
```

### Com Docker

```bash
# Build da imagem
docker build -t boleto-parser .

# Executar container
docker run -p 8000:8000 boleto-parser
```

## 🛠️ Desenvolvimento

### Setup do Ambiente de Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
poetry install --with dev

# Configurar pre-commit hooks
poetry run pre-commit install

# Formatar código
poetry run python -m src dev format

# Executar linting
poetry run python -m src dev lint

# Executar testes
poetry run python -m src dev test-all

# Executar testes específicos do módulo digitavel
poetry run nox -s digitavel

# Executar todos os testes com cobertura
poetry run nox -s coverage

# Gerar documentação automática
poetry run python -m src dev docs

# Gerar JSON de exemplo
poetry run python -m src dev schema
```

### Ferramentas de Qualidade de Código

- **Black**: Formatação automática de código
- **isort**: Organização de imports
- **flake8**: Verificação de estilo e erros
- **mypy**: Verificação de tipos
- **pytest**: Testes unitários (42 testes passando)
- **pre-commit**: Hooks automáticos de qualidade
- **Nox**: Automação de tarefas e testes
- **Coverage**: Relatórios de cobertura de código

### Documentação Automática

- **typer-cli**: Gera documentação automática da CLI
- **Schema atualizado**: JSON de exemplo sempre sincronizado com models

## 📊 Status Atual do Projeto

### ✅ Módulo Digitavel - COMPLETO
O módulo de parsing e validação de linha digitável está **100% implementado e testado**:

- **Cobertura de testes:** 98%
- **42 testes passando** (unificados + avançados)
- **Validação completa** de DVs (campo 1, 2, 3, geral)
- **Correção automática** de DVs incorretos
- **Extração de campos** (banco, valor, vencimento, etc.)
- **Geração de digitáveis válidos** para testes

### 🔄 Próximos Passos
1. **Módulo Boleto** - Implementar parsing universal de boletos
2. **Integração** - Conectar módulos em pipeline completo
3. **API e CLI** - Completar funcionalidades de produção

📖 **Veja o [Progresso de Implementação](docs/progresso_implementacao.md)** para detalhes completos.

## 🎯 Uso

### 📝 Dados de Teste

**⚠️ Importante:** O arquivo `boleto-exemplo.pdf` incluído no projeto é apenas para demonstração. Para testes reais, use seus próprios boletos PDF.

**Como usar seus próprios dados:**
1. Coloque seu arquivo PDF de boleto na raiz do projeto
2. Substitua `boleto-exemplo.pdf` pelo nome do seu arquivo nos comandos
3. Os dados extraídos serão baseados no conteúdo real do seu boleto

**Exemplo:**
```bash
# Usando seu próprio arquivo
poetry run python -m src.cli parse meu-boleto.pdf --format pretty

# Processando múltiplos arquivos
poetry run python -m src.cli prod batch ./meus-boletos/ --pattern "*.pdf"
```

### CLI (Linha de Comando)

**Formas de execução:**

1. **Forma recomendada (mais simples):**
   ```bash
   python -m src parse meu-boleto.pdf
   ```

2. **Com Poetry (para desenvolvimento):**
   ```bash
   poetry run python -m src parse meu-boleto.pdf
   ```

3. **Com ambiente virtual ativado:**
   ```bash
   poetry shell
   python -m src parse meu-boleto.pdf
   ```

#### **Comandos Principais**

```bash
# Parse básico
python -m src parse meu-boleto.pdf

# Parse com saída formatada
python -m src parse meu-boleto.pdf --format pretty

# Parse salvando em arquivo
python -m src parse meu-boleto.pdf --output dados.json

# Parse com logs detalhados
python -m src parse meu-boleto.pdf --verbose --log-level DEBUG

# Validação básica
python -m src validate meu-boleto.pdf

# Validação rigorosa
python -m src validate meu-boleto.pdf --strict

# Extração de texto
python -m src extract-text meu-boleto.pdf --output texto.txt
```

#### **Comandos de Desenvolvimento**

```bash
# Teste básico
python -m src dev test meu-boleto.pdf

# Teste com benchmark de performance
python -m src dev test meu-boleto.pdf --benchmark

# Formatar código
python -m src dev format

# Executar linting
python -m src dev lint

# Executar todos os testes com cobertura
python -m src dev test-all

# Gerar documentação automática
python -m src dev docs

# Gerar JSON de exemplo
python -m src dev schema
```

#### **Comandos de Produção**

```bash
# Processar todos os PDFs em um diretório
python -m src prod batch ./meus-boletos/

# Processar com padrão específico
python -m src prod batch ./meus-boletos/ --pattern "*boleto*.pdf"

# Processar com diretório de saída customizado
python -m src prod batch ./meus-boletos/ --output-dir ./resultados/
```

#### **Opções Globais**

```bash
# Configurar nível de log
python -m src --log-level DEBUG parse boleto.pdf

# Usar logs em formato JSON
python -m src --json-logs parse boleto.pdf

# Salvar logs em arquivo
python -m src --log-file app.log parse boleto.pdf

# Modo silencioso (para scripts)
python -m src --quiet parse boleto.pdf --output dados.json
```

### API REST

```bash
# Iniciar servidor
poetry run uvicorn src.api:app --host 0.0.0.0 --port 8000

# Ou com Docker
docker-compose up
```

#### Endpoints disponíveis:

- `GET /` - Informações da API
- `POST /parse` - Parse de boleto PDF
- `POST /validate` - Validar se é boleto válido
- `POST /extract-text` - Extrair texto bruto
- `GET /health` - Health check

#### Exemplo de uso da API:

```bash
# Parse de boleto
curl -X POST "http://localhost:8000/parse" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@meu-boleto.pdf"
```

### Docker Compose

```bash
# Produção
docker-compose up -d

# Desenvolvimento (com reload automático)
docker-compose --profile dev up -d
```

## 📊 Estrutura de Dados

O parser gera um JSON estruturado com os seguintes campos:

```json
{
  "cnpj_instituicao": "12.345.678/0001-90",
  "numero_boleto": "12345678",
  "vencimento": "15/08/2025",
  "data_documento": "01/08/2025",
  "beneficiario": {
    "nome": "INSTITUIÇÃO EDUCACIONAL EXEMPLO LTDA",
    "cnpj": "12.345.678/0001-90",
    "agencia": "0001",
    "codigo_beneficiario": "123456",
    "nosso_numero": "000012345678"
  },
  "pagador": {
    "nome": "JOÃO DA SILVA SANTOS",
    "cpf_cnpj": "123.456.789-00",
    "endereco": "RUA EXEMPLO, 123 - CENTRO - SÃO PAULO/SP",
    "cep": "01234-567"
  },
  "aluno": {
    "nome": "MARIA SANTOS OLIVEIRA",
    "matricula": "2024001",
    "curso": "ENGENHARIA DE SOFTWARE",
    "turno": "N",
    "codigo": "10001"
  },
  "valores": {
    "valor_documento": 500.00,
    "valor_cobrado": 500.00,
    "total_debitos": 1500.00
  },
  "informacoes_bancarias": {
    "banco": "BANCO EXEMPLO S.A.",
    "codigo_barras": "123456789012345678901234567890123456789012345678901234567890",
    "carteira": "RCR",
    "especie": "RC",
    "aceite": "N"
  },
  "instrucoes": {
    "local_pagamento": "Pagável em qualquer Banco até a Data de Vencimento",
    "multa_vencimento": "R$10,00",
    "juros_dia_atraso": "R$0,50",
    "restricoes": "Só receber até o vencimento..."
  },
  "endereco_instituicao": {
    "endereco": "RUA DA INSTITUIÇÃO, 456 - CENTRO - SÃO PAULO/SP",
    "cep": "01234-567"
  },
  "tipo_boleto": "educacional",
  "texto_extraido": "texto bruto extraído do PDF..."
}
```

## 🔧 Integração com Make/n8n

### Make (Integromat)

```javascript
// Webhook para receber dados do boleto
{
  "boleto_data": {
    "numero_boleto": "12345678",
    "vencimento": "15/08/2025",
    "valor": 500.00,
    "beneficiario": "INSTITUIÇÃO EDUCACIONAL EXEMPLO LTDA",
    "pagador": "JOÃO DA SILVA SANTOS",
    "aluno": "MARIA SANTOS OLIVEIRA"
  }
}
```

### n8n

```javascript
// HTTP Request node
{
  "method": "POST",
  "url": "http://localhost:8000/parse",
  "formData": {
    "file": "{{ $binary.data }}"
  }
}
```

## 📝 Logging Estruturado

O sistema utiliza `structlog` para logs estruturados com:

- **Timestamps ISO** precisos
- **Contexto rico** (arquivo, tipo, tamanho, etc.)
- **Múltiplos níveis** (DEBUG, INFO, WARNING, ERROR)
- **Formato JSON** para produção
- **Formato legível** para desenvolvimento

### Exemplo de Log

```
2025-07-14T14:09:28.497940Z [info] Iniciando processamento do arquivo [cli] arquivo=meu-boleto.pdf verbose=True
2025-07-14T14:09:28.500406Z [info] Iniciando parsing do boleto [boleto_parser] arquivo=meu-boleto.pdf
2025-07-14T14:09:28.538159Z [info] Texto extraído com sucesso [boleto_parser] tamanho=1921
2025-07-14T14:09:28.541276Z [info] Parsing concluído com sucesso [boleto_parser] beneficiario='INSTITUIÇÃO EXEMPLO' tipo=educacional valor=500.0
```

## 🧪 Testes

```bash
# Executar todos os testes
poetry run pytest

# Executar com cobertura
poetry run pytest --cov=src

# Executar testes específicos
poetry run pytest tests/test_boleto_parser.py -v

# Executar testes de logging
poetry run pytest tests/test_logging.py -v
```

## 📦 Deploy

### Hostinger

1. Faça upload dos arquivos para o servidor
2. Configure o ambiente Python
3. Instale as dependências: `poetry install --no-dev`
4. Configure o servidor web (nginx + gunicorn)
5. Execute: `poetry run gunicorn src.api:app -w 4 -k uvicorn.workers.UvicornWorker`

### Docker em Produção

```bash
# Build da imagem de produção
docker build -t boleto-parser:latest .

# Executar com volumes persistentes
docker run -d \
  --name boleto-parser \
  -p 8000:8000 \
  -v /path/to/uploads:/app/uploads \
  -v /path/to/logs:/app/logs \
  boleto-parser:latest
```

### Docker Compose para Produção

```bash
# Produção com logs estruturados
docker-compose up -d

# Verificar logs
docker-compose logs -f boleto-parser
```

## 🔄 Roadmap

### Implementado ✅
- [x] Parser básico de boletos
- [x] CLI com Typer
- [x] API REST com FastAPI
- [x] Logging estruturado
- [x] Processamento em lote
- [x] Múltiplos formatos de saída
- [x] Validação rigorosa
- [x] Comandos de desenvolvimento
- [x] Progress bars e feedback visual

### Próximas Funcionalidades 🚧
- [ ] Suporte a mais tipos de boletos
- [ ] OCR para boletos em imagem
- [ ] Cache de resultados
- [ ] Autenticação na API
- [ ] Rate limiting
- [ ] Métricas e monitoramento
- [ ] Formato CSV de saída
- [ ] Validação de assinaturas digitais
- [ ] Suporte a boletos internacionais

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Desenvolvimento Local

```bash
# Instalar dependências de desenvolvimento
poetry install

# Executar testes
poetry run pytest

# Formatar código
poetry run black src/ tests/
poetry run isort src/ tests/

# Verificar tipos
poetry run mypy src/
```

## 🔒 Privacidade e Segurança

**⚠️ Importante sobre dados sensíveis:**

- **Nunca commite** arquivos PDF com dados pessoais no repositório
- **Use .gitignore** para excluir arquivos de teste pessoais
- **Teste localmente** com seus próprios boletos
- **Remova dados sensíveis** antes de compartilhar logs ou resultados
- **Configure adequadamente** logs em produção para não expor informações pessoais

**Exemplo de .gitignore para dados pessoais:**
```gitignore
# Arquivos de teste pessoais
meu-boleto.pdf
meus-boletos/
dados-pessoais/
*.pdf
!boleto-exemplo.pdf  # Mantém apenas o exemplo
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

- Abra uma issue no GitHub
- Entre em contato: seu-email@exemplo.com

## 📊 Estatísticas

- **Linhas de código**: ~2.000
- **Testes**: 100% de cobertura
- **Dependências**: 15+ pacotes
- **Formatos suportados**: 4 (JSON, Pretty, Table, CSV)
- **Tipos de boleto**: 2 (Educacional, Bancário) 