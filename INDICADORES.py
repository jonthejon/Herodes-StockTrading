import numpy as np

def sharperatio(lista):
    
    nparray = np.array(lista)
    count = 0
    riskfree = 0
    invest = []
    
    for i in np.arange(len(nparray)-1):
        
        invest.append((float(nparray[i+1])/float(nparray[i])) - 1)
        count = count + 1
    
    invest = np.array(invest)
    excess = invest - riskfree
    med_excess = np.mean(excess)
    std_excess = np.std(excess,ddof=1)
    
    if std_excess == 0:
        std_excess = -0.000001
        sharpe = med_excess / std_excess
    elif std_excess <> 0:
        sharpe = med_excess / std_excess
    
    return sharpe

def sortinoratio(lista):
    
    nparray = np.array(lista)
    count = 0
    riskfree = 0
    invest = []
    
    for i in np.arange(len(nparray)-1):
        
        invest.append((float(nparray[i+1])/float(nparray[i])) - 1)
        count = count + 1
    
    invest = np.array(invest)
    excess = invest - riskfree
    
    excess_neg = []
    
    for i in excess:
        
        if i < 0:
            excess_neg.append(i)
    
    excess_neg = np.array(excess_neg)
    med_excess = np.average(excess)
    std_excess_neg = np.std(excess_neg,ddof=1)
    
    if std_excess_neg == 0:
        std_excess_neg = -0.000001
        sortino = med_excess / std_excess_neg
    elif std_excess_neg <> 0:
        sortino = med_excess / std_excess_neg
    
    return sortino

def calcula_alvo_perce(gain_c_v):
    
    percentual = 0.5
    #safe_alvo = 2
    #alvos_alvos = np.array(np.arange(0.002,0.053,0.005))
    #resultado_alvo = np.searchsorted(alvos_alvos,gain_c_v)-safe_alvo
    #item_alvo = -273
    alvo_final = gain_c_v * percentual
    
    #if alvo_final < 0.005:
        #alvo_final = 0.005
    #elif resultado_alvo >= 1:
        #item_alvo = resultado_alvo
        #alvo_alvo_f = alvos_alvos[item_alvo]
        
    return alvo_final

def mms(stock, period):
    
    peso = np.repeat(1.0,period)/period
    mms = np.convolve(stock,peso,'valid')
    
    return mms
    

def mme(stock, period):     
    
    #if len(stock) < 90:
        #raise ValueError("Input minimo de 90 dias!")    
    
    alpha = 2.0 / (period + 1.0)
    
    avg1 = np.average(stock[:period])
    
    mme = []
    
    actual_value = avg1
    
    for i in np.arange(len(stock)):
        if i <= period:
            mme.append(actual_value)
            continue
        actual_mme = ((stock[i] - actual_value) * alpha) + actual_value
        mme.append(round(actual_mme,3))
        actual_value = actual_mme
    
    return np.array(mme)

def macd(stock):
    
    mme_26 = mme(stock,26)
    mme_12 = mme(stock,12)
    dif_12_26 = mme_12 - mme_26
    signal = mme(dif_12_26,9)
    macd_symbol = dif_12_26 - signal
    
    return np.array(macd_symbol)

def new_macd(stock):
    
    mme_26 = mme(stock,26)
    mme_12 = mme(stock,12)
    dif_12_26 = mme_12 - mme_26
    signal = mme(dif_12_26,9)
    #macd_symbol = dif_12_26 - signal
    
    return np.array(dif_12_26), np.array(signal)

def get_macd_alvo(stock,direcao,macd_f_alvo):
    
    stock = list(stock)
    del stock[-1]
    vermelho_inic = 0.0
    
    if direcao > 0:
        
        delta_p = 0.01
        p_inic = stock[-1]
    
        for i in np.arange(10000):
            
            if vermelho_inic >= macd_f_alvo:
                return p_inic
            
            p_inic = p_inic + delta_p
            stock.append(p_inic)
            vermelho_array,azul_array = new_macd(stock)
            vermelho_inic = vermelho_array[-1]
            del stock[-1]
    
    elif direcao < 0:
                
        delta_p = -0.01
        p_inic = stock[-1]
        
        for i in np.arange(10000):
            
            if vermelho_inic <= macd_f_alvo:
                return p_inic
            
            p_inic = p_inic + delta_p
            stock.append(p_inic)
            vermelho_array,azul_array = new_macd(stock)
            vermelho_inic = vermelho_array[-1]
            del stock[-1]
            

