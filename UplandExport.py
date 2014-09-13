
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

'''Export daily upland flows to a monthly timeseries
in the following format:
Metzone,Date,Parm 1,Parm 2,...,Parm n
Met 1,2000-01-01,.034,.035,...,.031
Met 1,2000-02-01,.561,.046,...,.041
...  ,  ...  ,  ...  ,  ...  ,  ...
Met n,2009-12-01,.045,.376,...,.184
:param wdmpath:     Path of name of WDMfile, i.e. "example.wdm"
:param input:       Input.txt file with dsns listed in a matrix
                        with metzones as the header and dsns for a
                        particular metzone listed below, comma
                        delimitted.
:param output:      Output.txt file for time series to be exported,
                        exported file is comma delimited, parm as header,
                        metzone as first column, and data for a particular
                        dsn as a matrix.
:Example String
'''

print('-----------------------------------------------------------------------')
print('Export daily upland flows to a monthly timeseries.')
print('-----------------------------------------------------------------------')
print('')

quit_prog = raw_input('Continue with operation (y/n)?')
if quit_prog == 'n':
    sys.exit()
else:
    print('Running...')

start = time.clock()    #Start record of time process takes

#Initialize variables
f = 0
g = 1
h = 0
i = 1
l = 0
nParm = 1

#Read input file of DSNs
dsns = np.genfromtxt(dir+"\input\upland_flowdsns.csv", 'str', delimiter=',')
nMet = len(dsns[0])+1
start_date = None
end_date = None
Remain = len(dsns[0])+1
print( '{0} metzones to be processed.'.format(Remain-1))

#Create array
ToWrite = np.zeros((120*len(dsns[0])+1,len(dsns)+1))
ToWrite = np.asarray(ToWrite, '|S10')
ToWrite[0,0] = 'MetZone'
ToWrite[0,1] = 'Dates'
Dates = pd.date_range('1/1/2000', periods=120, freq='MS')
    
while f+1 < nMet:
    print( 'Metzone {0} is being worked...'.format(dsns[0,f]))
    k = 1
    g = 1
    h = 120*f
    if f == 0:
        while nParm < len(dsns):    #label first row
            dsn = dsns[nParm,0]
            if len(dsn) == 3:
                ToWrite[0,nParm+1] = '0' + dsn[2]
            else:
                ToWrite[0,nParm+1] = dsn[0] + dsn[3]
            nParm = nParm + 1
    while k < len(Dates)+1:
        ToWrite[k+h,0] = dsns[0,f]  #Label first col
        ToWrite[k+h,1] = str(Dates[k-1])    #label second column
        k = k + 1
    i = 1
    while i < len(dsns):
        dsn = dsns[i,f]
        #calls values for a particular DSN
        nts = wdm.read_dsn(dir+'\wdms\uplands.wdm',
                           int(int(dsn)),
                           start_date=start_date,
                           end_date=end_date)
#             mdates = pd.date_range('1/1/2000',periods=len(nts))   #Model time step
#             data = pd.TimeSeries( nts, index = mdates)  #Model time series
        by = lambda x: lambda y: getattr(y,x)
        data = nts.groupby([by('year'), by('month')]).apply(lambda x: np.sum(x))   #Original time series aggregated monthly
        l = 120*f
        g = 1
        while g < len(Dates)+1:     #Loop to return monthly results
            ToWrite[g+l,i+1] = str(np.round(data.iloc[g-1][0], decimals=6))
            g = g + 1
        i = i + 1
    f = f + 1
#     Remain = Remain - 1
#     if Remain == int(len(dsns)*9/10):
#         print( '10% complete')
#     elif Remain == int(len(dsns)*8/10):
#         print( '20% complete')
#     elif Remain == int(len(dsns)*7/10):
#         print( '30% complete')
#     elif Remain == int(len(dsns)*6/10):
#         print( '40% complete')
#     elif Remain == int(len(dsns)*5/10):
#         print( '50% complete')
#     elif Remain == int(len(dsns)*4/10):
#         print( '60% complete')
#     elif Remain == int(len(dsns)*3/10):
#         print( '70% complete')
#     elif Remain == int(len(dsns)*2/10):
#         print( '80% complete')
#     elif Remain == int(len(dsns)*1/10):
#         print( '90% complete')
ForOutput = csv.writer(open(dir+"\output\upland_flows.csv" , 'wb'))
for row in range(len(ToWrite)):
    ForOutput.writerow(ToWrite[row])

print( '100% complete with upland flows.')
# print( 'Completion time was {0} mins.'.format((time.clock()-start)/60))    #End record of time process takes

'''Export daily upland storages to monthly a monthly timeseries
in the following format:
Metzone,Date,Parm 1,Parm 2,...,Parm n
Met 1,2000-01-01,.034,.035,...,.031
Met 1,2000-02-01,.561,.046,...,.041
...  ,  ...  ,  ...  ,  ...  ,  ...
Met n,2009-12-01,.045,.376,...,.184
:param wdmpath:     Path of name of WDMfile, i.e. "example.wdm"
:param input:       Input.txt file with dsns listed in a matrix
                        with metzones as the header and dsns for a
                        particular metzone listed below, comma
                        delimitted.
:param output:      Output.txt file for time series to be exported,
                        exported file is comma delimited, parm as header,
                        metzone as first column, and data for a particular
                        dsn as a matrix.
:Example String
'''
print('')
print('-----------------------------------------------------------------------')
print('Export daily upland storages to a monthly timeseries.')
print('-----------------------------------------------------------------------')
start = time.clock()    #Start record of time process takes
#Initialize variables
f = 0
g = 1
h = 0
i = 1
l = 0
nParm = 1

