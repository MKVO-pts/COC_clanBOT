#modulos utilizados
from scrape import clan_full, individual, liga_atual, liga_info, guerra_logs, guerra_atual 
import json
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
    clan_profile ={ # info basica sobre o cla
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
    #print('Clan profile created!')

    



#info de todos os membros dp cla 
def prefil_individual(tag):
    function = individual(tag)
    dict_priv = dict(function)
    dict_individual = { # info simplificada
        'nome': dict_priv['name'],
        'centro_vila': dict_priv['townHallLevel'],
        'xp_lvl': dict_priv['expLevel'],
        'trufeus' : dict_priv['trophies'],
        'best_trf' : dict_priv['bestTrophies'],
        'estrelas_guerra' : dict_priv['warStars'],
        'atac_venc' : dict_priv['attackWins'],
        'defenseWins' : dict_priv['defenseWins'],
        'cv_noite' : dict_priv['builderHallLevel'],
        'trf_noite' : dict_priv['versusTrophies'],
        'best_trf_nt' : dict_priv['bestVersusTrophies'],
        'atac_venc_nt' : dict_priv['versusBattleWins'],
        'cla_lvl' : dict_priv['role'],
        'doacoes': dict_priv['donations'],
        'recebidas' : dict_priv['donationsReceived'],
        'cargo' : dict_priv['role'],
        'clan' : dict_priv['clan']['tag'],
        'tag' : dict_priv['tag'],
        '[+]': { #info obtida atravez das conquistas obtidas
            'total_doacoes' : dict_priv['achievements'][14]['value'],
            'all_war_stars' : dict_priv['achievements'][20]['value'],
            'all_league_stars' : dict_priv['achievements'][33]['value'],
            'all_clan_points' : dict_priv['achievements'][31]['value'],
            'all_atacs' : dict_priv['achievements'][12]['value'],
            'all_defense' : dict_priv['achievements'][13]['value'],
            'cvs_destruidos' : dict_priv['achievements'][10]['value'],            
            'ouro_ganho' : dict_priv['achievements'][5]['value'],
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
    guerra_dict = dict(guerra_atual())
    guerra_hist = dict(guerra_logs()) 
    #print(json.dumps(guerra_dict,indent=2))
    #print(json.dumps(guerra_hist,indent=4))

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