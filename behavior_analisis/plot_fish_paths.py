
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from matplotlib.pyplot import Axes
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

inner_dim = 250 # in mm
outer_dim = 350 # in mm
FISH_ATTRIBS = 3

def plot_boundrys(ax:Axes) :
    outer = Circle((0,0),outer_dim,fill=None,edgecolor='black')
    inner = Circle((0,0),inner_dim,fill=None,edgecolor='black')
    ax.add_patch(outer)
    ax.add_patch(inner)
    ax.set_xlim(-outer_dim, outer_dim)
    ax.set_xlabel('X position (mm)')
    ax.set_ylim(-outer_dim, outer_dim)
    ax.set_ylabel('Y position (mm)')
    ax.set_aspect('equal')


def plot_fish_paths(ax:plt.Axes, experement:pd.DataFrame) -> None :
    n_fish = experement.shape[1]//FISH_ATTRIBS

    plot_boundrys(ax)
    for i in range(0,n_fish*FISH_ATTRIBS,FISH_ATTRIBS) :
        ax.plot(experement.iloc[:,i],experement.iloc[:,i+1],label=f'fish {1 + i//FISH_ATTRIBS}')

    ax.legend()


def plot_animated_paths(fig:plt.Figure,ax:plt.Axes,experement:pd.DataFrame,path_length:int=20,fps:int=50) -> animation.Animation :

    plot_boundrys(ax)
    fish_paths :list[Line2D] = [
        ax.plot(experement.iloc[0,i],experement.iloc[0,i+1],label=f'fish {i//FISH_ATTRIBS +1}')[0] # add the first thing to the line
        for i in range(0,experement.shape[1],FISH_ATTRIBS) 
    ]

    ax.legend()

    def update(frame:int) -> tuple :

        start = max(0,frame-path_length)

        for i,path in enumerate(fish_paths) :
            i *= 3
            path.set_xdata(experement.iloc[start:frame,i])
            path.set_ydata(experement.iloc[start:frame,i+1])
            
        ax.set_title(f'Frame {frame}/{experement.shape[0]}')

        return fish_paths
    
    anim = animation.FuncAnimation(fig=fig,func=update,frames=experement.shape[0],interval=1/fps,repeat=True)
    return anim

def save_animation(anim:animation.Animation,fps:int=50) -> None :

    print('saving Animation')
    def callback(current,total) -> None :
        print(f'{current}/{total}',end='\r')

    anim.save('mymovie5fish.gif',progress_callback=callback,fps=fps)


if __name__ == '__main__' :
    data = 'data/5/exp05H20141001_10h05.csv'
    experement = pd.read_csv(data)
    #until aprox 30,000 fish 1 does not move
    a = experement.iloc[60000:60100,:]

    fig, ax = plt.subplots()
    
    anim = plot_animated_paths(fig,ax,a)
    
    save_animation(anim)
    plt.show()
