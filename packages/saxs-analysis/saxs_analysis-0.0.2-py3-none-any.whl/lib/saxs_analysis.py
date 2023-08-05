'''Python module for saxs data analysis
Created by : Elizabeth Mathew'''
#import packages
import numpy as np
import shutil
import os
import glob
import copy
import pandas as pd
import scipy
import matplotlib.pyplot as plt 
import ipympl
import pyFAI
import fabio
import cv2
from pyFAI.gui import jupyter

#------------------------------------------
#
# Function to read the dat file from SAXS
#
#------------------------------------------

def read_saxs_dat(filename):
    '''
    read the vd file or the normal dat file obtained from SAXS measurement
    parameters: 
    filename=name of file with location
    results : pandas dataframe of q in ängstrom, I in arbitary unit and sig_q
    '''
    data = open(filename,'r')
    read = data.read()
    splitted_data = read.split('\n')
    title = 'q(A-1)                    I(q)                      Sig(q)                    '
    def line_start(title,splitted_data):
        number = []
        for index, line in enumerate(splitted_data):
            if title in line:
                number.append(index)           
        return number
    start = line_start(title,splitted_data) 
    #print(start)
    data1D =  pd.read_csv(filename,skiprows=int(start[0])+1, header=None,sep="\s+")
    data1D.columns =['q', 'I', 'sig_q']
    return data1D
    
#------------------------------------------
#
# Function to plot the dat file from SAXS
#
#------------------------------------------

def plot_saxs_dat(filename,label):
    '''Plot the dat file
    parameters: 
    filename=name of file with location
    label= label that u want for the plot
    results : single I vs Q plots with legends named label'''
    df=read_saxs_dat(filename)
    plt.figure(figsize=(7, 5))
    plt.semilogy(df['q'],df['I'],label=label)
    plt.ylabel("Intensity (a.u.)", fontsize=14)
    plt.xlabel("q ($A^{-1}$)", fontsize=14)
    plt.xscale("log")
    plt.legend()
    return plt.show()
    

#----------------------------------------------
#
#Function to do 1D transformation
#
#----------------------------------------------

def one_D_transform(filename,mask_file=None,masking=False):

    '''read the edf file and do the 1D transformation with and without masking
     the function creates a dictoinary with I and q values after normalising the results'''
    # step 1: loading the file
    obj=fabio.open(filename)
    data=obj.data
    data2D = data.transpose()
    shape = data2D.shape
    #step5: creating bins, counting them and saving them to defined hist dictionary
    def hist_normalize(data,obj):
        centerX = float(obj.header['Center_1'])
        centerY = float(obj.header['Center_2'])
        pixelsize = float(obj.header['PSize_1'])
        detectordistance = float(obj.header['SampleDistance'])
        lambda1 = float(obj.header['WaveLength'])
        # step3: creating the data_points, stepsize
        posx = []
        posy = []
        for i in np.arange(1,shape[0]+1,1):
            posx.append((i-centerX)*pixelsize)
        for i in np.arange(1,shape[1]+1,1):
            posy.append((i-centerY)*pixelsize)
        qmin=0
        # divided the formulation in two parts f1 and then qmax
        f1 = ((np.sqrt(2)*shape[1]*pixelsize)/detectordistance)
        qmax = (4*np.pi/lambda1)*(np.sin(0.5*np.arctan(f1)))
        stepsize = (qmax-qmin)/1000
        numofsteps = np.round((qmax-qmin)/stepsize) 
        # step4: creating histogram to save the results
        hist={}
        t1 = []
        for i in np.arange(0,numofsteps+1,1):
            t1.append(i*stepsize)
        hist['q'] = np.array(t1)
        hist ['I'] = np.zeros(int(numofsteps)+1)
        hist ['I_corr'] = np.zeros(int(numofsteps)+1)
        low = 0
        high = 0
        bin2 = []
        for i in np.arange(0,shape[0],1):
            for j in np.arange(0,shape[1],1):
                f2 = np.sqrt((posx[i])**2+(posy[j])**2)/detectordistance
                q = (4*np.pi/lambda1)*(np.sin(0.5*np.arctan(f2)))
                bin1 = np.round((q-qmin+stepsize)/stepsize)
                if bin1<1:
                    low = low+1
                if bin1>numofsteps:
                    high = high+1
                if bin1>=1:
                    if bin1<=numofsteps:
                        if data[i][j] >=0:
                            bin2.append(bin1)
                            hist['I'][int(bin1)] = hist['I'][int(bin1)]+1
                            hist['I_corr'][int(bin1)] = hist['I_corr'][int(bin1)]+data[i][j]
        return hist,numofsteps
    if masking==True:
        mask = np.load(mask_file, allow_pickle=True)
        mask_t = mask.transpose()
        data_mask=data2D.copy()
        for i in np.arange(0,shape[0],1):
            for j in np.arange(0,shape[1],1):
                if mask_t[i][j]==0:
                    data_mask[i][j]=-144
        hist,numofsteps=hist_normalize(data_mask,obj)
    else:
        hist,numofsteps= hist_normalize(data2D,obj)
    #step6 : create another histogram to save the normalised results
    qscan = {}
    t2=[]
    for i in np.arange(0,int(numofsteps)+1,1):                        
        qscan['q'] = hist['q']
        if hist['I'][i]>0:
            t2.append(hist['I_corr'][i]/hist['I'][i])
    qscan['I'] = np.array(t2)
    return qscan
    
