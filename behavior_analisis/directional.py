# code for directional correlation


#H_ij funct of heading F_i evaluated at time t

#Heading F_j evaluated at time t- delay (tau)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

FISH_ATTRS = 3

def get_angles(x,y) -> np.typing.NDArray :
    '''returns the angle of a given pos'''

    x = np.array(x)
    y = np.array(y)

    theta = np.arctan2(x,y)

    theta %= np.pi*2

    return theta

# samples = 300

# true_angle = np.hstack((np.linspace(0,np.pi*4,samples//3),np.linspace(0,np.pi*4,samples//3)[::-1],np.linspace(0,np.pi*4,samples//3)))

# test_x = np.sin(true_angle)
# test_y = np.cos(true_angle)

# calc_angle = get_angles(test_x,test_y)


# x_axis = range(0,samples)
# plt.plot(x_axis,true_angle,label='True angle',alpha=0.5)
# plt.plot(x_axis,calc_angle,label='Renconstructed angle',alpha=0.5)
# plt.legend()
# plt.show()


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
def get_unit_vectors(data_chunk) -> list[np.ndarray]:
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
#
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

FPS = 50
DT = 1 / FPS

def compute_Cij_matrix(ei: np.ndarray, ej: np.ndarray, tau_max_s: float = 2.0, w: int = 2):
    tau_range = np.arange(2, int(tau_max_s * FPS) + 1)
    C_rows = [Cij(ei, ej, tau, w) for tau in tau_range]
    min_len = min(len(r) for r in C_rows)
    C_matrix = np.array([r[:min_len] for r in C_rows])
    return C_matrix, tau_range * DT

def plot_heatmap(C: np.ndarray, taus_s: np.ndarray, fish_i: int, fish_j: int, ax: plt.Axes = None):
    n_time = C.shape[1]
    t_axis = np.arange(n_time) * DT
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5))
    im = ax.imshow(C, aspect='auto', origin='lower',
                   extent=[t_axis[0], t_axis[-1], taus_s[0], taus_s[-1]],
                   vmin=-1, vmax=1, cmap='RdYlGn')
    best_tau = taus_s[int(np.argmax(C.mean(axis=1)))]
    ax.axhline(best_tau, color='blue', linewidth=1.2, linestyle='--', label=f'tau* = {best_tau:.2f}s')
    plt.colorbar(im, ax=ax, label='C_ij')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Delay tau (s)')
    ax.set_title(f'Fish {fish_i + 1} copying Fish {fish_j + 1}  (tau* = {best_tau:.2f}s)')
    ax.legend(fontsize=8)
    return ax

if __name__ == '__main__':
    from data_access import get_experement_paths, split_at_nans

    data_path  = get_experement_paths(group_size=2, limit=1)[0]
    data       = pd.read_csv(data_path)
    clean_data = split_at_nans(data)

    chunk   = max(clean_data, key=len)
    vectors = get_unit_vectors(chunk)
    n_fish  = len(vectors)

    pairs = [(i, j) for i in range(n_fish) for j in range(n_fish) if i != j]
    fig, axes = plt.subplots(1, len(pairs), figsize=(10 * len(pairs), 5))

    for ax, (i, j) in zip(axes, pairs):
        C, taus_s = compute_Cij_matrix(vectors[i], vectors[j])
        plot_heatmap(C, taus_s, i, j, ax=ax)

    plt.tight_layout()
    print(f'C matrix shape: {C.shape}')
    print(f'chunk length: {len(chunk)}')
    #plt.savefig('plots/directional_correlation.pdf')
    plt.show()


print('hi')