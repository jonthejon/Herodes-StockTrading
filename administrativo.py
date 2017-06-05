import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import numpy as np
import pandas as pd
import csv
import BOVESPA as bov
import herodes as hero
import INDICADORES as ind

def consultar_transacoes():
    
    periodo_raw = raw_input("Mes e ano do periodo(MM/AAAA): ")
    mes_raw = int(periodo_raw[0:2])
    ano_raw = int(periodo_raw[3:])
    
    filename = "pythonfiles/BDs/registro_notas.csv"
    reader = csv.reader(open(filename,'rU'),delimiter=',')
    reader.next()
    reader.next()
    
    lista_cabeca = ["DATA_V","TIPO","ATIVO","QUANT","PRECO_C","PRECO_V","TAXA_CBLC","TAXA_BOV","CORRETAGEM","IMPOSTOS","TOTAL_CUSTOS","LIQUIDO"]
    data_c_f = []
    data_v_f = []
    tipo_f = []
    ativo_f = []
    quant_f = []
    preco_c_f = []
    preco_v_f = []
    cblc_f = []
    bov_f = []
    corretagem_f = []
    impostos_f = []
    custos_f = []
    liquido_f = []
    
    for row in reader:
        
        mes_c_raw = int(row[7][3:5])
        ano_c_raw = int(row[7][6:])
        
        if mes_c_raw == mes_raw and ano_c_raw == ano_raw:
            
            tipo_f.append(row[4])
            ativo_f.append(row[5])
            quant_f.append(int(row[6]))
            data_c_f.append(row[7])
            preco_c_f.append(round(float(row[8]),2))
            data_v_f.append(row[9])
            preco_v_f.append(round(float(row[10]),2))
            cblc_f.append(round(float(row[11]),2))
            bov_f.append(round(float(row[12]),2))
            corretagem_f.append(round(float(row[13]),2))
            impostos_f.append(round(float(row[14]),2))
            liquido_f.append(round(float(row[15]),2))
            
            custos_f.append(round(float(row[11]),2) + round(float(row[12]),2) + round(float(row[13]),2) + round(float(row[14]),2))
            
    if len(cblc_f) == 0:
        
        print "Nao existem operacoes no periodo solicitado. A aplicacao sera encerrada."
        return
    
    corpo_dt = {'DATA_V':data_v_f,'TIPO':tipo_f,'ATIVO':ativo_f,'QUANT':quant_f,'PRECO_C':preco_c_f,'PRECO_V':preco_v_f,'TAXA_CBLC':cblc_f,'TAXA_BOV':bov_f,'CORRETAGEM':corretagem_f,'IMPOSTOS':impostos_f,'TOTAL_CUSTOS':custos_f,'LIQUIDO':liquido_f}
    dataframe = pd.DataFrame(corpo_dt, columns=lista_cabeca, index=data_c_f)
    
    print dataframe    


def consultar_saldo_preju():
    
    filename2 = "pythonfiles/BDs/saldo_IR.csv"
    reader_ir = csv.reader(open(filename2,'rU'),delimiter=',')
    reader_ir.next()
    
    saldo_dt = 0.0
    saldo_n = 0.0    
    
    for row in reader_ir:
        
        saldo_dt = round(float(row[0]),2)
        saldo_n = round(float(row[1]),2)
    
    print "Saldo em operacoes DAY-TRADE: R$", saldo_dt
    print "Saldo em operacoes NORMAIS: R$", saldo_n

def consultar_ir_pagos():
    
    filename3 = "pythonfiles/BDs/IR_pagos.csv"
    reader_pagos = csv.reader(open(filename3,'rU'),delimiter=',')
    reader_pagos.next()
    
    lista_pagos_cabeca = ["N_NOTAFISCAL","VALOR_PAGO","SITUACAO"]
    
    periodo_final = []
    n_notafiscal_final = []
    valor_pago_final = []
    pago_pago = []
    
    for row in reader_pagos:
        
        mes_pago = row[0]
        ano_pago = row[1]
        n_fiscal = int(row[2])
        v_pago = row[3]
        
        if n_fiscal == 0:
            
            pago_pago.append("nao pago")
            
        elif n_fiscal <> 0:
            
            pago_pago.append("pago")
        
        periodo_fabricado = mes_pago + "/" + ano_pago
        
        periodo_final.append(periodo_fabricado)
        n_notafiscal_final.append(n_fiscal)        
        valor_pago_final.append(v_pago)
         
    corpo_dt = {'N_NOTAFISCAL':n_notafiscal_final, 'VALOR_PAGO':valor_pago_final, 'SITUACAO':pago_pago}       
    dataframe = pd.DataFrame(corpo_dt, columns=lista_pagos_cabeca, index=periodo_final)
    
    print dataframe

