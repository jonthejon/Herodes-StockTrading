import csv
import datetime as dt
import numpy as np

def create_files(stocks_names):
    
    header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
    
    lista_arquivos = []
    
    for i in stocks_names:
        
        file_out = "pythonfiles/data_hist/" + i + ".csv"
        writer = csv.writer(open(file_out, 'wb'), delimiter=',')
        writer.writerow(header)
        
        lista_arquivos.append(file_out)
        
    return lista_arquivos

def atualiza_ibovespa_main():
    
    names_list = ['pythonfiles/data_hist/BANCO DE DADOS/2010e2011.csv', 'pythonfiles/data_hist/BANCO DE DADOS/2012.csv', 'pythonfiles/data_hist/BANCO DE DADOS/2013.csv', 'pythonfiles/data_hist/BANCO DE DADOS/2014.csv']
    num_ativos = raw_input("Digite o numero de novos ativos: ")
    num_ativos = int(num_ativos)
    
    nova_array = np.array(np.arange(num_ativos))
    
    stocks_names = []
    
    print ""
    
    for i in nova_array:
        ativo = raw_input("digite o nome do ativo: ")
        stocks_names.append(str(ativo))
    
    lista_files = create_files(stocks_names)
    
    for z in names_list:
        
        count_ativos = -1
        
        for i in lista_files:
            
            count_ativos = count_ativos + 1
            
            reader1 = csv.reader(open(i,'rU'),delimiter=',')
            header = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
            reader1.next()
            
            fileiras = []
            
            for row in reader1:
                
                stock_dia = []
                data_atual = row[0]
                aber_atual = row[1]
                maxi_atual = row[2]
                mini_atual = row[3]
                fech_atual = row[4]
                volume_atual = row[5]
                adjfech_atual = row[6]
                
                stock_dia.append(data_atual)
                stock_dia.append(aber_atual)
                stock_dia.append(maxi_atual)
                stock_dia.append(mini_atual)
                stock_dia.append(fech_atual)
                stock_dia.append(volume_atual)
                stock_dia.append(adjfech_atual)
                
                fileiras.append(stock_dia)
            
            stock_ind = stocks_names[count_ativos]
            data = str()
            aber = str()
            maxi = str()
            mini = str()
            fech = str()
            volume = str()
            adjfech = str()    
            fileira_hist = []
            
            reader2 = csv.reader(open(z,'rU'),delimiter=',')
            
            for row in reader2:
                
                stock_entrar = []
                stock_real = str(row[0])
                if stock_real == stock_ind:
                    data = row[1]
                    aber = row[2]
                    maxi = row[3]
                    mini = row[4]
                    fech = row[5]
                    volume = row[6]
                    adjfech = row[7]
                    
                    stock_entrar.append(data)
                    stock_entrar.append(aber)
                    stock_entrar.append(maxi)
                    stock_entrar.append(mini)
                    stock_entrar.append(fech)
                    stock_entrar.append(volume)
                    stock_entrar.append(adjfech)
                    
                    fileira_hist.append(stock_entrar) 
            
            file_final = i
            writer = csv.writer(open(file_final, 'wb'), delimiter=',')
            writer.writerow(header)
            
            for j in fileira_hist:
                
                writer.writerow(j)
            
            for h in fileiras:
                
                writer.writerow(h)
        
    print ""
    print "Os arquivos foram salvos com SUCESSO em /pythonfiles/data_hist/"