#!/usr/bin/env python3
# coding: utf-8
'''
NOME DA LIB:        connOracle.py
VERSÃO:             1.0
OBJETIVO:           CONEXÃO A BASE DE DADOS ORACLE COM SENHAS CRIPTOGRAFADAS
DESCRIÇÃO:          ESTA LIB PERMITE A CONEXÃO, EXECUÇÃO DAS PRINCIPAIS FUNÇÕES DO BANCO, BEM COMO BLOCO PL/SQL
                    ESTÃO CADASTRADAS AS PRINCIPAIS BASES DE HOMOLOGAÇÃO E PRODUÇÃO.
HISTÓRICO:          V1.0 - 17/04/2020   DANIEL ALVES DIAS JUNIOR
                                        - INSERIDO EM PRODUÇÃO.
'''
#IMPORTA A BIBLIOTECA cx_Oracle DISPONÍVEL NA PASTA PRINCIPAL
from cx_Oracle import cx_Oracle
import base64
class BancoDados:
    def __init__(self, prod, baseConn, serviceConn):
        self.cx_Oracle = cx_Oracle

        #DEFINE O HOST DE CONEXÃO
        if prod:
            host = 'PRODUÇÃO_HOST'
            passConn = switch_bd(serviceConn)
        else:
            host = 'HOMOLOGAÇÃO_HOST'
            passConn = switch_bd(serviceConn)

        #REALIZA A CONEXÃO
        self.conexao = cx_Oracle.connect("%s/%s@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=%s)(PORT = 1521)))(CONNECT_DATA=(SERVICE_NAME=%s)(SERVER=DEDICATED)))" % (baseConn, base64.b64decode(passConn), host, serviceConn))

    #EXECUTAR SELECT
    def bd(self, comando):
        conexao = self.conexao
        cursor = conexao.cursor()
        cursor.execute(comando)
        description = cursor.description
        dados = cursor.fetchall()
        return description, dados
    
    #EXECUTAR BLOCO PL E INSTRUÇÕES
    def bdpl(self, comando):
        conexao = self.conexao
        cursor = conexao.cursor()
        cursor.callproc("dbms_output.enable")
        cursor.execute(comando)
        dados = DbmsOutputGetLine(cursor)
        cursor.callproc("dbms_output.disable")
        conexao.commit()
        cursor.close()
        return dados

    #FECHAR CONEXÃO
    def sair(self):
        self.conexao.close()

#RECEBE O SERVIDOR
def switch_bd(argument):
    switcher = {
        'hom01': 'VEVTVEU=',
        'hom02': 'VEVTVEU=',
        'hom03': 'VEVTVEU=',
        'hom04': 'VEVTVEU=',
        'hom05': 'VEVTVEU=',
        'prod01': 'VEVTVEU=',
        'prod02': 'VEVTVEU=',
    }
    return switcher.get(argument)

def DbmsOutputGetLine(cursor):
    line = cursor.var(cx_Oracle.STRING)
    status = cursor.var(cx_Oracle.NUMBER)
    while True:
        cursor.callproc("dbms_output.get_line",(line,status))
        if status.getvalue() != 0:
            break
        else:
            return line.getvalue()
