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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
# Load in wdmtoolbox routines
from wdmtoolbox import wdmutil
wdm = wdmutil.WDM()

#get directory
dir = os.getcwd()

start = time.clock()
input = np.genfromtxt(dir+'\\input\\plotall_dsns.csv', 'str', delimiter =',')
wdmpath = input[0,0]
dsns = input[1:]
input = np.genfromtxt(dir+'\\input\\plotall_dsns.csv', 'float',delimiter =',')
tobs = input[1:,1]
Remain = len(dsns)
start_date = None
end_date = None
now = datetime.datetime.now()

dates = pd.date_range('1/1/2000', periods=120, freq='MS')
ddates = pd.date_range('1/1/2000', periods=3653, freq='D')

print( 'Creating {0} PDF...'.format(wdmpath))
#     savedest = '"c:\\SMD\\Stream/ Stage/ Plots\\' + now.strftime("%m%d%Y")+ '\\'+ wdmpath + '_' + now.strftime("%H%M") + '.pdf"'
# savedest = dir+'\\Plots\\' + now.strftime("%m_%Y") + '\\' + now.strftime("%d") + '\\'

savedest = dir+'\\Plots\\AllFlows\\' + now.strftime("%m_%Y") + '\\'
savetime = now.strftime("%m%d%Y")
if not os.path.exists(savedest):
    os.makedirs(savedest)
    

rev = 0
savename = 'All_Stages_Flows_'+savetime+'_r'+str(rev)+'.pdf'

while os.path.exists(savedest+savename)==True:
    rev = rev + 1
    savename = 'All_Stages_Flows'+savetime+'_r'+str(rev)+'.pdf'

pdfout = PdfPages(savedest + savename) # creates pdf wiht name of wdm and time_date

row = len(dsns)
i = 0
while i < row:
    dsn = dsns[i,0]

    stage_nts1 = wdm.read_dsn(dir+'\\WDMs\\WETLANDS.wdm', int(dsn), start_date=start_date, end_date=end_date)
    stage_nts2 = wdm.read_dsn(dir+'\\WDMs\\STREAMS.wdm', int(dsn), start_date=start_date, end_date=end_date)    # calls values for a particular DSN
    try:
        stage_nts3 = wdm.read_dsn(dir+'\\WDMs\\LAKES.wdm', int(dsn), start_date=start_date, end_date=end_date)    # calls values for a particular DSN
    except:
        stage_nts3 = wdm.read_dsn(dir+'\\WDMs\\LAKES.wdm', 1, start_date=start_date, end_date=end_date)
    stage_nts4 = wdm.read_dsn(dir+'\\WDMs\\RIVERS.wdm', int(dsn), start_date=start_date, end_date=end_date)    # calls values for a particular DSN
    flowdsn = '2' + dsn[1:]
    flow_nts1 = wdm.read_dsn(dir+'\\WDMs\\WETLANDS.wdm', int(flowdsn), start_date=start_date, end_date=end_date)    # calls values for a particular DSN
    flow_nts2 = wdm.read_dsn(dir+'\\WDMs\\STREAMS.wdm', int(flowdsn), start_date=start_date, end_date=end_date)    # calls values for a particular DSN
    try:
        flow_nts3 = wdm.read_dsn(dir+'\\WDMs\\LAKES.wdm', int(flowdsn), start_date=start_date, end_date=end_date)    # calls values for a particular DSN
    except:
        flow_nts3 = wdm.read_dsn(dir+'\\WDMs\\LAKES.wdm', 1, start_date=start_date, end_date=end_date)
    flow_nts4 = wdm.read_dsn(dir+'\\WDMs\\RIVERS.wdm', int(flowdsn), start_date=start_date, end_date=end_date)    # calls values for a particular DSN

    modeldate = dates#mdates.date2num(dates)  # Monthly model timeseries
    daily = ddates#mdates.date2num(ddates)

# Generate plot...
    fig = plt.figure()
    fig, (f1,f2) = plt.subplots(2,sharex=True)

    f1.set_title('Stage in all WDMs - DSN ' + dsn[1:])   # title graph
    f1.plot_date(daily,stage_nts1,'#4DB84D',label='Wetlands', linewidth=.75)
    f1.plot_date(daily,stage_nts2,'#70DBFF',label='Streams', linewidth=.75)
    f1.plot_date(daily,stage_nts3,'#A366FF',label='Lakes', linewidth=.75)
    f1.plot_date(daily,stage_nts4,'#1975FF',label='Rivers', linewidth=.75)
#         if wdmpath == 'lakes' or wdmpath == 'rivers':
#             f1.axhspan(0,2,facecolor='#D2B48C',edgecolor='none',label='Root Zone')  # Shades rootzone thickness of 2 ft
#         else:
#             f1.axhspan(0,4,facecolor='#D2B48C', edgecolor='none',label='Root Zone')  # Shades rootzone thickness of 4 ft
#         f1.axhline(y=tobs[i], color='#647628', linewidth=1, label='TOB')
#         f1.plot_date(modeldate,data,'#C22313',label='Mod. Stage')

    f1.grid(True)
    f1.legend(loc='upper right', ncol=2,prop={'size':6})
#         fig.autofmt_xdate() # Formats date tick labels
    f2.plot_date(daily,flow_nts1,'#4DB84D',label='Wetlands', linewidth=.75)
    f2.plot_date(daily,flow_nts2,'#70DBFF',label='Streams', linewidth=.75)
    f2.plot_date(daily,flow_nts3,'#A366FF',label='Lakes', linewidth=.75)
    f2.plot_date(daily,flow_nts4,'#1975FF',label='Rivers', linewidth=.75)
#         f2.plot_date(modeldate,bf_vol,'r-',label='Baseflow')
    f2.grid(True)
#         plt.subplots_adjust(hspace=0)
    f1.set_ylabel('Stage [ft]',labelpad=4) # Y-label title and placement
    f2.set_ylabel('Flow [cfs-d]',labelpad=4)
    f2.legend(loc='upper right', ncol=2,prop={'size':6})
    fig.autofmt_xdate(ha='right') # Formats date tick labels
    pdfout.savefig(bbox_inches='tight')    # Save plot to page... bbox_inches='tight'
    fig.clf()   # Clears the current figure

    # Reports remaining DSNs to be processed
    Remain = Remain - 1
    if Remain == int(len(dsns)*9/10):
        print( '10% complete')
    elif Remain == int(len(dsns)*8/10):
        print( '20% complete')
    elif Remain == int(len(dsns)*7/10):
        print( '30% complete')
    elif Remain == int(len(dsns)*6/10):
        print( '40% complete')
    elif Remain == int(len(dsns)*5/10):
        print( '50% complete')
    elif Remain == int(len(dsns)*4/10):
        print( '60% complete')
    elif Remain == int(len(dsns)*3/10):
        print( '70% complete')
    elif Remain == int(len(dsns)*2/10):
        print( '80% complete')
    elif Remain == int(len(dsns)*1/10):
        print( '90% complete')
    else:
        print( 'Plotting...')
    i = i + 1

pdfout.close()

print( '{0} PDF saved...'.format(wdmpath))

print( '100% complete')
print( 'Completion time was {0} mins.'.format((time.clock()-start)/60))    #End record of time process takes
# os.popen(pdfout,shell=True)
