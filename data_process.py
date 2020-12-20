#modulos utilizados
from scrape import clan_full, individual, liga_atual, liga_info, guerra_logs, guerra_atual 
import json

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
