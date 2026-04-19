# code for directional correlation


#H_ij funct of heading F_i evaluated at time t

#Heading F_j evaluated at time t- delay (tau)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def get_angles(x,y) -> np.typing.NDArray :
    '''returns the angle of a given pos'''

    x = np.array(x)
    y = np.array(y)

    theta = np.arctan2(x,y)

    theta %= np.pi*2

    return theta

samples = 300

true_angle = np.hstack((np.linspace(0,np.pi*4,samples//3),np.linspace(0,np.pi*4,samples//3)[::-1],np.linspace(0,np.pi*4,samples//3)))

test_x = np.sin(true_angle)
test_y = np.cos(true_angle)

calc_angle = get_angles(test_x,test_y)


x_axis = range(0,samples)
plt.plot(x_axis,true_angle,label='True angle',alpha=0.5)
plt.plot(x_axis,calc_angle,label='Renconstructed angle',alpha=0.5)
plt.legend()
plt.show()


def find_turning_points(x:np.typing.NDArray,y:np.typing.NDArray) -> list[tuple[int,int]] :

    '''
    find turning points in the movements of a fish , 
    given its x and y coords , will return a list of
    timestamps of detections of turnarounds.
    '''

    theta = np.arctan2(x,y)  #angle with horizontal 
    theta %= np.pi*2

    raw_diff = theta[1:] - theta[:-1]

    # find places where the diff is more than 180 degrees 
    # as that means that there was a wrap around 

    mod_diff = raw_diff % np.pi 

    mod_p1_diff = mod_diff - np.pi # incase the diff is in the other direction i.e 179 instead of -1 deg

    diff = np.array([

        v if abs(mod_p1_diff[i]) > v else mod_p1_diff[i]
        for i,v in enumerate(mod_diff)

    ])

    turn_arounds = []
    for start in np.where(np.diff(np.sign(diff)))[0] :
        turn_arounds.append((start,start+1))

    return turn_arounds

def find_turning_points(x:np.typing.NDArray,y:np.typing.NDArray) -> list[tuple[int,int]] :

    '''
    find turning points in the movements of a fish , 
    given its x and y coords , will return a list of
    timestamps of detections of turnarounds.
    '''

    theta = np.arctan2(x,y)  #angle with horizontal 
    theta %= np.pi*2

    raw_diff = theta[1:] - theta[:-1]

    # find places where the diff is more than 180 degrees 
    # as that means that there was a wrap around 

    mod_diff = raw_diff % np.pi 

    mod_p1_diff = mod_diff - np.pi # incase the diff is in the other direction i.e 179 instead of -1 deg

    diff = np.array([

        v if abs(mod_p1_diff[i]) > v else mod_p1_diff[i]
        for i,v in enumerate(mod_diff)

    ])

    turn_arounds = []
    for start in np.where(np.diff(np.sign(diff)))[0] :
        turn_arounds.append((start,start+1))

    return turn_arounds
#functions from Dans turnaround_detection

#calculating e=v/mod v
def get_unit_vectors(data_chunk: pd.DataFrame) -> list[np.ndarray]:
    vectors = []
    for fish_i in range(0, data_chunk.shape[1], FISH_ATTRS):
        x = data_chunk.iloc[:, fish_i].values
        y = data_chunk.iloc[:, fish_i + 1].values

        #velocity from finite differences (displacement per frame)
        vx = np.diff(x)
        vy = np.diff(y)

        #|v| — speed at each frame
        speed = np.sqrt(vx**2 + vy**2)

        #avoid division by zero when fish is stationary
        speed[speed == 0] = np.nan

        #e_i = v / |v|
        ex = vx / speed
        ey = vy / speed

        vectors.append(np.column_stack((ex, ey)))

    return vectors

def Hij(ei: np.ndarray, ej: np.ndarray, tau_frames: int) -> np.ndarray:
    '''
    H_ij(t, tau) = e_i(t) . e_j(t - tau)
    '''
    T = ei.shape[0]
    #e_i(t) . e_j(t - tau) for all t
    return np.einsum('ti,ti->t', ei[tau_frames:], ej[:T - tau_frames])


#w needs to be changed depending on noise of the data, could use value luca gave?
def Cij(ei: np.ndarray, ej: np.ndarray, tau_frames: int, w: int = 2) -> np.ndarray:
    
    #C_ij(t, tau, w) = 1/(2w+1) * sum_{k=-w}^{w} H_ij(t + k, tau)
    #Smoothed version of H_ij over (2w+1) frames.
    
    h      = Hij(ei, ej, tau_frames)
    window = 2 * w + 1

    if len(h) < window:
        return np.array([])

    cs = np.concatenate(([0], np.cumsum(h)))
    return (cs[window:] - cs[:-window]) / window

#ploarization
def polarisation(vectors: list[np.ndarray]) -> np.ndarray:
    N = len(vectors)
    summed = np.sum(vectors, axis=0)  #sum unit vectors across fish
    return np.linalg.norm(summed, axis=1) / N  #normalise by N

#collective u turn- when all fish turn together not just one fish
#ts - start of turn
#te- end 
#data provided in eloise's notes on how to calculate this, need to select parameters