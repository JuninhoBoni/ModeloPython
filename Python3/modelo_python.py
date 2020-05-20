#!/usr/bin/env python3
# coding: utf-8
'''
ESTE PROGRAMA CONTÉM COMENTÁRIOS EM SEU CORPO PARA FACILITAR O ENTENDIMENTO.

NOME DO PROGRAMA:   modelo_python.py
VERSÃO:             1.0
OBJETIVO:           ATENDER DEMANDA SOLICITADA PELA XPTO
DESCRIÇÃO:          EXECUTAR QUERY ATRAVÉS DE PARÂMETROS RECEBIDOS EXTERNAMENTE
LIBS:               connOracle (V1.0), logAdd (V1.0), sendMail (V1.0)
HISTÓRICO:          V1.0 - 18/05/2020   DANIEL ALVES DIAS JUNIOR
                                        - INSERIDO EM PRODUÇÃO.

'''
#IMPORTAR BIBLIOTECAS QUE SERÃO UTEIS NO PROJETO.
import sys, os, csv, time

#DEFINE O DIRETÓRIO QUE ARQUIVO PYTHON ESTÁ ARMAZENADO.
diretorioPython = os.path.dirname(os.path.realpath(__file__))

#ADICIONAR PASTAS EXTERNAS.
sys.path.append('{}/lib'.format(diretorioPython))
sys.path.append('{}/files'.format(diretorioPython))

#IMPORTAR ARQUIVOS QUE ESTÃO NAS PASTAS ACIMA IMPORTADAS.
import connOracle, logAdd, sendMail, query_modelo_python

''' -----------   INICIO DAS FUNÇÕES   ----------- '''

def variaveisExternas():
    #INICIA GERAÇÃO DE LOGS.   
    log.adicionar('---------       INICIO DO PROGRAMA        ---------')
    
    #DEFINE E DIRETÓRIOS PARA ARQUIVO(S) DE SAIDA
    diretorioSaida = '/XPTO/'

    #VERIFICA SE HÁ O DIRETÓRIO DE SAIDA, CASO NÃO EXISTA CRIA.
    try:
        if not (os.path.isdir(diretorioSaida)):
            os.makedirs(diretorioSaida)
    except:
        exitPrograma(2)

    #RECEBE ARGUMENTOS DA SHELL, DEFINE USUÁRIOS E BASE DE DADOS QUE SERÁ UTILIZADO. SE HOUVER ERRO O PROGRAMA FINALIZA.
    try:
        if producao:
            base = 'prod01'
        else:
            base = 'hom01'
            #base = 'hom02'
            #base = 'hom03'
            #base = 'hom04'
            #base = 'hom05'

        if sys.argv[1].count('xpto01') > 0:
            emissorAdquirente = 'XPTO01'
            if producao:
                user = 'prod01'
            else:
                user = 'homxpto01'
        elif sys.argv[1].count('xpto02') > 0:
            emissorAdquirente = 'XPTO02'
            if producao:
                user = 'prod02'
            else:
                user = 'homxpto02'
        else:
            exitPrograma(1)
    except:
        exitPrograma(1)

    #RECEBE ARGUMENTOS EXTRAS DA SHELL, ESTE ARGUMENTO INDICA A ETAPA QUE SERÁ EXECUTADO O PROGRAMA. SE HOUVER ERRO O PROGRAMA FINALIZA.
    try:
        etapa = sys.argv[2]
    except:
        exitPrograma(4)

    #INICIA CONEXÃO AO BANCO DE DADOS
    try:
        banco = connOracle.BancoDados(producao, user, base)
    except:
        #HAVENDO ERRO AO CONECTAR AO BANCO O PROGRAMA FINALIZA.
        exitPrograma(3)
    
    log.adicionar('''AS VARIÁVEIS USADAS FORAM: 
                    sys.argv[0] = '{}',
                    etapa = {}, 
                    producao = {}, 
                    diretorioSaida = {}''' .format(sys.argv[0], etapa, producao, diretorioSaida))
    
    return banco, etapa, diretorioSaida

