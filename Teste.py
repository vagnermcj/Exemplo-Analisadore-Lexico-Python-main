from ply.lex import lex
from ply.yacc import yacc

# Definindo tokens de palavras reservadas e variáveis
tokens = (
    'SOME', 'COM', 'VAR', 'NUM', 'FACA', 'SER', 'PONTO', 'MOSTRE', 
    'REPITA', 'VEZES', 'DOIS_PONTOS', 'FIM', 'SE', 'ENTAO', 'SENAO', 
    'MULTIPLIQUE', 'POR'
)

# Definindo expressões regulares para os tokens
t_SOME = r'(?i)some'
t_COM = r'(?i)com'
t_FACA = r'(?i)faca'
t_SER = r'(?i)ser'
t_PONTO = r'\.'
t_MOSTRE = r'(?i)mostre'
t_REPITA = r'(?i)repita'
t_VEZES = r'(?i)vezes'
t_DOIS_PONTOS = r':'
t_FIM = r'(?i)fim'
t_SE = r'(?i)se'
t_ENTAO = r'(?i)entao'
t_SENAO = r'(?i)senao'
t_MULTIPLIQUE = r'(?i)multiplique'
t_POR = r'(?i)por'

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.lower() in ('some', 'com', 'faca', 'ser', 'mostre', 'repita', 'vezes', 'fim', 'se', 'entao', 'senao', 'multiplique', 'por'):
        t.type = t.value.upper()
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignora espaços e novas linhas
t_ignore = ' \t\n'

# Tratamento de erros léxicos
def t_error(t):
    print("Caractere ilegal: ", t.value[0])
    t.lexer.skip(1)

# Inicializando o lexer
lexer = lex()

# Definindo a regra para o programa
def p_programa(p):
    '''programa : cmds'''
    p[0] = ('programa', p[1])

# Definindo a regra para lista de comandos
def p_cmds(p):
    '''cmds : cmd cmds
            | cmd'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

# Definindo a regra para um comando
def p_cmd(p):
    '''cmd : operacao
           | atribuicao
           | impressao
           | repeticao
           | condicional'''
    p[0] = p[1]

# Definindo a regra para atribuição
def p_atribuicao(p):
    '''atribuicao : FACA VAR SER NUM PONTO'''
    p[0] = f"{p[2]} = {p[4]}"

# Definindo a regra para operação de soma
def p_operacao(p):
    '''operacao : SOME VAR COM VAR PONTO
                | SOME VAR COM NUM PONTO
                | SOME NUM COM NUM PONTO'''
    p[0] = f"{p[2]} += {p[4]}"

# Definindo a regra para operação de multiplicação
def p_operacao_mult(p):
    '''operacao : MULTIPLIQUE VAR POR VAR PONTO
                | MULTIPLIQUE VAR POR NUM PONTO
                | MULTIPLIQUE NUM POR NUM PONTO'''
    p[0] = f"{p[2]} *= {p[4]}"

# Definindo a regra para impressão
def p_impressao(p):
    '''impressao : MOSTRE VAR PONTO
                 | MOSTRE NUM PONTO'''
    p[0] = f"print({p[2]})"

# Definindo a regra para repetição
def p_repeticao(p):
    '''repeticao : REPITA NUM VEZES DOIS_PONTOS cmds FIM'''
    p[0] = f"for _ in range({p[2]}):\n    " + "\n    ".join(p[5])



def p_condicional(p):
    '''condicional : SE VAR ENTAO cmds FIM
                   | SE VAR ENTAO cmds SENAO cmds FIM'''
    if len(p) == 6:
        # Bloco apenas com SE e ENTAO
        p[0] = f"if {p[2]} != 0:\n    " + "\n    ".join(p[4])
    else:
        # Bloco com SE, ENTAO e SENAO
        p[0] = f"if {p[2]} != 0:\n    " + "\n    ".join(p[4]) + "\nelse:\n    " + "\n    ".join(p[6])


# Tratamento de erros sintáticos
def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo a {p.value}")
    else:
        print("Erro de sintaxe no final da entrada")

# Inicializando o parser
parser = yacc()

# Teste de entrada com o comando REPITA
entrada1 = '''
FACA x SER 10.
MOSTRE x.
'''

entrada2 = '''
FACA a SER 3.
FACA b SER 7.
SOME a COM b.
MOSTRE a.
'''

entrada3 = '''
FACA total SER 0.
REPITA 5 VEZES : 
SOME total COM 2.
FIM
MOSTRE total.
'''

entrada4 = '''
FACA n SER 4.
SE n ENTAO
MOSTRE n.
FIM
'''

entrada5 = '''
FACA num SER 0.
SE num ENTAO
MOSTRE num.
SENAO
MOSTRE 10.
FIM
'''

entrada6 = '''
FACA x SER 3.
FACA y SER 5.
MULTIPLIQUE x POR y.
MOSTRE x.
'''

entrada7 = '''
FACA resultado SER 1.
REPITA 3 VEZES :
MULTIPLIQUE resultado POR 2.
FIM
MOSTRE resultado.
'''
entrada8 = '''
some 1 com 2.
'''

resultado = parser.parse(entrada8)
print(resultado)
