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


def herodes2(frame_abe,frame_max,frame_min,frame_fech,proibido):
    
    n = 15
    datas = frame_fech.index
    controle = 1
    pd_frame_dummy = 0
    abr = frame_abe.values
    maxi = frame_max.values
    mini = frame_min.values
    fech = frame_fech.values
    if fech[-1] < 9:
        controle = -1
        return controle,pd_frame_dummy
    
    MMSd = ind.mms(fech, 24)
    MMEd = ind.mme(fech, 24)
    delta_mms = get_delta(MMSd)
    delta_mme = get_delta(MMEd)
    signal_d = get_signal(delta_mme)
    direcao = 0
    
    #if signal_d < 0:
        
        #controle = -1
        #return controle,pd_frame_dummy

    
    vermelho,azul = ind.new_macd(fech)
    
    if azul[-1] < 0:
        direcao = -1
    elif azul[-1] >= 0:
        direcao = 1
        
    # controle para proibir operacoes short
    if direcao < 0:
        if proibido < 0:
            direcao = direcao * (-1)
        elif proibido > 0:
            direcao = direcao * (1)
        
    # PRIMEIRO FILTRO: MACD-S quebra a barreira do 0.0
    if direcao > 0:
        if azul[-1] < 0 or azul[-1] >= 0 and azul[-2] >= 0 or azul[-1] >= 0 and vermelho[-1] >= 0.5:
            controle = -1
            return controle,pd_frame_dummy
    elif direcao < 0:
        if azul[-1] > 0 or azul[-1] <= 0 and azul[-2] <= 0 or azul[-1] <= 0 and vermelho[-1] <= -0.5:
            controle = -1
            return controle,pd_frame_dummy
    
    IFR = ind.ifr(fech)
    
    # FILTROS DE GAIN
    
    sentido_deltas = delta_mme
    sentido_alvo = get_signal(sentido_deltas)
    bin_filtro_for_cv = get_consist(MMEd,sentido_alvo)
    bin_filtro_f_mme = get_consist(delta_mme,sentido_alvo)
    macd_f_abs = get_absolute(vermelho)
    teste_max_macd_hist = max(macd_f_abs[len(macd_f_abs)-n:])
    teste_init_macd = abs(vermelho[-1])
    
    # FILTRO 1 DE GAIN: eh preciso ter consistencia tanto no mmed quanto no delta do mmed
    if bin_filtro_for_cv != 1 or bin_filtro_f_mme != 1:
        controle = -1
        return controle,pd_frame_dummy
    
    # FILTRO 2 DE GAIN: eh proibido operar ativos onde o macd-f inicial eh o maximo do escopo
    if teste_init_macd >= teste_max_macd_hist:
        controle = -1
        return controle,pd_frame_dummy
    
    #if signal_d > 0:
        
        #if azul[-1] < 0 or azul[-1] >= 0 and azul[-2] >= 0 or azul[-1] >= 0 and vermelho[-1] >= 0.5:
            #controle = -1
            #return controle,pd_frame_dummy
    
    #elif signal_d < 0:
        
        #if azul[-1] > 0 or azul[-1] <= 0 and azul[-2] <= 0 or azul[-1] <= 0 and vermelho[-1] <= -0.5:
            #controle = -1
            #return controle,pd_frame_dummy
    
    
    ssz = ind.ssz2(abr,maxi,mini,fech,direcao)

    # o ativo passou por todos os filtros... devo retorna-lo mostrando os ultimos n dias atraves de um pandas dataframe
    
    indice = datas[len(datas)-n:]
    colunas = ["stop$","MACD-S","MACD-F","MME","MME_delta","MMS","MMS_delta","abertura","IFR"]
    MACDS_ret = azul[len(azul)-n:]
    MACDF_ret = vermelho[len(vermelho)-n:]
    MME_ret = MMEd[len(MMEd)-n:]
    MMEd_ret = delta_mme[len(delta_mme)-n:]
    MMS_ret = MMSd[len(MMSd)-n:]
    MMSd_ret = delta_mms[len(delta_mms)-n:]
    abe_ret = abr[len(abr)-n:]
    IFR_ret = IFR[len(IFR)-n:]
    
    
    corpo_dt = {'stop$':ssz, 'MACD-S':MACDS_ret, 'MACD-F':MACDF_ret, 'MME':MME_ret, 'MME_delta':MMEd_ret, 'MMS':MMS_ret, 'MMS_delta':MMSd_ret, 'abertura':abe_ret, 'IFR':IFR_ret}

    dataframe = pd.DataFrame(corpo_dt, columns=colunas, index=indice)

    return controle,dataframe


