import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import numpy as np
import pandas as pd
import BOVESPA as bov
import csv
import INDICADORES as ind


def main_analyze():
    
    arquivo_raw = raw_input("HERODES-2>> Nome do arquivo a ser usado para analise (somente .csv): ")
    nome_arquivo = str(arquivo_raw)
    filename = "pythonfiles/" + nome_arquivo + ".csv"
    print ""
    normal = raw_input("HERODES-2>> Valor a ser utilizado para a normalizacao (sugestao = 1): ")
    normal = int(normal)
    normal = round(normal,2)
    data_herodes_e = []
    data_herodes_s = []
    fundo_gains = []
    benchmark = []
    
    print ""
    ativo_raw = raw_input("HERODES-2>> Comparar fundo com qual ativo (ibovespa = IBVSP): ")
    print ""
    
    benchmark.append(str(ativo_raw))
    
    reader = csv.reader(open(filename,'rU'),delimiter=',')
    controle_cabeca = 0
    
    for row in reader:
        
        if controle_cabeca <= 0:
            data_herodes_e.append(dt.datetime(int(row[1]),int(row[2]),int(row[3]),16))
            data_herodes_s.append(dt.datetime(int(row[6]),int(row[7]),int(row[8]),16))
            controle_cabeca = controle_cabeca + 1
            continue
        
        fundo_gains.append(float(row[10]))
    
    dt_start = data_herodes_e[0]
    dt_end = data_herodes_s[-1]
    timestamps = bov.get_BOV_days(dt_start,dt_end)
    ls_keys = ['open', 'high', 'low', 'close', 'actual_close']
    dataobj = da.DataAccess('Ibovespa')
    close = dataobj.get_data(timestamps, benchmark, ls_keys)
    d_data = dict(zip(ls_keys, close))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
    
    indice_p = d_data['actual_close'][benchmark[0]]
    indice_p = np.array(indice_p.values)
    indice_p_n = (indice_p / indice_p[0])  * normal
    indice_gains = []
    for i in np.arange(len(indice_p_n)):
        try:
            indice_gains.append(round((indice_p_n[i+1]/indice_p_n[i])-1,4))
        except:
            break
        
    valor_atual = normal
    fundo_p_n = []
    fundo_p_n.append(valor_atual)
    for j in fundo_gains:
        valor_atual = round(valor_atual + (valor_atual * j),2)
        fundo_p_n.append(valor_atual)
    
    fundo_result = round((fundo_p_n[-1]/fundo_p_n[0]) - 1,4)
    indice_result = round((indice_p_n[-1]/indice_p_n[0]) - 1 ,4)
    
    fundo_sharpe = round(ind.sharperatio(fundo_p_n),4)
    indice_sharpe = round(ind.sharperatio(indice_p_n),4)
    
    fundo_sortino = round(ind.sortinoratio(fundo_p_n),4)
    indice_sortino = round(ind.sortinoratio(indice_p_n),4)
    
    indice_pd = []
    indice_pd.append(benchmark[0])
    indice_pd.append("herodes-2")
    
    resultado_pd = []
    resultado_pd.append(indice_result)
    resultado_pd.append(fundo_result)
    
    sharpe_pd = []
    sharpe_pd.append(indice_sharpe)
    sharpe_pd.append(fundo_sharpe)
    
    sortino_pd = []
    sortino_pd.append(indice_sortino)
    sortino_pd.append(fundo_sortino)
    
    colunas_pd = ["Resultado","Sharpe","Sortino"]
    
    corpo_pd = {'Resultado':resultado_pd, 'Sharpe':sharpe_pd, 'Sortino':sortino_pd}
    
    dataframe = pd.DataFrame(corpo_pd, columns=colunas_pd, index=indice_pd)
    
    print ""
    print "arquivo analisado:", filename
    print "periodo:", dt_start, "a", dt_end
    print ""
    print dataframe