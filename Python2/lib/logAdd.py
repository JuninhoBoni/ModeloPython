#!/usr/bin/env python2.4
# coding: utf-8
'''
NOME DA LIB:        logAdd.py
VERSÃO:             1.0
OBJETIVO:           GERAR LOGS
DESCRIÇÃO:          ESTA LIB GERA AS LOGS DOS PROGRAMAS.
HISTÓRICO:          V1.0 - 17/04/2020   DANIEL ALVES DIAS JUNIOR
                                        - INSERIDO EM PRODUÇÃO.
'''
import time, os
class diretorio:
    def __init__(self, diretorio, logNome):
        self.diretorio_log = diretorio + logNome
    
    def adicionar(self, dadosLog):
        #print(dadosLog)
        arq = open(self.diretorio_log, 'a+')
        arq.writelines(time.strftime('%d/%m/%Y - %H:%M:%S') + ' ' + dadosLog + '\n')
        arq.close()