def herodes2_total(frame_abe,frame_max,frame_min,frame_fech,proibido):
    
    n = 15
    datas = frame_fech.index
    controle = 1
    pd_frame_dummy = 0
    abr = frame_abe.values
    maxi = frame_max.values
    mini = frame_min.values
    fech = frame_fech.values
    if fech[-1] < 9:
        controle = -1
        return controle,pd_frame_dummy
    
    MMSd = ind.mms(fech, 24)
    MMEd = ind.mme(fech, 24)
    delta_mms = get_delta(MMSd)
    delta_mme = get_delta(MMEd)
    signal_d = get_signal(delta_mme)
    direcao = 0
    
    #if signal_d < 0:
        
        #controle = -1
        #return controle,pd_frame_dummy

    
    vermelho,azul = ind.new_macd(fech)
    
    if azul[-1] < 0:
        direcao = -1
    elif azul[-1] >= 0:
        direcao = 1
        
    # controle para proibir operacoes short
    if direcao < 0:
        if proibido < 0:
            direcao = direcao * (-1)
        elif proibido > 0:
            direcao = direcao * (1)
        
    # PRIMEIRO FILTRO: MACD-S quebra a barreira do 0.0
    if direcao > 0:
        if azul[-1] < 0 or azul[-1] >= 0 and azul[-2] >= 0 or azul[-1] >= 0 and vermelho[-1] >= 0.5:
            controle = -1
            return controle,pd_frame_dummy
    elif direcao < 0:
        if azul[-1] > 0 or azul[-1] <= 0 and azul[-2] <= 0 or azul[-1] <= 0 and vermelho[-1] <= -0.5:
            controle = -1
            return controle,pd_frame_dummy
    
    IFR = ind.ifr(fech)
    
    '''# FILTROS DE GAIN
    
    sentido_deltas = delta_mme
    sentido_alvo = get_signal(sentido_deltas)
    bin_filtro_for_cv = get_consist(MMEd,sentido_alvo)
    bin_filtro_f_mme = get_consist(delta_mme,sentido_alvo)
    macd_f_abs = get_absolute(vermelho)
    teste_max_macd_hist = max(macd_f_abs[len(macd_f_abs)-n:])
    teste_init_macd = abs(vermelho[-1])
    
    # FILTRO 1 DE GAIN: eh preciso ter consistencia tanto no mmed quanto no delta do mmed
    if bin_filtro_for_cv != 1 or bin_filtro_f_mme != 1:
        controle = -1
        return controle,pd_frame_dummy
    
    # FILTRO 2 DE GAIN: eh proibido operar ativos onde o macd-f inicial eh o maximo do escopo
    if teste_init_macd >= teste_max_macd_hist:
        controle = -1
        return controle,pd_frame_dummy'''
    
    #if signal_d > 0:
        
        #if azul[-1] < 0 or azul[-1] >= 0 and azul[-2] >= 0 or azul[-1] >= 0 and vermelho[-1] >= 0.5:
            #controle = -1
            #return controle,pd_frame_dummy
    
    #elif signal_d < 0:
        
        #if azul[-1] > 0 or azul[-1] <= 0 and azul[-2] <= 0 or azul[-1] <= 0 and vermelho[-1] <= -0.5:
            #controle = -1
            #return controle,pd_frame_dummy
    
    
    ssz = ind.ssz2(abr,maxi,mini,fech,direcao)

    # o ativo passou por todos os filtros... devo retorna-lo mostrando os ultimos n dias atraves de um pandas dataframe
    
    indice = datas[len(datas)-n:]
    colunas = ["stop$","MACD-S","MACD-F","MME","MME_delta","MMS","MMS_delta","abertura","IFR"]
    MACDS_ret = azul[len(azul)-n:]
    MACDF_ret = vermelho[len(vermelho)-n:]
    MME_ret = MMEd[len(MMEd)-n:]
    MMEd_ret = delta_mme[len(delta_mme)-n:]
    MMS_ret = MMSd[len(MMSd)-n:]
    MMSd_ret = delta_mms[len(delta_mms)-n:]
    abe_ret = abr[len(abr)-n:]
    IFR_ret = IFR[len(IFR)-n:]
    
    corpo_dt = {'stop$':ssz, 'MACD-S':MACDS_ret, 'MACD-F':MACDF_ret, 'MME':MME_ret, 'MME_delta':MMEd_ret, 'MMS':MMS_ret, 'MMS_delta':MMSd_ret, 'abertura':abe_ret, 'IFR':IFR_ret}

    dataframe = pd.DataFrame(corpo_dt, columns=colunas, index=indice)

    return controle,dataframe

