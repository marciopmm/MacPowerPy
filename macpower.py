from subprocess import Popen, PIPE
from datetime import datetime
import re
import requests
import time
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

while True:
    output = Popen(["ioreg", "-r", "-k", "LegacyBatteryInfo", "-w", "0"], stdout=PIPE).communicate()[0]
    strOutput = str(output, encoding='utf-8')

    external = re.search(r'"ExternalConnected" = (Yes|No)', strOutput).groups(0)[0]
    isCharging = re.search(r'"IsCharging" = (Yes|No)', strOutput).groups(0)[0]
    fully = re.search(r'"FullyCharged" = (Yes|No)', strOutput).groups(0)[0]
    state = int(re.search(r'"StateOfCharge"=(\d+)', strOutput).groups(0)[0])

    if external == 'Yes' or isCharging == 'Yes':
        if fully == 'Yes' or state >= 99:
            requests.get('http://192.168.1.30/relayOff') #Command to get relay server OFF
    elif (external == 'No' or isCharging == 'No') and state <= 10:
        requests.get('http://192.168.1.30/relayOn') #Command to get relay server ON command

    now = datetime.now()
    
    horario = now.strftime('%H:%M:%S')

    sys.stdout.write(f"({bcolors.WARNING}{horario}{bcolors.ENDC}) - {bcolors.OKBLUE}Conector Externo: {bcolors.BOLD}{external == 'Yes'}{bcolors.ENDC}{bcolors.ENDC} | {bcolors.OKCYAN}Carregando: {bcolors.BOLD}{isCharging == 'Yes'}{bcolors.ENDC}{bcolors.ENDC} | {bcolors.OKGREEN}Estado da Carga: {bcolors.BOLD}{state}%{bcolors.ENDC} \r")
    sys.stdout.flush()
    time.sleep(30)
