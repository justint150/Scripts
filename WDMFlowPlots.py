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



# def plottopdf(dsncsv,outname,calcheck,*kwds):
'''Save stage/flow for a single WDMS list
   of DSNS to a pdf.
'''

start = time.clock()
input = np.genfromtxt(dir+'\\input\\WDMFlowPlots_dsns.csv', 'str', delimiter =',')
wdmpath = input[0,0]
dsns = input[1:]
input = np.genfromtxt(dir+'\\input\\WDMFlowPlots_dsns.csv', 'float',delimiter =',')
tobs = input[1:,1]
Remain = len(dsns)
#     data = np.zeros((3653))
start_date = None
end_date = None
now = datetime.datetime.now()

dates = pd.date_range('1/1/2000', periods=120, freq='MS')
ddates = pd.date_range('1/1/2000', periods=3653, freq='D')

print( 'Creating {0} PDF...'.format(wdmpath))
#     savedest = '"c:\\SMD\\Stream/ Stage/ Plots\\' + now.strftime("%m%d%Y")+ '\\'+ wdmpath + '_' + now.strftime("%H%M") + '.pdf"'
# savedest = dir+'\\Plots\\' + now.strftime("%m_%Y") + '\\' + now.strftime("%d") + '\\'

savedest = dir+'\\Plots\\WDMFlows\\' + now.strftime("%m_%Y") + '\\'
savetime = now.strftime("%m%d%Y")
if not os.path.exists(savedest):
    os.makedirs(savedest)
    

rev = 0
savename = 'All_Stages_Flows_'+savetime+'_r'+str(rev)+'.pdf'

while os.path.exists(savedest+savename)==True:
    rev = rev + 1
    savename = 'All_Stages_Flows'+savetime+'_r'+str(rev)+'.pdf'

pdfout = PdfPages(savedest + savename) # creates pdf wiht name of wdm and time_date
# #         return dsns[:row,j]
row = len(dsns)
i = 0
while i < row:
    dsn = dsns[i,0]
    nts = wdm.read_dsn(dir+'\\WDMs\\' + wdmpath + '.wdm', int(dsn), start_date=start_date, end_date=end_date)    # calls values for a particular DSN
    if len(nts) > 150000:
        by = lambda x: lambda y: getattr(y,x)
        data = nts.groupby([by('year'), by('month')]).apply(lambda x: np.mean(x))   # Original time series aggregated monthly
    elif len(nts) < 150000 and len(nts) >10000:
        by = lambda x: lambda y: getattr(y,x)
        data = nts.groupby([by('year'), by('month')]).apply(lambda x: np.mean(x))   # Original time series aggregated monthly
    elif len(nts) < 10000 and len(nts) > 200:
        by = lambda x: lambda y: getattr(y,x)
        data = nts.groupby([by('year'), by('month')]).apply(lambda x: np.mean(x))   # Original time series aggregated monthly
    elif len(nts) < 200:
        by = lambda x: lambda y: getattr(y,x)
        data = nts.groupby([by('year'), by('month')]).apply(lambda x: np.mean(x))   # Original time series aggregated monthly

    flowdsn = '2' + dsn[1:]
    flow_nts = wdm.read_dsn(dir+'\\WDMs\\' + wdmpath + '.wdm', int(flowdsn), start_date=2000/01/01, end_date=2010/01/01)    # calls values for a particular DSN
#     if calcheck == 'yes':
    obsstagedsn = '7' + dsn[1:]
    obsflowdsn = '8' + dsn[1:]
#         if dsn == '2471':
#             obsstage_nts = np.zeros(3653)
#             nts1 = wdm.read_dsn(dir+'\\WDMs\\' + wdmpath + '.wdm', 7470, start_date=2000/01/01, end_date=2010/01/01)    # calls values for a particular DSN
#             nts2 = wdm.read_dsn(dir+'\\WDMs\\' + wdmpath + '.wdm', 7471, start_date=2000/01/01, end_date=2010/01/01)    # calls values for a particular DSN
#             for line in nts1:
#                 obsstage_nts[line] = (nts1[line]+nts2[line])/2
#                 obsflow_nts[line] = nts1[line] + nts2[line]
#             by = lambda x: lambda y: getattr(y,x)
#             obsstage_data = obsstage_nts.groupby([by('year'), by('month')]).apply(lambda x: np.mean(x))   # Original time series aggregated monthly
# 
#         else:
    obsstage_nts = wdm.read_dsn(dir+'\\WDMs\\' + wdmpath + '.wdm', int(obsstagedsn), start_date=2000/01/01, end_date=2010/01/01)    # calls values for a particular DSN
    by = lambda x: lambda y: getattr(y,x)
    obsstage_data = obsstage_nts.groupby([by('year'), by('month')]).apply(lambda x: np.mean(x))   # Original time series aggregated monthly

    obsflow_nts = wdm.read_dsn(dir+'\\WDMs\\' + wdmpath + '.wdm', int(obsflowdsn), start_date=2000/01/01, end_date=2010/01/01)    # calls values for a particular DSN

    modeldate = dates#mdates.datestr2num(dates)  # Monthly model timeseries
    daily = ddates#mdates.datestr2num(ddates)