def herodes2_sem_filtro(frame_abe,frame_max,frame_min,frame_fech):
    
    n = 15
    datas = frame_fech.index
    #controle = 1
    #pd_frame_dummy = 0
    abr = frame_abe.values
    maxi = frame_max.values
    mini = frame_min.values
    fech = frame_fech.values
    #if fech[-1] < 9:
        #controle = -1
        #return controle,pd_frame_dummy
    
    MMSd = ind.mms(fech, 24)
    MMEd = ind.mme(fech, 24)
    delta_mms = get_delta(MMSd)
    delta_mme = get_delta(MMEd)
    signal_d = get_signal(delta_mme)
    direcao = 0
    
    #if signal_d < 0:
        
        #controle = -1
        #return controle,pd_frame_dummy

    
    vermelho,azul = ind.new_macd(fech)
    
    if azul[-1] < 0:
        direcao = -1
    elif azul[-1] >= 0:
        direcao = 1
        
    # controle para proibir operacoes short
    #if direcao < 0:
        #if proibido < 0:
            #direcao = direcao * (-1)
        #elif proibido > 0:
            #direcao = direcao * (1)
        
    # PRIMEIRO FILTRO: MACD-S quebra a barreira do 0.0
    #if direcao > 0:
        #if azul[-1] < 0 or azul[-1] >= 0 and azul[-2] >= 0 or azul[-1] >= 0 and vermelho[-1] >= 0.5:
            #controle = -1
            #return controle,pd_frame_dummy
    #elif direcao < 0:
        #if azul[-1] > 0 or azul[-1] <= 0 and azul[-2] <= 0 or azul[-1] <= 0 and vermelho[-1] <= -0.5:
            #controle = -1
            #return controle,pd_frame_dummy
    
    #if signal_d > 0:
        
        #if azul[-1] < 0 or azul[-1] >= 0 and azul[-2] >= 0 or azul[-1] >= 0 and vermelho[-1] >= 0.5:
            #controle = -1
            #return controle,pd_frame_dummy
    
    #elif signal_d < 0:
        
        #if azul[-1] > 0 or azul[-1] <= 0 and azul[-2] <= 0 or azul[-1] <= 0 and vermelho[-1] <= -0.5:
            #controle = -1
            #return controle,pd_frame_dummy
    
    
    ssz = ind.ssz2(abr,maxi,mini,fech,direcao)

    # o ativo passou por todos os filtros... devo retorna-lo mostrando os ultimos n dias atraves de um pandas dataframe
    
    indice = datas[len(datas)-n:]
    colunas = ["stop$","MACD-S","MACD-F","MME","MME_delta","MMS","MMS_delta","abertura"]
    MACDS_ret = azul[len(azul)-n:]
    MACDF_ret = vermelho[len(vermelho)-n:]
    MME_ret = MMEd[len(MMEd)-n:]
    MMEd_ret = delta_mme[len(delta_mme)-n:]
    MMS_ret = MMSd[len(MMSd)-n:]
    MMSd_ret = delta_mms[len(delta_mms)-n:]
    abe_ret = abr[len(abr)-n:]
    
    corpo_dt = {'stop$':ssz, 'MACD-S':MACDS_ret, 'MACD-F':MACDF_ret, 'MME':MME_ret, 'MME_delta':MMEd_ret, 'MMS':MMS_ret, 'MMS_delta':MMSd_ret, 'abertura':abe_ret}

    dataframe = pd.DataFrame(corpo_dt, columns=colunas, index=indice)

    return dataframe


