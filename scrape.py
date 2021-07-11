import requests
import re
import json
import random
import config
#INFORMATION
'''
O .json recebito tem 20 pares de key,value:
1  [tag] tag do cla
2  [name] nome do cla
3  [type] convite, aberto ...
4  [description] descricao do cla 
5  [location] localizacao 
6  [badgeUrls] ??
7  [clanLevel] nivel do cla 
8  [clanPoints] pontos do cla ?? na guerra?
9  [clanVersusPoints] cla inimigo ?? na guerra??
10 [requiredTrophies] minimo de trufeus 
11 [warFrequency] always
12 [warWinStreak] 1
13 [warWins] N total de guerras vencidas
14 [warTies]  Numero total de guerras empatadas
15 [warLosses] numero total de guerras perdidas
16 [isWarLogPublic] Diz se o registo de guerra é publico ou nao
17 [warLeague] {'id': 48000007, 'name': 'Gold League III'} / liga em que o cla está
18 [members] Quantidade total de membros 
19 [memberList] Lista com informacao sobre todos os membros 
20 [labels] ???3 quadrados que definem o cla ????

Metodos relativos ao individual(cada membro):
[tag]
[name]
[townHallLevel]
[townHallWeaponLevel]
[expLevel]
[trophies]
[bestTrophies]
[warStars]
[attackWins]
[defenseWins]
[builderHallLevel]
[versusTrophies]
[bestVersusTrophies]
[versusBattleWins]
[role]
[donations]
[donationsReceived]
[clan]
[league]
[achievements]
[versusBattleWinCount]
[labels]
[troops]
[heroes]
[spells]
'''

clan_tag = config.clanTag

api_key = config.api__key


trans_tag = re.sub('[#]','%23',clan_tag) #troca o '#' por '%23'

verification = {
        'Accept': 'application/json',
        'authorization': 'Bearer {}'.format(api_key)
    }


#clan
def clan_full():
    info = requests. get("https://api.clashofclans.com/v1/clans/{}".format(trans_tag),headers=verification)
    user_json = info.json() #passa para json
    dicionario = dict(user_json)
    return dicionario


#players
def individual(tag):
    link_url = "https://api.clashofclans.com/v1/players/{}".format(re.sub('[#]','%23', tag))
    response = requests.get(link_url,headers=verification)
    user_json = response.json()
    dicionario = dict(user_json)
    return dicionario

#liga data
def liga_info():
    resposta = requests.get('https://api.clashofclans.com/v1/clanwarleagues/wars/{}'.format(trans_tag),headers=verification)
    user_json = resposta.json()
    dicionario = dict(user_json)
    return dicionario

#info da guerra atual da liga  // nao funciona , n sei pq :(
def liga_atual():
    resposta = requests.get('https://api.clashofclans.com/v1/clans/{}/currentwar/leaguegroup'.format(trans_tag),headers=verification)
    user_json = resposta.json()
    dicionario = dict(user_json)
    #importante: 'state' e 'season'
    return dicionario

#full guerra logs
def guerra_logs():
    acess = requests.get('https://api.clashofclans.com/v1/clans/{}/warlog'.format(trans_tag),headers=verification)
    war_json = acess.json()
    dicionario = dict(war_json)
    return dicionario

#info da guerra arual 
def guerra_atual():
    acess = requests.get('https://api.clashofclans.com/v1/clans/{}/currentwar'.format(trans_tag),headers=verification)
    war_json = acess.json()
    dicionario = dict(war_json)
    return dicionario
