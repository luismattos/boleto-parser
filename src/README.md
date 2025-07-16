# Estrutura do Código Fonte - Boleto Parser

## 📁 Organização dos Diretórios

### 🎯 **Core** (`src/core/`)
Classes principais e fundamentais do sistema:

- **`boleto.py`** - Classe `BoletoBancario` com estrutura Febraban
- **`digitavel.py`** - Classe `Digitavel` para processamento de códigos digitáveis
- **`__init__.py`** - Exports das classes principais

**Classes Principais:**
- `BoletoBancario` - Representação completa de um boleto
- `TipoDocumento` - Enum com tipos de documento Febraban
- `TipoAceite` - Enum para aceite do documento
- `Digitavel` - Processamento e validação de códigos digitáveis
- `CamposDigitavel` - Estrutura dos campos da linha digitável

### 🛠️ **Utils** (`src/utils/`)
Utilitários e ferramentas auxiliares:

- **`logger.py`** - Sistema de logging estruturado com structlog
- **`__init__.py`** - Exports das utilidades

**Funcionalidades:**
- `get_logger()` - Obter logger configurado
- `setup_logging()` - Configurar logging customizado
- `setup_default_logging()` - Configuração padrão

### 🧪 **Tests** (`src/tests/`)
Testes de desenvolvimento e validação:

- **`test_*.py`** - Testes unitários e de integração
- **`__init__.py`** - Módulo de testes (não parte da API pública)

**Arquivos de Teste:**
- `test_parser.py` - Testes do parser principal
- `test_boleto_classe.py` - Testes da classe BoletoBancario
- `test_digitavel_*.py` - Testes de validação de códigos digitáveis
- `test_split_digitavel.py` - Testes de divisão de campos
- `test_prototype_real.py` - Testes com dados reais

### 🔬 **Prototypes** (`src/prototypes/`)
Arquivos de protótipo e experimentação:

- **`prototype_*.py`** - Protótipos em desenvolvimento
- **`__init__.py`** - Módulo de protótipos (não parte da API pública)

**Categorias de Protótipos:**
- **Classes:** `prototype_classe_*.py` - Evolução das classes principais
- **Parsers:** `prototype_universal_parser*.py` - Estratégias de parsing
- **Validação:** `prototype_validacao_*.py` - Cálculos de dígitos verificadores
- **Decodificação:** `prototype_decodificar_*.py` - Processamento de códigos
- **Análise:** `prototype_analise_*.py` - Debug e análise detalhada

## 📄 **Arquivos Principais** (Raiz de `src/`)

### 🚀 **Entry Points**
- **`__main__.py`** - Ponto de entrada para execução direta
- **`__init__.py`** - API pública do pacote

### 🔌 **Interfaces**
- **`cli.py`** - Interface de linha de comando (Typer + Rich)
- **`api.py`** - API REST (FastAPI)

### 🧠 **Lógica Principal**
- **`parser.py`** - Parser principal de boletos PDF
- **`models.py`** - Modelos Pydantic para validação

## 🔄 **Fluxo de Desenvolvimento**

### 1. **Prototipagem** (`src/prototypes/`)
- Desenvolver novas funcionalidades em protótipos
- Testar diferentes abordagens
- Validar conceitos antes da implementação

### 2. **Implementação** (`src/core/`)
- Migrar código validado dos protótipos
- Refatorar para produção
- Manter compatibilidade com API pública

### 3. **Testes** (`src/tests/`)
- Testes unitários para cada componente
- Testes de integração
- Validação com dados reais

### 4. **Utilitários** (`src/utils/`)
- Ferramentas auxiliares reutilizáveis
- Sistema de logging
- Helpers e funções utilitárias

## 📋 **Convenções**

### **Nomenclatura**
- **Classes:** PascalCase (`BoletoBancario`)
- **Funções/Variáveis:** snake_case (`extrair_texto_pdf`)
- **Constantes:** UPPER_SNAKE_CASE (`TIPO_DOCUMENTO`)
- **Arquivos:** snake_case (`boleto_parser.py`)

### **Imports**
```python
# Imports internos
from .core import BoletoBancario, Digitavel
from .utils.logger import get_logger

# Imports externos
from fastapi import FastAPI
from pydantic import BaseModel
```

### **Documentação**
- Docstrings em todas as classes e métodos
- Type hints obrigatórios
- Exemplos de uso nos docstrings principais

## 🎯 **Próximos Passos**

1. **Consolidar Protótipos** - Integrar melhores partes dos protótipos no core
2. **Expandir Testes** - Aumentar cobertura de testes
3. **Documentação** - Melhorar documentação das classes principais
4. **Performance** - Otimizar processamento em lote
5. **Validação** - Implementar validação rigorosa de DVs

## 📊 **Estatísticas**

- **Core:** 3 arquivos (15KB)
- **Utils:** 1 arquivo (3KB)
- **Tests:** 7 arquivos (25KB)
- **Prototypes:** 19 arquivos (200KB+)
- **Total:** ~30 arquivos, ~250KB de código 