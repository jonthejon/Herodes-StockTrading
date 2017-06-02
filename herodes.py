import numpy as np
import pandas as pd
import INDICADORES as ind


def get_absolute(ndarray):
    
    absoluto = []
    
    for i in ndarray:
        
        atual = 0
        
        if i < 0:
            atual = i * (-1)
        elif i >= 0:
            atual = i
        
        absoluto.append(atual)
    
    return absoluto

def get_delta(mme_array):
    
    delta = []
    
    for i in np.arange(len(mme_array)-1):
        diff = mme_array[i+1] - mme_array[i]
        delta.append(diff)
    
    return delta

def get_signal(ndarray):

    signal = 0

    if ndarray[-1] < 0:
        signal = -1
    elif ndarray[-1] > 0:
        signal = 1
    elif ndarray[-1] == 0:
        if ndarray[-2] < 0:
            signal = -1
        elif ndarray[-2] > 0:
            signal = 1
        elif ndarray[-2] == 0:
            signal = 1
    
    return signal

def get_consist(ndarray,signal_d):
    
    binary = 0
    last_days = ndarray[len(ndarray)-4:]
    primes_array = np.array([3,5,7])
    peneira = []
    
    for i in np.arange(3):
        if signal_d > 0:
            if last_days[i] < last_days[i+1]:
                peneira.append(True)
            elif last_days[i] >= last_days[i+1]:
                peneira.append(False)
        if signal_d < 0:
            if last_days[i] > last_days[i+1]:
                peneira.append(True)
            elif last_days[i] <= last_days[i+1]:
                peneira.append(False)
    
    peneira_array = np.array(peneira)
    filtro = primes_array[peneira_array]
    
    if filtro.sum() > 8:
        binary = 1
    
    return binary

def herodes(frame_abe,frame_max,frame_min,frame_fech):
    
    n = 7
    datas = frame_fech.index
    colunas = ["Fech","MMEs","MMEd","MACD","IFR"]
    controle = 1
    pd_frame_dummy = 0
    abr = frame_abe.values
    maxi = frame_max.values
    mini = frame_min.values
    fech = frame_fech.values
    if fech[-1] < 9:
        controle = -1
        return controle,pd_frame_dummy
    
    d_semana_array = ind.dadosSemanais(frame_fech)
    MMEs = ind.mme(d_semana_array, 10)
    MMEd = ind.mme(fech, 20)
    delta_s = get_delta(MMEs)
    delta_d = get_delta(MMEd)
    signal_s = get_signal(delta_s)
    signal_d = get_signal(delta_d)

    # PRIMEIRO FILTRO: MMEs = MMEd
    if signal_d != signal_s:
        controle = -1
        return controle,pd_frame_dummy

    # SEGUNDO FILTRO: MINh < MMEh ou MAXh > MMEh
    if signal_d > 0:
        if mini[-1] > MMEd[-1]:
            #print "minimo nao rompeu MMEd"
            controle = -1
            return controle,pd_frame_dummy
    elif signal_d < 0:
        if maxi[-1] < MMEd[-1]:
            controle = -1
            return controle,pd_frame_dummy

    # TERCEIRO FILTRO: MACD com mesmo sinal da MMEdh ou proximo
    MACD = ind.macd(fech)
    signal_macd = get_signal(MACD)
    abs_macd = np.absolute(MACD)
    trigger = (ind.mme(abs_macd,10) / 3)    
    if signal_d != signal_macd and abs_macd[-1] > trigger[-1]:
        controle = -1
        return controle,pd_frame_dummy 

    # QUARTO FILTRO: IFR na faixa de seguranca (40<ifr<60)
    IFR = ind.ifr(fech)
    
    if IFR[-1] < 40 or IFR[-1] > 60:
        controle = -1
        return controle,pd_frame_dummy      
    

    # QUINTO FILTRO: consistencia minima do MACD
    binary = get_consist(MACD,signal_d)
    
    if binary == 0:
        controle = -1
        return controle,pd_frame_dummy
    
    # SEXTO FILTRO: consistencia minima da MMEs
    binary_s = get_consist(MMEs,signal_s)
    
    if binary_s == 0:
        controle = -1
        return controle,pd_frame_dummy
    
    
    
    #IFRs_alvos = []
    #IFR_alvo = IFR[len(IFR)-n:]
    #for i in np.arange(len(IFR_alvo)-1):
        #if signal_d > 0:
            #if IFR_alvo[i+1] > IFR_alvo[i]:
                #IFRs_alvos.append(IFR_alvo[i+1] - IFR_alvo[i])
                #continue
        #elif signal_d < 0:
            #if IFR_alvo[i+1] < IFR_alvo[i]:
                #IFRs_alvos.append(IFR_alvo[i+1] - IFR_alvo[i])
                #continue
    #IFRs_alvos_arr = np.array(IFRs_alvos)
    #ifr_delta = np.average(IFRs_alvos_arr)
    #novo_ifr = IFR_alvo[-1] + ifr_delta
    #novo_fech = list(fech)
    #delta_fech = 0.0
    #alvo_f_ifr = 0.0
    #fech_teste = list(novo_fech)
    #for i in np.arange(99999):
        #dummy_fech = fech_teste[-1]
        #fech_teste.append(fech_teste[-1])
        #if signal_d > 0:
            #del fech_teste[-1]
            #fech_teste.append(dummy_fech+delta_fech)
            #IFR_teste = ind.ifr(fech_teste)
            #if IFR_teste[-1] >= novo_ifr:
                #alvo_f_ifr = fech_teste[-1]
                #break
            #delta_fech = delta_fech + 0.01
        #elif signal_d < 0:
            #del fech_teste[-1]
            #fech_teste.append(dummy_fech-delta_fech)
            #IFR_teste = ind.ifr(fech_teste)
            #if IFR_teste[-1] <= novo_ifr:
                #alvo_f_ifr = fech_teste[-1]
                #break
            #delta_fech = delta_fech - 0.01      
    
    
    
    
    ssz = ind.ssz(abr,maxi,mini,signal_d)

    # o ativo passou por todos os filtros... devo retorna-lo mostrando os ultimos n dias atraves de um pandas dataframe
    
    indice = datas[len(datas)-n:]
    colunas = ["g%$/a%$/s%$","MMEs","MACD","IFR","MMEd","Fech"]
    fech_ret = fech[len(fech)-n:]
    MMEs_ret = MMEs[len(MMEs)-n:]
    MMEd_ret = MMEd[len(MMEd)-n:]
    MACD_ret = MACD[len(MACD)-n:]
    IFR_ret = IFR[len(IFR)-n:]

    corpo_dt = {'g%$/a%$/s%$':ssz, 'MMEs':MMEs_ret, 'MACD':MACD_ret, 'IFR':IFR_ret, 'MMEd':MMEd_ret, 'Fech':fech_ret}

    dataframe = pd.DataFrame(corpo_dt, columns=colunas, index=indice)

    return controle,dataframe
