from ply.lex import lex
from ply.yacc import yacc

reservados = ("FACA", "SER", "PONTO")

t_FACA = r'FACA'
t_SER = r'SER'
t_PONTO = r'.'
t_ignore = ' \t\n' # ignora espaços e tabs



def t_num(t): 
    r'\d+'
    t.value = int(t.value)
    return t

def t_var(t):
    r'[a-zA-Z][a-zA-Z]*'
    if t.value in reservados: # igual
        t.type = t.value
    return t

def t_error(t): # nos dizer qual caractere ilegal e se tem erro
    print("Caracter ilegal: ", t.value[0])
    t.lexer.skip(1)

tokens = reservados + ('num', 'var')

lexer = lex(debug=True) # construção do lexer

def p_programa(regras):
    '''
    programa : cmds
    '''
    regras[0] = "#include <stdio.h>\nint main(void){\n" + regras[1] + "\nreturn 0;\n}"


def p_cmds(regras):
    '''
    cmds : cmd cmds
        | cmd
    '''
    if len(regras) == 3:
        regras[0] = regras[1] + "\n" + regras[2]
    else:
        regras[0] = regras[1]


def p_cmd(regras):
    '''
    cmd : atribuicao
    '''
    regras[0] = regras[1]

def p_atribuicao(regras):
    '''
    atribuicao : FACA var SER num PONTO
    '''
    regras[0] = f"int {regras[2]} = {regras[4]};"


def p_error(regras):
    print("Erro de sintaxe"+ str(regras))

parser = yacc(debug=True) # construção do parser

parseado = parser.parse("FACA b SER 3.") # execução do parser
print(parseado)