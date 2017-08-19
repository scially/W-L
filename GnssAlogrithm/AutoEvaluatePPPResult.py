# coding=utf-8
import easygui as gui
import os
import matplotlib.pyplot as plt
import sys
import numpy as np
from matplotlib.font_manager import FontProperties

def f(x):
    return x*x
def find_convergence_time(L,M,N):
    t=0 # count number
    k=list()
    for ii in range(len(L)):
        if ((abs(L[ii] * 10) < 10) and (abs(M[ii] * 10) < 10) and (abs(N[ii] * 10) < 10) ):
            if (t== 1):
                k=(ii)
                t=0
        else :
            t=1
    return k

def read_plot_PosResult(infile):
    in_file = open(infile, 'r')
    Hour = list()
    Minute = list()
    Second = list()
    N = list()
    E = list()
    U = list()
    lines = in_file.read().splitlines()
    in_file.close()
    for line in lines:
        L = line.split()
        if(L[0]!='%'):
            TIME=L[1].split(':')
            Hour.append(int(TIME[0]))
            Minute.append(int(TIME[1]))
            Second.append(float(TIME[2]))
            N.append(float(L[2]))
            E.append(float(L[3]))
            U.append(float(L[4]))
    epoch=len(N)
    X = range(1, len(N) + 1)

    convergence_epoch = find_convergence_time(N, E, U)
    N_conve = N[convergence_epoch:]
    N_conve_1=list(map(f,N_conve))
    RMS_N_conve = str(np.sqrt(sum(N_conve_1)/ len(N_conve_1)))
    E_conve = E[convergence_epoch:]
    E_conve_1 = list(map(f, E_conve))
    RMS_E_conve = str(np.sqrt(sum(E_conve_1) / len(E_conve_1)))
    U_conve = E[convergence_epoch:]
    U_conve_1 = list(map(f, U_conve))
    RMS_U_conve = str(np.sqrt(sum(U_conve_1) / len(U_conve_1)))

    ThreeD_RMS = str(np.sqrt(sum(N_conve_1 + E_conve_1 + U_conve_1) / (3 * len(E_conve_1))))
    Naxes=plt.plot(X, N, color='blue',linewidth=3,linestyle='-', label='N,RMS='+RMS_N_conve)
    Eaxes=plt.plot(X, E, color='red', linewidth=3,linestyle='-', label='E,RMS='+RMS_E_conve)
    Uaxes=plt.plot(X, U, color='yellow',linewidth=3,linestyle='-', label='U,RMS='+RMS_U_conve)
    plt.legend(loc='upper right')

    ymax = max(max(N),max(E),max(U))
    xmax = len(N)
    t = convergence_epoch
    plt.plot([t, t], [-5, 5], color='black', linewidth=2.5, linestyle="--")
    plt.scatter([t, ], [0, ], 150, color='green')
    # tx=2*xmax/3
    # ty=2*ymax/3
    tx =  xmax / 4
    ty =  ymax / 2
    # plt.text(tx,ty,'3D RMS='+str(ThreeD_RMS),fontsize=10,verticalalignment="top",horizontalalignment="right")
    plt.annotate(r'$Convergence Epoch=$'+str(Hour[t])+':'+str(Minute[t])+':'+str(Second[t]),xy=(t, 0), xytext=(tx, ty),  fontsize=10,arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

    # plt.legend(('N','E','U',),loc='upper right')
    # plt.legend(loc='upper right')
    plt.xticks([0,480,960,1440,1920,2400,2880],[r'$0$', r'$4$', r'$8$', r'$12$', r'$16$',r'$20$', r'$24$'])
    plt.xlabel(u'TIME（Hour）',fontproperties=font_set)
    plt.ylabel(u'Error（m）',fontproperties=font_set)
    outdir,out_file=os.path.split(infile)
    outname=os.path.splitext(out_file)

    out_path=outdir+'\\'+str(convergence_epoch)+'-'+str(ThreeD_RMS)+'-'+outname[0]+'.png'
    plt.savefig(out_path)
    plt.close()
    Hour =[]
    Minute = []
    Second = []
    N = []
    E = []
    U = []
def walk_dir(dir,topdown=True):
    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            infile=os.path.join(root,name)
            file_type=infile.split('.')
            if file_type[-1]=='dat':
                read_plot_PosResult(infile)

font_set=FontProperties(fname=r"C:\Windows\winsxs\amd64_microsoft-windows-font-truetype-simsun_31bf3856ad364e35_6.1.7600.16385_none_56fe10b1895fd80b\simsun.ttc",size=15)
path= str(gui.diropenbox('choose dir','choose folder','E:\ '))
walk_dir(path)