#         # Generate plot...
#         fig = plt.figure()
#         plt.plot_date(modeldate, data, '#C22313', linewidth=.75, label='Model')    # data to plot, color and lineweight
#         plt.title('Stage in ' + wdmpath[:-1] +' - DSN ' + dsn[1:])   # title graph
#         plt.grid(True)
#         plt.ylim((0,tobs[i]*1.4)) # fix y-axis minimum
# 
#         if wdmpath == 'lakes':
#             plt.axhspan(0, 2,facecolor='#D2B48C',edgecolor='none',label='Root Zone')  # Shades rootzone thickness of 2 ft
#         else:
#             plt.axhspan(0,4,facecolor='#D2B48C', edgecolor='none',label='Root Zone')  # Shades rootzone thickness of 4 ft
#         plt.axhline(y=tobs[i], color='#647628', linewidth=1, label='TOB')
#         plt.ylabel('Stage (ft)',labelpad=5) # Y-label title and placement
#         plt.legend(bbox_to_anchor=(.5, -.7), loc=8, ncol=3, borderaxespad=10)
#         fig.autofmt_xdate() # Formats date tick labels
#         pdfout.savefig(bbox_inches='tight')    # Save plot to page...
#         fig.clf()   # Clears the current figure
# Generate plot...
    fig = plt.figure()
    fig, (f1,f2) = plt.subplots(2,sharex=True)

    f1.set_title('Stage in ' + wdmpath[:-1] +' - DSN ' + dsn[1:])   # title graph
#         plt.ylim(0) # fix y-axis minimum
    if wdmpath == 'lakes' or wdmpath == 'rivers':
        f1.axhspan(0,2,facecolor='#D2B48C',edgecolor='none',label='Root Zone')  # Shades rootzone thickness of 2 ft
    else:
        f1.axhspan(0,4,facecolor='#D2B48C', edgecolor='none',label='Root Zone')  # Shades rootzone thickness of 4 ft
    f1.axhline(y=tobs[i], color='#647628', linewidth=1, label='TOB')

#     if calcheck == 'yes':
#         f1.plot_date(modeldate,obsstage_data,'#0066FF',linestyle='-',label='Obs. Stage')

    f1.plot_date(modeldate,data,'#3A753A',linestyle='-',label='Mod. Stage')
#         f1.plot_date(modeldate,bf_inch,'r-',label='Baseflow')
    f1.grid(True)
    f1.legend(loc='upper right', ncol=3,prop={'size':6})
#         fig.autofmt_xdate() # Formats date tick labels

#     if calcheck == 'yes':
#         f2.plot_date(daily,obsflow_nts,'#0066FF',linestyle='-',label='Obs. Flow')

    f2.plot_date(daily,flow_nts,'#3A753A',linestyle='-',label='Mod. Flow')
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
    if Remain == int(len(dsns)*5/6):
        print( '17% of WDM complete')
    elif Remain == int(len(dsns)*4/6):
        print( '35% of WDM complete')
    elif Remain == int(len(dsns)*3/6):
        print( '50% of WDM complete')
    elif Remain == int(len(dsns)*2/6):
        print( '67% of WDM complete')
    elif Remain == int(len(dsns)*1/6):
        print( '81% of WDM complete')
        
    i = i + 1

#         plt.savefig(wdmpath[j]+'_'+now.strftime("%H%M%S_%m%d%Y")+'.pdf')
pdfout.close()

print( '{0} PDF saved...'.format(wdmpath))

print( '100% complete')
print( 'Completion time was {0} mins.'.format((time.clock()-start)/60))    #End record of time process takes
