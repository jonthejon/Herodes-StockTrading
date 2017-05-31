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
    

def atualizaStocks(bdin_name):
    
    nome_bdin = "pythonfiles/data_hist/" + bdin_name + ".csv"
    
    listaStock = bov.get_BD_symbols()
    header = ["Date","Open","High","Low","Close","Volume","Adj Close"]
    today_list = []
    try:
        reader = csv.reader(open(nome_bdin,'rU'),delimiter=',')
    except:
        print "Arquivo " + nome_bdin + " nao existe!"
        return
    
    for row in reader:
        for i in listaStock:
            stock_atual = i
            if stock_atual == row[0]:
                lista_atual = []
                abe = row[4]
                maxi = row[5]
                mini = row[6]
                fech = row[7]
                vol = row[8]
                fech2 = row[7]
                
                data_init = row[2]
                data = stripData(data_init)
                
                lista_atual.append(str(stock_atual))
                lista_atual.append(str(data))
                lista_atual.append(float(abe))
                lista_atual.append(float(maxi))
                lista_atual.append(float(mini))
                lista_atual.append(float(fech))
                lista_atual.append(float(vol))
                lista_atual.append(float(fech2))
                            
                today_list.append(lista_atual)
    
    # Teste para ver se algum arquivo estnao existe.            
    for i in today_list:
        nomeparateste = "C:/Python27/Lib/site-packages/QSTK/QSData/Ibovespa/" + i[0] + ".csv"
        try:
            reader = csv.reader(open(nomeparateste,'rU'),delimiter=',')
        except:
            print "Arquivo " + nomeparateste + " nao existe!"
            print "Planilhas NAO atualizadas!"
            return
    
    for i in today_list:
        st_file_name = "C:/Python27/Lib/site-packages/QSTK/QSData/Ibovespa/" + i[0] + ".csv"
        stock_hist = []
        reader = csv.reader(open(st_file_name,'rU'),delimiter=',')
        reader.next()
        
        for row in reader:
            stock_dia = []
            data = row[0]
            abe = row[1]
            maxi = row[2]
            mini = row[3]
            fech = row[4]
            vol = row[5]
            fech2 = row[6]
            
            stock_dia.append(data)
            stock_dia.append(abe)
            stock_dia.append(maxi)
            stock_dia.append(mini)
            stock_dia.append(fech)
            stock_dia.append(vol)
            stock_dia.append(fech2)
        
            stock_hist.append(stock_dia)
        
        
        last_day = i[1:]
        writer = csv.writer(open(st_file_name, 'wb'), delimiter=',')
        writer.writerow(header)
        writer.writerow(last_day)
        for j in stock_hist:
            writer.writerow(j)
    
    print "Planilhas atualizadas com sucesso!"
            
            
