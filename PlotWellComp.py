import os
import sys


import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
plt.rcParams['figure.max_open_warning']=0
print('-----------------------------------------------------------------------')
print('Plot well comparision of current and previous run.')
print('-----------------------------------------------------------------------')

dir = os.getcwd()

print('Provide PREVIOUS run head file...')
pre_input = str(raw_input())
if os.path.exists(dir + '\\' + pre_input+'.csv')==False:
    print('File does not exist, provide valid PREVIOUS run head file...')
    pre_input = str(raw_input())
    
print('Provide CURRENT run head file...')
cur_input = str(raw_input())
if os.path.exists(dir + '\\' + cur_input+'.csv')==False:
    print('File does not exist, provide valid CURRENT run head file...')
    cur_input = str(raw_input())

start = time.clock()
pre_rawin = np.genfromtxt(pre_input+'.csv', 'str', delimiter =',')
pre_well = pre_rawin[1:,0]
pre_dates = pre_rawin[1:,1]
pre_layer = pre_rawin[1:,2]
pre_rawin = np.genfromtxt(pre_input+'.csv', 'float',delimiter =',')
# obs_in = pre_rawin[1:,3]
pre_modelin = pre_rawin[1:,4]

cur_rawin = np.genfromtxt(cur_input+'.csv', 'str', delimiter =',')
cur_well = cur_rawin[1:,0]
# cur_dates = cur_rawin[1:,1]
cur_layer = cur_rawin[1:,2]
cur_rawin = np.genfromtxt(cur_input+'.csv', 'float',delimiter =',')
obs_in = cur_rawin[1:,3]
cur_modelin = cur_rawin[1:,4]

now = datetime.datetime.now()

Remain = len(pre_rawin)

print( 'Creating PDF...')

rev = 0
savetime = now.strftime("%m%d%Y")
savename = 'WellComp_'+savetime+'_r'+str(rev)+'.pdf'

while os.path.exists(savename)==True:
    rev = rev + 1
    savename = 'WellComp_'+savetime+'_r'+str(rev)+'.pdf'

pdfout = PdfPages(savename) # creates pdf with time_date and revision

i = 0
j = 0
while i < len(pre_well):
    try:
#         print('Working...')
        if pre_well[i] == pre_well[i+1]:
            i = i + 1 # continue next iteration
        else:
            if j == 0:
                pts = i + 1
            else:
                pts = i + 1 - j
#             obs_dates = np.zeros((pts)) # size output arrays
            obs_out = np.zeros((pts)) # size output arrays
            dates = np.zeros((pts)) # size output arrays
            cur_modelout = np.zeros((pts)) # size output arrays
            pre_modelout = np.zeros((pts)) # size output arrays
            dates[:] = pre_dates[j:i + 1]
            obs_out[:] = obs_in[j:i + 1]
            cur_modelout[:] = cur_modelin[j:i + 1]
            pre_modelout[:] = pre_modelin[j:i + 1]
#             Generate plot...
            fig = plt.figure()
            plt.title(pre_input +' vs '+ cur_input + ' - Well ' + pre_well[j] +' - Layer ' + pre_layer[j], fontsize = 18)
            plt.plot(dates,obs_out[:],'b-',label='Observed',aa=True)
            plt.plot(dates,pre_modelout[:],'r-',label=pre_input,linewidth=1.5,aa=True)
            plt.plot(dates,cur_modelout[:],'g-',label=cur_input,aa=True)
            plt.grid(True)
            plt.ylabel('Elevation [ft]',labelpad=4) # Y-label title and placement
            plt.xlabel('Days')
            plt.legend(loc='upper right', ncol=2,prop={'size':8})
#             plt.show()
            pdfout.savefig()    # Save plot to page...
            fig.clf()   # Clears the current figure
            
            obs_dates = None
            cur_modelout = None
            pre_modelout = None
            
            j = i + 1# set start of next array
            i = i + 1# continue next iteration
    except IndexError:
        pts = i + 1 - j
#         obs_dates = np.zeros((pts)) # size output arrays
        obs_out = np.zeros((pts)) # size output arrays
        dates = np.zeros((pts)) # size output arrays
        cur_modelout = np.zeros((pts)) # size output arrays
        pre_modelout = np.zeros((pts)) # size output arrays
        dates[:] = pre_dates[j:i+ 1]
        obs_out[:] = obs_in[j:i + 1]
        cur_modelout[:] = cur_modelin[j:i+1]
        pre_modelout[:] = pre_modelin[j:i+1]
        # Generate plot...
        fig = plt.figure()
        plt.title(pre_input +' vs '+ cur_input + ' - Well ' + pre_well[j] +' - Layer ' + pre_layer[j], fontsize = 18)
        plt.plot(dates,obs_out[:],'b-',label='Observed',aa=True)
        plt.plot(dates,pre_modelout[:],'r-',label=pre_input,linewidth=1.5,aa=True)
        plt.plot(dates,cur_modelout[:],'g-',label=cur_input,aa=True)
        plt.grid(True)
        plt.ylabel('Elevation [ft]',labelpad=4) # Y-label title and placement
        plt.xlabel('Days')
        plt.legend(loc='upper right', ncol=2,prop={'size':8})
#         plt.show()
        pdfout.savefig()    # Save plot to page...
        fig.clf()   # Clears the current figure
        
        obs_dates = None
        cur_modelout = None
        pre_modelout = None
        
        j = i + 1 # set start of next array
        i = i + 1 # continue next iteration

    # Reports remaining DSNs to be processed
    Remain = Remain - 1
    if Remain == int(len(pre_rawin)*9/10):
        print( '10% complete')
    elif Remain == int(len(pre_rawin)*8/10):
        print( '20% complete')
    elif Remain == int(len(pre_rawin)*7/10):
        print( '30% complete')
    elif Remain == int(len(pre_rawin)*6/10):
        print( '40% complete')
    elif Remain == int(len(pre_rawin)*5/10):
        print( '50% complete')
    elif Remain == int(len(pre_rawin)*4/10):
        print( '60% complete')
    elif Remain == int(len(pre_rawin)*3/10):
        print( '70% complete')
    elif Remain == int(len(pre_rawin)*2/10):
        print( '80% complete')
    elif Remain == int(len(pre_rawin)*1/10):
        print( '90% complete')

pdfout.close()
print( '100% complete')
print( 'PDF saved...')
print( 'Completion time was {0} mins.'.format((time.clock()-start)/60))    #End record of time process takes

