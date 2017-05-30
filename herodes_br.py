import herodes_go_daily as hero_go
import atualiza_stocks as atualiza
import administrativo as adm
import atualiza_ibovespa as atualiza_ibov
import herodes2_backtest as back
#import herodes2_backtest_g6 as back
#import salva_backtest2 as back
#import herodes2_backtest_lote as back
import analyze_herodes2 as analyze


def menu_backtest():
    
    print "--MENU BACKTEST--"
    print "1: BACKTEST"
    print "2: ANALISE"
    print ""
    
    entrada_menu = raw_input("Digite o numero do menu: ")
    entrada_menu = int(entrada_menu)    
    
    print ""

    if entrada_menu == 1:
        back.main_backtest()
    elif entrada_menu == 2:
        analyze.main_analyze() 

def menu_atualiza():
    
    print "--MENU BANCO DE DADOS--"
    print "1: ATUALIZAR DADOS DIARIOS"
    print "2: ATUALIZAR DADOS HISTORICOS"
    print ""
    
    entrada_menu = raw_input("Digite o numero do menu: ")
    entrada_menu = int(entrada_menu)    
    
    print ""

    if entrada_menu == 1:
        bdin_name = raw_input("Nome do arquivo CSV(extraido do BDIN): ")
        atualiza.atualizaStocks(bdin_name)
    elif entrada_menu == 2:
        atualiza_ibov.atualiza_ibovespa_main() 



def menu_algoritmo():
    
    print "--MENU ALGORITMOS--"
    print "1: HERODES 1"
    print "2: HERODES 2"
    print ""    
    
    entrada_menu = raw_input("Digite o numero do menu: ")
    entrada_menu = int(entrada_menu)    
    
    print ""    
    
    if entrada_menu == 1:
        
        pergunta = raw_input("Iniciar algoritmo com apresentacao da metodologia? (S/N): ")
        
        if pergunta == "S":
            hero_go.metodologia()
            output = hero_go.run_herodes()
        elif pergunta == "N":
            output = hero_go.run_herodes()
    
        for i in output.keys():
            print output[i]
            print ""
            
    elif entrada_menu == 2:
        
        pergunta = raw_input("Iniciar algoritmo com apresentacao da metodologia? (S/N): ")
        
        if pergunta == "S":
            hero_go.metodologia2()
            output2 = hero_go.run_herodes2()
        elif pergunta == "N":
            output2 = hero_go.run_herodes2()
    
        for i in output2.keys():
            print output2[i]
            print ""

def menu_administrativo():
    
    print "--MENU ADMINISTRATIVO--"
    print "1: ESTATISTICAS DO HERODES_BR"
    print "2: IMPOSTO DE RENDA DEVIDO"
    print "3: CADASTRAR DARF PAGO"
    print "4: CADASTRAR NOTA DE CORRETAGEM"
    print "5: CONSULTAR ALAVANCAGEM"
    print "6: CONSULTAR IR PAGOS"
    print "7: CONSULTAR SALDO DE PREJUIZOS"
    print "8: CONSULTAR TRANSACOES REALIZADAS"
    print ""

    entrada_menu = raw_input("Digite o numero do menu: ")
    entrada_menu = int(entrada_menu)

    print ""

    if entrada_menu == 1:
        adm.estatisticas()
    elif entrada_menu == 2:
        adm.ir_devido()
    elif entrada_menu == 3:
        adm.cadastrar_darf()
    elif entrada_menu == 4:
        adm.salva_nota_de_corretagem()
    elif entrada_menu == 5:
        adm.alavancagem()
    elif entrada_menu == 6:
        adm.consultar_ir_pagos()
    elif entrada_menu == 7:
        adm.consultar_saldo_preju()
    elif entrada_menu == 8:
        adm.consultar_transacoes()


print ""
print "--MENU HERODES_BR--"
print "1: ADMINISTRATIVO"
print "2: ATUALIZAR BANCO DE DADOS"
print "3: INICIAR ALGORITMOS"
print "4: BACKTEST"
print ""

entrada_menu = raw_input("Digite o numero do menu: ")
entrada_menu = int(entrada_menu)

print ""

if entrada_menu == 1:
    menu_administrativo()
elif entrada_menu == 2:
    menu_atualiza()
elif entrada_menu == 3:
    menu_algoritmo()
elif entrada_menu == 4:
    menu_backtest()