def calculate_ifr(stock,period):
    
    ganhos = []
    perdas = []
    
    for i in np.arange(len(stock)-1):
        if stock[i+1] >= stock[i]:
            g_dummy = stock[i+1] - stock[i]
            p_dummy = 0.0
            ganhos.append(g_dummy)
            perdas.append(p_dummy)
        elif stock[i+1] < stock[i]:
            g_dummy = 0.0
            p_dummy = (stock[i+1]-stock[i])*(-1)
            ganhos.append(g_dummy)
            perdas.append(p_dummy)
    
    ganhos_array = np.array(ganhos)
    perdas_array = np.array(perdas)
    
    u_linha = ifr_assist(ganhos_array,period)
    d_linha = ifr_assist(perdas_array,period)
    
    rs = u_linha / d_linha
    
    ifr = (100 - (100 / (1+rs)))
    
    return np.array(ifr)


def ifr_assist(g_p,period):
    
    avg1 = np.average(g_p[:period])
    
    linha = []
    
    actual_value = avg1
    
    for i in np.arange(len(g_p)):
        if i <= period:
            linha.append(actual_value)
            continue
        actual_linha = ((actual_value * (period-1)) + g_p[i]) / period
        linha.append(actual_linha)
        actual_value = actual_linha
    
    return np.array(linha)

    
def get_ifr_final(stock,inicial_period):
    
    array_contagem = []
    cont = 0
    final_period = inicial_period
    ifr_atual = []
    
    for i in np.arange(50):
        ifr_atual = calculate_ifr(stock,final_period)
        
        for j in ifr_atual:
            if j >= 70 or j <= 30:
                cont = 1
                array_contagem.append(cont)
                continue
            cont = 0
            array_contagem.append(cont)
        
        uns = float(np.sum(array_contagem))
        total = float(len(array_contagem))
        percent = uns/total
        
        if percent >= 0.20:
            final_period = final_period + 1
            array_contagem = []
        elif percent < 0.20:
            final_period = final_period - 1
            ifr_atual = calculate_ifr(stock,final_period)
            break
    
    #print final_period
    return ifr_atual
        

def ifr(stock):
    
    inicial_period = 2
    ifr_final = get_ifr_final(stock,inicial_period)
    
    return ifr_final