def cadastrar_darf():
    
    periodo_raw = raw_input("Mes e ano do periodo(MM/AAAA): ")
    mes_raw = int(periodo_raw[0:2])
    ano_raw = int(periodo_raw[3:])
    
    n_darf = raw_input("Inserir o numero do DARF: ")
    
    filename3 = "pythonfiles/BDs/IR_pagos.csv"
    reader_pagos = csv.reader(open(filename3,'rU'),delimiter=',')
    reader_pagos.next()
    
    lista_pagos_cabeca = ["MES","ANO","N_NOTAFISCAL","VALOR_PAGO"]
    lista_pagos_resto = []
    
    count = 0
    
    for row in reader_pagos:
        
        lista_row = []
        mes_pago = int(row[0])
        ano_pago = int(row[1])
        n_fiscal = int(row[2])
        v_pago = float(row[3])
        
        lista_row.append(mes_pago)
        lista_row.append(ano_pago)
        
        if mes_raw == mes_pago and ano_raw == ano_pago:
            
            count = count + 1
            
            if n_fiscal <> 0:
                print "DARF ja cadastrada! A aplicacao foi encerrada."
                return
            
            n_fiscal = n_darf
        
        lista_row.append(n_fiscal)
        lista_row.append(v_pago)
        
        lista_pagos_resto.append(lista_row)
        
    if count == 0:
        
        print "Nao existe IR calculado para periodo solicitado. A aplicacao sera encerrada."
        return        
        
    writer2 = csv.writer(open("pythonfiles/BDs/IR_pagos.csv", 'wb'), delimiter=',')
    writer2.writerow(lista_pagos_cabeca)
    for j in lista_pagos_resto:
        writer2.writerow(j)    
    
    print ""
    print "DARF", n_fiscal , "cadastrado com sucesso!"

def ir_devido():
    
    periodo_raw = raw_input("Mes e ano do periodo(MM/AAAA): ")
    mes_raw = int(periodo_raw[0:2])
    ano_raw = int(periodo_raw[3:])
    
    filename3 = "pythonfiles/BDs/IR_pagos.csv"
    reader_pagos = csv.reader(open(filename3,'rU'),delimiter=',')
    reader_pagos.next()
    
    lista_pagos_cabeca = ["MES","ANO","N_NOTAFISCAL","VALOR_PAGO"]
    lista_pagos_resto = []
    
    for row in reader_pagos:
        
        lista_row = []
        mes_pago = int(row[0])
        ano_pago = int(row[1])
        n_fiscal = int(row[2])
        v_pago = float(row[3])
        
        lista_row.append(mes_pago)
        lista_row.append(ano_pago)
        lista_row.append(n_fiscal)
        lista_row.append(v_pago)
        
        lista_pagos_resto.append(lista_row)
        
        if mes_raw == mes_pago and ano_raw == ano_pago:
        
            print "O IR do periodo solicitado ja foi calculado! A aplicacao foi encerrada."
            return
    
    ir_dt_devido = 0.0
    ir_n_devido = 0.0
    aliquota_dt = 0.2
    aliquota_n = 0.15
    tipo_op = []
    liquido_op = []
    liquido_dt = []
    liquido_n = []
    saldo_dt = 0.0
    saldo_n = 0.0
    novo_saldo_dt = 0.0
    novo_saldo_n = 0.0
    
    filename = "pythonfiles/BDs/registro_notas.csv"
    reader = csv.reader(open(filename,'rU'),delimiter=',')
    reader.next()
    reader.next()
    
    for row in reader:
        
        mes_l_crua = int(row[9][3:5])
        ano_l_crua = int(row[9][6:])
        
        if mes_raw == mes_l_crua and ano_raw == ano_l_crua:
                
            tipo_op.append(row[4])
            liquido_op.append(round(float(row[15]),2))
    
    if len(tipo_op) == 0:
        
        print "Nao existem operacoes no periodo solicitado. A aplicacao sera encerrada."
        return
    
    b = np.array(np.arange(len(tipo_op)))
    for i in b:
        
        if tipo_op[i] == "day-trade":
            liquido_dt.append(liquido_op[i])
        elif tipo_op[i] == "normal":
            liquido_n.append(liquido_op[i])
    
    cum_dt = sum(liquido_dt)
    cum_n = sum(liquido_n)
    
    filename2 = "pythonfiles/BDs/saldo_IR.csv"
    reader_ir = csv.reader(open(filename2,'rU'),delimiter=',')
    reader_ir.next()
    
    for row in reader_ir:
        
        saldo_dt = round(float(row[0]),2)
        saldo_n = round(float(row[1]),2)
    
    final_dt = cum_dt - saldo_dt
    final_n = cum_n - saldo_n
    
    if final_dt <= 0:
        ir_dt_devido = 0.0
        novo_saldo_dt = abs(final_dt)
    elif final_dt >= 0:
        ir_dt_devido = final_dt * aliquota_dt
        novo_saldo_dt = 0.0
    
    if final_n <= 0:
        ir_n_devido = 0.0
        novo_saldo_n = abs(final_n)
    elif final_n >= 0:
        ir_n_devido = final_n * aliquota_n
        novo_saldo_n = 0.0
    
    lista_cabeca = ["SALDO_DT","SALDO_N"]
    lista_saldo = [str(novo_saldo_dt),str(novo_saldo_n)]
    
    writer = csv.writer(open("pythonfiles/BDs/saldo_IR.csv", 'wb'), delimiter=',')
    writer.writerow(lista_cabeca)
    writer.writerow(lista_saldo)
    
    last_pago_row = [str(mes_raw),str(ano_raw),str(0),str(ir_dt_devido + ir_n_devido)]
    lista_pagos_resto.append(last_pago_row)
    
    writer2 = csv.writer(open("pythonfiles/BDs/IR_pagos.csv", 'wb'), delimiter=',')
    writer2.writerow(lista_pagos_cabeca)
    for j in lista_pagos_resto:
        writer2.writerow(j)
    
    print ""
    print "IR devido para o periodo selecionado: R$", ir_dt_devido + ir_n_devido

