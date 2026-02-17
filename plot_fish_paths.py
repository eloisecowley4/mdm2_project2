
import matplotlib.pyplot as plt
import pandas as pd


def plot_fish_paths(experement:pd.DataFrame) -> None :
    n_fish = experement.shape[1]//3

    for i in range(0,n_fish*3,3) :
        plt.plot(experement.iloc[:,i],experement.iloc[:,i+1],label=f'fish {1 + i//3}')

    plt.legend()
    plt.savefig('plots/paths.pdf')

def plot_fish_turn_rate(experement:pd.DataFrame) -> None :
    n_fish = experement.shape[1]//3

    fps = 50
    
    for i in range(0,n_fish*3,3) :
        headings = experement.iloc[:,i+2]
        turn_rate = headings.diff() * fps
        plt.plot(turn_rate,label=f'fish {1 + i//3}')

    plt.ylabel('Turn Rate (rads/s)')
    plt.legend()
    plt.savefig('plots/turn rates.pdf')



if __name__ == '__main__' :
    data = 'data/2/exp02H20141127_14h13.csv'
    experement = pd.read_csv(data)
    a = experement.iloc[:1000,:]
    plot_fish_paths(a)
    plt.clf()
    plot_fish_turn_rate(a)