def ssz(abertura,maximo,minimo,signal_d):
    
    if len(abertura) != len(maximo) or len(maximo) != len(minimo):
        raise ValueError("As arrays tem tamanhos diferentes!")    
    
    count_max = 0
    count_min = 0
    gordura = 1.5
    ssz_max = []
    ssz_min = []
    maximos = []
    minimos = []
    count_maximos = 0
    count_minimos = 0
    j = np.arange(len(abertura))
    j_invert = np.flipud(j)
    
    for i in j_invert:
        if count_max >= 5 and count_min >= 5:
            break
        if count_max < 5:
            if maximo[i] > maximo[i-1]:
                safe_zone_max = (maximo[i] - abertura[i]) * gordura
                ssz_max.append(safe_zone_max)
                count_max = count_max + 1
        if count_min < 5:
            if minimo[i] < minimo[i-1]:
                safe_zone_min = (abertura[i] - minimo[i]) * gordura
                ssz_min.append(safe_zone_min)
                count_min = count_min + 1
    
    for k in j_invert:
        if count_maximos >= 5 and count_minimos >= 5:
            break
        if count_maximos < 5:
            if maximo[k] > abertura[k]:
                margem = maximo[k] - abertura[k]
                maximos.append(margem)
                count_maximos = count_maximos + 1
        if count_minimos < 5:
            if minimo[k] < abertura[k]:
                margem = abertura[k] - minimo[k]
                minimos.append(margem)
                count_minimos = count_minimos + 1
    
    ssz_list = []
    
    zero_dummy = 0
    zeros = round(float(zero_dummy),2)
    
    ssz_vendido = round(float(np.average(ssz_max)),2)
    stop_vendido = round(float(ssz_vendido / abertura[-1]),4)
    gsz_vendido = round(float(np.average(minimos)),2)
    gain_vendido = round(float(gsz_vendido / abertura[-1]),4)
    
    ssz_comprado = round(float(np.average(ssz_min)),2)
    stop_comprado = round(float(ssz_comprado / abertura[-1]),4)
    gsz_comprado = round(float(np.average(maximos)),2)
    gain_comprado = round(float(gsz_comprado / abertura[-1]),4)
    
    if signal_d > 0:
        alvo_final = calcula_alvo_perce(gain_comprado)
        alvo_val_f = round(float(alvo_final * abertura[-1]),4)
        ssz_list.append(gain_comprado)
        ssz_list.append(gsz_comprado)
        ssz_list.append(alvo_final)
        ssz_list.append(alvo_val_f)
        ssz_list.append(zeros)
        ssz_list.append(stop_comprado)
        ssz_list.append(-ssz_comprado)
    elif signal_d < 0:
        alvo_final = calcula_alvo_perce(gain_vendido)
        alvo_final = alvo_final * (-1)
        alvo_val_f = round(float(alvo_final * abertura[-1]),4)
        ssz_list.append(gain_vendido)
        ssz_list.append(-gsz_vendido)
        ssz_list.append(alvo_final)
        ssz_list.append(alvo_val_f)
        ssz_list.append(zeros)
        ssz_list.append(stop_vendido)
        ssz_list.append(ssz_vendido)
    
    return ssz_list

def dadosSemanais(dataF):
    
    week_num = -1
    fechamento_s = []
    fech_dummy = 0.0
    
    for i in np.arange(len(dataF)):
        
        if dataF.index[i].isocalendar()[1] != week_num:
            fech_dummy = dataF.ix[i-1]
            valor = round(float(fech_dummy),2)
            fechamento_s.append(valor)
            week_num = dataF.index[i].isocalendar()[1]
            
            try:
                dummy_dummy = dataF.ix[i+1]
                continue
            except:
                fech_dummy = dataF.ix[i]
                valor = round(float(fech_dummy),2)
                fechamento_s.append(valor)
                week_num = dataF.index[i].isocalendar()[1]
                continue
        
        elif dataF.index[i].isocalendar()[1] == week_num:
            try:
                dummy_dummy = dataF.ix[i+1]
                continue
            except:
                fech_dummy = dataF.ix[i]
                valor = round(float(fech_dummy),2)
                fechamento_s.append(valor)
                week_num = dataF.index[i].isocalendar()[1]
                continue
    
    del fechamento_s[0]
    return np.array(fechamento_s)




def ssz2(abr,maxi,mini,fech,direcao):
    
    gordura_stop = 1.5
    
    if direcao > 0:
        
        stop_final_delta = (abr[-1] - mini[-1]) * gordura_stop
        stop_final_RS = round(float(abr[-1] - stop_final_delta),2)
        #alvo_p = get_macd_alvo(fech,direcao)
    
    elif direcao < 0:
        
        stop_final_delta = (maxi[-1] - abr[-1]) * gordura_stop
        stop_final_RS = round(float(abr[-1] + stop_final_delta),2)
        #alvo_p = get_macd_alvo(fech,direcao)
    
    
    ssz_list = []
        
    zero_dummy = 0
    zeros = round(float(zero_dummy),2)
    
    ssz_list.append(zeros)
    ssz_list.append(zeros)
    ssz_list.append(zeros)
    ssz_list.append(zeros)
    ssz_list.append(zeros)
    ssz_list.append(zeros)
    ssz_list.append(zeros)
    ssz_list.append(zeros)
    ssz_list.append(zeros)
    ssz_list.append(zeros)
    ssz_list.append(zeros)
    ssz_list.append(zeros)
    ssz_list.append(zeros)
    ssz_list.append(direcao)
    ssz_list.append(stop_final_RS)
    
    return ssz_list
