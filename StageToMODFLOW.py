
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

print('-----------------------------------------------------------------------')
print('Export monthly stage for MODFLOW import.')
print('-----------------------------------------------------------------------')
#get directory
quit_prog = raw_input('Continue with operation (y/n)?')
if quit_prog == 'n':
    sys.exit()
else:
    print('Running...')
dir = os.getcwd()

start = time.clock()
input = np.genfromtxt(dir+'\input\MODFLOW_stagedsns.csv', 'str', delimiter =',')
wdmpath = input[0]
dsns = input[1:]
row = len(input[1:])
#     print row
col = len(input[0])
#     print col
ToWrite = np.zeros((66481,4))
ToWrite = np.asarray(ToWrite, '|S10')

stdate = 0
i = 0
j = 0
start_date = None
end_date = None
ToWrite[0,0] = 'DSN'
ToWrite[0,1] = 'Year'
ToWrite[0,2] = 'Month'
ToWrite[0,3] = 'Stage(ft)'
dates = pd.date_range('1/1/2000', periods=120, freq='MS')

while j < col:
    i = 0
    oldrow = row
    row = 0
    for line in dsns[:,j]:
        if line <> '':
            row = row + 1
        else:
            continue
    Remain = row

    while i < row and row:
        dsn = dsns[i,j]
        nts = wdm.read_dsn(dir+'\WDMs\RIVERS.wdm', int(dsn), start_date=start_date, end_date=end_date)    #calls values for a particular DSN
        by = lambda x: lambda y: getattr(y,x)
        data = nts.groupby([by('year'), by('month')]).apply(lambda x: np.mean(x))   #Original time series aggregated monthly
        k = 1

        while k <= len(dates):
            ToWrite[stdate+k,3] = np.round(data.iloc[k-1][0], decimals=4)
            if j == 0:
                dsn = '1' + str(dsn[1:])
            elif j == 1:
                dsn = '2' + str(dsn[1:])
            elif j == 2:
                dsn = '3' + str(dsn[1:])
            elif j == 3:
                dsn = '4' + str(dsn[1:])
            elif j == 4:
                dsn = '5' + str(dsn[1:])
            ToWrite[stdate+k,0] = dsn
            tempDate = str(dates[k-1])
            ToWrite[stdate+k,1] = tempDate[:4]
            ToWrite[stdate+k,2] = tempDate[5:7]
            k = k + 1

        stdate = stdate + len(dates)
        i = i + 1
        
        Remain = Remain - 1
        if Remain == int(len(dsns[0])*5/6):
            print( '17% of WDM complete')
        elif Remain == int(len(dsns[0])*4/6):
            print( '35% of WDM complete')
        elif Remain == int(len(dsns[0])*3/6):
            print( '50% of WDM complete')
        elif Remain == int(len(dsns[0])*2/6):
            print( '67% of WDM complete') 
        elif Remain == int(len(dsns[0])*1/6):
            print( '81% of WDM complete')
    j = j + 1
    print( '{0} WDMs to be processed'.format(col-j))
now = datetime.datetime.now()
savetime = now.strftime("%m%d%Y")

savedest = dir+'\\Stage Output\\'

if not os.path.exists(savedest):
    os.makedirs(savedest)

rev = 0
name = 'MonthlyStage_'+savetime+'_r'+str(rev)+'.csv'

while os.path.exists(savedest+name)==True:
    rev = rev + 1
    name = 'MonthlyStage_'+savetime+'_r'+str(rev)+'.csv'
    
ForOutput = csv.writer(open(savedest+name, 'wb'))

for row in range(len(ToWrite)):
    ForOutput.writerow(ToWrite[row])
print( '100% complete')
print( 'Completion time was {0} mins.'.format((time.clock()-start)/60))    #End record of time process takes                                   
# shutil.copyfile(source, 'P:\ENG-CEE-Ross\Projects\Mosaic\Justin\ForTrout\MonthlyStage_'+savetime+'.csv')
sys.exit()