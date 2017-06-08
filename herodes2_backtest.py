import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import numpy as np
import pandas as pd
import csv
import BOVESPA as bov
import herodes as hero
import INDICADORES as ind


# REALIZA O BACKDOOR TEST USANDO O ALGORITMO HERODES 2. APRESENTA OPCOES UMA A UMA E LHE DA A OPCAO DE OPERAR OU NAO. EM CASO DE ACEITE, GRAVA AS INFORMACOES EM UM ARQUIVO DO TIPO csv PARA SER ANALISADO PELO xxx.py. ESTE PROGRAMA NAO TEM BENCHMARK TIMING!!

def save_to_file(last_row):
    
    list_total = []
    #list_total.append(first_row)
    reader = csv.reader(open("pythonfiles/herodes2_backtest_record.csv",'rU'),delimiter=',')
    #reader.next()
    
    for row in reader:
        lista_row = []
        
        Stock_l = row[0]
        Ano_e_l = row[1]
        Mes_e_l = row[2]
        Dia_e_l = row[3]
        entrada_l = row[4]
        stop_l = row[5]
        Ano_s_l = row[6]
        Mes_s_l = row[7]
        Dia_s_l = row[8]
        saida_l = row[9]
        percentual_l = row[10]
        
        lista_row.append(Stock_l)
        lista_row.append(Ano_e_l)
        lista_row.append(Mes_e_l)
        lista_row.append(Dia_e_l)
        lista_row.append(entrada_l)
        lista_row.append(stop_l)
        lista_row.append(Ano_s_l)
        lista_row.append(Mes_s_l)
        lista_row.append(Dia_s_l)
        lista_row.append(saida_l)
        lista_row.append(percentual_l)
        
        list_total.append(lista_row)
    
    list_total.append(last_row)
    
    writer = csv.writer(open("pythonfiles/herodes2_backtest_record.csv", 'wb'), delimiter=',')
    for j in list_total:
        writer.writerow(j)

def anota_herodes(dia_um,dia_ultimo,data_entrada,ativo_operado,abe_entrada,fech_saida,data_saida,preco_stop,perda_ou_ganho,comp_vend):
    
    ano_primeiro = dia_um.year
    mes_primeiro = dia_um.month
    dia_primeiro = dia_um.day
    
    ano_ultimo = dia_ultimo.year
    mes_ultimo = dia_ultimo.month
    dia_ultimo = dia_ultimo.day
    
    ano_e = data_entrada.year
    mes_e = data_entrada.month
    dia_e = data_entrada.day
    
    ano_s = data_saida.year
    mes_s = data_saida.month
    dia_s = data_saida.day
    
    if perda_ou_ganho < 0:
        
        saida_rs = round(preco_stop,2)
        
        if comp_vend > 0:
            saida_perce = round((saida_rs / abe_entrada) - 1,4)
        elif comp_vend < 0:
            saida_perce = round(((saida_rs / abe_entrada) - 1) * (-1),4)
            
    elif perda_ou_ganho > 0:
        
        saida_rs = round(fech_saida,2)
        
        if comp_vend < 0:
            saida_perce = round(((saida_rs / abe_entrada) - 1) * (-1),4)
        elif comp_vend > 0:
            saida_perce = round((saida_rs / abe_entrada) - 1,4)
    
    #print ""
    #print "Operacao realizada: ",ativo_operado,",",abe_entrada,",",preco_stop,",",saida_rs,",",saida_perce
    
    #first_row = ["Stock",str(ano_primeiro),str(mes_primeiro),str(dia_primeiro),"entrada","stop",str(ano_ultimo),str(mes_ultimo),str(dia_ultimo),"saida","percentual"]
    last_row = [str(ativo_operado),str(ano_e),str(mes_e),str(dia_e),str(abe_entrada),str(preco_stop),str(ano_s),str(mes_s),str(dia_s),str(saida_rs),str(saida_perce)]
    
    save_to_file(last_row)
    
    #print "dados gravados com sucesso!"
    return saida_perce


