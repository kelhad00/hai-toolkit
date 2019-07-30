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
import time

from mic_acqui import record

import asyncio
import cozmo
from cozmo.util import degrees

mic = []; datafile = []
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

def equations(p, tau, dct):
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
    return (v*tau[0] - sqrt((dct['x2']-x)**2 + (dct['y2']-y)**2) + sqrt((dct['x1']-x)**2 + (dct['y1']-y)**2),
            v*tau[1] - sqrt((dct['x3']-x)**2 + (dct['y3']-y)**2) + sqrt((dct['x2']-x)**2 + (dct['y2']-y)**2))

def cozmo_direction(prev_ang, ang):
    def newfunc(sdk_conn):
        robot = sdk_conn.wait_for_robot()
        robot.set_head_angle(degrees(44.5)).wait_for_completed()
        sol = ang-prev_ang
        if sol != sol :
            sol = 0
        if abs(sol) > 180 :
#            sol = 360-sol
            sol= -np.sign(sol)*(360-abs(sol))
        print(sol)
        robot.turn_in_place(degrees(sol)).wait_for_completed()
        robot.set_head_angle(degrees(20)).wait_for_completed()
    return newfunc

def main(prev_ang):
    tmp = []; sol = []; tau = []; test = []; ang = []
    sample_width, audio_buffer, rate = record() 
    tau = delay_f([audio_buffer[0].get_data(), audio_buffer[1].get_data(), audio_buffer[2].get_data()], rate)
    print(tau)

    dct = {'x1':x1,'x2':x2,'x3':x3,
           'y1':y1,'y2':y2,'y3':y3}
    sol=root(equations, [0, 0], (tau, dct), tol = 10)
    abs_angle = np.arccos(1 - ssd.cosine([dct['x1'], dct['x2']], sol.x))*180/np.pi
#    ang = np.arccos(1 - ssd.cosine([dct['x1'], dct['x2']], sol.x))*180/np.pi
#    ang = np.arctan2(sol.x[1], sol.x[0])*180/np.pi
#    print(sol.x[1], sol.x[0])
#    print(ang)
#    test.append(np.sin(sol[i].x[0]))
    test = np.sin(sol.x[0])
    if test >= 0 :
        ang = -1*abs_angle
    else :
        ang = abs_angle
    if ang != ang :
        ang = 0
    print(prev_ang, ang)
    cozmo_program = cozmo_direction(prev_ang, ang)
    return ang, cozmo_program
    
if __name__ == '__main__' :
    cozmo.setup_basic_logging()
    prev_angle = 0
    while True :
        prev_angle, cozmo_program = main(prev_angle)
        cozmo.connect(cozmo_program)
        time.sleep(1)
#    f = open('last_angle', 'w')
#    f.write(str(last_angle))
#    f.close()
    