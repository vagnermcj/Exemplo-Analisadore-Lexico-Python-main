from ply.lex import lex
from ply.yacc import yacc

reservados = ("FACA", "SER", "DOISPONTO", "PONTO", "MOSTRE", "SOME", "MULTIPLIQUE", 
              "COM", "REPITA", "VEZES","FIM", "SE", "ENTAO", "SENAO", "POR")

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
t_SE = r'SE'
t_ENTAO = r'ENTAO'
t_SENAO = r'SENAO'
t_POR = r'POR'
t_ignore = ' \t\n' # ignora espaços e tabs

tokens = reservados + ("num", "var")
variaveis = []

def t_var(t):
    r'[a-zA-Z][a-zA-Z]*'
    if t.value in reservados: # igual
        t.type = t.value
    return t

def t_num(t): 
    r'\d+'
    t.value = int(t.value)
    return t



def t_error(t): # nos dizer qual caractere ilegal e se tem erro
    print("Caracter ilegal: ", t.value[0])
    t.lexer.skip(1)


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
        | operacao_soma
        | operacao_mult
        | repeticao
        | condicao
    '''
    regras[0] = regras[1]


def p_atribuicao(regras):
    '''
    atribuicao : FACA var SER num PONTO
        | FACA var SER var PONTO
    '''
    if(regras[2] in variaveis):
        regras[0] = f"{regras[2]} = {regras[4]};"
    else:
        variaveis.append(regras[2])
        regras[0] = f"int {regras[2]} = {regras[4]};"


def p_condicao(regras):
    '''
    condicao :  SE var ENTAO cmds SENAO cmds FIM 
        | SE var ENTAO cmds FIM
    '''

    if(regras[5] == "SENAO"):
        regras[0] = "if(" + regras[2] + "){\n\t" + regras[4] + "\n\t} else {\n\t" + regras[6] + "\n}\n"
    else:
        regras[0] = "if(" + regras[2] + "){\n\t" + regras[4] + "\n\t}"
      


def p_repeticao(regras):
    '''
    repeticao : REPITA num VEZES DOISPONTO cmds FIM
    '''
    regras[0] = "for(int i = 0; i < " + str(regras[2]) + "; i++){\n\t" + regras[5] + "\n\t}"




def p_operacao_soma(regras):
    '''
    operacao_soma : SOME var COM var PONTO
        | SOME var COM num PONTO
        | SOME num COM num PONTO
    '''
    if isinstance(regras[2], int):
        regras[0] = f"{regras[2]} + {regras[4]}"
    else:
        regras[0] = f"{regras[2]} += {regras[4]};"



def p_operacao_mult(regras):
    '''
    operacao_mult : MULTIPLIQUE var POR var PONTO
        | MULTIPLIQUE var POR num PONTO
        | MULTIPLIQUE num POR num PONTO
    '''

    if isinstance(regras[2], int):
        regras[0] == f"{regras[2]} * {regras[4]}"
    else:
        regras[0] = f"{regras[2]} *= {regras[4]};"

def p_impressao(regras):
    '''
    impressao : MOSTRE var PONTO
        | MOSTRE operacao_soma PONTO
        | MOSTRE operacao_mult PONTO
        | MOSTRE num PONTO
    '''
    regras[0] = f'printf("%d", {regras[2]});'

def p_error(regras):
    print("Erro de sintaxe"+ str(regras))


def escrever_arquivo_c(nome_arquivo, conteudo):
    if not nome_arquivo.endswith('.c'):
        nome_arquivo += '.c'
    
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(conteudo)

def ler_arquivo_matemagica(nome_arquivo):    
    with open(nome_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
  
    return conteudo

parser = yacc(debug=True) # construção do parser

matemagica = ler_arquivo_matemagica("./TestesMatemagica/test_case_9.txt")
parseado = parser.parse(matemagica) # execução do parser
escrever_arquivo_c("Teste.c", parseado)
