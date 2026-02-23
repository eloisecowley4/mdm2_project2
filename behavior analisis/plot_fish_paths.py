
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from matplotlib.pyplot import Axes
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

inner_dim = 250
outer_dim = 350
FISH_ATTRIBS = 3

def plot_boundrys(ax:Axes) :
    outer = Circle((0,0),outer_dim,fill=None,edgecolor='black')
    inner = Circle((0,0),inner_dim,fill=None,edgecolor='black')
    ax.add_patch(outer)
    ax.add_patch(inner)


def plot_fish_paths(experement:pd.DataFrame) -> None :
    n_fish = experement.shape[1]//FISH_ATTRIBS

    for i in range(0,n_fish*FISH_ATTRIBS,FISH_ATTRIBS) :
        plt.plot(experement.iloc[:,i],experement.iloc[:,i+1],label=f'fish {1 + i//FISH_ATTRIBS}')

    plt.legend()
    plt.savefig('plots/paths.pdf')



def plot_animated_paths(fig:plt.Figure,ax:plt.Axes,experement:pd.DataFrame,path_length:int=20,frame_step:int=5) -> animation.Animation :

    fish_paths :list[Line2D] = [
        ax.plot(experement.iloc[0,i],experement.iloc[0,i+1],label=f'fish {i}')[0] # add the first thing to the line
        for i in range(0,experement.shape[1],FISH_ATTRIBS) 
    ]

    def update(frame:int) -> tuple :

        start = max(0,frame-path_length)

        for i,path in enumerate(fish_paths) :
            i *= 3
            path.set_xdata(experement.iloc[start:frame,i])
            path.set_ydata(experement.iloc[start:frame,i+1])

        return fish_paths
    
    anim = animation.FuncAnimation(fig=fig,func=update,frames=experement.shape[0],interval=frame_step)
    return anim

def save_animation(anim:animation.Animation) -> None :

    def callback(current,total) -> None :
        print(f'{current}/{total}',end='\r')

    anim.save('mymovie.gif',progress_callback=callback)



if __name__ == '__main__' :
    data = 'data/2/exp02H20141127_14h13.csv'
    experement = pd.read_csv(data)
    #until aprox 30,000 fish 1 does not move
    a = experement.iloc[60000:61000,:]

    fig, ax = plt.subplots()
    
    anim = plot_animated_paths(fig,ax,a)
    plot_boundrys(ax)
    ax.set_xlim(-outer_dim, outer_dim)
    ax.set_ylim(-outer_dim, outer_dim)
    ax.set_aspect('equal')
    
    save_animation(anim)
    plt.show()