def calcula_percentual(nparray):
    
    perce_array = []
    
    for i in np.arange(len(nparray)-1):
        
        diff = nparray[i+1] - nparray[i]
        
        if diff < 0:
            perce_array.append(0)
        elif diff >= 0:
            perce_array.append(1)
        
    perce_final = float(sum(perce_array)) / float(len(perce_array))
    
    return perce_final


def estatisticas():
    
    # VALOR INICIAL DO FUNDO DE 40 MIL. DATA INICIAL EM 03/07/2013. VALOR DO BOVESPA, NA DATA INCIAL E 45229.
    bovespa_init = 45229
    fund_init = 40000.00
    
    data_init_raw = raw_input("Data INICIAL do periodo(DD/MM/AAAA): ")
    dia_init_raw = int(data_init_raw[0:2])
    mes_init_raw = int(data_init_raw[3:5])
    ano_init_raw = int(data_init_raw[6:])
    
    data_fim_raw = raw_input("Data FINAL do periodo (DD/MM/AAAA): ")
    dia_fim_raw = int(data_fim_raw[0:2])
    mes_fim_raw = int(data_fim_raw[3:5])
    ano_fim_raw = int(data_fim_raw[6:])    
    
    dt_start = dt.datetime(ano_init_raw,mes_init_raw,dia_init_raw)
    dt_end = dt.datetime(ano_fim_raw,mes_fim_raw,dia_fim_raw)
    
    bovespa_value = []
    fund_value = []
    
    filename = "pythonfiles/BDs/registro_notas.csv"
    reader = csv.reader(open(filename,'rU'),delimiter=',')
    reader.next()
    bovespa_anterior = []
    fundo_anterior = []
    
    for row in reader:
        
        dia_l_crua = int(row[0][0:2])
        mes_l_crua = int(row[0][3:5])
        ano_l_crua = int(row[0][6:])
        data_l_cozida = dt.datetime(ano_l_crua,mes_l_crua,dia_l_crua)
        
        bovespa_anterior.append(int(row[1]))
        fundo_anterior.append(float(row[2]))
        
        if data_l_cozida >= dt_start and data_l_cozida <= dt_end:
            
            if len(bovespa_value) == 0:
                bovespa_value.append(bovespa_anterior[-2])
                fund_value.append(fundo_anterior[-2])
                
            bovespa_value.append(int(row[1]))
            fund_value.append(float(row[2]))    
    
    if len(bovespa_value) == 0:
        
        print "Nao existem operacoes no periodo solicitado. A aplicacao sera encerrada."
        return
    
    acerto_bovespa = calcula_percentual(bovespa_value)
    acerto_fundo = calcula_percentual(fund_value)
    retorno_bovespa = (float(bovespa_value[-1]) / float(bovespa_value[0])) - 1
    retorno_fundo = (float(fund_value[-1]) / float(fund_value[0])) - 1
    
    bov_ret = []
    fundo_ret = []
    
    bov_ret.append(round(acerto_bovespa,4))
    bov_ret.append(bovespa_value[0])
    bov_ret.append(bovespa_value[-1])
    bov_ret.append(round(retorno_bovespa,4))
    bov_ret.append(ind.sharperatio(bovespa_value))
    bov_ret.append(ind.sortinoratio(bovespa_value))
    
    fundo_ret.append(round(acerto_fundo,4))
    fundo_ret.append(fund_value[0])
    fundo_ret.append(fund_value[-1])
    fundo_ret.append(round(retorno_fundo,4))
    fundo_ret.append(ind.sharperatio(fund_value))
    fundo_ret.append(ind.sortinoratio(fund_value))
    
    indice = ["% acertos","valor inicial","valor final","retorno","sharpe","sortino"]
    colunas = ["IBovespa","Herodes_BR"]       
    corpo_dt = {'IBovespa':bov_ret, 'Herodes_BR':fundo_ret}       
    dataframe = pd.DataFrame(corpo_dt, columns=colunas, index=indice)

    print ""
    print "Periodo analisado:", dt_start.strftime("%d/%m/%y"), "a", dt_end.strftime("%d/%m/%y")
    print "Foram realizadas", len(fund_value)-1, "operacoes neste periodo."
    print ""
    print dataframe

        