def herodes2_macd_f(frame_abe,frame_max,frame_min,frame_fech):
    
    n = 15
    datas = frame_fech.index
    #controle = 1
    pd_frame_dummy = 0
    abr = frame_abe.values
    maxi = frame_max.values
    mini = frame_min.values
    fech = frame_fech.values
    #if fech[-1] < 9:
        #controle = -1
        #return controle,pd_frame_dummy
    
    MMSd = ind.mms(fech, 24)
    MMEd = ind.mme(fech, 24)
    delta_mms = get_delta(MMSd)
    delta_mme = get_delta(MMEd)
    signal_d = get_signal(delta_mme)
    #direcao = 0
    
    #if signal_d < 0:
        
        #controle = -1
        #return controle,pd_frame_dummy

    # PRIMEIRO FILTRO: MACD-S quebra a barreira do 0.0
    vermelho,azul = ind.new_macd(fech)
    minimo_hoje = mini[-1]
    
    #if azul[-1] < 0 or azul[-1] >= 0 and azul[-2] >= 0 or azul[-1] >= 0 and vermelho[-1] >= 0.5:
        #controle = -1
        #return controle,pd_frame_dummy
    
    #if azul[-1] < 0:
        #direcao = -1
    #elif azul[-1] > 0:
        #direcao = 1
    
    #if signal_d > 0:
        
        #if azul[-1] < 0 or azul[-1] >= 0 and azul[-2] >= 0 or azul[-1] >= 0 and vermelho[-1] >= 0.5:
            #controle = -1
            #return controle,pd_frame_dummy
    
    #elif signal_d < 0:
        
        #if azul[-1] > 0 or azul[-1] <= 0 and azul[-2] <= 0 or azul[-1] <= 0 and vermelho[-1] <= -0.5:
            #controle = -1
            #return controle,pd_frame_dummy
    
    
    #ssz = ind.ssz2(abr,maxi,mini,fech,direcao)

    # o ativo passou por todos os filtros... devo retorna-lo mostrando os ultimos n dias atraves de um pandas dataframe
    
    #indice = datas[len(datas)-n:]
    #colunas = ["stop$","MACD-S","MACD-F","MME","MME_delta","MMS","MMS_delta","abertura"]
    #MACDS_ret = azul[len(azul)-n:]
    #MACDF_ret = vermelho[len(vermelho)-n:]
    #MME_ret = MMEd[len(MMEd)-n:]
    #MMEd_ret = delta_mme[len(delta_mme)-n:]
    #MMS_ret = MMSd[len(MMSd)-n:]
    #MMSd_ret = delta_mms[len(delta_mms)-n:]
    #abe_ret = abr[len(abr)-n:]
    
    #corpo_dt = {'stop$':ssz, 'MACD-S':MACDS_ret, 'MACD-F':MACDF_ret, 'MME':MME_ret, 'MME_delta':MMEd_ret, 'MMS':MMS_ret, 'MMS_delta':MMSd_ret, 'abertura':abe_ret}

    #dataframe = pd.DataFrame(corpo_dt, columns=colunas, index=indice)

    return vermelho,azul,minimo_hoje

