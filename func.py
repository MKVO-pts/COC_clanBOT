from data_process import clan_profile , prefil_individual, guerras_complet #funcoes
from data_process import clan_dic, prefil_individual #variavel
from scrape import clan_full, individual, liga_info, liga_atual, guerra_atual, guerra_logs #funcoes diretas da api
import datetime
import time
import json
import re
import os
# Info
'''
Promenores sobre as funcoes importadas acima
'''
# para armazenar os membros em ficheiros json (precisa de update para trabaçlhar com diretorios)
def store(objective, filename,indt):
    with open('{}{}'.format(filename,'.json'),'w') as f:
        f.write(json.dumps(objective,indent=indt))
        f.close()

#cria um ficheiro para cada pessoa no cla
def individual_profile_update():
    os.chdir('C:\\Users\\Ricardo\\Code\\coc_bot\\realtime')
    for x in clan_dic['memberList']:
        #print(x) #toda a info antes de ser filtrada
        for key in x:
            #para cada 'tag' do cla, cria um ficheiro .json para cada membro
            if key == 'tag':
                store(prefil_individual(x[key]), prefil_individual(x[key])['tag'],3)
                #print('Perfil atualizado')
                #print(dt.prefil_individual(x[key])) #o que esta a ser guardado
def updater(tag):
    for m in clan_dic['memberList']:
        #print(m)
        for key in m:
            if key == 'tag':
                if m[key] == tag:
                    store(prefil_individual(m[key]), prefil_individual(m[key])['tag'],3)
def lista_actual(): #lista com os membros atuais 
    newLista = []
    for x in clan_dic['memberList']:
        for key in x:
            if key == 'tag':
                newLista.append(x[key])
    return newLista
def lista_antiga():
    oldLista = []
    os.chdir('C:\\Users\\Ricardo\\Code\\coc_bot\\realtime')
    for y in os.scandir():
        ex = str(y).replace('.json\'>','').replace('<DirEntry \'','')
        oldLista.append(ex)
    
    return oldLista
#funcao final 'verify'
def verify_main():
    old = lista_antiga()
    new = lista_actual()
    #print('Nem: ', new)     
    #print('Old: ', old)
    if old == new:
        print(datetime.datetime.now().strftime('%X'),'      No new members!', 'Updating members data')
    else:
        print(datetime.datetime.now().strftime('%X'),'      New members!','Adding new members data')               

    for x in new:
        if old == new:
            os.chdir('C:\\Users\\Ricardo\\Code\\coc_bot\\realtime')
            updater(x)
            print('Normal update')
        else:
            if len(old) > len(new): #apagar membros
                print(datetime.datetime.now().strftime('%X'),'  Removing the members that left...')
                for y in old:
                    if y not in new:
                        os.chdir('C:\\Users\\Ricardo\\Code\\coc_bot\\realtime')
                        os.remove('{dir}/{file}{f_type}'.format(file=y,f_type='.json',dir='C:\\Users\\Ricardo\\Code\\coc_bot\\'))
                        print(y)
            elif len(old) < len(new):# adicionar
                if x not in old:
                    os.chdir('C:\\Users\\Ricardo\\Code\\coc_bot\\realtime')
                    updater(x)
                    os.chdir('C:\\Users\\Ricardo\\Code\\coc_bot\\bank')
                    updater(x)
                    print(datetime.datetime.now().strftime('%X'), 'New profile added to the bank: ´{}´'.format(x))
            else:
                print('SOmething went rong ://')
#individual_profile_update()

#verifica se existem alteracoes e se houver atualiza o ficheiro
def war_logs():
    os.chdir('C:\\Users\\Ricardo\\Code\\coc_bot\\guerras') #muda o diretorio
    new = guerras_complet() #dicionario com os 'war_logs'
    #abre o feicheiro e verifica se existem diferencas
    with open('guerras.json') as f:
        ler = json.load(f)
        print('Outdated data:', len(ler),'  Updated data:',len(new))

        if len(new) == len(ler):
            print('No need to updated!')            
        elif len(new) > len(ler):
            print('Updatting war logs...')
            store(guerras_complet(),'guerras',1)
        else:
            print('Something went badddd!')
verify_main()