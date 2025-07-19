"""
Analisador Léxico - Arquivo principal
"""

import sys
import argparse
from pathlib import Path
from src.lexer import Lexer, LexerError, analyze_code


def main():
    """Função principal do programa"""
    parser = argparse.ArgumentParser(
        description='Analisador Léxico para uma linguagem simples',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos de uso:
  python -m src.main "int x = 10 + 5;"
  python -m src.main arquivo.txt
  python -m src.main --verbose "int x = 10;"
        '''
    )
    
    parser.add_argument(
        'input',
        help='Código para analisar ou arquivo contendo o código'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostra tokens de whitespace e comentários'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Arquivo de saída (padrão: stdout)'
    )
    
    parser.add_argument(
        '--format',
        choices=['simple', 'detailed', 'json'],
        default='simple',
        help='Formato de saída dos tokens'
    )
    
    args = parser.parse_args()
    
    # Determina se o input é um arquivo ou código direto
    input_path = Path(args.input)
    if input_path.exists() and input_path.is_file():
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                code = f.read()
            print(f"Analisando arquivo: {input_path}")
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        code = args.input
        print("Analisando código fornecido:")
    
    print(f"Código: {repr(code)}")
    print("-" * 50)
    
    try:
        # Analisa o código
        lexer = Lexer(code)
        tokens = lexer.tokenize(skip_whitespace=not args.verbose, skip_comments=not args.verbose)
        
        # Prepara a saída
        output_lines = []
        
        if args.format == 'simple':
            output_lines.append("Tokens:")
            for token in tokens:
                if token.type.value != 'EOF':
                    output_lines.append(f"  {token}")
        
        elif args.format == 'detailed':
            output_lines.append("Análise detalhada:")
            output_lines.append(f"{'Tipo':<20} {'Valor':<15} {'Linha':<6} {'Coluna':<6}")
            output_lines.append("-" * 50)
            for token in tokens:
                if token.type.value != 'EOF':
                    output_lines.append(
                        f"{token.type.value:<20} {repr(token.value):<15} "
                        f"{token.line:<6} {token.column:<6}"
                    )
        
        elif args.format == 'json':
            import json
            token_data = []
            for token in tokens:
                if token.type.value != 'EOF':
                    token_data.append({
                        'type': token.type.value,
                        'value': token.value,
                        'line': token.line,
                        'column': token.column
                    })
            output_lines.append(json.dumps(token_data, indent=2, ensure_ascii=False))
        
        # Mostra estatísticas
        non_eof_tokens = [t for t in tokens if t.type.value != 'EOF']
        output_lines.append(f"\nEstatísticas:")
        output_lines.append(f"  Total de tokens: {len(non_eof_tokens)}")
        output_lines.append(f"  Linhas processadas: {max(t.line for t in tokens) if tokens else 0}")
        
        # Saída
        result = '\n'.join(output_lines)
        
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"Resultado salvo em: {args.output}")
            except Exception as e:
                print(f"Erro ao salvar arquivo: {e}", file=sys.stderr)
                print(result)
        else:
            print(result)
    
    except LexerError as e:
        print(f"Erro de análise léxica: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