def exitPrograma(sysExit):
    mensagem = []
    if sysExit == 0:
        mensagem.append('--------- PROGRAMA FINALIZADO COM SUCESSO ---------\n')
     
    elif sysExit == 1:
        mensagem.append('VARIAVEL EXTERNA NÃO INFORMADA, GENTILEZA VERIFICAR CHAMADA DA SHELL.')
        mensagem.append('---------  PROGRAMA FINALIZADO COM ERRO   ---------\n')
    
    elif sysExit == 2:
        mensagem.append('IMPOSSIVEL CRIAR DIRETÓRIO DE SAÍDA.')
        mensagem.append('---------  PROGRAMA FINALIZADO COM ERRO   ---------\n')
   
    elif sysExit == 3:
        mensagem.append('ERRO DE CONEXAO COM O BANCO')
        mensagem.append('---------  PROGRAMA FINALIZADO COM ERRO   ---------\n')

    elif sysExit == 4:
        #SE O RETORNO ACIMA TIVER ERRO, MOSTRA NA TELA AS INFORMAÇÕES ABAIXO E FINALIZA O PROGRAMA:
        mensagem.append('----------------------------------------------------------------------------------------------------')
        mensagem.append('ESTE PROGRAMA EXIGE A INSERÇÃO DE PARÂMETROS.')
        mensagem.append('O PRIMEIRO PARÂMETRO INSERIDO, INDICA QUAL ETAPA DO PROCESSO SERÁ EXECUTADA, SENDO:')
        mensagem.append('2 - FILA_')
        mensagem.append('3 - PAGTO_SUSPENSO_XPTO_')
        mensagem.append('4 - FILA_ESTADO_200_')
        mensagem.append('5 - FILA_ESTADO_201_')
        mensagem.append('6 - FILA_ESTADO_202_')
        mensagem.append('7 - PAGTO_SUSPENSO_XPTO_APOS_MASSIVO_')
        mensagem.append('8 - UPDATE_ESTADO_4_REMS_')
        mensagem.append('all - SERÁ EXECUTADA TODAS AS ETAPAS')
        mensagem.append('----------------------------------------------------------------------------------------------------')
        mensagem.append('---------  PROGRAMA FINALIZADO COM ERRO   ---------\n')

    elif sysExit == 5:
        mensagem.append('IMPOSSIVEL CRIAR DIRETÓRIO DE LOG.')
        mensagem.append('---------  PROGRAMA FINALIZADO COM ERRO   ---------\n')

    elif sysExit == 7:
        mensagem.append('FOI INFORMADO A VARIÁVEL etapa = {}, PORÉM ESTA ETAPA NÃO EXISTE NESTE PROGRAMA.' .format(etapa))
        mensagem.append('---------  PROGRAMA FINALIZADO COM ERRO   ---------\n')

    for msg in mensagem:
        log.adicionar(msg)
    
    sys.exit(sysExit)

def queryXPTO(acao, txt, nome, query_principal):
    #RECEBE A AÇÃO, O TIPO DE ARQUIVO A SER GERADO, NOME DO ARQUIVO E A QUERY
    hoje = time.strftime('%Y%m%d_%H%M')
    arquivoSaida = '{}{}'.format(nome, hoje) 
    log.adicionar('GERANDO ARQUIVO: {}'.format(arquivoSaida))
    
    if txt:
        arqSaida = open('{}{}.txt'.format(diretorioLogs, arquivoSaida), 'a+')
        csv_txt = 'txt'
    else:
        arqSaida = open('/{}/{}.csv'.format(diretorioSaida, arquivoSaida), 'a+')
        output = csv.writer(arqSaida, delimiter=' ', lineterminator="\n")
        csv_txt = 'csv'
    
    if acao == 'bloco' or acao == 'insert':
        log.adicionar('CARREGANDO DADOS')
        dados = banco.bdpl(query_principal)
        log.adicionar('QUERY EXECUTADA')
        if dados != None:
            arqSaida.writelines(dados)
        else:
            arqSaida.writelines('NENHUM DADO FOI INSERIDO E/OU MODIFICADO\n')
    
    if acao == 'select':
        log.adicionar('CARREGANDO DADOS PARA CONSULTA')
        head, dados = banco.bd(query_principal)
        log.adicionar('QUERY EXECUTADA')

        #RECEBE A DESCRIPTION DOS CAMPOS, CRIA O HEAD
        if head != None:
            cols = []
            for head_dados in head:
                cols.append(head_dados[0])
            output.writerow(cols)

            #RECEBE OS DADOS GERADOS E INSERE NO ARQUIVO
            if dados != None:
                log.adicionar('FIM CONSULTA AO BANCO')
                log.adicionar('LENDO DADOS DA QUERY')
                #INSERE OS DADOS NO ARQUIVO OUTPUT
                for dadosTabela in dados:
                    #NESTE PONTO O PROGRAMA LOCALIZA QUAL VARIAVEL É FLOAT E SUBSTITUI (.) POR (,).
                    output.writerow([[sub, str(sub).replace('.', ',')][type(sub) is float] for sub in dadosTabela])

    log.adicionar('GERANDO {}.{}'.format(arquivoSaida, csv_txt))
    arqSaida.close()
    log.adicionar('{}.{} GERADO'.format(arquivoSaida, csv_txt))
    return dados
        