#------------------------------------------------
#    
# Function to plot 1D transformation
#    
#------------------------------------------------

def one_D_plot(filename,label,mask_file=None,masking=False):
    '''plot the 1D transformation of SAXS data
    parameters: 
    filename=name of file with location
    label= label that u want for the plot
    results : single I vs Q plots with legends named label'''
    qscan = one_D_transform(filename)
    if masking==True:
        qscan = one_D_transform(filename,mask_file,masking) 
    plt.figure(figsize=(7, 5))
    plt.semilogy(qscan['q'][0:len(qscan['I'])],qscan['I'],label=label)
    plt.ylabel("Intensity (a.u.)", fontsize=14)
    plt.xlabel("q ($m^{-1}$)", fontsize=14)
    #plt.yscale("log")
    plt.xscale("log")
    plt.legend()
    return plt.show()
    
#------------------------------------------------
#    
# Function to plot scotch and metal
#    
#------------------------------------------------  

def scotch_metal_plot_check_dat(filedetails,file_saxs,dist=None,n=None):
    '''
      Here, I use this to compare it with the dat file 
      and see if its comparing with the edf 1D trandformation
      filedetails= csv file with material,detector_distance,
      filename
      filesaxs=loaction of the folder
      eg:file_saxs ='/home/eliza/work/SAXS/SAXS_hpt/20220708/'
      use dist and n if we donot want to use all the distance and all
      the values from center
      dist= diatance from the detector
      n =  number of calculation from center, care should be the first one should be 
      scotch and I did max upto 5 points so in that case maximum can be 5+1=6
      
    '''
    df = pd.read_csv(file_details)
    if dist != None:
        df = df[df.detector_distance==dist]
        if n != None:
            df = df[0:n] 
            df= df.reset_index(drop=True)# change the index
    fig, ax = plt.subplots(ncols=1,nrows=1, figsize=(8, 5))
    colors = plt.cm.Spectral(np.linspace(0, 1, len(df.filename)))
    i=0
    dist=0
    for mat,file,distance,c in zip(df.material,df.filename,df.detector_distance,colors):
        if distance != dist:
            i=0
            dist = distance
        else:   
            i=i+1
        

        if mat == 'scotch_tape':
            filename_s_dat = file_saxs+file+'.dat'
        
            filename_s_edf = file_saxs+file+'.edf'
            s = fabio.open(filename_s_edf)
            i_ratio_s = float(s.header['SumForIntensity1'])*(float(s.header['PSize_1'])/float(s.header['SampleDistance']))**2
            dt_s_dat = read_saxs_dat(filename_s_dat)
            dt_s_edf = one_D_transform(filename_s_edf)
            plt.plot(dt_s_dat['q']*10000000000,dt_s_dat['I'],color=c,label='{}_dat'.format(mat))
            plt.plot(dt_s_edf['q'][0:len(dt_s_edf['I'])],dt_s_edf['I']/i_ratio_s,color='r',label='{}_edf'.format(mat))
        if mat == 'metal':
            filename_m_dat = file_saxs+file+'.dat'
            filename_m_edf = file_saxs+file+'.edf'
            m = fabio.open(filename_m_edf)
            i_ratio_m = float(m.header['SumForIntensity1'])*(float(s.header['PSize_1'])/float(s.header['SampleDistance']))**2
            dt_m_dat = read_saxs_dat(filename_m_dat)
            dt_m_edf = one_D_transform(filename_m_edf)
            plt.plot(dt_m_dat['q']*10000000000,dt_m_dat['I'],color=c,label='{}_dat({})'.format(mat,i))
            plt.plot(dt_m_edf['q'][0:len(dt_s_edf['I'])],dt_m_edf['I']/i_ratio_m,color=c,label='{}_edf({})'.format(mat,i))
        plt.xscale("log")
        plt.yscale("log")
        plt.legend(loc='upper left',bbox_to_anchor=(1,1))
    plt.ylabel("Intensity (a.u.)", fontsize=14)
    plt.xlabel("q ($m^{-1}$)", fontsize=14)
    plt.tight_layout()
    plt.show() 
 
