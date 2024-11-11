from ply.lex import lex
from ply.yacc import yacc

reservados = ("FACA", "SER", "DOISPONTO", "PONTO", "MOSTRE", "SOME", "MULTIPLIQUE", 
              "COM", "REPITA", "VEZES","FIM")

t_FACA = r'FACA'
t_SER = r'SER'
t_PONTO = r'\.'
t_DOISPONTO = r':'
t_MOSTRE = r'MOSTRE'
t_SOME = r'SOME'
t_MULTIPLIQUE = r'MULTIPLIQUE'
t_COM = r'COM'
t_REPITA = r'REPITA'
t_VEZES = r'VEZES'
t_FIM = r'FIM'
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
    regras[0] = "#include <stdio.h>\nint main(void){\n\t" + regras[1] + "\n\treturn 0;\n}"


def p_cmds(regras):
    '''
    cmds : cmd cmds
        | cmd
    '''
    if len(regras) == 3:
        regras[0] = regras[1] + "\n\t" + regras[2]
    else:
        regras[0] = regras[1]


def p_cmd(regras):
    '''
    cmd : atribuicao
        | impressao
        | operacao
        | repeticao
    '''
    regras[0] = regras[1]

def p_repeticao(regras):
    '''
    repeticao : REPITA num VEZES DOISPONTO cmds FIM
    '''
    regras[0] = "for(int i = 0; i < " + str(regras[2]) + "; i++){\n\t" + regras[5] + "\n\t}"


def p_atribuicao(regras):
    '''
    atribuicao : FACA var SER num PONTO
    '''
    regras[0] = f"int {regras[2]} = {regras[4]};"

def p_operacao(regras):
    '''
    operacao : SOME var COM var PONTO
        | SOME var COM num PONTO
        | SOME num COM num PONTO
        | MULTIPLIQUE var COM var PONTO
        | MULTIPLIQUE var COM num PONTO
        | MULTIPLIQUE num COM num PONTO
    '''
    if regras[1] == 'SOME':
        regras[0] = f"{regras[2]} += {regras[4]};"
    elif regras[1] == 'MULTIPLIQUE':
        regras[0] = f"{regras[2]} *= {regras[4]};"


def p_impressao(regras):
    '''
    impressao : MOSTRE var PONTO
        | MOSTRE operacao PONTO
    '''
    regras[0] = f'printf("%d", {regras[2]});'

def p_error(regras):
    print("Erro de sintaxe"+ str(regras))

parser = yacc(debug=True) # construção do parser

parseado = parser.parse("FACA b SER 1. FACA a SER 0. REPITA 3 VEZES: SOME a COM b. FIM MOSTRE a.") # execução do parser
print(parseado)