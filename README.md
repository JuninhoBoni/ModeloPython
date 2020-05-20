#MODELO DE CONEXÃO A BASE ORACLE

O objetivo deste programa é realizar conexão a base ORACLE e exportar os dados para formatos CSV e TXT.

Este programa recebe duas variáveis externas sendo a primeira variável responável por identificar qual usuário do banco será utiizado e a segunda espera receber qual etapa do programa será executada:

Parâmetro 1 aceita os valores:
xpto01
xpto02

Parâmetro 2 aceita os valores:
2 Para executar a etapa FILA_
3 Para executar a etapa PAGTO_SUSPENSO_XPTO_
4 Para executar a etapa FILA_ESTADO_200_
5 Para executar a etapa FILA_ESTADO_201_
6 Para executar a etapa FILA_ESTADO_202_
7 Para executar a etapa PAGTO_SUSPENSO_XPTO_APOS_MASSIVO_
8 Para executar a etapa UPDATE_ESTADO_4_REMS_
all - SERÁ EXECUTADA TODAS AS ETAPAS

Programa principal: modelo_python.py

Exemplos de execução:
python2 modelo_python.py xpto01 1
python3 modelo_python.py xpto01 2
modelo_python.py  xpto01 3

Pode realizar a execução com informando o caminho completo exemplo:
/XPTO01/teste/modelo/py/modelo_python.py xpto01 4

Se o ambiente de execução não tiver variáveis de ambiente declaradas, será necessário uma SHELL para executar. Há um modelo de shell neste repositório. Exemplo de execução:

/XPTO02/teste/modelo/shell/sh_py.sh modelo_python xpto01 all

Se o seu ambiente executa programas COBOL, com esta shell é possível executar os programas COBOL dentro do python.
A shel está preparada para receber o códigos de exit do programa python, caso esteja utilizando um gerenciador de JOBS e seu programa apresentar algum exit, esta informação será repassada para o JOB.