def scotch_metal_plot(filedetails,file_saxs,dist=None,n=None):
    '''
      filedetails= csv file with material,detector_distance,
      filename
      filesaxs=loaction of the folder
      eg:file_saxs ='/home/eliza/work/SAXS/SAXS_hpt/20220708/'
      use dist and n if we donot want to use all the distance and all
      the values from center
      dist= diatance from the detector only for one distance
      n =  number of calculation from center, care should be the first one should be 
      scotch and I did max upto 5 points so in that case maximum can be 5+1=6
      
    '''
    df = pd.read_csv(filedetails)
    if dist != None:
        df = df[df.detector_distance==dist]
        if n != None:
            df = df[0:n] 
            df= df.reset_index(drop=True)# change the index
    fig, ax = plt.subplots(ncols=1,nrows=1, figsize=(8, 5))
    colors = plt.cm.Spectral(np.linspace(0, 1, len(df.filename)))
    i=0
    dist=0
    for mat,file,distance,c in zip(df.material,df.filename,df.detector_distance,colors):
        if distance != dist:
            i=0
            dist = distance
        else:   
            i=i+1
        
        if mat == 'scotch_tape':
            filename_s_edf = file_saxs+file+'.edf'
            s = fabio.open(filename_s_edf)
            i_ratio_s = float(s.header['Intensity1'])/float(s.header['WaveLength'])
            dt_s_edf = one_D_transform(filename_s_edf)
            plt.plot(dt_s_edf['q'][0:len(dt_s_edf['I'])],dt_s_edf['I']/i_ratio_s,color=c,label='{}_edf'.format(mat))
        if mat == 'metal':
            #i=i+1
            filename_m_edf = file_saxs+file+'.edf'
            m = fabio.open(filename_m_edf)
            i_ratio_m = float(m.header['Intensity1'])/float(m.header['WaveLength'])            
            dt_m_edf = one_D_transform(filename_m_edf)
            plt.plot(dt_m_edf['q'][0:len(dt_m_edf['I'])],dt_m_edf['I']/i_ratio_m,color=c,label='{}_edf({})'.format(mat,i))
        plt.xscale("log")
        plt.yscale("log")
        plt.legend(loc='upper left',bbox_to_anchor=(1,1))
    plt.ylabel("Intensity (a.u.)", fontsize=14)
    plt.xlabel("q ($m^{-1}$)", fontsize=14)
    plt.tight_layout()
    plt.show()
    
 
