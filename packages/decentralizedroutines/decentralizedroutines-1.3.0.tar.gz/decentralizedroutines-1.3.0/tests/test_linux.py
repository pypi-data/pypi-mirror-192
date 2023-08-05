# implements a decentralized routines worker 
# connects to worker pool
# broadcast heartbeat
# listen to commands
# environment variables:
# SOURCE_FOLDER
# WORKERPOOL_STREAM
# GIT_SERVER
# GIT_USER
# GIT_ACRONYM
# GIT_TOKEN

import os,time
from importlib.metadata import version
import numpy as np
from threading import Thread

import sys
sys.path.append('/home/jcooloj/src/DecentralizedRoutines/src/')
print(sys.path[0])

import decentralizedroutines.defaults as defaults 


import os,sys,psutil,time,subprocess

command = 'git -C /home/jcooloj/src clone -b 202301 https://jcarlitooliveira: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@github.com/jcarlitooliveira/MarketData-BVMF /home/jcooloj/src/MarketData-BVMF#202301'
command = command.split(' ')
process = subprocess.Popen(command,\
    stdout=subprocess.PIPE, stderr=subprocess.PIPE,\
    universal_newlines=True, shell=True)        
while True:
        output = process.stdout.readline()
        if ((output == '') | (output == b''))\
                & (process.poll() is not None):
            break        
        if (output):
            output = output.rstrip()
            if output!='':
                print('command response:'+output)  
rc = process.poll() #block until process terminated
success= rc==0