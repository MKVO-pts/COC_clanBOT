#este ficheiro e a base para o funcionamento de todo o processo
#from func import verify_main # atualiza sempre que entram membros novos
#from func import war_logs # historico de guerrasimport time as t
import os 
import json
import discord
import time
import asyncio
from datetime import datetime  # módulo que vai ser usado para cria os objetos "datetime"
from dateutil.relativedelta import relativedelta  # para instalar esta lib, use o comando "pip install python-dateutil" 
from discord.ext import commands,tasks
from data_process import guerra_profile,store,updater,lista_actual,lista_antiga,clan_profile,guerras_complet

import config

#define o prefixo dos commandos do bot
bot = commands.Bot(command_prefix='!')
token = config.discord_token
id_join_channel = config.id_join_channel
jogando = config.activity
client = discord.Client()


#zona de eventos 
@bot.event
async def on_ready():
    print('__________________________________________')
    print('|  Bot: ON                                |')
    print('|  Info: ',bot.user.name,'ID: ', bot.user.id,'|')
    print('|  Status: Personalizado                  |')
    print('__________________________________________\n')
    await bot.change_presence(activity=discord.Game(name=jogando,type=3))
    print('Activity: ')
    #start background functions

#envia mensagem quando alguem novo entra no server
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Bem vindo ao servidor {member.name}! Usa o commando ``!help``para veres os commandos disponiveis e como usa-los.'    
        )


#TODOS OS COMMANDOS DISPONIVEIS 
"""
@bot.commands 
async def commando(ctx, parametros1, parametros2):
    acao     #a acao em si
    ctx.send()
commando = commando sem o prefixo "!"
"""


@bot.command()
async def teste(ctx):    
    print('Embed teste...')
    embedVar = discord.Embed(title='Titlo', color=0x1abc9c,content='Conteudo aqui',description='Isto é a descricao' )
    embedVar.add_field(name="Field1", value="hi", inline=False)
    embedVar.add_field(name="Field2", value="hi2", inline=False)
    embedVar.set_footer(text='Footer', icon_url=discord.Embed.Empty)
    await ctx.send(embed=embedVar)
    
    #Embed exemplo
    '''
    embedVar = discord.Embed(title='Titlo', color=0x1abc9c,content='Conteudo aqui',description='Isto é a descricao' )
    embedVar.add_field(name="Field1", value="hi", inline=False)
    embedVar.add_field(name="Field2", value="hi2", inline=False)
    await ctx.send(embed=embedVar)'''

    #await ctx.send('Os parametros sao {}'.format(person))
    '''
@bot.command()
async def help(ctx):
    await ctx.send('Commandos: ```\n !help - mostra esta mensagem \n !info_clan - mostra info basica sobre o cla \n !info nome_do_membro - envia info sobre o membro \n !rank - mostra a tabela de ranks de doacoes \n !envite -convida o bot para o teu servidor ```')
'''
    
#Envia a info do membro que se escolher 
@bot.command(brief=' -Mostra detalhes sobre o membro',description='Mostra informação sobre o membro caso ele esteja no cla, este comando usa-se da seguinte forma ```!info nome_no_clash```Se o nome do membro tiver espacos deve se usar ```!info "nome_no_clash " ```A informacao de cada membro é atualizada automaticamente de 5 em 5 minutos')
async def info(ctx, pessoa):
    os.chdir(config.individual_member_dir)
    for y in os.scandir():
        files = str(y).replace('\'>','').replace('<DirEntry \'','')
        #print('Files: ',files)
        with open(files) as f:
            #print(f)
            open_dict = json.load(f)
            if pessoa == open_dict['Nome']: #ficheiro certo
                print('File found')
                #print(open_dict)
                info_embed = discord.Embed(title='Info about: {}'.format(open_dict['Nome']), color=0x1abc9c)
                for key, value in open_dict.items():           
                    if key == '[+]':                        #se key=[+], ele adiciona os items e para 
                        print('Same')
                        for more_key, more_value in value.items():                #para os valores no 
                            print('Key:', more_key,'Valor:',more_value)
                            info_embed.add_field(name=key + more_key, value=more_value, inline=True)
                        break                 #para parar
                    info_embed.add_field(name=key,value=value,inline=True)
                #await ctx.send('Nome: {name} \n Info completa: ```{info}```'.format(name=open_dict['nome'], info=json.dumps(open_dict,indent=2)))
                info_embed.set_footer(text='Gang do Cavalo', icon_url='https://icon-library.com/images/clash-of-clans-icon/clash-of-clans-icon-5.jpg' )
                await ctx.send(embed=info_embed)
                break
            else:
                pass

#envia info sobre o cla 
@bot.command(brief=' -Mostra detalhes sobre o cla', description='Mostra informacao detalhada sobre o cla, é simples de se usar ```!cla```')
async def cla(ctx):
    os.chdir(config.clan_file_dir)
    f = open('GANG DO CAVALO.json')
    dict_f = json.load(f)
    json_f = json.dumps(dict_f,indent=1)
    await ctx.send('Gang Do Cavalo : ```{}```'.format(json_f))