def scotch_metal_plot_adv(filedetails,file_saxs):
    '''
      filedetails= csv file with material,detector_distance,
      filename
      filesaxs=loaction of the folder
      eg:file_saxs ='/home/eliza/work/SAXS/SAXS_hpt/20220708/'
      use dist and n if we donot want to use all the distance and all
      the values from center
      dist= diatance from the detector
      n =  number of calculation from center, care should be the first one should be 
      scotch and I did max upto 5 points so in that case maximum can be 5+1=6
      
      Note : the labels are for 300, 600 , 1200 distance, change in the csv order or 
      adding the new distance care should be taken to consider all that 
      changes.
      
    '''
    df = pd.read_csv(filedetails)
    fig, ax = plt.subplots(ncols=1,nrows=1, figsize=(7.5, 7))
    colors = plt.cm.Spectral(np.linspace(0, 1, len(df.filename)))
    i=0
    distance=0
    dist=[]
    for j,mat in enumerate(df.material):
        if distance != df.detector_distance[j]:
            i=0
            distance = df.detector_distance[j]
            dist.append(distance)
        else:   
            i=i+1

        if mat == 'scotch_tape':
            filename_s_edf = file_saxs+df.filename[j]+'.edf'
            s = fabio.open(filename_s_edf)
            i_ratio_s = float(s.header['Intensity1'])/float(s.header['WaveLength'])
            dt_s_edf = one_D_transform(filename_s_edf)
            plt.plot(dt_s_edf['q'][0:len(dt_s_edf['I'])],dt_s_edf['I']/i_ratio_s,color=colors[j],label='{}_edf'.format(mat))
        if mat == 'metal':
            filename_m_edf = file_saxs+df.filename[j]+'.edf'
            m = fabio.open(filename_m_edf)
            i_ratio_m = float(m.header['Intensity1'])/float(m.header['WaveLength'])            
            dt_m_edf = one_D_transform(filename_m_edf)
            plt.plot(dt_m_edf['q'][0:len(dt_m_edf['I'])],dt_m_edf['I']/i_ratio_m,color=colors[j],label='{}_edf({})'.format(mat,i))
            plt.xscale("log")
            plt.yscale("log")
    h, l = ax.get_legend_handles_labels()
    ph = [plt.plot([],marker="", ls="")[0]]*3
    handles = ph[:1] + h[0:6] + ph[1:2] + h[6:12]+ ph[-1:] + h[12:18]
    labels = ["600"] + l[0:6] + ["1200"] + l[6:12]+['300']+ l[12:18]
    leg = plt.legend(handles, labels,loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
    for vpack in leg._legend_handle_box.get_children():
        for hpack in vpack.get_children()[:1]:
            hpack.get_children()[0].set_width(0)

    plt.ylabel("Intensity (a.u.)", fontsize=14)
    plt.xlabel("q ($m^{-1}$)", fontsize=14)
    plt.tight_layout()
    plt.show()
    
    
def scotch_minus_metal_plot(filedetails,file_saxs,dist=None,n=None):
    '''
      filedetails= csv file with material,detector_distance,
      filename
      filesaxs=loaction of the folder
      eg:file_saxs ='/home/eliza/work/SAXS/SAXS_hpt/20220708/'
      use dist and n if we donot want to use all the distance and all
      the values from center
      dist= diatance from the detector
      n =  number of calculation from center, care should be the first one should be 
      scotch and I did max upto 5 points so in that case maximum can be 5+1=6
      
    '''
    df = pd.read_csv(filedetails)
    if dist != None:
        df = df[df.detector_distance==dist]
        if n != None:
            df = df[0:n] 
            df= df.reset_index(drop=True)# change the index
    fig, ax = plt.subplots(ncols=1,nrows=1, figsize=(8, 5))
    colors = plt.cm.Spectral(np.linspace(0, 1, len(df.filename)))
    i=0
    for mat,file,c in zip(df.material,df.filename,colors):
        if mat == 'scotch_tape':        
            filename_s_edf = file_saxs+file+'.edf'
            s = fabio.open(filename_s_edf)
            i_ratio_s = float(s.header['Intensity1'])/float(s.header['WaveLength'])
            dt_s_edf = one_D_transform(filename_s_edf)
        if mat == 'metal':
            i=i+1
            filename_m_edf = file_saxs+file+'.edf'
            m = fabio.open(filename_m_edf)
            i_ratio_m = float(m.header['Intensity1'])/float(m.header['WaveLength'])            
            dt_m_edf = one_D_transform(filename_m_edf)
            dt_m_edf['lim_q']=dt_m_edf['q'][0:len(dt_s_edf['I'])]
            dt_m_edf['I_sm']=dt_m_edf['I']/i_ratio_m-dt_s_edf['I']/i_ratio_s
            dt= pd.DataFrame(dt_m_edf['lim_q'],columns=['lim_q'])
            dt['I_sm']= dt_m_edf['I_sm']
            dt=dt[dt['I_sm'] > 0]
            #print(dt)
            plt.plot(dt['lim_q'],dt['I_sm'],color=c,label='{}_edf({})'.format(mat,i))
        plt.xscale("log")
        plt.yscale("log")
        plt.legend(loc='upper left',bbox_to_anchor=(1,1))
    plt.ylabel("Intensity (a.u.)", fontsize=14)
    plt.xlabel("q ($m^{-1}$)", fontsize=14)
    plt.tight_layout()
    plt.show()
     
#------------------------------------------------
#    
# Function to create mask
#    
#------------------------------------------------  
        
            