def herodes2_lote(frame_abe,frame_max,frame_min,frame_fech,proibido):
    
    n = 15
    datas = frame_fech.index
    controle = 1
    pd_frame_dummy = 0
    abr = frame_abe.values
    maxi = frame_max.values
    mini = frame_min.values
    fech = frame_fech.values 
    
    if fech[-1] < 9:
        controle = -1
        return controle,pd_frame_dummy
    
    MMSd = ind.mms(fech, 24)
    MMEd = ind.mme(fech, 24)
    delta_mms = get_delta(MMSd)
    delta_mme = get_delta(MMEd)
    signal_d = get_signal(delta_mme)
    direcao = 0
    
    #if signal_d < 0:
        
        #controle = -1
        #return controle,pd_frame_dummy

    
    vermelho,azul = ind.new_macd(fech)
    
    if azul[-1] < 0:
        direcao = -1
    elif azul[-1] >= 0:
        direcao = 1
        
    # controle para proibir operacoes short
    if direcao < 0:
        if proibido < 0:
            direcao = direcao * (-1)
        elif proibido > 0:
            direcao = direcao * (1)
        
    # PRIMEIRO FILTRO: MACD-S quebra a barreira do 0.0
    if direcao > 0:
        if azul[-1] < 0 or azul[-1] >= 0 and azul[-2] >= 0 or azul[-1] >= 0 and vermelho[-1] >= 0.5:
            controle = -1
            return controle,pd_frame_dummy
    elif direcao < 0:
        if azul[-1] > 0 or azul[-1] <= 0 and azul[-2] <= 0 or azul[-1] <= 0 and vermelho[-1] <= -0.5:
            controle = -1
            return controle,pd_frame_dummy
    
    IFR = ind.ifr(fech)
    
    # FILTROS DE GAIN
    
    sentido_deltas = delta_mme
    sentido_alvo = get_signal(sentido_deltas)
    bin_filtro_for_cv = get_consist(MMEd,sentido_alvo)
    bin_filtro_f_mme = get_consist(delta_mme,sentido_alvo)
    macd_f_abs = get_absolute(vermelho)
    teste_max_macd_hist = max(macd_f_abs[len(macd_f_abs)-n:])
    teste_init_macd = abs(vermelho[-1])
    
    # FILTRO 1 DE GAIN: eh preciso ter consistencia tanto no mmed quanto no delta do mmed
    if bin_filtro_for_cv != 1 or bin_filtro_f_mme != 1:
        controle = -1
        return controle,pd_frame_dummy
    
    # FILTRO 2 DE GAIN: eh proibido operar ativos onde o macd-f inicial eh o maximo do escopo
    if teste_init_macd >= teste_max_macd_hist:
        controle = -1
        return controle,pd_frame_dummy
    
    #if signal_d > 0:
        
        #if azul[-1] < 0 or azul[-1] >= 0 and azul[-2] >= 0 or azul[-1] >= 0 and vermelho[-1] >= 0.5:
            #controle = -1
            #return controle,pd_frame_dummy
    
    #elif signal_d < 0:
        
        #if azul[-1] > 0 or azul[-1] <= 0 and azul[-2] <= 0 or azul[-1] <= 0 and vermelho[-1] <= -0.5:
            #controle = -1
            #return controle,pd_frame_dummy
    
    
    ssz = ind.ssz2(abr,maxi,mini,fech,direcao)

    # o ativo passou por todos os filtros... devo retorna-lo mostrando os ultimos n dias atraves de um pandas dataframe
    
    indice = datas[len(datas)-n:]
    colunas = ["stop$","MACD-S","MACD-F","MME","MME_delta","MMS","MMS_delta","abertura","IFR"]
    MACDS_ret = azul[len(azul)-n:]
    MACDF_ret = vermelho[len(vermelho)-n:]
    MME_ret = MMEd[len(MMEd)-n:]
    MMEd_ret = delta_mme[len(delta_mme)-n:]
    MMS_ret = MMSd[len(MMSd)-n:]
    MMSd_ret = delta_mms[len(delta_mms)-n:]
    abe_ret = abr[len(abr)-n:]
    IFR_ret = IFR[len(IFR)-n:]
    
    
    corpo_dt = {'stop$':ssz, 'MACD-S':MACDS_ret, 'MACD-F':MACDF_ret, 'MME':MME_ret, 'MME_delta':MMEd_ret, 'MMS':MMS_ret, 'MMS_delta':MMSd_ret, 'abertura':abe_ret, 'IFR':IFR_ret}

    dataframe = pd.DataFrame(corpo_dt, columns=colunas, index=indice)

    return controle,dataframe

