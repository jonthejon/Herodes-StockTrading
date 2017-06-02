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
