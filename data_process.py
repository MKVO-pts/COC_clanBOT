#modulos utilizados
from scrape import clan_full, individual, liga_atual, liga_info, guerra_logs, guerra_atual 
import config
import json,os
#vamos ter os instantaneios e os demorados 
'''
memberlis:[
          {(abertura1)
               "tag": "#92RU8URLV",
               "name": "Sub Ninja",
               "role": "admin",
               "expLevel": 178,
               
               "league": {(abertura2)
                    "id": 29000016,
                    "name": "Champion League III",
               
                    "iconUrls": {(abertura3)
                         "small": "https://api-assets.clashofclans.com/leagues/72/JmmTbspV86xBigM7OP5_SjsEDPuE7oXjZC9aOy8xO3s.png",
                         "tiny": "https://api-assets.clashofclans.com/leagues/36/JmmTbspV86xBigM7OP5_SjsEDPuE7oXjZC9aOy8xO3s.png",
                         "medium": "https://api-assets.clashofclans.com/leagues/288/JmmTbspV86xBigM7OP5_SjsEDPuE7oXjZC9aOy8xO3s.png"
                    }(fecho3)
               
               },(fecho2)
               "trophies": 3288,
               "versusTrophies": 3659,
               "clanRank": 2,
               "previousClanRank": 2,
               "donations": 689,
               "donationsReceived": 0
          }(fecho1)

Resumo:
O fecho 0 é o que abre tudo e na verdade inclui toda a informacao relativa a cada membro do cla, este apenas representa um exemplo, 
logo o fecho 0 nao se encontra representado. Depois temos o fecho 1 que inclui a informacao individual de cada membro, vai ser usada
para criar os perfis individuais. O fecho numero dois inclui informacao relativa a liga em que o membro se encontra ("Champion League III"), 
daqui apenas interessa o nome da liga. O fecho 3 nao 

esquema do memberList

memberList (abertura0)
    abertura1(membro 1)
        data
        data
        abertura2
            data 
            data
            abertura3
                data
                data
                fecho3
            data
        fecho2
        data 
        data
        data
        decho1
    *proximo membro
    abertura 1(novo membro)
        data
        data
        ...

E assim se repete
'''

total_guerras = {}
clan_dic = clan_full()
def clan_profile(): 
    clan_info ={ # info basica sobre o cla
        'nome': clan_dic['name'],
        'nivel': clan_dic['clanLevel'],
        'liga': clan_dic['warLeague']['name'],
        'membros' : clan_dic['members'],
        'guerra_freq': clan_dic['warFrequency'],
        'total_guerras': clan_dic['warWins'] + clan_dic['warLosses'] + clan_dic['warTies'],
        'gueras_ganhas': clan_dic['warWins'],
        'guerras_perdidas': clan_dic['warLosses'],
        'guerras_empatadas': clan_dic['warTies'],
        'trufeus' : clan_dic['clanPoints'],
        'trufeus_vialnoite' : clan_dic['clanVersusPoints'],
        'hist_guerra': clan_dic['isWarLogPublic'],
        'tipo_entrada': clan_dic['type'],
        'min_trufeus' : clan_dic['requiredTrophies'],
        'pais': clan_dic['location']['name'],
        'descricao': clan_dic['description'],
        'tag': clan_dic['tag']
    }
    return clan_info
    #print('Clan profile created!')

    



#info de todos os membros dp cla 
def prefil_individual(tag):
    function = individual(tag)
    dict_priv = dict(function)
    dict_individual = { # info simplificada
        'Nome': dict_priv['name'],
        'Centro_vila': dict_priv['townHallLevel'],
        'xp_lvl': dict_priv['expLevel'],
        'Trufeus' : dict_priv['trophies'],
        'Recorde de Trufeus' : dict_priv['bestTrophies'],
        'estrelas_guerra' : dict_priv['warStars'],
        'Ataques Vencidos' : dict_priv['attackWins'],
        'Defesas Vencidas' : dict_priv['defenseWins'],
        'CV noite' : dict_priv['builderHallLevel'],
        'Trufeus noite' : dict_priv['versusTrophies'],
        'Recorde trufeus Noite' : dict_priv['bestVersusTrophies'],
        'Ataques Vencidos noite' : dict_priv['versusBattleWins'],
        'Tropas Doadas': dict_priv['donations'],
        'Tropas Doacoes Recebidas' : dict_priv['donationsReceived'],
        'Cargo' : dict_priv['role'],
        'Clan' : dict_priv['clan']['tag'],
        'tag' : dict_priv['tag'],
        '[+]': { #info obtida atravez das conquistas obtidas
            'Total_doacoes' : dict_priv['achievements'][14]['value'],
            'Estrelas de Guerra' : dict_priv['achievements'][20]['value'],
            'Estrelad de Liga' : dict_priv['achievements'][33]['value'],
            'Jogos do Cla pontos' : dict_priv['achievements'][31]['value'],
            'Total de ataques' : dict_priv['achievements'][12]['value'],
            'Total defesas' : dict_priv['achievements'][13]['value'],
            'CVs Destruidos' : dict_priv['achievements'][10]['value'],            
            'Ouro Ganho' : dict_priv['achievements'][5]['value'],
            'elixir_ganho' : dict_priv['achievements'][6]['value'],
            'elixir_negro' : dict_priv['achievements'][16]['value'],
            'ouro_castelo_clan' : dict_priv['achievements'][21]['value'],
            'battlepass_pontos' : dict_priv['achievements'][35]['value'],
            'rede_social' : dict_priv['achievements'][24]["completionInfo"],
            'supercell_id' : dict_priv['achievements'][34]["completionInfo"]
        }
    }
    return dict_individual
    #print(json.dumps(individual_profile, indent=3))