#encia info sobre a guerra atual
@bot.command(brief=' -Informacão sobre a guerra', description='Envia informação mais geral sobre a guerra de clas')
async def guerra(ctx):
    guerra_atual = dict(guerra_profile())
    embedVar = discord.Embed(title='{aliados}  :vs:  {inimigos}'.format(aliados=guerra_atual['Aliados']['Nome'],inimigos=guerra_atual['Inimigo']['Nome']), color=0x1abc9c,description='Estado:{e}    Tamanho:{t}'.format(e=guerra_atual['Estado'],t=guerra_atual['Tamanho']))
    embedVar.add_field(name=guerra_atual['Aliados']['Nome'], value='Numero de ataques: {ata}\nEsrelas totais: {es}\nPercentagem: {cem}%'.format(ata=guerra_atual['Aliados']['Atacks'],es=guerra_atual['Aliados']['Estrelas'],cem=guerra_atual['Inimigo']['%']), inline=True)    
    embedVar.add_field(name=guerra_atual['Inimigo']['Nome'], value='Numero de ataques: {ata}\nEsrelas totais: {es}\nPercentagem: {cem} %'.format(ata=guerra_atual['Inimigo']['Atacks'],es=guerra_atual['Inimigo']['Estrelas'],cem=guerra_atual['Inimigo']['%']), inline=True)
    embedVar.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)
    await ctx.send(embed=embedVar)


#envia o link para convidar o bot
@bot.command(brief=' -Convida o bot para o teu servidor')
async def invite(ctx):
    await ctx.send('Envite code: https://discord.com/api/oauth2/authorize?client_id=792173813000306718&permissions=0&scope=bot')
    print('Cla info sended whit sucess')

#Commandos de Moderação

#commando para expulsar alguem
@commands.has_permissions(kick_members=True)
@bot.command(brief=' -Para expulsar alguem', description='Para expulsar alguem do servidor basta escrever```!kick @membro```, é preciso ter permição para usar este comando')
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        kick = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)

#banir membros 
@bot.command(brief=' -Para banir alguem do servidor',description='Expulsa o membro do servidor e impede que ele retorne, pelo menos com o mesmo IP ```!ban @membro```')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Membro {member} foi banido')

# comando para desbanir membros
@bot.command(brief=' -Para desbanir membros', description='Nao tenho a certeza se é preciso o id ou se basta o nome')
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

'''
# se um commando for mal executado 
@info.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Nao consegui encontrar o membro ...')
        print('Houve um erro durante o processamento do comando')
'''



##
#Zonda de tasks
## Tasks incluem loops e funcoes q sao executadas priodicamente
@tasks.loop(seconds=120) #150s=2,3min
async def member_control():
    await bot.wait_until_ready()
    
    print('Control start!')    
    new = lista_actual()
    old = lista_antiga()
    channel = await bot.fetch_channel(id_join_channel)
    #await channel.send("Working!")
    
    #atualiza a informacao de cada membro
    if len(old) ==len(new): #
        for members in new:
            os.chdir(config.individual_member_dir)
            updater(members)

    if len(old) > len(new): #apagar membros /remover membros antigos
        for member in old:    #verifica que membros e que nao na lista "new" e apaga o ficheiro deles
            if member not in new:
                #envia uma mensagem para o discord
                embedVar = discord.Embed(title='{} saiu do cla!'.format(member), color=0x1abc9c)
                await channel.send(embed=embedVar)
                #remove the file
                os.chdir(config.individual_member_dir)
                os.remove('{file}{f_type}'.format(file=member,f_type='.json'))

    elif len(old) < len(new):# adicionar /membros novos
        for member in new:
            if member not in old:   #verifica os membros que estao na new mas nao na old, e atualiza com os novos
                #envia uma mensaggem para o discord
                embedVar = discord.Embed(title='{} entrou no cla!'.format(member), color=0x1abc9c)
                await channel.send(embed=embedVar)

                os.chdir(config.individual_member_dir)
                updater(member)
                os.chdir(config.data_bank_dir) #guarda a info no bank, nada de importante
                updater(member)
                print(datetime.datetime.now().strftime('%X'), 'New profile added to the bank: ´{}´'.format(members))

@tasks.loop(seconds=1800) #1800 segundos = 30 min        
async def guerra_historico():
    os.chdir(config.war_logs_dir) #muda o diretorio
    new = guerras_complet() #dicionario com os 'war_logs'
    #abre o feicheiro e verifica se existem diferencas
    with open('guerras.json') as f:      # abre o ficheiro com o registo das guerras
        ler = json.load(f)
        print('Outdated data:', len(ler),'  Updated data:',len(new))
        print(f)
        if len(new) == len(ler):            #nao muda nada
            print('No need to updated!')            
        elif len(new) > len(ler):                #atualiza a info (ficheiro)
            print('Updatting war logs...')      
            store(guerras_complet(),'guerras',1)



@tasks.loop(seconds=240) #240s =2min
async def clan_info():
    #clan profile é im dicionario com  toda a info sobre o cla
    os.chdir(config.clan_file_dir)
    info = clan_profile() #dcionario com info do cla 
    store(info, info['nome'], 1) #atualiza a info do cla 

    
    
    
# To Run the Discord BOT
client.loop.create_task(clan_info())
client.loop.create_task(guerra_historico())
client.loop.create_task(member_control())
bot.run(token)  #inicia o bot
