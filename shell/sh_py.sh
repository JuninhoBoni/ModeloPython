#INSERE VARIÁVEIS DE AMBIENTE
export SURCARD_ROOT=/${2}/CMS
export ORACLE_HOME=/appl/oracle/product/11.2.0/client_2/
#A VARIAVEL ABAIXO, PERMITE EXECUTARMOS PROGRAMA COBOL DENTRO DO PYTHON
export LD_LIBRARY_PATH=/opt/microfocus/cobol/lib:/usr/lib:/appl/oracle/product/11.2.0/client_2/lib:/lib:/appl/CMS/oracle/lib
export TNS_ADMIN=/appl/oracle/product/11.2.0/client_2/

#SETA VARIÁVEL CodExitPython PARA ERRO.
CodExitPython="-1"

#VERIFICA SE EXISTE O ARQUIVO PYTHON
if  [ -f "/appl/CMS/${2}/CMS/bin/py/${1}.py" ];
then #EXISTINDO, EXECUTA O COMANDO ABAIXO
    /${2}/teste/modelo/py/${1}.py ${2} ${3} ${4} ${5} ${6} ${7} ${8}
    CodExitPython="$?" #RECEBE O RETORNO DO PYTHON, MODIFICANDO
else
    #PRINTA O ERRO NA TELA E MANTÉM O exit -1
    echo "HOUVE UM ERRO NOS PARAMETROS FORNECIDOS À ESTA SHELL."
fi

#TRATATIVA DAS SAÍDAS DO EXIT DO PYTHON.
#SE NECESSÁRIO PODE INCLUIR MAIS LINHAS E ATUALIZAR ESTA SHELL
case "$CodExitPython" in
    "-1") exit -1 ;;
    "0") exit 0 ;;
    "1") exit 1 ;;
    "2") exit 2 ;;
    "3") exit 3 ;;
    "4") exit 4 ;;
    "5") exit 5 ;;
    "6") exit 6 ;;
    "7") exit 7 ;;
    "8") exit 8 ;;
    "9") exit 9 ;;
    "10") exit 10 ;;
    "11") exit 11 ;;
    "12") exit 12 ;;
esac