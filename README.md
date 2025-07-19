# Analisador Léxico para Linguagem Simples

## Integrantes

- Daniel Ferreira Nunes - Matrícula: 211061565 
- Nicollas Gabriel Oliveira Sousa - Matrícula: 211062802
- Felipe Guimaraes Fernandes - Matrícula: 211041132
- Paulo Henrique Virgilio Cerqueira  - Matrícula: 211030630

## Introdução

Este projeto implementa um **analisador léxico (lexer ou scanner)** para uma linguagem de programação simples. O analisador léxico é a primeira fase de um compilador, responsável por ler uma string de entrada (código fonte) e dividi-la em tokens - unidades léxicas como palavras-chave, identificadores, números, operadores e delimitadores.

### Estratégias e Algoritmos

O projeto utiliza **expressões regulares** em Python para identificar e classificar os diferentes tipos de tokens. As principais estratégias implementadas incluem:

1. **Reconhecimento por padrões**: Cada tipo de token é definido por uma expressão regular específica
2. **Precedência de tokens**: A ordem dos padrões garante que palavras-chave sejam reconhecidas antes de identificadores
3. **Rastreamento de posição**: Mantém controle da linha e coluna atual para relatório de erros
4. **Tratamento de erros**: Identifica e reporta caracteres inválidos com localização precisa

### Linguagem Suportada

A linguagem implementada suporta:

**Tipos de dados**: `int`, `float`, `string`, `bool`

**Palavras-chave de controle**: `if`, `else`, `while`, `for`, `function`, `return`

**Operadores aritméticos**: `+`, `-`, `*`, `/`, `%`

**Operadores de comparação**: `==`, `!=`, `<`, `>`, `<=`, `>=`

**Operadores lógicos**: `and`, `or`, `not`

**Delimitadores**: `(`, `)`, `{`, `}`, `[`, `]`, `;`, `,`

**Literais**: números inteiros e decimais, strings com aspas duplas ou simples, booleanos (`true`, `false`)

**Comentários**: de linha (`//`) e de bloco (`/* */`)

### Exemplos de Sintaxe

```
// Declaração de variáveis
int idade = 25;
float altura = 1.75;
string nome = "João";
bool ativo = true;

// Estrutura condicional
if (idade >= 18) {
    string status = "maior de idade";
} else {
    string status = "menor de idade";
}

// Função recursiva
function fibonacci(int n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}
```

## Instalação

### Pré-requisitos
- Python 3.8 ou superior

### Passos para instalação e execução

1. **Clone o repositório** (se necessário):
   ```bash
   git clone <url-do-repositorio>
   cd trabalho-final-trabalho_final_comp
   ```

2. **Execute o analisador léxico**:

   **Análise de código direto**:
   ```bash
   python -m src.main "int x = 10 + 5;"
   ```

   **Análise de arquivo**:
   ```bash
   python -m src.main exemplos/01_hello_world.txt
   ```

   **Modo verboso (mostra whitespace e comentários)**:
   ```bash
   python -m src.main --verbose "int x = 10; // comentário"
   ```

   **Diferentes formatos de saída**:
   ```bash
   python -m src.main --format detailed "int x = 10;"
   python -m src.main --format json "int x = 10;"
   ```

3. **Execute os testes unitários**:
   ```bash
   python -m pytest tests/ -v
   ```
   
   ou usando unittest:
   ```bash
   python -m unittest tests.test_lexer -v
   ```

### Exemplo de uso básico

```bash
python -m src.main "int x = 10 + 5;"
```

**Saída esperada**:
```
Analisando código fornecido:
Código: 'int x = 10 + 5;'
--------------------------------------------------
Tokens:
  INT
  IDENTIFIER(x)
  ASSIGN
  NUMBER(10)
  PLUS
  NUMBER(5)
  SEMICOLON

Estatísticas:
  Total de tokens: 7
  Linhas processadas: 1
```

## Exemplos

O projeto contém uma pasta `exemplos/` com arquivos demonstrando diferentes aspectos da linguagem:

1. **01_hello_world.txt** - Exemplo básico com string
2. **02_variaveis.txt** - Declaração de variáveis de diferentes tipos
3. **03_operacoes.txt** - Operações aritméticas básicas
4. **04_condicional.txt** - Estruturas condicionais (if/else)
5. **05_loop.txt** - Estruturas de repetição (while)
6. **06_fibonacci.txt** - Função recursiva
7. **07_busca_linear.txt** - Estruturas de dados simples e busca
8. **08_bubble_sort.txt** - Algoritmo de ordenação complexo

Para testar qualquer exemplo:
```bash
python -m src.main exemplos/06_fibonacci.txt
```

