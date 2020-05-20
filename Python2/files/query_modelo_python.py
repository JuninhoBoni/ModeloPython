#!/usr/bin/env python2.4
# coding: utf-8
'''
TODAS AS QUERYS DOS PROGRAMA ESTÃO NESTE DOCUMENTO
'''
import time
from datetime import timedelta, date, datetime

def query02():
    return """
SELECT *
FROM TESTE T
WHERE         T.CAMPO1 = 1
          AND T.CAMPO2 = 2
          AND T.CAMPO3 = 3
          AND T.CAMPO4 = 4
ORDER BY T.CAMPO1
"""
def query03():
    return """
SELECT *
FROM TESTE T
WHERE         T.CAMPO1 = 1
          AND T.CAMPO2 = 2
          AND T.CAMPO3 = 3
          AND T.CAMPO4 = 4
ORDER BY T.CAMPO1
"""

def query04(): #SYSDATE OK
    dataFinal = date(year=int(time.strftime('%Y')), month=int(time.strftime('%m')), day=int(time.strftime('%d')))
    if dataFinal.weekday() == 0:#SEG
        dataInicial = dataFinal - timedelta(days = 5)
    if dataFinal.weekday() == 1:#TER
        dataInicial = dataFinal - timedelta(days = 1)
    if dataFinal.weekday() == 2:#QUA
        dataInicial = dataFinal - timedelta(days = 2)
    if dataFinal.weekday() == 3:#QUI
        dataInicial = dataFinal - timedelta(days = 1)
    if dataFinal.weekday() == 4:#SEX
        dataInicial = dataFinal - timedelta(days = 2)
    if dataFinal.weekday() == 5:#SAB
        dataInicial = dataFinal - timedelta(days = 3)
    if dataFinal.weekday() == 6:#DOM
        dataInicial = dataFinal - timedelta(days = 4)
    

    return dataInicial, dataFinal, """
SELECT *
FROM TESTE T
WHERE         T.CAMPO1  =       1
          AND T.CAMPO2  =       2
          AND T.CAMPO3  =       3
          AND T.DATA   BETWEEN %s AND %s
ORDER BY T.CAMPO1
""" % (dataInicial, dataFinal)

def query05():
    return """
SELECT *
FROM TESTE T
WHERE         T.CAMPO1 = 1
          AND T.CAMPO2 = 2
          AND T.CAMPO3 = 3
          AND T.CAMPO4 = 4
ORDER BY T.CAMPO1
"""

def query06():
    return """
SELECT *
FROM TESTE T
WHERE         T.CAMPO1 = 1
          AND T.CAMPO2 = 2
          AND T.CAMPO3 = 3
          AND T.CAMPO4 = 4
ORDER BY T.CAMPO1
""" 

def query07():
    return """
SELECT *
FROM TESTE T
WHERE         T.CAMPO1 = 1
          AND T.CAMPO2 = 2
          AND T.CAMPO3 = 3
          AND T.CAMPO4 = 4
ORDER BY T.CAMPO1
"""

def query08(SYSDATE):
    if SYSDATE == None:
        SYSDATE = "SYSDATE"
    return
'''
SELECT *
FROM TESTE T
WHERE         T.CAMPO1 = 1
          AND T.CAMPO2 = 2
          AND T.CAMPO3 = 3
          AND T.DATA   = %s
ORDER BY T.CAMPO1
''' %(SYSDATE)

def testePL():
    return """
        DECLARE
            X NUMBER;
        BEGIN
            SELECT 1 INTO X FROM DUAL;
        DBMS_OUTPUT.PUT_LINE (X);
        END;
"""  