#FUNCAO PRINCIPAL
def main():
    #ABAIXO ESTÃO OS IFS RELACIONADO A CADA ETAPA DO PROCESSO

    #QUERY 2: REALIZADO AJUSTES DE CARACTERES PARA CAIXA ALTA E INDICADO QUE AS VARIAVEIS DE RETORNO SÃO CHAR.
    if etapa == '2' or etapa == 'all':
        log.adicionar('INICIO SELECT_02')
        queryXPTO('select', False, 'FILA_', query_modelo_python.query02())
    
    #QUERY 3: REALIZADO AJUSTES DE CARACTERES PARA CAIXA ALTA E INDICADO QUE AS VARIAVEIS DE RETORNO SÃO CHAR.
    if etapa == '3' or etapa == 'all':
        log.adicionar('INICIO SELECT_03')
        queryXPTO('select', False, 'PAGTO_SUSPENSO_XPTO_', query_modelo_python.query03())
    
    #QUERY 4: NÃO HOUVE VARIAÇÃO. IMPLEMENTAMOS UMA VARIAVEL PARA RECEBER A DATA INICIAL DO PERIODO
    if etapa == '4' or etapa == 'all':
        dataInicial, dataFinal, query04 = query_modelo_python.query04()
        log.adicionar('INICIO BLOCO_04 - PERÍODO {} À {}' .format(dataInicial, dataFinal))
        queryXPTO('bloco', True, 'FILA_ESTADO_200_', query04)
        
        if etapa == 'all': 
            log.adicionar('AGUARDANDO 15 MINUTOS CONFORME SOLICITAÇÃO DO CLIENTE')
            time.sleep(15*60)
                
    #QUERY 5: REALIZADO AJUSTES DE CARACTERES PARA CAIXA ALTA E INDICADO QUE AS VARIAVEIS DE RETORNO SÃO CHAR.
    if etapa == '5' or etapa == 'all':
        log.adicionar('INICIO SELECT_05')
        queryXPTO('select', False, 'FILA_ESTADO_201_', query_modelo_python.query05())
    
    #QUERY 6: REALIZADO AJUSTES DE CARACTERES PARA CAIXA ALTA E INDICADO QUE AS VARIAVEIS DE RETORNO SÃO CHAR.
    if etapa == '6' or etapa == 'all':
        log.adicionar('INICIO SELECT_06')
        queryXPTO('select', False, 'FILA_ESTADO_202_', query_modelo_python.query06())
    
    #QUERY 7: REALIZADO AJUSTES DE CARACTERES PARA CAIXA ALTA E INDICADO QUE AS VARIAVEIS DE RETORNO SÃO CHAR.
    if etapa == '7' or etapa == 'all':
        log.adicionar('INICIO SELECT_07')
        dados = queryXPTO('select', False, 'PAGTO_SUSPENSO_XPTO_APOS_MASSIVO_', query_modelo_python.query07())

    #QUERY 8: REALIZADO AJUSTES DE CARACTERES PARA CAIXA ALTA.
    if etapa == '8' or etapa == 'all':
        log.adicionar('INICIO SELECT_08')
        queryXPTO('bloco', True, 'UPDATE_ESTADO_4_REMS_', query_modelo_python.query08())

''' -----------   FIM DAS FUNÇÕES   ----------- '''

if __name__ == "__main__":
    #A PRIMEIRA AÇÃO DESTE PROGRAMA E CRIAR A VARIÁVEL LOG E VERIFICAR SE ESTAMOS EM HOMOLOGAÇÃO OU PRODUÇÃO
    diretorioLogs = '/XPTO/log/' + time.strftime('%Y%m%d') + '/'
    
    #VERIFICA SE HÁ O DIRETÓRIO DE LOG, CASO NÃO EXISTA CRIA.
    try:
        if not (os.path.isdir(diretorioLogs)):
            os.makedirs(diretorioLogs)
    except:
        exitPrograma(5)

    #DEFINE O NOME E DESTINO DA LOG GERADA PELO PROGRAMA, SENDO QUE os.path.basename(__file__) RETORNA O NOME DO PROGRAMA PYTHON.
    logNome = ('{}.log'.format(os.path.basename(__file__)))
    log = logAdd.diretorio(diretorioLogs, logNome)
    
    #POR PADRÃO, SETAMOS O PROGRAMA PARA HOMOLOGAÇÃO, ESTA INFORMAÇÃO SÓ É MODIFICADA SE O PRÓXIMO IF FOR VERDADEIRO
    producao = False 
    if (os.environ['HOSTNAME'].upper() == 'HOSTNAME_SERV_PROD'): #HOSTMANME DA MAQUINA DE PRODUÇÃO
        producao = True    
    
    #RECEBE AS VARIÁVEIS EXTERNAS.
    banco, etapa, diretorioSaida = variaveisExternas()

    #FUNÇÃO PRINCIPAL
    main()
    exitPrograma(0)