#Read input file of DSNs
dsns = np.genfromtxt(dir+'\input\upland_storedsns.csv', 'str', delimiter=',')
nMet = len(dsns[0])+1
start_date = None
end_date = None

Remain = len(dsns[0])+1
print( '{0} metzones to be processed.'.format(Remain-1))

#Create array
ToWrite = np.zeros((120*len(dsns[0])+1,len(dsns)+1))
ToWrite = np.asarray(ToWrite, '|S10')
Diffs = np.zeros((120*len(dsns[0])+1,((len(dsns)-1)/3)+2))
Diffs = np.asarray(Diffs, '|S10')
Diffs[0,0] = 'MetZone'
Diffs[0,1] = 'Date'
ToWrite[0,0] = 'MetZone'
ToWrite[0,1] = 'Date'
Dates = pd.date_range('1/1/2000', periods=120, freq='MS')
    
while f + 1 < nMet:
    print( 'Metzone {0} is being worked...'.format(dsns[0,f]))
    k = 1
    g = 1
    h = 120*f
    if f == 0:
        while nParm < len(dsns): # write column headers to storage output
            dsn = dsns[nParm,0]
            if len(dsn) == 3:
                ToWrite[0,nParm+1] = '0' + dsn[2] 
            else:
                ToWrite[0,nParm+1] = dsn[0] + dsn[3]
            nParm = nParm + 1
        i = 1
        while g < len(dsns): # write column headers to change in USZ time series
            if g % 3 == 0:
                dsn = dsns[g,0]
                if len(dsn) == 3:
                    Diffs[0,i+1] = '0' + dsn[2]
                    i = i + 1
                else:
                    Diffs[0,i+1] = dsn[0] + dsn[3]
                    i = i + 1
                g = g + 1
            else:
                g = g + 1

    while k < len(Dates)+1: # write metzone and date to
        ToWrite[k+h,0] = dsns[0,f]
        ToWrite[k+h,1] = str(Dates[k-1])
        k = k + 1
    
    i = 1
    c = 1
    while i < len(dsns):
        dsn = dsns[i,f]
        #calls values for a particular DSN
        nts = wdm.read_dsn(dir+'\wdms\uplands.wdm',
                           int(int(dsn)),
                           start_date=start_date,
                           end_date=end_date)
#             mdates = pd.date_range('1/1/2000',periods=len(nts))   #Model time step
#             data = pd.TimeSeries( nts, index = mdates)  #Model time series
        by = lambda x: lambda y: getattr(y,x)

        if i % 3 == 0:  #third dsn in input file is AGWS, we are taking change in storage in addition to mean
            first = nts.groupby([by('year'), by('month')]).apply(lambda x: x.iloc[0][0])
            last = nts.groupby([by('year'), by('month')]).apply(lambda x: x.iloc[-1][0])
            l = 120*f
            g = 1
            while g < len(Dates)+1:
                Diffs[g+l,0] = dsn[1:3]
                Diffs[g+l,1] = str(Dates[g-1])
                Diffs[g+l,c+1] = str(np.round((last[g-1]-first[g-1]), decimals=6))
                g = g + 1
            c = c + 1
#                 data = data.groupby([by('year'), by('month')]).apply(lambda x: x[0])  #First value of each month
#                 l = 120*f
#                 g = 1
#                 while g < len(Dates)+1: #Loop to return monthly results
#                     ToWrite[g+l,i+1] = str(np.round(data[g-1], decimals=6))
#                     g = g + 1
#                 i = i + 1
#  
#             else: #mean aggregation for all other storage timeseries

        data = nts.groupby([by('year'), by('month')]).apply(lambda x: np.mean(x))   #Original time series aggregated monthly
        l = 120*f
        g = 1
        while g < len(Dates)+1:     #Loop to return monthly results
            ToWrite[g+l,i+1] = str(np.round(data.iloc[g-1][0], decimals=6))
            g = g + 1
        i = i + 1
    f = f + 1
#     Remain = Remain - 1
#     if Remain == int(len(dsns)*9/10):
#         print( '10% complete')
#     elif Remain == int(len(dsns)*8/10):
#         print( '20% complete')
#     elif Remain == int(len(dsns)*7/10):
#         print( '30% complete')
#     elif Remain == int(len(dsns)*6/10):
#         print( '40% complete')
#     elif Remain == int(len(dsns)*5/10):
#         print( '50% complete')
#     elif Remain == int(len(dsns)*4/10):
#         print( '60% complete')
#     elif Remain == int(len(dsns)*3/10):
#         print( '70% complete')
#     elif Remain == int(len(dsns)*2/10):
#         print( '80% complete')
#     elif Remain == int(len(dsns)*1/10):
#         print( '90% complete')

ForOutput = csv.writer(open(dir+'\output\upland_storages.csv' , 'wb'))
ChangeStor = csv.writer(open(dir+'\output\D_storage.csv', 'wb'))

for row in range(len(ToWrite)):
    ForOutput.writerow(ToWrite[row])

for row in range(len(Diffs)):
    ChangeStor.writerow(Diffs[row])


print( '100% complete with upland storages.')
print( 'Completion time was {0} mins.'.format((time.clock()-start)/60))    #End record of time process takes                                   