def calcula_resultado(ativo_ativo,nome_ativo,ls_keys,dataobj,bloco,winka):
    
    macd_array = []
    stop_raw = ativo_ativo['stop$'].values[-1]
    stop_loss = 0.0
    direcao = ativo_ativo['stop$'].values[-2]
    macd_f_historico_max = max(hero.get_absolute(ativo_ativo['MACD-F'].values))
    array_de_percent = [0.25,0.5,0.75,1,1.25,1.5]
    #macd_f_historico = ativo_ativo['MACD-F'].values
    macd_f_atual = ativo_ativo['MACD-F'].values[-1]
    macd_f_alvo = 0.0
    selo = ativo_ativo.index.values[-1] + dt.timedelta(days=1)
    stop_or_gain = 0
    novo_symbols = []
    novo_symbols.append(nome_ativo)
    
    data_on = selo - dt.timedelta(days=300)
    data_off = selo + dt.timedelta(days=70)
    periodo_teste = bov.get_BOV_days(data_on,data_off)
    close_teste = dataobj.get_data(periodo_teste, novo_symbols, ls_keys)
    d_data_teste = dict(zip(ls_keys, close_teste))
    for s_key in ls_keys:
        d_data_teste[s_key] = d_data_teste[s_key].fillna(method = 'ffill')
        d_data_teste[s_key] = d_data_teste[s_key].fillna(method = 'bfill')
        d_data_teste[s_key] = d_data_teste[s_key].fillna(1.0)
    
    #lista_dos_gains = [0.005,0.01,0.015]
    #lista_dos_stops = [0.005,0.0075,0.01,0.015,0.02,0.03]
    
    if direcao > 0:
        
        #macd_f_alvo = raw_input("HERODES-2>> Defina o MACD-F alvo: ")
        #macd_f_alvo = float(macd_f_alvo)

        #macd_f_alvo = (macd_f_historico_max - macd_f_atual) * array_de_percent[0]
        macd_f_alvo = macd_f_atual + (macd_f_historico_max - macd_f_atual) * array_de_percent[0]
        #print macd_f_alvo
        #macd_f_alvo = 0.5
        minimo_atual = 1000000
        #print macd_f_alvo
        count_stop = 0
        abe_stop = 0.0
        
        for k in np.arange(len(periodo_teste)-bloco):
                
            for i in d_data_teste[ls_keys[4]].columns:
                frame_abe2 = d_data_teste[ls_keys[0]][i][k:bloco+k]
                frame_min2 = d_data_teste[ls_keys[2]][i][k:bloco+k]
                frame_max2 = d_data_teste[ls_keys[1]][i][k:bloco+k]
                frame_fech2 = d_data_teste[ls_keys[4]][i][k:bloco+k]
                    
                if frame_fech2.index[-1] < selo:
                    continue
                
                elif frame_fech2.index[-1] >= selo:
                    
                    if count_stop == 0:
                        count_stop = count_stop + 1                    
                        abe_stop = frame_abe2.values[-1]
                        stop_stop_stop = abe_stop - (abe_stop * winka[0])
                        gain_gain_gain = abe_stop + (abe_stop * winka[1])
                    
                    '''    
                    if count_stop == 0:
                        count_stop = count_stop + 1
                        abe_stop = frame_abe2.values[-1]
                        teste_stop = (abe_stop - stop_raw) / abe_stop
                        if teste_stop >= 0.02:
                            stop_loss = stop_raw
                        elif teste_stop < 0.02:
                            stop_loss = abe_stop - (abe_stop * 0.02)
                            
                        if teste_stop > 0.04:
                            stop_loss = abe_stop - (abe_stop * 0.04)
                    '''            
                    vermelho,azul = ind.new_macd(frame_fech2.values)
                    macd_f_atual = vermelho[-1]
                    minimo_atual = frame_min2.values[-1]
                    maximo_atual = frame_max2.values[-1]
                    fech_atual = frame_fech2.values[-1]
                    
                    #fech_atual_teste = frame_fech2.values
                    #print fech_atual_teste[-1]
                    #print "(MACD-F)",macd_f_atual
                    macd_array.append(macd_f_atual)
                    #print fech_atual_teste[-1]
                    #preco_teste = ind.get_macd_alvo2(fech_atual_teste,direcao,macd_f_atual)
                    #print preco_teste
                    #print frame_fech2.values[-1]
                    
                    if maximo_atual >= gain_gain_gain and minimo_atual <= stop_stop_stop:
                        if fech_atual >= abe_stop:
                            stop_or_gain = -1
                            return selo,nome_ativo,abe_stop,gain_gain_gain,frame_fech2.index.values[-1],stop_stop_stop,stop_or_gain,macd_array
                        elif fech_atual < abe_stop:
                            stop_or_gain = 1
                            return selo,nome_ativo,abe_stop,gain_gain_gain,frame_fech2.index.values[-1],stop_stop_stop,stop_or_gain,macd_array
                    
                    if maximo_atual >= gain_gain_gain:
                        stop_or_gain = 1
                        return selo,nome_ativo,abe_stop,gain_gain_gain,frame_fech2.index.values[-1],stop_stop_stop,stop_or_gain,macd_array
                    
                    if minimo_atual <= stop_stop_stop:
                        stop_or_gain = -1
                        return selo,nome_ativo,abe_stop,gain_gain_gain,frame_fech2.index.values[-1],stop_stop_stop,stop_or_gain,macd_array
                    
                    '''
                    if minimo_atual <= stop_loss:
                        
                        stop_or_gain = -1
                        return selo,nome_ativo,abe_stop,frame_fech2.values[-1],frame_fech2.index.values[-1],stop_loss,stop_or_gain,macd_array
                    
                    elif macd_f_atual >= macd_f_alvo:
                        
                        stop_or_gain = 1
                        return selo,nome_ativo,abe_stop,frame_fech2.values[-1],frame_fech2.index.values[-1],stop_loss,stop_or_gain,macd_array'''
                    
                
    elif direcao < 0:
        
        #macd_f_alvo = raw_input("HERODES-2>> Defina o MACD-F alvo: ")
        #macd_f_alvo = float(macd_f_alvo)

        #macd_f_alvo = (macd_f_historico_max - (macd_f_atual*(-1))) * array_de_percent[0]
        macd_f_alvo = macd_f_atual - (macd_f_historico_max - (macd_f_atual*(-1))) * array_de_percent[0]
        #print macd_f_alvo
        #macd_f_alvo = -0.5
        maximo_atual = -1000000
        count_stop = 0
        abe_stop = 0.0

        
        for k in np.arange(len(periodo_teste)-bloco):
                
            for i in d_data_teste[ls_keys[4]].columns:
                frame_abe2 = d_data_teste[ls_keys[0]][i][k:bloco+k]
                frame_min2 = d_data_teste[ls_keys[2]][i][k:bloco+k]
                frame_max2 = d_data_teste[ls_keys[1]][i][k:bloco+k]
                frame_fech2 = d_data_teste[ls_keys[4]][i][k:bloco+k]
                    
                if frame_fech2.index[-1] < selo:
                    continue

                elif frame_fech2.index[-1] >= selo:
                    
                    if count_stop == 0:
                        count_stop = count_stop + 1                      
                        abe_stop = frame_abe2.values[-1]
                        stop_stop_stop = abe_stop + (abe_stop * winka[0])
                        gain_gain_gain = abe_stop - (abe_stop * winka[1])
                    '''    
                    if count_stop == 0:
                        count_stop = count_stop + 1
                        abe_stop = frame_abe2.values[-1]
                        teste_stop = (stop_raw - abe_stop) / abe_stop
                        if teste_stop >= 0.02:
                            stop_loss = stop_raw
                        elif teste_stop < 0.02:
                            stop_loss = abe_stop + (abe_stop * 0.02)
                        
                        if teste_stop > 0.04:
                            stop_loss = abe_stop + (abe_stop * 0.04)'''                       
                                
                    vermelho,azul = ind.new_macd(frame_fech2.values)
                    macd_f_atual = vermelho[-1]
                    minimo_atual = frame_min2.values[-1]
                    maximo_atual = frame_max2.values[-1]
                    fech_atual = frame_fech2.values[-1]
                    #print "(MACD-F)",macd_f_atual
                    macd_array.append(macd_f_atual)                  

                    if maximo_atual >= stop_stop_stop and minimo_atual <= gain_gain_gain:
                        if fech_atual >= abe_stop:
                            stop_or_gain = 1
                            return selo,nome_ativo,abe_stop,gain_gain_gain,frame_fech2.index.values[-1],stop_stop_stop,stop_or_gain,macd_array

                        elif fech_atual < abe_stop:
                            stop_or_gain = -1
                            return selo,nome_ativo,abe_stop,gain_gain_gain,frame_fech2.index.values[-1],stop_stop_stop,stop_or_gain,macd_array
                    
                    if maximo_atual >= stop_stop_stop:
                        stop_or_gain = -1
                        return selo,nome_ativo,abe_stop,gain_gain_gain,frame_fech2.index.values[-1],stop_stop_stop,stop_or_gain,macd_array                 
                                        
                    if minimo_atual <= gain_gain_gain:
                        stop_or_gain = 1
                        return selo,nome_ativo,abe_stop,gain_gain_gain,frame_fech2.index.values[-1],stop_stop_stop,stop_or_gain,macd_array                  
                    '''    
                    if maximo_atual >= stop_loss:
                        
                        stop_or_gain = -1
                        return selo,nome_ativo,abe_stop,frame_fech2.values[-1],frame_fech2.index.values[-1],stop_loss,stop_or_gain,macd_array
                    
                    elif macd_f_atual < macd_f_alvo:
                        
                        stop_or_gain = 1
                        return selo,nome_ativo,abe_stop,frame_fech2.values[-1],frame_fech2.index.values[-1],stop_loss,stop_or_gain,macd_array'''
                  