def herodes3(frame_abe,frame_max,frame_min,frame_fech,proibido):
    
    n = 15
    datas = frame_fech.index
    controle = 1
    pd_frame_dummy = 0
    abr = frame_abe.values
    maxi = frame_max.values
    mini = frame_min.values
    fech = frame_fech.values
    
    # FILTRO ZERO: nao operar nenhum ativo com valor menor que 9
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
    
    # PRIMEIRO FILTRO: direcao da MMEs = direcao da MMEd
    if signal_d != signal_s:
        controle = -1
        return controle,pd_frame_dummy
    
    # FILTRO EXTRA: proibido operar vendido
    if proibido < 0:
        if signal_d < 0:
            controle = -1
            return controle,pd_frame_dummy
    
    # FILTRO 2/3: MMEd cruza MMEs e mantem uma consistencia de mais 1 dia
    if signal_d > 0:
        if MMEd[-2] >= MMEs[-2] and MMEd[-3] < MMEs[-3]:
            delta_mm_1 = MMEd[-1] - MMEs[-1]
            delta_mm_2 = MMEd[-2] - MMEs[-2]
            if delta_mm_1 > delta_mm_2:
                pass
            else:
                controle = -1
                return controle,pd_frame_dummy                
        else:
            controle = -1
            return controle,pd_frame_dummy
        
    if signal_d < 0:
        if MMEd[-2] <= MMEs[-2] and MMEd[-3] > MMEs[-3]:
            delta_mm_1 = MMEd[-1] - MMEs[-1]
            delta_mm_2 = MMEd[-2] - MMEs[-2]
            if delta_mm_1 < delta_mm_2:
                pass
            else:
                controle = -1
                return controle,pd_frame_dummy                
        else:
            controle = -1
            return controle,pd_frame_dummy    


    
    
    
    #ssz = ind.ssz(abr,maxi,mini,signal_d)
    ssz = ind.ssz2(abr,maxi,mini,fech,signal_d)

    # o ativo passou por todos os filtros... devo retorna-lo mostrando os ultimos n dias atraves de um pandas dataframe
    
    indice = datas[len(datas)-n:]
    colunas = ["stop$","Abe","Fech","MMEs","MMEd"]
    fech_ret = fech[len(fech)-n:]
    abre_ret = abr[len(abr)-n:]
    MMEs_ret = MMEs[len(MMEs)-n:]
    MMEd_ret = MMEd[len(MMEd)-n:]

    corpo_dt = {'stop$':ssz, 'Abe':abre_ret, 'Fech':fech_ret, 'MMEs':MMEs_ret, 'MMEd':MMEd_ret}

    dataframe = pd.DataFrame(corpo_dt, columns=colunas, index=indice)

    return controle,dataframe
