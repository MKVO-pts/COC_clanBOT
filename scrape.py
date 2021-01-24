import requests
import re
import json
import random
import config
'''
tot al importantes 


# autorizacao, api key
headers ={
    'Accept': 'application/json',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjEwYTgyZTZhLTVhNTItNGZiMi05MDdiLWZmOTlkNzE0MTllNyIsImlhdCI6MTYwNjE1NTA1OSwic3ViIjoiZGV2ZWxvcGVyLzI0YmYyOTNkLTZiMzktOTI0ZC1iN2FkLTllNWRhNGZiMzUyNyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjc3LjU0LjE5Ny43NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.0SshuczcOfzP2TcyaeOzl5tpE6H26jQXRDHhaXcLVGcS0xHrYEKe8qA0LDtI8Q0Vl9ixP38h_nS49BAlE9YLbA'
} 

#realiza o pedido de informacao
response = requests.get("https://api.clashofclans.com/v1/clans/%232PUROCYCO",headers=headers) #envia um pedido
user_json = response.json() #passa para json

#transforma a info de json para dicionario(armazenada e mais facil de se interagir)
dicionario = dict(user_json)
dict_org = json.dumps(dicionario, indent=5) #melhora a intrepretação do dict

#Info sobre o dicionario criado / estado de organização
#a indo entre [xxx] representa a "key no dicionario", vai ser importante porque vai ser como vamos usar os "valores" com o dicionario
'''
'''
dicionario tem 20 pares de key,value 
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

Metodos relativos ao individul 
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
#algo = requests.get('https://api.clashofclans.com/v1/clans/{}/currentwar'.format(trans_tag),headers=verification).json()
#print(json.dumps(algo, indent=2))
#print(individual('#2QC202JC2'))
print(guerra_logs())
print(guerra_atual())
print(guerra_logs())
print(guerra_atual())
'''
for key,value in guerra_atual().items():
    print(key)
    if key == 'state':
        print('------------')
        print(value)
        print('-------------')

for key, value in dicionario.items():
    print(key, ' : ', value)
    if key == "memberList":
        for key, value in dicionario[memberList]:
            print(key,' : ', value)
'''