def alavancagem():
    
    ac_fund_value = raw_input("Digite o valor atual do fundo (R$ xxx.xx): ")
    ac_fund_value = round(float(ac_fund_value),2)
    
    fund_init = 20000
    stop_mensal = 0.06
    alavancagem = np.array(np.arange(1,4.1,0.1))
    n_stops = 3
    
    fund_compara = []
    
    for i in alavancagem:
        
        fund_resid = (fund_init * stop_mensal * i * n_stops) / (1-(stop_mensal * i * n_stops))
        
        fund_alavancado = (fund_init + fund_resid) * i
        
        fund_atual = fund_alavancado / i
        fund_atual = round(float(fund_atual),2)
        
        fund_compara.append(fund_atual)
        
    alav_atual = alavancagem[np.searchsorted(fund_compara,ac_fund_value)-1]
    valor_atual = fund_compara[np.searchsorted(fund_compara,ac_fund_value)-1] * alav_atual
    
    valor_prox = fund_compara[np.searchsorted(fund_compara,ac_fund_value)]
    
    print ""
    print "VALOR ATUAL DO FUNDO: R$", ac_fund_value
    print "ALAVANCAGEM ATUAL: ", alav_atual
    print "VOLUME DE OPERACAO ATUAL: R$", round(float(valor_atual),2)
    print "VALOR ALVO DO FUNDO PARA PROXIMO NIVEL: R$", round(float(valor_prox),2)
    print ""

