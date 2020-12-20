import requests
import re
import json

clan_tag = '#2PUROCYCO' #Put your clan tag
api_key = 'YOUR_API_KEY' #generate and add your api


trans_tag = re.sub('[#]','%23',clan_tag) #troca o '#' por '%23'

verification = {
        'Accept': 'application/json',
        'authorization': 'Bearer {}'.format(api_key)
    }


#clan
def clan_full():
    info = requests.get("https://api.clashofclans.com/v1/clans/{}".format(trans_tag),headers=verification)
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
