from matplotlib.pyplot import Axes
from matplotlib.patches import Circle

inner_dim = 25
outer_dim = 35

def plot_boundrys(ax:Axes) :
    outer = Circle((0,0),outer_dim/2,fill=None,edgecolor='black')
    inner = Circle((0,0),inner_dim/2,fill=None,edgecolor='black')
    ax.add_patch(outer)
    ax.add_patch(inner)


if __name__ == '__main__' :

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    plot_boundrys(ax)

    ax.set_xlim(-outer_dim, outer_dim)
    ax.set_ylim(-outer_dim, outer_dim)
    ax.set_aspect('equal')
    plt.grid(True)
    plt.show()