#transforma o war_logs em varios dicionarios com info basica sobre cada guerra
def guerras_complet():
    global total_guerras
    k = 0    
    x = 0
    guerra_hist = dict(guerra_logs()) 
    #print(json.dumps(guerra_hist,indent=4))
    print()
    for y in guerra_logs()['items']:
        try:
            guerra_base = {
                'genero': 'Guerra de cla',
                'resultado' : guerra_hist['items'][x]['result'],
                'clan_aliado': guerra_hist['items'][x]['clan']['name'],
                'num_equipa': guerra_hist['items'][x]['teamSize'],
                'ataques': guerra_hist['items'][x]['clan']['attacks'],
                'estrelas': guerra_hist['items'][x]['clan']['stars'],
                'percentagem': guerra_hist['items'][x]['clan']['destructionPercentage'],
                'xp': guerra_hist['items'][x]['clan']['expEarned'],
                'inimigo':{
                    'nome': guerra_hist['items'][x]['opponent']['name'],
                    'estrelas': guerra_hist['items'][x]['opponent']['stars'],
                    'percentagem': guerra_hist['items'][x]['opponent']['destructionPercentage']
                }
            }
        except KeyError: # ERROS:(ligas war)
            k += 1
            liga_war = { # dict base para a liga (evita o erro)
                'genero': 'Liga de cla',
                'resultado' : guerra_hist['items'][x]['result'],
                'clan_aliado' : guerra_hist['items'][x]['clan']['name'],
                'num_equipa': guerra_hist['items'][x]['teamSize'],
                'ataques' : guerra_hist['items'][x]['clan']['attacks'],
                'estrelas': guerra_hist['items'][x]['clan']['stars'],
                '%_destruicao': guerra_hist['items'][x]['clan']['destructionPercentage']
            }
            # adiciona ao dict total_guerras
            total_guerras[x] = liga_war
            #print('Liga ', k)
            
        else: #guerras normais
            total_guerras[x] = guerra_base # adiciona ao dict total_guerras 
            #print('Guerra ', x)
        finally: 
            #
            # passa ao proximo elemento
            x = x + 1
    return total_guerras


def guerra_profile():
    dict_war = dict(guerra_atual())
    profile_war = {
        'Estado': dict_war['state'],
        'Tamanho':'{num}x{num}'.format(num=dict_war['teamSize']),
        'Aliados': {
            'Nome': dict_war['clan']['name'],
            'Nivel': dict_war['clan']['clanLevel'],
            'Atacks': dict_war['clan']['attacks'],
            'Estrelas': dict_war['clan']['stars'],
            '%':dict_war['clan']['destructionPercentage']
        },
        'Inimigo': {
            'Nome': dict_war['opponent']['name'],
            'Nivel': dict_war['opponent']['clanLevel'],
            'Atacks': dict_war['opponent']['attacks'],
            'Estrelas': dict_war['opponent']['stars'],
            '%':dict_war['opponent']['destructionPercentage']
        }   
    }
    return profile_war



'''
atual = guerra_atual()

print(type(atual))

for key,value in atual.items():
    print(key)
#print(json.dumps(atual,indent=1))
''''''Keys:
state- important
teamSize (tamanho)
preparationStartTime (?inutil?)
startTime (?importante?)
endTime (?importante?)
clan - nao muito
opponent -important
'''









#print(json.dumps(total_guerras, indent=2))
'''
Deste ficheiro aproveitamos o Individual que
- 'guerras_complet()' -todo o historico de guerras
- clan_profile() - info basica sobre o cla 
- prefil_individual(tag) -info promenorizada sobre cada membro do cla 
'''
#for key, value in individual("#8Q0L2YGQ").items():
'''

ISTO E O INTRESSANTE QUE SE CONSEGUE OBTER ATRAVEZ DA ANALISE DAS ACHIVEMENTS:
#Total de obstaculos rmovidos  {3
#Ouro total roubado  {5
#Elixir total roubado  {6
#Muros totais destruidos  {9
#Quantidade de cvs destruidos  {10
#Total de batalhas ganhas  {12
#Total de defesas ganhas  {13
#total de doacoes des de sempre  {14
#total de exexir negro roubado  {16
#total de ouro reconlhido do castelo do cla  { 21
#Tem a conta ligada a uma rede social  {24
#total de pontos feitos pelo cla 31
#total de estrelas feitas na liga de clans  {33
#Tem supercell id ativado 34
#total de pontos feitos do battle pass 35




#tags de todos os membros
tags = []
#cria uma lista com todas as tags
for x in clan_dic['memberList']:
    tag = x['tag']
    tags.append(tag)
for key, value in individual("#8Q0L2YGQ").items():
    print(key)



#print(json.dumps(individual("#8Q0L2YGQ"), indent=4))'''



#FUNCTIONS
# para armazenar os membros em ficheiros json (precisa de update para trabaçlhar com diretorios)
def store(objective, filename,indt):
    with open('{}{}'.format(filename,'.json'),'w') as f:
        f.write(json.dumps(objective,indent=indt))
        f.close()

#cria um ficheiro para cada pessoa no cla
def individual_profile_update():
    os.chdir(config.individual_member_dir)
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
    os.chdir(config.individual_member_dir)
    for y in os.scandir():
        ex = str(y).replace('.json\'>','').replace('<DirEntry \'','')
        oldLista.append(ex)    
    return oldLista


