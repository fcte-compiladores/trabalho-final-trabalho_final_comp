import unittest
import sys
import os

# Adiciona o diretório pai ao path para importar o módulo src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import Lexer, LexerError, TokenType, Token


class TestLexer(unittest.TestCase):
    """Testes unitários para o analisador léxico"""
    
    def setUp(self):
        """Configuração executada antes de cada teste"""
        pass
    
    def test_simple_assignment(self):
        """Testa uma atribuição simples: int x = 10 + 5;"""
        code = "int x = 10 + 5;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.INT,
            TokenType.IDENTIFIER,
            TokenType.ASSIGN,
            TokenType.NUMBER,
            TokenType.PLUS,
            TokenType.NUMBER,
            TokenType.SEMICOLON,
            TokenType.EOF
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_numbers(self):
        """Testa reconhecimento de números inteiros e decimais"""
        code = "123 45.67 0 0.0"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        number_tokens = [t for t in tokens if t.type == TokenType.NUMBER]
        self.assertEqual(len(number_tokens), 4)
        self.assertEqual(number_tokens[0].value, "123")
        self.assertEqual(number_tokens[1].value, "45.67")
        self.assertEqual(number_tokens[2].value, "0")
        self.assertEqual(number_tokens[3].value, "0.0")
    
    def test_identifiers(self):
        """Testa reconhecimento de identificadores"""
        code = "variavel _privada var123 CamelCase"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        identifier_tokens = [t for t in tokens if t.type == TokenType.IDENTIFIER]
        self.assertEqual(len(identifier_tokens), 4)
        self.assertEqual(identifier_tokens[0].value, "variavel")
        self.assertEqual(identifier_tokens[1].value, "_privada")
        self.assertEqual(identifier_tokens[2].value, "var123")
        self.assertEqual(identifier_tokens[3].value, "CamelCase")
    
    def test_keywords(self):
        """Testa reconhecimento de palavras-chave"""
        code = "int float string bool if else while for function return"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.BOOL,
            TokenType.IF, TokenType.ELSE, TokenType.WHILE, TokenType.FOR,
            TokenType.FUNCTION, TokenType.RETURN, TokenType.EOF
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_operators(self):
        """Testa reconhecimento de operadores"""
        code = "+ - * / % = == != < > <= >="
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE,
            TokenType.MODULO, TokenType.ASSIGN, TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.LESS_THAN, TokenType.GREATER_THAN, TokenType.LESS_EQUAL,
            TokenType.GREATER_EQUAL, TokenType.EOF
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_delimiters(self):
        """Testa reconhecimento de delimitadores"""
        code = "( ) { } [ ] ; ,"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN,
            TokenType.LEFT_BRACE, TokenType.RIGHT_BRACE,
            TokenType.LEFT_BRACKET, TokenType.RIGHT_BRACKET,
            TokenType.SEMICOLON, TokenType.COMMA, TokenType.EOF
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_strings(self):
        """Testa reconhecimento de strings"""
        code = '"hello world" "string com \\"aspas\\"" \'single quotes\''
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        string_tokens = [t for t in tokens if t.type == TokenType.STRING_LITERAL]
        self.assertEqual(len(string_tokens), 3)
        self.assertEqual(string_tokens[0].value, '"hello world"')
        self.assertEqual(string_tokens[1].value, '"string com \\"aspas\\""')
        self.assertEqual(string_tokens[2].value, "'single quotes'")
    
    def test_boolean_literals(self):
        """Testa reconhecimento de literais booleanos"""
        code = "true false"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        bool_tokens = [t for t in tokens if t.type == TokenType.BOOLEAN_LITERAL]
        self.assertEqual(len(bool_tokens), 2)
        self.assertEqual(bool_tokens[0].value, "true")
        self.assertEqual(bool_tokens[1].value, "false")
    
    def test_comments(self):
        """Testa reconhecimento de comentários"""
        code = """
        // Comentário de linha
        int x = 5; // Comentário no final da linha
        /* Comentário
           de múltiplas
           linhas */
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize(skip_comments=False, skip_whitespace=False)
        
        comment_tokens = [t for t in tokens if t.type == TokenType.COMMENT]
        self.assertEqual(len(comment_tokens), 3)
    
    def test_line_and_column_tracking(self):
        """Testa rastreamento de linha e coluna"""
        code = "int x\n= 10;"
        lexer = Lexer(code)
        tokens = lexer.tokenize(skip_whitespace=False)
        
        # Verifica posições específicas
        int_token = tokens[0]  # "int"
        self.assertEqual(int_token.line, 1)
        self.assertEqual(int_token.column, 1)
        
        assign_token = next(t for t in tokens if t.type == TokenType.ASSIGN)
        self.assertEqual(assign_token.line, 2)
        self.assertEqual(assign_token.column, 1)
    
    def test_complex_expression(self):
        """Testa uma expressão mais complexa"""
        code = """
        function fibonacci(int n) {
            if (n <= 1) {
                return n;
            } else {
                return fibonacci(n - 1) + fibonacci(n - 2);
            }
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Verifica que não há erros e que temos tokens suficientes
        self.assertGreater(len(tokens), 20)
        
        # Verifica alguns tokens específicos
        function_tokens = [t for t in tokens if t.type == TokenType.FUNCTION]
        self.assertEqual(len(function_tokens), 1)
        
        if_tokens = [t for t in tokens if t.type == TokenType.IF]
        self.assertEqual(len(if_tokens), 1)
        
        return_tokens = [t for t in tokens if t.type == TokenType.RETURN]
        self.assertEqual(len(return_tokens), 2)  # Corrigido de 3 para 2
    
    def test_invalid_character(self):
        """Testa tratamento de caracteres inválidos"""
        code = "int x = @;"  # @ não é um caractere válido
        lexer = Lexer(code)
        
        with self.assertRaises(LexerError) as context:
            lexer.tokenize()
        
        self.assertIn("Caractere inesperado", str(context.exception))
    
    def test_empty_input(self):
        """Testa entrada vazia"""
        code = ""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        self.assertEqual(len(tokens), 1)  # Apenas EOF
        self.assertEqual(tokens[0].type, TokenType.EOF)
    
    def test_whitespace_only(self):
        """Testa entrada apenas com whitespace"""
        code = "   \t\n  "
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Espera apenas NEWLINE e EOF quando skip_whitespace=True
        self.assertEqual(len(tokens), 2)  # NEWLINE e EOF
        self.assertEqual(tokens[0].type, TokenType.NEWLINE)
        self.assertEqual(tokens[1].type, TokenType.EOF)
    
    def test_token_string_representation(self):
        """Testa representação em string dos tokens"""
        code = "int x = 10;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        token_strings = lexer.get_tokens_as_strings()
        expected = ["INT", "IDENTIFIER(x)", "ASSIGN", "NUMBER(10)", "SEMICOLON"]
        self.assertEqual(token_strings, expected)


class TestTokenType(unittest.TestCase):
    """Testes para a enumeração TokenType"""
    
    def test_token_type_values(self):
        """Testa os valores da enumeração TokenType"""
        self.assertEqual(TokenType.INT.value, "INT")
        self.assertEqual(TokenType.IDENTIFIER.value, "IDENTIFIER")
        self.assertEqual(TokenType.ASSIGN.value, "ASSIGN")


class TestToken(unittest.TestCase):
    """Testes para a classe Token"""
    
    def test_token_creation(self):
        """Testa criação de tokens"""
        token = Token(TokenType.IDENTIFIER, "variavel", 1, 5)
        self.assertEqual(token.type, TokenType.IDENTIFIER)
        self.assertEqual(token.value, "variavel")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.column, 5)
    
    def test_token_string_with_value(self):
        """Testa string representation com valor"""
        token = Token(TokenType.IDENTIFIER, "test", 1, 1)
        self.assertEqual(str(token), "IDENTIFIER(test)")
    
    def test_token_string_without_value(self):
        """Testa string representation sem valor"""
        token = Token(TokenType.SEMICOLON, ";", 1, 1)
        self.assertEqual(str(token), "SEMICOLON")


if __name__ == '__main__':
    # Executa os testes
    unittest.main(verbosity=2)
