import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import numpy as np
import pandas
import csv
import BOVESPA as bov
import herodes as hero


def metodologia():
    
    print ""
    print "Atentar para os seguintes padroes, por ordem de importancia:"
    print "1) Consistencia da MME semanal"
    print "2) Consistencia do MACD"
    print "3) Consistencia forte do IFR ou divergencia do IFR com o MACD"
    print "4) Consistencia da MME diaria"
    print "5) Espaco para movimento do preco de fechamento"
    print ""

def metodologia2():
    
    print ""
    print "Atentar para os seguintes padroes:"
    print "1) Consistencia do MACD-S"
    print "2) Consistencia do MACD-F"
    print "3) MACD-F com folga ate o alvo |0.5|"
    print "4) Consistencia ou indicio de ruptura da MME(24)"
    print "5) Consistencia ou indicio de ruptura da MMS(24)"
    print ""

def run_herodes():
    
    dia_raw = raw_input("HERODES>> Dia a ser analisado: ")
    mes_raw = raw_input("HERODES>> Mes a ser analisado: ")
    ano_raw = raw_input("HERODES>> Ano a ser analisado: ")

    dia = int(dia_raw)
    mes = int(mes_raw)
    ano = int(ano_raw)
    
    dt_start = dt.datetime(2011,1,1)
    dt_end = dt.datetime(ano,mes,dia)
    
    print ""
    
    timestamps = bov.get_BOV_days(dt_start,dt_end)
    
    symbols = bov.get_BOV_symbols()
    
    ls_keys = ['open', 'high', 'low', 'close', 'actual_close']
    dataobj = da.DataAccess('Ibovespa')
    close = dataobj.get_data(timestamps, symbols, ls_keys)
    d_data = dict(zip(ls_keys, close))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
        
    bloco = 140
    stocks_dict = {}
    k = len(timestamps) - bloco
    
    for i in d_data[ls_keys[4]].columns:
        frame_abe = d_data[ls_keys[0]][i][k:bloco+k]
        frame_max = d_data[ls_keys[1]][i][k:bloco+k]
        frame_min = d_data[ls_keys[2]][i][k:bloco+k]
        frame_fech = d_data[ls_keys[4]][i][k:bloco+k]
            
        controle,frame_stock = hero.herodes(frame_abe,frame_max,frame_min,frame_fech)
            
        if controle < 0:
            continue
        elif controle > 0:
            stocks_dict[i] = frame_stock
    
    print ""
    print "HERODES>> data analisada: ", timestamps[-1].strftime("%d/%m/%y")
    print "HERODES>> output herodes: ", stocks_dict.keys()
    print ""
    
    return stocks_dict


def run_herodes2():
    
    proibido = 1
    
    dia_raw = raw_input("HERODES-2>> Dia a ser analisado: ")
    mes_raw = raw_input("HERODES-2>> Mes a ser analisado: ")
    ano_raw = raw_input("HERODES-2>> Ano a ser analisado: ")

    dia = int(dia_raw)
    mes = int(mes_raw)
    ano = int(ano_raw)
    
    dt_start = dt.datetime(2011,1,1)
    dt_end = dt.datetime(ano,mes,dia)
    
    print ""
    
    timestamps = bov.get_BOV_days(dt_start,dt_end)
    
    symbols = bov.get_BOV_symbols()
    
    ls_keys = ['open', 'high', 'low', 'close', 'actual_close']
    dataobj = da.DataAccess('Ibovespa')
    close = dataobj.get_data(timestamps, symbols, ls_keys)
    d_data = dict(zip(ls_keys, close))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
        
    bloco = 140
    stocks_dict = {}
    k = len(timestamps) - bloco
    
    for i in d_data[ls_keys[4]].columns:
        frame_abe = d_data[ls_keys[0]][i][k:bloco+k]
        frame_max = d_data[ls_keys[1]][i][k:bloco+k]
        frame_min = d_data[ls_keys[2]][i][k:bloco+k]
        frame_fech = d_data[ls_keys[4]][i][k:bloco+k]
            
        controle,frame_stock = hero.herodes2(frame_abe,frame_max,frame_min,frame_fech,proibido)
            
        if controle < 0:
            continue
        elif controle > 0:
            stocks_dict[i] = frame_stock
    
    print ""
    print "HERODES>> data analisada: ", timestamps[-1].strftime("%d/%m/%y")
    print "HERODES>> output herodes: ", stocks_dict.keys()
    print ""
    
    return stocks_dict