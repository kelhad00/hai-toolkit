# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:14:24 2019

@author: hugob
"""

import numpy as np
import scipy.spatial.distance as ssd
import scipy.signal as ssg

from scipy.optimize import root
from math import sqrt
from scipy.io import wavfile
from glob import glob
from array import array

from mic_acqui import record

mic = []; datafile = []; tmp = []; tau = []; sol = []
v = 343
PATH = r"C:\Users\hugob\Documents\Umons\Ankara\Python\DB\ENTERFACE\ENT_rasp_pya_cozmo_far_same\ENT_rasp_pya_cozmo_"
num_file = 12

#Coordinates of microphones
x1, y1 = (0, 0.05) #(0, 0.711) (0, 0.05)
x2, y2 = (0.043, -0.025) #(-0.5, -0.289) (-0.043, -0.025)
x3, y3 = (-0.043, -0.025) #(0.5, -0.289) (0.043, -0.025)


#Error rate
def error_f(v, i) :
    """
    Print the error between angle |M1-O-Real_Source| 
    and angle |M1-O-Estimated_Source|
    
    Arguments:
        v {float[]} -- Coordonates of Estimated_Source
        i {int} -- Iteration
    """
    u = (0, 0.05)
    error = -1 + ssd.cosine(u, v) + np.cos((i*np.pi/6))
    error = (np.arcsin(error)*180/np.pi)
    print(error)

#Cross correlation
def CC_f(m_1, m_2) :
    """
    Calculate the cross-correlation between 
    two vectors
    
    Arguments:
        m_1 {array_like} -- Data array 1
        m_2 {array_like} -- Data array 2
    
    Returns:
        array -- Values of the cross-correlation
    """
    return ssg.fftconvolve(m_1, m_2[::-1], 'full')

#Delay values
def delay_f(data, samplingFreq) :
    """
    Estimate the delay between the moments of reception
    of the sound in each microphone
    
    Arguments:
        data_path {list} -- The path to the samples we want to analyze
    
    Returns:
        tau {list} -- Contains the 2 delays (t2-t1, t3-t2)
    """
    CC = []; tau = []
    
    #Cross-Correlation between two samples
    for i in range (2) : #2
        CC.append(CC_f(data[(i+1)], data[i]))
    
    #Timeline for representation of CC
    timeTau = np.arange(-len(data[0])+1, len(data[0]))
    timeTau = timeTau/samplingFreq
    
    for i in range(2) : #2
        tau.append(timeTau[abs(CC[i]).argmax()])
    return tau

def equations(p, tau, dct, i):
    """
    Functions used in scipy.optimize.root() to obtain
    coordonates of origin of the sound
    
    Arguments:
        p {2-D array} -- Initial guess (centre of the microphones)
        tau {2-D array} -- Delays
        dct {dict} -- Microphones coordonates
        i {int} -- Iteration
    
    Returns:
        2-D array -- Solutions of both equations, need to be 0 at best
    """
    x, y = p
    return (v*tau[i][0] - sqrt((dct['x2']-x)**2 + (dct['y2']-y)**2) + sqrt((dct['x1']-x)**2 + (dct['y1']-y)**2),
            v*tau[i][1] - sqrt((dct['x3']-x)**2 + (dct['y3']-y)**2) + sqrt((dct['x2']-x)**2 + (dct['y2']-y)**2))
#    return (v*tau[0]- sqrt((dct['x2']-x)**2 + (dct['y2']-y)**2) + sqrt((dct['x1']-x)**2 + (dct['y1']-y)**2))

def main():
    tmp = []
    data, rate = record()
    for i in range(len(data)) :
        # def to_float(data):
        #     return np.array(list(data))/256
        tmp.append(array('h'))
        # tau.append(delay_f([data[0][j], data[1][j], data[2][j]], rate))
        for j in range(data[i].len()) :
            f = data[i].get_data(j) 
            tmp[i].extend(f)
    
    tau.append(delay_f([tmp[0], tmp[1], tmp[2]], rate))
    print(tau)

    dct = {'x1':x1,'x2':x2,'x3':x3,
           'y1':y1,'y2':y2,'y3':y3}
    test = []
    for i in range(1) : #12
#        print(root(equations, [0, 0], (tau, dct, i), tol = 10))
        sol.append(root(equations, [0, 0], (tau, dct, i), tol = 10))
        abs_angle = np.arccos(1 - ssd.cosine([dct['x1'], dct['x2']], sol[i].x))*180/np.pi
        test.append(np.sin(sol[i].x[0]))
        if test[i] >= 0 : angle = -abs_angle
        else : angle = abs_angle
        print(angle)

if __name__ == '__main__' :
    main()
    