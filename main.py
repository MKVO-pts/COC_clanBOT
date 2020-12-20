
##
'''
THIS FILE IS NOT FINISHED YET
'''
#este ficheiro e a base para o funcionamento de todo o processo
from func import verify_main # atualiza sempre que entram membros novos
from func import war_logs # historico de guerrasimport time as t
import threading
import datetime
import time as t
import json 
import os


##
'''
THIS FILE IS NOT FINISHED YET
'''
realtime = datetime.datetime.now().strftime('%X')
while True:
    print(realtime,'      Confirmando os membros do cla')
    t.sleep(80)# espera 80 segundos 
    verify_main()
    print(realtime,'     Verificando se ha atualizacoes no historico de guerras')
    t.sleep(120) # espera 2 min + 80 seg iniciais 
    war_logs()

##
'''
THIS FILE IS NOT FINISHED YET
'''


