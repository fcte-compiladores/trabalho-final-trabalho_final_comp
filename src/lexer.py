import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Iterator


class TokenType(Enum):
    """Tipos de tokens suportados pelo analisador léxico"""
    # Tipos de dados
    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOL = "BOOL"
    
    # Identificadores e literais
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING_LITERAL = "STRING_LITERAL"
    BOOLEAN_LITERAL = "BOOLEAN_LITERAL"
    
    # Operadores aritméticos
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    
    # Operadores de comparação
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    
    # Operadores de atribuição
    ASSIGN = "ASSIGN"
    
    # Operadores lógicos
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    
    # Palavras-chave de controle
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    FUNCTION = "FUNCTION"
    RETURN = "RETURN"
    
    # Delimitadores
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    LEFT_BRACKET = "LEFT_BRACKET"
    RIGHT_BRACKET = "RIGHT_BRACKET"
    
    # Especiais
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"


@dataclass
class Token:
    """Representa um token identificado pelo lexer"""
    type: TokenType
    value: str
    line: int
    column: int
    
    def __str__(self):
        if self.value and self.type in [TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.STRING_LITERAL, TokenType.BOOLEAN_LITERAL]:
            return f"{self.type.value}({self.value})"
        return self.type.value


class LexerError(Exception):
    """Exceção para erros do analisador léxico"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Erro léxico na linha {line}, coluna {column}: {message}")


class Lexer:
    """Analisador léxico para uma linguagem simples"""
    
    # Palavras-chave da linguagem
    KEYWORDS = {
        'int': TokenType.INT,
        'float': TokenType.FLOAT,
        'string': TokenType.STRING,
        'bool': TokenType.BOOL,
        'true': TokenType.BOOLEAN_LITERAL,
        'false': TokenType.BOOLEAN_LITERAL,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'function': TokenType.FUNCTION,
        'return': TokenType.RETURN,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }
    
    # Padrões de expressões regulares para diferentes tipos de tokens
    TOKEN_PATTERNS = [
        # Comentários (devem vir antes de operadores)
        (r'//.*', TokenType.COMMENT),
        (r'/\*[\s\S]*?\*/', TokenType.COMMENT),
        
        # Strings
        (r'"([^"\\]|\\.)*"', TokenType.STRING_LITERAL),
        (r"'([^'\\]|\\.)*'", TokenType.STRING_LITERAL),
        
        # Números (decimais e inteiros)
        (r'\d+\.\d+', TokenType.NUMBER),
        (r'\d+', TokenType.NUMBER),
        
        # Operadores de comparação (devem vir antes dos operadores simples)
        (r'==', TokenType.EQUAL),
        (r'!=', TokenType.NOT_EQUAL),
        (r'<=', TokenType.LESS_EQUAL),
        (r'>=', TokenType.GREATER_EQUAL),
        (r'<', TokenType.LESS_THAN),
        (r'>', TokenType.GREATER_THAN),
        
        # Operadores aritméticos e de atribuição
        (r'=', TokenType.ASSIGN),
        (r'\+', TokenType.PLUS),
        (r'-', TokenType.MINUS),
        (r'\*', TokenType.MULTIPLY),
        (r'/', TokenType.DIVIDE),
        (r'%', TokenType.MODULO),
        
        # Delimitadores
        (r';', TokenType.SEMICOLON),
        (r',', TokenType.COMMA),
        (r'\(', TokenType.LEFT_PAREN),
        (r'\)', TokenType.RIGHT_PAREN),
        (r'\{', TokenType.LEFT_BRACE),
        (r'\}', TokenType.RIGHT_BRACE),
        (r'\[', TokenType.LEFT_BRACKET),
        (r'\]', TokenType.RIGHT_BRACKET),
        
        # Identificadores (devem vir após as palavras-chave)
        (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
        
        # Whitespace
        (r'[ \t]+', TokenType.WHITESPACE),
        (r'\n', TokenType.NEWLINE),
    ]
    
    def __init__(self, text: str):
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def tokenize(self, skip_whitespace: bool = True, skip_comments: bool = True) -> List[Token]:
        """
        Analisa o texto e retorna uma lista de tokens
        
        Args:
            skip_whitespace: Se True, remove tokens de whitespace da saída
            skip_comments: Se True, remove tokens de comentário da saída
        """
        self.tokens = []
        self.position = 0
        self.line = 1
        self.column = 1
        
        while self.position < len(self.text):
            match_found = False
            
            for pattern, token_type in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.text, self.position)
                
                if match:
                    value = match.group(0)
                    
                    # Verifica se é uma palavra-chave
                    if token_type == TokenType.IDENTIFIER and value in self.KEYWORDS:
                        token_type = self.KEYWORDS[value]
                    
                    token = Token(token_type, value, self.line, self.column)
                    
                    # Adiciona o token apenas se não for para pular
                    if not (skip_whitespace and token_type == TokenType.WHITESPACE) and \
                       not (skip_comments and token_type == TokenType.COMMENT):
                        self.tokens.append(token)
                    
                    # Atualiza posição
                    self.position = match.end()
                    
                    # Atualiza linha e coluna
                    if token_type == TokenType.NEWLINE:
                        self.line += 1
                        self.column = 1
                    else:
                        self.column += len(value)
                    
                    match_found = True
                    break
            
            if not match_found:
                char = self.text[self.position]
                raise LexerError(f"Caractere inesperado: '{char}'", self.line, self.column)
        
        # Adiciona token EOF no final
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def get_tokens_as_strings(self) -> List[str]:
        """Retorna os tokens como uma lista de strings para compatibilidade com o exemplo"""
        return [str(token) for token in self.tokens if token.type != TokenType.EOF]


def analyze_code(code: str, verbose: bool = False) -> List[Token]:
    """
    Função utilitária para analisar código e retornar tokens
    
    Args:
        code: O código fonte para analisar
        verbose: Se True, inclui whitespace e comentários
    """
    lexer = Lexer(code)
    return lexer.tokenize(skip_whitespace=not verbose, skip_comments=not verbose)


if __name__ == "__main__":
    # Exemplo de uso
    test_code = "int x = 10 + 5;"
    
    try:
        lexer = Lexer(test_code)
        tokens = lexer.tokenize()
        
        print("Código analisado:")
        print(f"'{test_code}'")
        print("\nTokens identificados:")
        for token in tokens:
            if token.type != TokenType.EOF:
                print(f"  {token}")
        
        print(f"\nSaída compatível com o exemplo:")
        print(lexer.get_tokens_as_strings())
        
    except LexerError as e:
        print(f"Erro: {e}")