def main_backtest():
    
    contagem_dias = 0
    proibido = 0
    print ""
    proibido_raw = raw_input("HERODES-2>> Deseja PROIBIR operacoes do tipo short (S/N): ")
    proibido_raw = str(proibido_raw)
    if proibido_raw == "S":
        proibido = -1
    elif proibido_raw == "N":
        proibido = 1
    elif proibido_raw <> "S" and proibido_raw <> "N":
        print ""
        print "Entrada diferente de S ou N. A aplicacao sera finalizada."
        return
    
    print ""
    dia_init_raw = raw_input("HERODES-2>> Dia INICIAL: ")
    mes_init_raw = raw_input("HERODES-2>> Mes INICIAL: ")
    ano_init_raw = raw_input("HERODES-2>> Ano INICIAL: ")
    print ""
    
    dia_init = int(dia_init_raw)
    mes_init = int(mes_init_raw)
    ano_init = int(ano_init_raw)
    
    dia_final_raw = raw_input("HERODES-2>> Dia FINAL: ")
    mes_final_raw = raw_input("HERODES-2>> Mes FINAL: ")
    ano_final_raw = raw_input("HERODES-2>> Ano FINAL: ")
    print ""
    
    dia_final = int(dia_final_raw)
    mes_final = int(mes_final_raw)
    ano_final = int(ano_final_raw)
    
    dia_um = dt.datetime(ano_init,mes_init,dia_init)
    dia_very_um = dt.datetime(ano_init,mes_init,dia_init)
    dia_ultimo = dt.datetime(ano_final,mes_final,dia_final)
    
    dt_start = dia_um - dt.timedelta(days=300)
    dt_end = dia_ultimo + dt.timedelta(days=50)
    
    timestamps = bov.get_BOV_days(dt_start,dt_end)
    
    
    num_ativos = raw_input("HERODES-2>> Quantidade de ativos (BD inteiro = 0): ")
    num_ativos = int(num_ativos)
    
    nova_array = np.array(np.arange(num_ativos))
    
    symbols = []
    
    print ""
    
    if len(nova_array) == 0:
        symbols = bov.get_BOV_symbols()
    elif len(nova_array) > 0:
        for i in nova_array:
            ativo = raw_input("HERODES-2>> Nome do ativo: ")
            symbols.append(str(ativo))
    
    print ""
    #lista_com_todos_alvos = [[0.005,0.005],[0.005,0.0075],[0.005,0.01],[0.005,0.015],[0.005,0.02],[0.005,0.025],[0.005,0.03],[0.0075,0.005],[0.0075,0.0075],[0.0075,0.01],[0.0075,0.015],[0.0075,0.02],[0.0075,0.025],[0.0075,0.03],[0.01,0.005],[0.01,0.0075],[0.01,0.01],[0.01,0.015],[0.01,0.02],[0.01,0.025],[0.01,0.03],[0.015,0.005],[0.015,0.0075],[0.015,0.01],[0.015,0.015],[0.015,0.02],[0.015,0.025],[0.015,0.03],[0.02,0.005],[0.02,0.0075],[0.02,0.01],[0.02,0.015],[0.02,0.02],[0.02,0.025],[0.02,0.03],[0.025,0.005],[0.025,0.0075],[0.025,0.01],[0.025,0.015],[0.025,0.02],[0.025,0.025],[0.025,0.03],[0.03,0.005],[0.03,0.0075],[0.03,0.01],[0.03,0.015],[0.03,0.02],[0.03,0.025],[0.03,0.03]]
    #lista_com_todos_alvos = [[0.0075,0.025],[0.01,0.015],[0.01,0.02],[0.01,0.025],[0.01,0.03],[0.015,0.015],[0.015,0.02],[0.015,0.025],[0.02,0.025],[0.02,0.03],[0.025,0.005],[0.03,0.005],[0.03,0.025],[0.03,0.03]]
    lista_com_todos_alvos = [[0.03,0.03]]
    for winka in lista_com_todos_alvos:
        
        print winka
        
        last_row = ["t","t","t","t","t","t","t","t","t","t","t"]
        save_to_file(last_row)
    
        ls_keys = ['open', 'high', 'low', 'close', 'actual_close']
        dataobj = da.DataAccess('Ibovespa')
        close = dataobj.get_data(timestamps, symbols, ls_keys)
        d_data = dict(zip(ls_keys, close))
        for s_key in ls_keys:
            d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
            d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
            d_data[s_key] = d_data[s_key].fillna(1.0)
            
        bloco = 140
        
        call_ativo = []
        sen_ativo = []
        for_sen_ativo = []
        for_mme_ativo = []
        for_mms_ativo = []
        #sen_ativo = []
        #for_mme_ativo = []
        #for_mms_ativo = []
        ext_macdf_ativo_hist = []
        med_macdf_ativo_hist = []
        init_macdf_real = []
        ifr_init_real = []
        ext_macdf_ativo_real = []
        index_result = []
        perc_res_teste_alpha = []
        col_teste_result = ["ativo","c/v","for_c/v","f_mme","f_mms","ext_m_A_h","med_m_A_h","init_m_A_r","ext_m_A_r","resultado","ifr_init"]
        

        for k in np.arange(len(timestamps)-bloco):
            
            controle = 0
            find = False
            stocks_dict = {}
            for i in d_data[ls_keys[4]].columns:
    
                frame_abe = d_data[ls_keys[0]][i][k:bloco+k]
                frame_max = d_data[ls_keys[1]][i][k:bloco+k]
                frame_min = d_data[ls_keys[2]][i][k:bloco+k]
                frame_fech = d_data[ls_keys[4]][i][k:bloco+k]
                
                if i == "IBVSP":
                    frame_stock_ibvsp = hero.herodes2_sem_filtro(frame_abe,frame_max,frame_min,frame_fech)
                
                if frame_fech.index[-1] < dia_um:
                    continue
                elif frame_fech.index[-1] > dia_ultimo:
                    find = True
                    break
                elif frame_fech.index[-1] >= dia_um:
                        
                    controle,frame_stock = hero.herodes2_total(frame_abe,frame_max,frame_min,frame_fech,proibido)
                
                if controle <= 0:
                    continue
                elif controle > 0:
                    stocks_dict["IBVSP"] = frame_stock_ibvsp
                    stocks_dict[i] = frame_stock
                             
            if len(stocks_dict) < 1:
                continue
            elif len(stocks_dict) >= 1:
                
                contagem_dias = contagem_dias + 1
                #print ""
                #print contagem_dias
                #print "" 
                
                for m in stocks_dict.keys():
        
                    #pprint.pprint(stocks_dict[m])
                    nome_ativo = m
                    
                    #filtro para retirar IBVSP do resultado
                    if m == "IBVSP":
                        continue
                    
                    #print nome_ativo
                    #print stocks_dict[m].to_string()
                    ativo_ativo = stocks_dict[m]
                    
                    data_entrada,ativo_operado,abe_entrada,prec_saida,data_saida,preco_stop,perda_ou_ganho,macd_f_array = calcula_resultado(ativo_ativo,nome_ativo,ls_keys,dataobj,bloco,winka)
                    #dia_um = data_saida + dt.timedelta(days=1)
                    comp_vend = ativo_ativo["stop$"].values[-2]
                    sentido_alvo = ativo_ativo['stop$'].values[-2]
                    bin_filtro_for_cv = hero.get_consist(ativo_ativo['MME'].values,sentido_alvo)
                    bin_filtro_f_mme = hero.get_consist(ativo_ativo['MME_delta'].values,sentido_alvo)
                    macd_f_abs = hero.get_absolute(ativo_ativo['MACD-F'].values)
                    teste_max_macd_hist = max(macd_f_abs)
                    teste_init_macd = abs(ativo_ativo['MACD-F'].values[-1])
                    
                    if m != "IBVSP":
                    
                        if bin_filtro_for_cv != 1 or bin_filtro_f_mme != 1:
                            continue
                        
                        if teste_init_macd >= teste_max_macd_hist:
                            continue                    
                    
                    perc_result_teste = anota_herodes(dia_very_um,dia_ultimo,data_entrada,ativo_operado,abe_entrada,prec_saida,data_saida,preco_stop,perda_ou_ganho,comp_vend)
                    '''
                    try:
                        data_entrada,ativo_operado,abe_entrada,prec_saida,data_saida,preco_stop,perda_ou_ganho,macd_f_array = calcula_resultado(ativo_ativo,nome_ativo,ls_keys,dataobj,bloco)
                        #dia_um = data_saida + dt.timedelta(days=1)
                        comp_vend = ativo_ativo["stop$"].values[-2]
                        perc_result_teste = anota_herodes(dia_very_um,dia_ultimo,data_entrada,ativo_operado,abe_entrada,prec_saida,data_saida,preco_stop,perda_ou_ganho,comp_vend)
                    except:
                        print ""
                        print "EXCESSAO DO ANOTA_HERODES!"
                        print ""
                        continue
                    # devo fazer os meus filtros de GAIN aqui!'''              
                    
                    sentido_deltas = hero.get_delta(ativo_ativo['MME'].values)
                    #sentido_alvo = hero.get_signal(sentido_deltas)
                    #sentido_alvo = ativo_ativo['stop$'].values[-2]
                    #bin_filtro_for_cv = hero.get_consist(ativo_ativo['MME'].values,sentido_alvo)
                    #bin_filtro_f_mme = hero.get_consist(ativo_ativo['MME_delta'].values,sentido_alvo)
                    #macd_f_abs = hero.get_absolute(ativo_ativo['MACD-F'].values)
                    #teste_max_macd_hist = max(macd_f_abs)
                    #teste_init_macd = abs(ativo_ativo['MACD-F'].values[-1])
                    IFR_init = ativo_ativo['IFR'].values[-1]
                    
                    '''if m != "IBVSP":
                    
                        if bin_filtro_for_cv != 1 or bin_filtro_f_mme != 1:
                            continue
                        
                        if teste_init_macd >= teste_max_macd_hist:
                            continue'''
                    
                    #inicio da anotacao par ciracao da tabela                    
                    call_ativo.append(nome_ativo)
                    index_result.append(contagem_dias)
                    sen_ativo.append(sentido_alvo)
                    for_sen_ativo.append(bin_filtro_for_cv)
                    for_mme_ativo.append(bin_filtro_f_mme)
                    for_mms_ativo.append(hero.get_consist(ativo_ativo['MMS_delta'].values,sentido_alvo))
                    
                    ext_macdf_ativo_hist.append(teste_max_macd_hist)
                    med_macdf_ativo_hist.append(sum(macd_f_abs) / float(len(macd_f_abs)))
                    macd_f_array = hero.get_absolute(macd_f_array)
                    ext_macdf_ativo_real.append(max(macd_f_array))
                    perc_res_teste_alpha.append(perc_result_teste)
                    init_macdf_real.append(teste_init_macd)
                    ifr_init_real.append(IFR_init)
        
        
        #aqui eu imprimo a tabela final
        '''print ""
        print "INDICE = numero que reune todos os ativos do mesmo dia"
        print "ATIVO = nome do ativo"
        print "C/V = indica se a operacao e comprada ou vendida"
        print "FOR_C/V = mostra se o sentido da operacao possui consistencia ou nao"
        print "F_MME = mostra se o delta do MME do ativo possui consistencia ou nao"
        print "F_MMS = mostra se o delta do MMS do ativo possui consistencia ou nao"
        print "EXT_M_A_H = mostra o valor absoluto maximo do MACD-F (historico)"
        print "MED_M_A_H = mostra o valor absoluto medio do MACD-F (historico)"
        print "INIT_MACDF_REAL = mostra o valor absoluto inicial do MACD-F"
        print "EXT_M_A_R = mostra o valor absoluto maximo do MACD-F (pos-operacao)"
        print "RESULTADO = mostra o resultado da operacao (pos-operacao)"
        print ""'''
        
        corpo_teste = {'ativo':call_ativo, 'c/v':sen_ativo, 'for_c/v':for_sen_ativo, 'f_mme':for_mme_ativo, 'f_mms':for_mms_ativo, 'ext_m_A_h':ext_macdf_ativo_hist, 'med_m_A_h':med_macdf_ativo_hist, 'init_m_A_r':init_macdf_real, 'ext_m_A_r':ext_macdf_ativo_real, 'resultado':perc_res_teste_alpha, 'ifr_init':ifr_init_real}
    
        dataframe_teste = pd.DataFrame(corpo_teste, columns=col_teste_result, index=index_result)
        print ""
        print "TABELA RESUMO DO TESTE"
        print ""
        print dataframe_teste.to_string()
                
        print ""
        print "Teste finalizado."
        
        # aqui eu salvo o restultado em um arquivo csv para posterior analise seja em python ou no excel.
        
        primeira_fileira = ["controle","ativo","c/v","for_c/v","f_mme","f_mms","ext_m_A_h","med_m_A_h","init_m_A_r","ext_m_A_r","resultado","ifr_init"]
        linha_total_teste = []
    
        for i in np.arange(len(call_ativo)):
            
            list_linha_atual = []
            list_linha_atual.append(index_result[i])
            list_linha_atual.append(call_ativo[i])
            list_linha_atual.append(sen_ativo[i])
            list_linha_atual.append(for_sen_ativo[i])
            list_linha_atual.append(for_mme_ativo[i])
            list_linha_atual.append(for_mms_ativo[i])
            list_linha_atual.append(ext_macdf_ativo_hist[i])
            list_linha_atual.append(med_macdf_ativo_hist[i])
            list_linha_atual.append(init_macdf_real[i])
            list_linha_atual.append(ext_macdf_ativo_real[i])
            list_linha_atual.append(perc_res_teste_alpha[i])
            
            linha_total_teste.append(list_linha_atual)
            
        writer = csv.writer(open("pythonfiles/resultado_teste.csv", 'wb'), delimiter=',')
        writer.writerow(primeira_fileira)
        for j in linha_total_teste:
            writer.writerow(j)
        #last_row = [str(ativo_operado),str(ano_e),str(mes_e),str(dia_e),str(abe_entrada),str(preco_stop),str(ano_s),str(mes_s),str(dia_s),str(saida_rs),str(saida_perce)]