## Referências

Este projeto foi desenvolvido utilizando as seguintes referências:

1. **"Crafting Interpreters" por Robert Nystrom** - Fonte principal para entender os fundamentos de análise léxica e estrutura de compiladores. Utilizado como guia teórico para implementação do lexer.

2. **Documentação oficial do módulo `re` do Python** - Referência técnica para implementação das expressões regulares utilizadas no reconhecimento de padrões de tokens.

3. **"Compilers: Principles, Techniques, and Tools" (Dragon Book) por Aho, Sethi, Ullman** - Consulta teórica sobre algoritmos de análise léxica e técnicas de compilação.

4. **Material da disciplina de Compiladores** - Slides e anotações de aula utilizados como base conceitual para o projeto.

### Contribuições Originais

- **Implementação completa do lexer**: Todo o código foi desenvolvido do zero seguindo os princípios teóricos estudados
- **Sistema de tratamento de erros**: Implementação original de rastreamento de posição (linha/coluna) para relatório de erros precisos
- **Suporte a múltiplos formatos de saída**: Funcionalidade adicional para exportar tokens em formatos simples, detalhado e JSON
- **Suite de testes abrangente**: Desenvolvimento de testes unitários cobrindo diversos cenários
- **Exemplos práticos**: Criação de conjunto de exemplos com complexidade crescente

## Estrutura do Código

O projeto está organizado nos seguintes módulos principais:

### `src/lexer.py` - Módulo Principal do Analisador Léxico

**Classes principais**:
- `TokenType` (Enum): Define todos os tipos de tokens suportados
- `Token` (dataclass): Representa um token com tipo, valor e posição
- `Lexer`: Implementa o analisador léxico principal
- `LexerError`: Exceção customizada para erros de análise

**Algoritmos implementados**:
- **Análise léxica por expressões regulares**: Utiliza padrões regex para identificar tokens
- **Reconhecimento com precedência**: Palavras-chave são verificadas antes de identificadores
- **Rastreamento de posição**: Mantém controle preciso de linha e coluna

### `src/main.py` - Interface de Linha de Comando

Fornece uma interface user-friendly para o lexer com:
- Análise de código direto ou arquivos
- Múltiplos formatos de saída
- Modo verboso para debug
- Tratamento de erros robusto

### `tests/test_lexer.py` - Suite de Testes Unitários

Contém testes abrangentes cobrindo:
- Reconhecimento de todos os tipos de tokens
- Tratamento de erros
- Rastreamento de posição
- Casos extremos (entrada vazia, apenas whitespace)

### Etapas de Compilação Implementadas

**Análise Léxica (Lexical Analysis)**: Completamente implementada no módulo `lexer.py`
- Tokenização de entrada
- Classificação de tokens
- Tratamento de erros léxicos
- Rastreamento de posição no código fonte

*Nota*: Este projeto foca especificamente na análise léxica. As etapas subsequentes (análise sintática, semântica, geração de código) não estão implementadas, pois o escopo é um analisador léxico puro.

## Bugs/Limitações/Problemas Conhecidos

### Limitações Atuais

1. **Escapes em strings**: O reconhecimento de caracteres de escape em strings é básico. Strings complexas com múltiplos escapes podem não ser processadas corretamente.

2. **Números em notação científica**: Não há suporte para números em notação científica (ex: 1.5e10).

3. **Comentários aninhados**: Comentários de bloco aninhados (`/* /* */ */`) não são suportados adequadamente.

4. **Unicode**: Identificadores com caracteres Unicode não são suportados, apenas ASCII.

### Melhorias Incrementais Possíveis

1. **Expandir suporte a strings**: Implementar reconhecimento completo de sequências de escape (\n, \t, \", etc.)

2. **Adicionar mais operadores**: Incluir operadores como `++`, `--`, `+=`, `-=`, etc.

3. **Melhorar tratamento de números**: Adicionar suporte a números hexadecimais, binários e notação científica

4. **Otimização de performance**: Implementar um lexer baseado em autômatos finitos para melhor performance em arquivos grandes

5. **Melhor integração**: Criar API mais robusta para integração com analisadores sintáticos

6. **Configurabilidade**: Permitir configuração dinâmica de palavras-chave e operadores

7. **Relatórios de erro mais detalhados**: Incluir sugestões de correção e contexto adicional nos erros

8. **Suporte a preprocessamento**: Adicionar capacidade básica de preprocessamento (inclusão de arquivos, macros simples)

### Problemas Conhecidos

- Em alguns casos raros, comentários de bloco muito longos podem impactar a performance
- O rastreamento de coluna pode ficar inconsistente com caracteres tab em configurações não-padrão 
