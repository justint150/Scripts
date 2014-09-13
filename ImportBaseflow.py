# Python batteries included imports
import os
import sys
import datetime
import time

# Third party imports
# import baker

# Local imports
import pandas as pd
import numpy as np
import csv
# Load in wdmtoolbox routines
from wdmtoolbox import wdmutil
wdm = wdmutil.WDM()
#get directory
dir = os.getcwd()

start = time.clock()
input = np.genfromtxt(dir+'\\baseflow\\baseflow.csv',delimiter=',')
bfdsns = input[1:,0]
input = np.genfromtxt(dir+'\\baseflow\\baseflow.csv','double',delimiter=',')    
bf = input[1:,3]
layer = input[1:,2]
input = np.genfromtxt(dir+'\\input\\baseflow_dsns.csv',delimiter=',')
input_dsn = input[:]
data = np.zeros((120))
Remain = len(input_dsn)
i = 0

start_date = datetime.date(2000,1,1)

while i < len(bfdsns):
    dsn = bfdsns[i]
    j = 0
    while j < len(input_dsn):
        if bfdsns[i] == input_dsn[j]:
            data[:] = bf[i:i+120]/43560
#                 print( len(data))
#                 print( data)
            dsn = str(dsn)
            if dsn[0] == '1':
                wdmpath = dir+'\WDMs\WETLANDS.wdm'
#                     wdmpath = '/home/justin/SMD/wetlands.wdm' #linux
            elif dsn[0] == '2':
                wdmpath = dir+'\WDMs\STREAMS.wdm'
#                     wdmpath = '/home/justin/SMD/streams.wdm' #linux
            elif dsn[0] == '3':
                wdmpath = dir+'\WDMs\RIVERS.wdm'
#                     wdmpath = '/home/justin/SMD/rivers.wdm' #linux
            elif dsn[0] == '4':
                wdmpath = dir+'\WDMs\LAKES.wdm'
#                     wdmpath = '/home/justin/SMD/lakes.wdm' #linux
            elif dsn[0] == '5':
                wdmpath = dir+'\WDMs\CSA.wdm'
            else:
                print('ERROR: Unable to locate WDM...')
                sys.exit()
            if layer[i] == 1:
                dsn = int('3' + dsn[1:4])
            elif layer[i] > 1 and layer[i] < 12:
                dsn = int('4' + dsn[1:4])
            else:
                print('ERROR: Did not provide valid baseflow type')
                sys.exit()
            wdm.write_dsn(wdmpath, dsn, data, start_date)
            break
        else:
            j = j + 1

    Remain = Remain - 1
    if Remain == int(len(input_dsn)*5/6):
        print( '17% of WDM complete')
    elif Remain == int(len(input_dsn)*4/6):
        print( '35% of WDM complete')
    elif Remain == int(len(input_dsn)*3/6):
        print( '50% of WDM complete')
    elif Remain == int(len(input_dsn)*2/6):
        print( '67% of WDM complete') 
    elif Remain == int(len(input_dsn)*1/6):
        print( '81% of WDM complete')  
    
    i = i + 120
print('100% complete')
print('Completion time was {0} mins.'.format((time.clock()-start)/60))    #End record of time process takes