def grava_valores(data_l,bovespa,fund_value,n_nota,dn,ativo,quant,data_c,preco_c,data_v,preco_v,taxa_cblc,taxa_bov,corretagem,impostos,liquido):
    
    last_row = [data_l,bovespa,fund_value,n_nota,dn,ativo,quant,data_c,preco_c,data_v,preco_v,taxa_cblc,taxa_bov,corretagem,impostos,liquido]
    
    list_total = []

    reader = csv.reader(open("pythonfiles/BDs/registro_notas.csv",'rU'),delimiter=',')
    
    for row in reader:
        
        lista_row = []
        
        DATA_L = row[0]
        BOVESPA_VALUE = row[1]
        FUND_VALUE = row[2]
        N_NOTA = row[3]
        TIPO = row[4]
        ATIVO = row[5]
        QUANT = row[6]
        DATA_C = row[7]
        PRECO_C = row[8]
        DATA_V = row[9]
        PRECO_V = row[10]
        TAXA_CBLC = row[11]
        TAXA_BOV = row[12]
        CORRETAGEM = row[13]
        IMPOSTOS = row[14]
        LIQUIDO = row[15]
        
        lista_row.append(DATA_L)
        lista_row.append(BOVESPA_VALUE)
        lista_row.append(FUND_VALUE)
        lista_row.append(N_NOTA)
        lista_row.append(TIPO)
        lista_row.append(ATIVO)
        lista_row.append(QUANT)
        lista_row.append(DATA_C)
        lista_row.append(PRECO_C)
        lista_row.append(DATA_V)
        lista_row.append(PRECO_V)
        lista_row.append(TAXA_CBLC)
        lista_row.append(TAXA_BOV)
        lista_row.append(CORRETAGEM)
        lista_row.append(IMPOSTOS)
        lista_row.append(LIQUIDO)
        
        list_total.append(lista_row)
    
    list_total.append(last_row)
    
    writer = csv.writer(open("pythonfiles/BDs/registro_notas.csv", 'wb'), delimiter=',')
    
    for j in list_total:
        writer.writerow(j)
    
    print "dados inseridos com sucesso!"
    

def salva_nota_de_corretagem():
    
    data_l = raw_input("Digite a data da liquidacao (dd/mm/aaaa): ")
    data_l = str(data_l)     
    
    bovespa = raw_input("Digite a pontuacao ATUAL do ibovespa: ")
    bovespa = str(bovespa)    
    
    fund_value = raw_input("Digite o valor ATUAL do fundo (R$ xxx.xx): ")
    fund_value = str(fund_value)

    n_nota = raw_input("Digite o numero da nota de corretagem: ")
    n_nota = str(n_nota)

    dn = raw_input("Digite o tipo de operacao (day-trade/normal): ")
    dn = str(dn)

    ativo = raw_input("Digite o nome do ativo: ")
    ativo = str(ativo)

    quant = raw_input("Digite a quantidade transacionada: ")
    quant = str(quant)

    data_c = raw_input("Digite a data da compra (dd/mm/aaaa): ")
    data_c = str(data_c)

    preco_c = raw_input("Digite o preco medio de compra (R$ xxx.xx): ")
    preco_c = str(preco_c)

    data_v = raw_input("Digite a data da venda (dd/mm/aaaa): ")
    data_v = str(data_v)

    preco_v = raw_input("Digite o preco medio de venda (R$ xxx.xx): ")
    preco_v = str(preco_v)

    taxa_cblc = raw_input("Digite o valor total das taxas CBLC (R$ xxx.xx): ")
    taxa_cblc = str(taxa_cblc)

    taxa_bov = raw_input("Digite o valor total das taxas BOVESPA (R$ xxx.xx): ")
    taxa_bov = str(taxa_bov)

    corretagem = raw_input("Digite o valor da taxa de corretagem (R$ xxx.xx): ")
    corretagem = str(corretagem)

    impostos = raw_input("Digite o valor dos impostos (R$ xxx.xx): ")
    impostos = str(impostos)
    
    liquido = raw_input("Digite o valor liquido da operacao (R$ xxx.xx): ")
    liquido = str(liquido)    
    
    print ""
    print "FAVOR, CONFERIR OS DADOS:"
    print ""
    print "DATA_L: ", data_l
    print "IBOVESPA_VALUE: ", bovespa
    print "FUND_VALUE: ", fund_value
    print "N_NOTA: ", n_nota
    print "TIPO: ", dn
    print "ATIVO: ", ativo
    print "QUANT: ", quant
    print "DATA_C: ", data_c
    print "PRECO_C: ", preco_c
    print "DATA_V: ", data_v
    print "PRECO_V: ", preco_v
    print "TAXA_CBLC: ", taxa_cblc
    print "TAXA_BOV: ", taxa_bov
    print "CORRETAGEM: ", corretagem
    print "IMPOSTOS: ", impostos
    print "LIQUIDO: ", liquido
    print ""
    
    gravar = raw_input("Gravar estes valores? (s/n): ")
    gravar = str(gravar)
    
    if gravar == str("s"):
        grava_valores(data_l,bovespa,fund_value,n_nota,dn,ativo,quant,data_c,preco_c,data_v,preco_v,taxa_cblc,taxa_bov,corretagem,impostos,liquido)
    elif gravar == str("n"):
        print "erro na gravacao dos arquivos! O programa sera finalizado." 
    