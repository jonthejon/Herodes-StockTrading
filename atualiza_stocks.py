import numpy as np
import csv
import sys
import BOVESPA as bov
import datetime as dt

def stripData(string_data):
    
    m_ext = string_data[0:2]
    d_ext = string_data[3:5]
    y_ext = string_data[6:]
    
    int_m_ext = int(m_ext)
    int_d_ext = int(d_ext)
    int_y_ext = int(y_ext)
    
    traco = "-"
    
    str_m_ext = str(int_m_ext)
    str_d_ext = str(int_d_ext)
    int_y_ext = str(int_y_ext)
    
    data_f = int_y_ext + traco + str_m_ext + traco + str_d_ext
    
    return data_f
    

